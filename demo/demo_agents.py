"""
NeuraScheme AI — Agent Demo Script
====================================
Run this to showcase each AI agent individually to your mentors.
This script is completely separate from the main project.

Usage:
    cd "c:\\...\\NeuraScheme-AI\\backend"
    venv\\Scripts\\Activate.ps1
    python ../demo/demo_agents.py

Each agent runs one by one with clear output showing what it does.
"""

import asyncio
import sys
import os

# Add backend to path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\backend")

# ── Sample user profile for demo ─────────────────────────────────────────────
DEMO_PROFILE = {
    "state": "tamil nadu",
    "gender": "female",
    "occupation": "student",
    "education": "graduate",
    "annual_income": 180000.0,
    "category": "obc",
    "is_student": True,
    "is_farmer": False,
    "is_business_owner": False,
    "has_disability": False,
    "age": 21,
}

DEMO_USER_ID = "demo_user_001"

SEP = "=" * 65


def print_header(title: str):
    print(f"\n{SEP}")
    print(f"  {title}")
    print(SEP)


def print_section(label: str, value):
    print(f"\n  {label}:")
    if isinstance(value, list):
        for i, item in enumerate(value[:5], 1):
            print(f"    {i}. {item}")
        if len(value) > 5:
            print(f"    ... and {len(value) - 5} more")
    elif isinstance(value, dict):
        for k, v in list(value.items())[:5]:
            print(f"    {k}: {v}")
    else:
        print(f"    {value}")


# ─────────────────────────────────────────────────────────────────────────────
# AGENT 1 — Profile Agent
# ─────────────────────────────────────────────────────────────────────────────
def demo_profile_agent():
    print_header("AGENT 1 — Profile Agent")
    print("  Purpose: Validates and normalizes the user profile.")
    print("  Input  : Raw user profile data")

    from app.agents.profile_agent import profile_agent, AgentState

    raw_profile = {
        "state": "Tamil Nadu",
        "gender": "Female",
        "occupation": "Student",
        "education": "Graduate",
        "annual_income": 180000,
        "category": "OBC",
        "is_student": True,
        "is_farmer": False,
        "is_business_owner": False,
        "has_disability": False,
        "age": 21,
    }

    print("\n  Raw Input Profile:")
    for k, v in raw_profile.items():
        print(f"    {k}: {v}")

    state: AgentState = {"profile": raw_profile}
    result = profile_agent(state)

    print("\n  Output After Normalization:")
    for k, v in result["profile"].items():
        print(f"    {k}: {v}")

    print(f"\n  Profile Valid      : {result['profile_valid']}")
    print(f"  Profile Completeness: {round(result['profile_completeness'] * 100)}%")
    print(f"  Error              : {result.get('error') or 'None'}")
    print("\n  ✅ Profile Agent — DONE")
    return result


# ─────────────────────────────────────────────────────────────────────────────
# AGENT 2 — Retrieval Agent
# ─────────────────────────────────────────────────────────────────────────────
async def demo_retrieval_agent(profile_state: dict):
    print_header("AGENT 2 — Retrieval Agent")
    print("  Purpose: Retrieves candidate schemes from ChromaDB (semantic)")
    print("           or MongoDB (fallback text search).")

    from app.database.connection import connect_to_mongodb
    from app.agents.retrieval_agent import retrieval_agent

    await connect_to_mongodb()

    result = await retrieval_agent(profile_state)
    candidates = result.get("candidates", [])

    print(f"\n  Schemes Retrieved  : {len(candidates)}")
    print("\n  Top 5 Candidates:")
    for i, s in enumerate(candidates[:5], 1):
        score = s.get("vector_score", 0)
        print(f"    {i}. {s.get('scheme_name', 'N/A')[:55]}")
        print(f"       Level: {s.get('level', '?')} | Vector Score: {round(score, 3)}")

    print("\n  ✅ Retrieval Agent — DONE")
    return result


# ─────────────────────────────────────────────────────────────────────────────
# AGENT 3 — Eligibility Agent
# ─────────────────────────────────────────────────────────────────────────────
async def demo_eligibility_agent(retrieval_state: dict):
    print_header("AGENT 3 — Eligibility Agent")
    print("  Purpose: Scores each candidate scheme against the user profile.")
    print("           Filters out schemes below the eligibility threshold.")

    from app.agents.eligibility_agent import eligibility_agent

    result = await eligibility_agent(retrieval_state)
    scored = result.get("scored_schemes", [])

    print(f"\n  Schemes Scored     : {len(retrieval_state.get('candidates', []))}")
    print(f"  Passed Threshold   : {len(scored)}")
    print("\n  Top 5 Scored Schemes:")
    for i, item in enumerate(scored[:5], 1):
        scheme = item["scheme"]
        print(f"    {i}. {scheme.get('scheme_name', 'N/A')[:50]}")
        print(f"       Eligibility Score : {item['eligibility_score']}%")
        print(f"       Matched Conditions: {', '.join(item['matched_conditions'][:3]) or 'None'}")
        print(f"       Missing Conditions: {', '.join(item['missing_conditions'][:2]) or 'None'}")

    print("\n  ✅ Eligibility Agent — DONE")
    return result


# ─────────────────────────────────────────────────────────────────────────────
# AGENT 4 — Recommendation Agent
# ─────────────────────────────────────────────────────────────────────────────
async def demo_recommendation_agent(eligibility_state: dict):
    print_header("AGENT 4 — Recommendation Agent")
    print("  Purpose: Combines eligibility score + semantic similarity +")
    print("           profile completeness into a final confidence score.")
    print("  Formula: (eligibility*0.60) + (vector*0.25) + (completeness*0.15)")

    from app.agents.recommendation_agent import recommendation_agent

    result = await recommendation_agent(eligibility_state)
    ranked = result.get("ranked_schemes", [])

    completeness = round(eligibility_state.get("profile_completeness", 0) * 100)
    print(f"\n  Profile Completeness: {completeness}%")
    print(f"  Total Ranked        : {len(ranked)}")
    print("\n  Top 5 Final Rankings:")
    for i, item in enumerate(ranked[:5], 1):
        scheme = item["scheme"]
        print(f"    {i}. {scheme.get('scheme_name', 'N/A')[:50]}")
        print(f"       Eligibility Score : {item['eligibility_score']}%")
        print(f"       Confidence Score  : {item['combined_score']}%")

    print("\n  ✅ Recommendation Agent — DONE")
    return result


# ─────────────────────────────────────────────────────────────────────────────
# AGENT 5 — Explanation Agent
# ─────────────────────────────────────────────────────────────────────────────
async def demo_explanation_agent(recommendation_state: dict):
    print_header("AGENT 5 — Explanation Agent (Groq / Llama)")
    print("  Purpose: Generates personalized AI explanations for top schemes.")
    print("           Uses Groq (Llama) for top 3, fallback text for rest.")

    from app.agents.explanation_agent import explanation_agent

    result = await explanation_agent(recommendation_state)
    explanations = result.get("explanations", {})
    ranked = recommendation_state.get("ranked_schemes", [])

    print(f"\n  Explanations Generated: {len(explanations)}")
    print("\n  Top 3 AI Explanations:")
    for i, item in enumerate(ranked[:3], 1):
        slug = item["scheme"].get("slug", "")
        name = item["scheme"].get("scheme_name", "N/A")
        explanation = explanations.get(slug, "No explanation generated.")
        print(f"\n    {i}. {name[:55]}")
        print(f"       Score: {item['eligibility_score']}%")
        print(f"       Explanation: {explanation[:200]}...")

    print("\n  ✅ Explanation Agent — DONE")
    return result


# ─────────────────────────────────────────────────────────────────────────────
# AGENT 6 — AI Assistant Agent
# ─────────────────────────────────────────────────────────────────────────────
async def demo_assistant_agent():
    print_header("AGENT 6 — AI Assistant Agent (Groq / Llama)")
    print("  Purpose: Answers user questions about government schemes.")
    print("           Routes to sub-agents: general, documents, deadlines,")
    print("           comparison, recommendations.")

    from app.agents.application_agent import application_agent

    question = "What documents do I need to apply for a scholarship scheme in Tamil Nadu?"
    print(f"\n  Demo Question: \"{question}\"")
    print("\n  Running assistant agent...")

    result = await application_agent(
        user_id=DEMO_USER_ID,
        question=question,
        conversation_id=None,
        scheme_slugs=[],
    )

    print(f"\n  Agents Used   : {', '.join(result.get('agents_used', []))}")
    print(f"\n  AI Response:\n")
    response = result.get("response", "No response.")
    # Print response in wrapped lines
    words = response.split()
    line = "    "
    for word in words:
        if len(line) + len(word) > 75:
            print(line)
            line = "    " + word + " "
        else:
            line += word + " "
    if line.strip():
        print(line)

    print("\n  ✅ AI Assistant Agent — DONE")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN — Run all agents in order
# ─────────────────────────────────────────────────────────────────────────────
async def main():
    print(f"\n{'#' * 65}")
    print("  NeuraScheme AI — Multi-Agent Demo")
    print("  Showcasing all 6 agents running individually")
    print(f"{'#' * 65}")

    print("\n  Demo Profile:")
    for k, v in DEMO_PROFILE.items():
        if v not in (False, None):
            print(f"    {k}: {v}")

    try:
        # Agent 1 — Profile Agent (sync)
        profile_state = demo_profile_agent()

        if not profile_state.get("profile_valid"):
            print("\n  ❌ Profile invalid. Cannot continue demo.")
            return

        # Agent 2 — Retrieval Agent
        retrieval_state = await demo_retrieval_agent(profile_state)

        if not retrieval_state.get("candidates"):
            print("\n  ❌ No candidates retrieved. Cannot continue demo.")
            return

        # Agent 3 — Eligibility Agent
        eligibility_state = await demo_eligibility_agent(retrieval_state)

        if not eligibility_state.get("scored_schemes"):
            print("\n  ❌ No schemes passed eligibility. Cannot continue demo.")
            return

        # Agent 4 — Recommendation Agent
        recommendation_state = await demo_recommendation_agent(eligibility_state)

        # Agent 5 — Explanation Agent
        await demo_explanation_agent(recommendation_state)

        # Agent 6 — AI Assistant Agent
        await demo_assistant_agent()

        print(f"\n{'#' * 65}")
        print("  ✅ All 6 Agents Demonstrated Successfully!")
        print(f"{'#' * 65}\n")

    except Exception as e:
        print(f"\n  ❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
