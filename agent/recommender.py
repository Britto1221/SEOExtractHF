import json

from .llm.client import generate_text
from .llm.prompts import build_recommendation_prompt
from .schemas import SEORecommendationResult


def generate_recommendations(
    audit_result,
    business_domain: str = "",
    target_audience: str = "",
    target_keyword: str = "",
) -> SEORecommendationResult:
    audit_json = audit_result.model_dump_json(indent=2)

    prompt = build_recommendation_prompt(
        audit_json=audit_json,
        business_domain=business_domain,
        target_audience=target_audience,
        target_keyword=target_keyword,
    )

    response = generate_text(prompt)

    try:
        data = json.loads(response)
        return SEORecommendationResult(**data)

    except Exception as e:
        return SEORecommendationResult(
            overall_summary=f"Failed to parse structured AI response: {e}",
            priority_action_plan=[
                "Check whether the LLM returned valid JSON.",
                "Try running the audit again.",
            ],
        )