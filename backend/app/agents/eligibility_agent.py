import json
import logging
from app.agents.profile_agent import AgentState
from app.services.eligibility_service import score_scheme
from app.agents.gemini_client import generate
from app.agents.prompts import eligibility_interpretation_prompt

logger = logging.getLogger(__name__)

MIN_SCORE = 35.0
GEMINI_ASSIST_THRESHOLD = 45.0  # Only call Gemini for borderline schemes


async def eligibility_agent(state: AgentState) -> AgentState:
    """
    Scores each candidate scheme using deterministic rule-based logic.
    For borderline schemes, optionally uses Gemini to interpret complex
    eligibility text — but never overrides the rule-based score entirely.
    """
    candidates = state.get("candidates", [])
    profile = state.get("profile", {})

    if not candidates:
        return {**state, "scored_schemes": []}

    scored = []

    for scheme in candidates:
        # Step 1 — deterministic rule-based scoring (always runs)
        result = score_scheme(scheme, profile)
        eligibility_score = result["eligibility_score"]

        # Step 2 — Gemini assists only for borderline schemes with complex eligibility text
        if MIN_SCORE <= eligibility_score <= GEMINI_ASSIST_THRESHOLD:
            eligibility_text = scheme.get("eligibility", "")
            if len(eligibility_text) > 100:  # Only if there's substantial text to interpret
                try:
                    prompt = eligibility_interpretation_prompt(eligibility_text, profile)
                    raw = await generate(prompt, temperature=0.1)
                    parsed = json.loads(raw)
                    meets = parsed.get("meets", [])
                    does_not_meet = parsed.get("does_not_meet", [])

                    # Adjust score slightly based on Gemini interpretation
                    # Gemini can nudge score by max ±10 points, never fully override
                    if meets and not does_not_meet:
                        eligibility_score = min(eligibility_score + 8, 100)
                        result["matched_conditions"] += [f"AI: {m}" for m in meets[:2]]
                    elif does_not_meet and not meets:
                        eligibility_score = max(eligibility_score - 8, 0)
                        result["missing_conditions"] += [f"AI: {d}" for d in does_not_meet[:2]]

                except Exception as e:
                    logger.warning(f"Gemini eligibility assist failed for {scheme.get('slug')}: {e}")

        if eligibility_score >= MIN_SCORE:
            scored.append({
                "scheme": scheme,
                "eligibility_score": round(eligibility_score, 1),
                "confidence_score": result["confidence_score"],
                "matched_conditions": result["matched_conditions"],
                "missing_conditions": result["missing_conditions"],
                "vector_score": scheme.get("vector_score", 0.0),
            })

    # Sort by eligibility score descending
    scored.sort(key=lambda x: x["eligibility_score"], reverse=True)

    logger.info(f"Eligibility agent scored {len(scored)} schemes above threshold")
    return {**state, "scored_schemes": scored}
