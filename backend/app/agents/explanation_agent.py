import logging
from app.agents.profile_agent import AgentState
from app.agents.gemini_client import generate
from app.agents.prompts import explanation_prompt

logger = logging.getLogger(__name__)

EXPLAIN_TOP_N = 10  # Only generate Gemini explanations for top N schemes


async def explanation_agent(state: AgentState) -> AgentState:
    """
    Generates personalized explanations for top recommendations using Gemini.
    Falls back to the rule-based explanation for remaining schemes.
    All explanations are grounded in stored scheme data only.
    """
    ranked = state.get("ranked_schemes", [])
    profile = state.get("profile", {})
    explanations = {}

    for i, item in enumerate(ranked):
        scheme = item["scheme"]
        slug = scheme.get("slug", "")
        matched = item.get("matched_conditions", [])
        missing = item.get("missing_conditions", [])

        if i < EXPLAIN_TOP_N:
            try:
                prompt = explanation_prompt(scheme, profile, matched, missing)
                explanation = await generate(prompt, temperature=0.4)
                explanations[slug] = explanation
            except Exception as e:
                logger.warning(f"Gemini explanation failed for {slug}: {e}")
                explanations[slug] = _fallback_explanation(matched, missing, item["eligibility_score"])
        else:
            explanations[slug] = _fallback_explanation(matched, missing, item["eligibility_score"])

    return {**state, "explanations": explanations}


def _fallback_explanation(matched: list, missing: list, score: float) -> str:
    if score >= 75:
        verdict = "You are likely eligible for this scheme."
    elif score >= 50:
        verdict = "You may partially qualify for this scheme."
    else:
        verdict = "You may not meet all requirements for this scheme."

    matched_str = "; ".join(matched) if matched else "No strong matches identified"
    missing_str = "; ".join(missing) if missing else "No major gaps identified"
    return f"{verdict} Matched: {matched_str}. Gaps: {missing_str}."
