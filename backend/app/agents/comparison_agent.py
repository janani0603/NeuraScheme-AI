import json
import asyncio
import logging
from app.agents.gemini_client import generate
from app.database.connection import db

logger = logging.getLogger(__name__)


COMPARISON_PROMPT = """You are comparing Indian government schemes for a citizen.

CITIZEN PROFILE:
- State: {state}
- Occupation: {occupation}
- Income: {income}
- Category: {category}

SCHEMES TO COMPARE:
{schemes_text}

Provide a structured comparison. Respond in this exact JSON format:
{{
  "summary": "One sentence summarizing the key difference between these schemes",
  "best_for_user": "slug of the scheme most suitable for this specific user",
  "reason": "One sentence explaining why that scheme is best for this user",
  "comparison": [
    {{
      "slug": "scheme-slug",
      "scheme_name": "Name",
      "key_benefit": "Main benefit in one line",
      "target_audience": "Who this is primarily for",
      "ease_of_apply": "Easy / Moderate / Complex",
      "benefit_amount": "Amount or type of benefit if mentioned, else 'Not specified'",
      "pros": ["pro1", "pro2"],
      "cons": ["con1", "con2"]
    }}
  ]
}}

Do not add explanation outside the JSON.
"""


async def comparison_agent(scheme_slugs: list[str], profile: dict) -> dict:
    """
    Compares 2-4 schemes side by side for a given user profile.
    """
    if len(scheme_slugs) < 2:
        return {"error": "At least 2 schemes required for comparison"}
    if len(scheme_slugs) > 4:
        scheme_slugs = scheme_slugs[:4]

    # Fetch all schemes concurrently
    cursor = db["schemes"].find(
        {"slug": {"$in": scheme_slugs}},
        {"slug": 1, "scheme_name": 1, "benefits": 1, "eligibility": 1, "documents": 1, "application": 1, "level": 1, "schemeCategory": 1}
    )
    schemes = await cursor.to_list(length=4)

    if len(schemes) < 2:
        return {"error": "Could not find enough schemes to compare"}

    schemes_text = "\n\n".join([
        f"SCHEME {i+1}: {s.get('scheme_name', '')}\n"
        f"Slug: {s.get('slug', '')}\n"
        f"Level: {s.get('level', '')}\n"
        f"Benefits: {s.get('benefits', '')[:300]}\n"
        f"Eligibility: {s.get('eligibility', '')[:300]}\n"
        f"Documents: {s.get('documents', '')[:200]}\n"
        f"Application: {s.get('application', '')[:200]}"
        for i, s in enumerate(schemes)
    ])

    prompt = COMPARISON_PROMPT.format(
        state=profile.get("state", "Not specified"),
        occupation=profile.get("occupation", "Not specified"),
        income=profile.get("annual_income", "Not specified"),
        category=profile.get("category", "Not specified"),
        schemes_text=schemes_text,
    )

    try:
        raw = await generate(prompt, temperature=0.2)
        result = json.loads(raw)

        # Attach full scheme data to each comparison item
        slug_to_scheme = {s["slug"]: s for s in schemes}
        for item in result.get("comparison", []):
            s = slug_to_scheme.get(item["slug"], {})
            item["level"] = s.get("level", "")
            item["schemeCategory"] = s.get("schemeCategory", [])

        return {
            "summary": result.get("summary", ""),
            "best_for_user": result.get("best_for_user", ""),
            "reason": result.get("reason", ""),
            "comparison": result.get("comparison", []),
            "schemes_compared": len(schemes),
        }

    except Exception as e:
        logger.error(f"Comparison agent failed: {e}")
        # Fallback: return basic scheme info without AI analysis
        return {
            "summary": "Comparison analysis unavailable. Showing basic scheme information.",
            "best_for_user": "",
            "reason": "",
            "comparison": [
                {
                    "slug": s.get("slug", ""),
                    "scheme_name": s.get("scheme_name", ""),
                    "key_benefit": s.get("benefits", "")[:100],
                    "target_audience": "",
                    "ease_of_apply": "Not analyzed",
                    "benefit_amount": "Not specified",
                    "pros": [],
                    "cons": [],
                    "level": s.get("level", ""),
                    "schemeCategory": s.get("schemeCategory", []),
                }
                for s in schemes
            ],
            "schemes_compared": len(schemes),
        }
