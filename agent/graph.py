from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from seoextract import SEOExtract

from config import MAX_PAGES, GOOGLE_SAFE_BROWSING_API_KEY
from agent.recommender import generate_recommendations


class SEOAgentState(TypedDict):
    url: str
    business_domain: str
    target_audience: str
    target_keyword: str

    audit_result: object
    recommendations: object
    triage: dict


def audit_node(state: SEOAgentState):

    audit = SEOExtract.audit(
        state["url"],
        max_pages=MAX_PAGES,
        safe_browsing_api_key=GOOGLE_SAFE_BROWSING_API_KEY,
    )

    return {
        "audit_result": audit
    }


def recommendation_node(state: SEOAgentState):
    recommendations = generate_recommendations(
        state["audit_result"],
        business_domain=state["business_domain"],
        target_audience=state["target_audience"],
        target_keyword=state["target_keyword"],
    )

    return {
        "recommendations": recommendations
    }

def triage_node(state: SEOAgentState):
    audit = state["audit_result"]

    triage = {
        "metadata": [],
        "content": [],
        "technical": [],
        "linking": [],
        "security": [],
    }

    for issue in audit.issues:
        issue_name = issue.issue_type.value.lower()

        if "title" in issue_name or "meta" in issue_name:
            triage["metadata"].append(issue)
        elif "content" in issue_name or "h1" in issue_name:
            triage["content"].append(issue)
        elif "canonical" in issue_name or "schema" in issue_name or "viewport" in issue_name:
            triage["technical"].append(issue)
        elif "link" in issue_name:
            triage["linking"].append(issue)
        else:
            triage["security"].append(issue)

    return {"triage": triage}

builder = StateGraph(SEOAgentState)

builder.add_node("audit", audit_node)
builder.add_node("recommend", recommendation_node)
builder.add_node("triage", triage_node)

builder.add_edge(START, "audit")
builder.add_edge("audit", "triage")
builder.add_edge("triage", "recommend")
builder.add_edge("recommend", END)

seo_graph = builder.compile()