import streamlit as st
from seoextract import SEOExtract

from config import MAX_PAGES, GOOGLE_SAFE_BROWSING_API_KEY
from agent.recommender import generate_recommendations


st.set_page_config(page_title="AI SEO Audit Agent", page_icon="🖥️", layout="wide")


st.markdown("""
<style>
.stApp {
    background-color: #010409;
    color: #c9d1d9;
    font-family: Consolas, monospace;
}

.block-container {
    background-color: #010409;
    padding-top: 2rem;
}

h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: #c9d1d9 !important;
    font-family: Consolas, monospace !important;
}

.stTextInput input {
    background-color: #010409 !important;
    color: #58a6ff !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    font-family: Consolas, monospace !important;
}

.stButton button {
    background-color: #010409 !important;
    color: #c9d1d9 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    font-family: Consolas, monospace !important;
}

.stButton button:hover {
    border-color: #238636 !important;
    color: #58a6ff !important;
}

.terminal-output, .terminal-box {
    background-color: #010409;
    border: 1px solid #30363d;
    border-left: 3px solid #238636;
    border-radius: 8px;
    padding: 18px;
    font-family: Consolas, monospace;
    color: #c9d1d9;
    white-space: pre-wrap;
}

pre {
    background-color: #010409 !important;
    color: #c9d1d9 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown("# 🖥️ AI SEO Audit Agent")
st.markdown("### Developer terminal-style SEO audit interface")

url = st.text_input("Enter website_url", placeholder="https://example.com")
business_domain = st.text_input("Enter business_domain", placeholder="AI automation agency")
target_audience = st.text_input("Enter target_audience", placeholder="small business owners")
target_keyword = st.text_input("Enter target_keyword", placeholder="AI automation services")


if st.button("▶ run audit"):
    if not url:
        st.error("ERROR: website_url is required")
        st.stop()

    st.markdown('<div class="terminal-box">Running SEOExtract.audit()...</div>', unsafe_allow_html=True)

    audit_result = SEOExtract.audit(
        url,
        max_pages=MAX_PAGES,
        safe_browsing_api_key=GOOGLE_SAFE_BROWSING_API_KEY,
    )

    st.markdown("## Audit Summary")

    summary = f"""$ seoextract audit {url}

site_score      : {audit_result.site_score}
grade           : {audit_result.grade}
pages_crawled   : {audit_result.pages_crawled}
total_issues    : {audit_result.total_issues}
safe_browsing   : {audit_result.safe_browsing.is_safe}
"""

    st.code(summary, language="text")

    st.markdown("## Detected Issues")

    if audit_result.issues:
        issues_text = ""

        for issue in audit_result.issues:
            issues_text += (
                f"[{issue.severity.value}] {issue.issue_type.value}\n"
                f"page: {issue.page_url}\n"
                f"fix : {issue.suggestion}\n\n"
            )

        st.code(issues_text, language="text")
    else:
        st.code("No SEO issues detected.", language="text")

    st.markdown("## AI Recommendations")

    recommendations = generate_recommendations(
        audit_result,
        business_domain=business_domain,
        target_audience=target_audience,
        target_keyword=target_keyword,
    )

    st.markdown("### Overall Summary")
    st.code(recommendations.overall_summary, language="text")

    st.markdown("### Title Recommendations")
    for item in recommendations.title_recommendations:
        st.code(
            f"""page        : {item.page_url}
current     : {item.current_title}
recommended : {item.recommended_title}
reason      : {item.reason}""",
            language="text",
        )

    st.markdown("### Meta Description Recommendations")
    for item in recommendations.meta_recommendations:
        st.code(
            f"""page        : {item.page_url}
current     : {item.current_meta}
recommended : {item.recommended_meta}
reason      : {item.reason}""",
            language="text",
        )

    st.markdown("### Heading Recommendations")
    for item in recommendations.heading_recommendations:
        h2_text = "\n".join([f"- {h}" for h in item.recommended_h2])

        st.code(
            f"""page       : {item.page_url}
current_h1 : {item.current_h1}
new_h1     : {item.recommended_h1}
new_h2     :
{h2_text}

reason     : {item.reason}""",
            language="text",
        )

    st.markdown("### Internal Link Suggestions")
    for item in recommendations.internal_link_recommendations:
        links = "\n".join([f"- {link}" for link in item.suggested_links])

        st.code(
            f"""page   : {item.page_url}
links  :
{links}

reason : {item.reason}""",
            language="text",
        )

    st.markdown("### Content Recommendations")
    for item in recommendations.content_recommendations:
        st.code(
            f"""page       : {item.page_url}
word_count : {item.current_word_count}
fix        : {item.recommendation}
reason     : {item.reason}""",
            language="text",
        )

    st.markdown("### Priority Action Plan")
    st.code(
        "\n".join([f"[ ] {step}" for step in recommendations.priority_action_plan]),
        language="text",
    )

    with st.expander("$ show raw_json"):
        st.code(
            audit_result.model_dump_json(indent=2),
            language="json",
        )