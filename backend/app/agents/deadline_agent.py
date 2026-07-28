import asyncio
import logging
from datetime import datetime, UTC
from app.agents.gemini_client import generate
from app.database.connection import db

logger = logging.getLogger(__name__)


DEADLINE_PROMPT = """You are analyzing a government scheme for deadline information.

SCHEME NAME: {scheme_name}
SCHEME DETAILS: {details}
BENEFITS: {benefits}
ELIGIBILITY: {eligibility}
APPLICATION PROCESS: {application}

Extract any deadline, last date, or time-sensitive information from the above text.

Respond in this exact JSON format:
{{
  "has_deadline": true or false,
  "deadline_text": "exact deadline text from the scheme or null",
  "deadline_date": "YYYY-MM-DD if a specific date is found, else null",
  "is_ongoing": true if the scheme is ongoing/permanent with no fixed deadline,
  "urgency": "high" if deadline is within 30 days, "medium" if within 90 days, "low" otherwise or if no deadline
}}

Do not add any explanation outside the JSON.
"""


async def _extract_deadline(scheme: dict) -> dict:
    """Use Groq to extract deadline info from a single scheme."""
    prompt = DEADLINE_PROMPT.format(
        scheme_name=scheme.get("scheme_name", ""),
        details=scheme.get("details", "")[:500],
        benefits=scheme.get("benefits", "")[:300],
        eligibility=scheme.get("eligibility", "")[:300],
        application=scheme.get("application", "")[:300],
    )
    try:
        import json
        raw = await generate(prompt, temperature=0.1)
        parsed = json.loads(raw)
        return {
            "slug": scheme.get("slug", ""),
            "scheme_name": scheme.get("scheme_name", ""),
            "has_deadline": parsed.get("has_deadline", False),
            "deadline_text": parsed.get("deadline_text"),
            "deadline_date": parsed.get("deadline_date"),
            "is_ongoing": parsed.get("is_ongoing", False),
            "urgency": parsed.get("urgency", "low"),
        }
    except Exception as e:
        logger.warning(f"Deadline extraction failed for {scheme.get('slug')}: {e}")
        return {
            "slug": scheme.get("slug", ""),
            "scheme_name": scheme.get("scheme_name", ""),
            "has_deadline": False,
            "deadline_text": None,
            "deadline_date": None,
            "is_ongoing": True,
            "urgency": "low",
        }


async def deadline_agent(user_id: str, scheme_slugs: list[str]) -> dict:
    """
    Extracts deadline information for a list of schemes.
    Runs Groq extractions concurrently.
    Returns schemes sorted by urgency.
    """
    if not scheme_slugs:
        return {"deadlines": [], "urgent_count": 0}

    # Fetch schemes from MongoDB
    cursor = db["schemes"].find(
        {"slug": {"$in": scheme_slugs}},
        {"slug": 1, "scheme_name": 1, "details": 1, "benefits": 1, "eligibility": 1, "application": 1}
    )
    schemes = await cursor.to_list(length=len(scheme_slugs))

    if not schemes:
        return {"deadlines": [], "urgent_count": 0}

    # Concurrent deadline extraction
    tasks = [_extract_deadline(s) for s in schemes]
    results = await asyncio.gather(*tasks)

    # Sort: high urgency first, then medium, then low, ongoing last
    urgency_order = {"high": 0, "medium": 1, "low": 2}
    results_list = list(results)
    results_list.sort(key=lambda x: (
        0 if x["has_deadline"] else 1,
        urgency_order.get(x["urgency"], 2)
    ))

    urgent_count = sum(1 for r in results_list if r["urgency"] == "high" and r["has_deadline"])

    # Save to MongoDB for notification use
    if user_id:
        await db["deadline_alerts"].update_one(
            {"userId": user_id},
            {
                "$set": {
                    "userId": user_id,
                    "deadlines": results_list,
                    "updatedAt": datetime.now(UTC),
                }
            },
            upsert=True,
        )

    return {
        "deadlines": results_list,
        "urgent_count": urgent_count,
    }
