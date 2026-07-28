import json
import logging
from app.agents.gemini_client import generate
from app.database.connection import db

logger = logging.getLogger(__name__)


DOCUMENT_CHECK_PROMPT = """You are a document verification assistant for Indian government schemes.

SCHEME NAME: {scheme_name}
REQUIRED DOCUMENTS (from scheme): {documents}
ELIGIBILITY: {eligibility}

USER'S AVAILABLE DOCUMENTS: {user_documents}

Analyze which required documents the user has and which are missing.

Respond in this exact JSON format:
{{
  "required_documents": ["doc1", "doc2", ...],
  "have": ["doc1", ...],
  "missing": ["doc2", ...],
  "optional": ["doc3", ...],
  "ready_to_apply": true or false,
  "readiness_score": 0-100,
  "advice": "One sentence of practical advice for the user"
}}

Rules:
- Extract individual document names from the scheme's documents text
- Match user documents against required ones (be flexible with naming, e.g. "Aadhaar" matches "Aadhaar Card")
- ready_to_apply is true only if all required (non-optional) documents are present
- Do not add explanation outside the JSON
"""


async def document_checker_agent(scheme_slug: str, user_documents: list[str]) -> dict:
    """
    Checks if the user has all required documents for a specific scheme.
    """
    scheme = await db["schemes"].find_one(
        {"slug": scheme_slug},
        {"scheme_name": 1, "documents": 1, "eligibility": 1}
    )

    if not scheme:
        return {"error": "Scheme not found"}

    if not user_documents:
        user_documents = []

    prompt = DOCUMENT_CHECK_PROMPT.format(
        scheme_name=scheme.get("scheme_name", ""),
        documents=scheme.get("documents", "No document information available"),
        eligibility=scheme.get("eligibility", "")[:400],
        user_documents=", ".join(user_documents) if user_documents else "None provided",
    )

    try:
        raw = await generate(prompt, temperature=0.1)
        result = json.loads(raw)
        return {
            "scheme_slug": scheme_slug,
            "scheme_name": scheme.get("scheme_name", ""),
            "required_documents": result.get("required_documents", []),
            "have": result.get("have", []),
            "missing": result.get("missing", []),
            "optional": result.get("optional", []),
            "ready_to_apply": result.get("ready_to_apply", False),
            "readiness_score": result.get("readiness_score", 0),
            "advice": result.get("advice", ""),
        }
    except Exception as e:
        logger.error(f"Document checker failed for {scheme_slug}: {e}")
        return {
            "scheme_slug": scheme_slug,
            "scheme_name": scheme.get("scheme_name", ""),
            "required_documents": [],
            "have": [],
            "missing": [],
            "optional": [],
            "ready_to_apply": False,
            "readiness_score": 0,
            "advice": "Could not analyze documents. Please check the scheme page for document requirements.",
        }
