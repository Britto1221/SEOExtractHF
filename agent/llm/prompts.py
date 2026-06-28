def build_recommendation_prompt(
    audit_json: str,
    business_domain: str = "",
    target_audience: str = "",
    target_keyword: str = "",
) -> str:
    return f"""
You are an expert SEO consultant.

Use the technical SEO audit and business context to generate structured SEO recommendations.

Business Domain:
{business_domain}

Target Audience:
{target_audience}

Primary Target Keyword:
{target_keyword}

SEO Audit Data:
{audit_json}

Return ONLY valid JSON.

Required JSON structure:

{{
  "overall_summary": "short summary of the SEO condition",
  "title_recommendations": [
    {{
      "page_url": "page URL",
      "current_title": "existing title or null",
      "recommended_title": "new SEO title",
      "reason": "why this title is better"
    }}
  ],
  "meta_recommendations": [
    {{
      "page_url": "page URL",
      "current_meta": "existing meta description or null",
      "recommended_meta": "new meta description",
      "reason": "why this meta description is better"
    }}
  ],
  "heading_recommendations": [
    {{
      "page_url": "page URL",
      "current_h1": "existing H1 or null",
      "recommended_h1": "new H1",
      "recommended_h2": ["H2 suggestion 1", "H2 suggestion 2"],
      "reason": "why these headings are better"
    }}
  ],
  "internal_link_recommendations": [
    {{
      "page_url": "page URL",
      "suggested_links": ["suggested internal link 1", "suggested internal link 2"],
      "reason": "why these links help"
    }}
  ],
  "content_recommendations": [
    {{
      "page_url": "page URL",
      "current_word_count": 0,
      "recommendation": "content improvement suggestion",
      "reason": "why this content improvement matters"
    }}
  ],
  "priority_action_plan": [
    "first action",
    "second action",
    "third action"
  ]
}}

Rules:
- Return JSON only.
- Do not use markdown.
- Do not invent crawled pages.
- Use only page URLs present in the audit data.
- Titles should be around 50–60 characters.
- Meta descriptions should be around 120–160 characters.
- Recommendations must match the business domain, audience, and keyword.
"""