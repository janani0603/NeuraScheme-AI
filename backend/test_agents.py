import asyncio
import sys

PROFILE = {
    "state": "Tamil Nadu",
    "gender": "female",
    "occupation": "student",
    "education": "graduate",
    "annual_income": 200000,
    "category": "general",
    "is_student": True,
    "is_farmer": False,
    "is_business_owner": False,
    "has_disability": False,
    "age": 21,
}

BASE_STATE = {
    "user_id": "test123",
    "profile": PROFILE,
    "profile_valid": False,
    "profile_completeness": 0.0,
    "candidates": [],
    "scored_schemes": [],
    "ranked_schemes": [],
    "explanations": {},
    "final_recommendations": [],
    "error": None,
}


def test_profile_agent():
    from app.agents.profile_agent import profile_agent
    state = dict(BASE_STATE)
    state["profile"] = dict(PROFILE)
    result = profile_agent(state)
    print(f"[Profile Agent] valid={result['profile_valid']} completeness={result['profile_completeness']} error={result['error']}")
    return result


async def test_retrieval_agent(profile_state):
    from app.agents.retrieval_agent import retrieval_agent
    result = await retrieval_agent(profile_state)
    print(f"[Retrieval Agent] candidates={len(result.get('candidates', []))}")
    return result


def test_eligibility_agent_sync(candidates, profile):
    from app.services.eligibility_service import score_scheme
    scored = []
    for scheme in candidates[:5]:
        r = score_scheme(scheme, profile)
        scored.append(r)
    print(f"[Eligibility Service] scored 5 samples, scores: {[round(r['eligibility_score'],1) for r in scored]}")
    return scored


async def test_eligibility_agent(retrieval_state):
    from app.agents.eligibility_agent import eligibility_agent
    result = await eligibility_agent(retrieval_state)
    print(f"[Eligibility Agent] scored_schemes={len(result.get('scored_schemes', []))}")
    return result


async def test_recommendation_agent(eligibility_state):
    from app.agents.recommendation_agent import recommendation_agent
    result = await recommendation_agent(eligibility_state)
    ranked = result.get("ranked_schemes", [])
    print(f"[Recommendation Agent] ranked={len(ranked)}")
    if ranked:
        top = ranked[0]
        print(f"  Top: {top['scheme']['scheme_name'][:50]} | eligibility={top['eligibility_score']} confidence={top['confidence_score']}")
    return result


async def test_explanation_agent(recommendation_state):
    from app.agents.explanation_agent import explanation_agent
    result = await explanation_agent(recommendation_state)
    explanations = result.get("explanations", {})
    print(f"[Explanation Agent] explanations generated={len(explanations)}")
    if explanations:
        first_key = list(explanations.keys())[0]
        print(f"  Sample ({first_key}): {explanations[first_key][:120]}")
    return result


async def test_groq_direct():
    from app.agents.gemini_client import generate
    try:
        response = await asyncio.wait_for(generate("Say hello in one word.", temperature=0.1), timeout=10)
        print(f"[Groq/LLM] OK - response: {response[:80]}")
        return True
    except Exception as e:
        print(f"[Groq/LLM] FAILED - {e}")
        return False


async def test_deadline_agent():
    from app.agents.deadline_agent import deadline_agent
    try:
        result = await asyncio.wait_for(
            deadline_agent(user_id="test123", scheme_slugs=["pm-kisan-samman-nidhi", "national-scholarship-portal"]),
            timeout=20
        )
        print(f"[Deadline Agent] deadlines={len(result.get('deadlines', []))} urgent={result.get('urgent_count', 0)}")
        return True
    except Exception as e:
        print(f"[Deadline Agent] FAILED - {e}")
        return False


async def test_document_checker_agent():
    from app.agents.document_checker_agent import document_checker_agent
    try:
        result = await asyncio.wait_for(
            document_checker_agent("national-scholarship-portal", ["Aadhaar Card", "Income Certificate"]),
            timeout=20
        )
        if "error" in result:
            print(f"[Document Checker Agent] scheme not found - {result['error']}")
        else:
            print(f"[Document Checker Agent] readiness={result.get('readiness_score')} have={result.get('have')} missing={result.get('missing')}")
        return True
    except Exception as e:
        print(f"[Document Checker Agent] FAILED - {e}")
        return False


async def test_comparison_agent():
    from app.agents.comparison_agent import comparison_agent
    try:
        result = await asyncio.wait_for(
            comparison_agent(
                scheme_slugs=["pm-kisan-samman-nidhi", "national-scholarship-portal"],
                profile=PROFILE
            ),
            timeout=20
        )
        if "error" in result:
            print(f"[Comparison Agent] FAILED - {result['error']}")
        else:
            print(f"[Comparison Agent] summary={result.get('summary','')[:80]} best_for_user={result.get('best_for_user')}")
        return True
    except Exception as e:
        print(f"[Comparison Agent] FAILED - {e}")
        return False


async def test_full_pipeline():
    from app.agents.workflow import run_recommendation_pipeline
    try:
        result = await asyncio.wait_for(
            run_recommendation_pipeline(PROFILE, "test123"),
            timeout=90
        )
        print(f"[Full Pipeline] total={result['total']} completeness={result['profile_completeness']} error={result.get('error')}")
        if result["recommendations"]:
            top = result["recommendations"][0]
            print(f"  Top rec: {top['scheme_name'][:50]} | eligibility={top['eligibility_score']} confidence={top['confidence_score']}")
            print(f"  Explanation: {top['explanation'][:120]}")
        return True
    except Exception as e:
        print(f"[Full Pipeline] FAILED - {e}")
        return False


async def main():
    print("\n" + "="*60)
    print(" NeuraScheme AI — Agent Status Check")
    print("="*60 + "\n")

    # 1. Profile Agent
    profile_state = test_profile_agent()

    # 2. Retrieval Agent
    retrieval_state = await test_retrieval_agent(profile_state)

    # 3. Eligibility Agent
    eligibility_state = await test_eligibility_agent(retrieval_state)

    # 4. Recommendation Agent
    recommendation_state = await test_recommendation_agent(eligibility_state)

    # 5. Explanation Agent
    await test_explanation_agent(recommendation_state)

    # 6. Groq LLM direct
    await test_groq_direct()

    # 7. Deadline Agent
    await test_deadline_agent()

    # 8. Document Checker Agent
    await test_document_checker_agent()

    # 9. Comparison Agent
    await test_comparison_agent()

    # 10. Full LangGraph Pipeline
    print("\n--- Full Pipeline Test ---")
    await test_full_pipeline()

    print("\n" + "="*60)
    print(" Done")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
