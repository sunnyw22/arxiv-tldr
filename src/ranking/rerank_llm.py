import json
from dataclasses import dataclass

from src.core.config import LLMConfig
from src.core.models import Paper
from src.profiles.schema import UserProfile
from src.summarization.llm_client import call_llm
from src.summarization.prompts import build_ranking_prompt


@dataclass
class RankedPaper:
    """A paper with LLM-assigned relevance score and summary."""

    paper: Paper
    relevance_score: int
    reasoning: str
    summary: str
    abstract_takeaway: str = ""
    why_relevant: str = ""


def rerank_and_summarize(
    papers: list[Paper],
    profile: UserProfile,
    llm_config: LLMConfig,
    batch_size: int = 10,
    top_n: int = 10,
) -> list[RankedPaper]:
    """Send papers to LLM in batches for relevance scoring and summarization.

    Args:
        papers: Candidate papers to evaluate.
        profile: User research profile.
        llm_config: LLM configuration.
        batch_size: Number of papers per LLM call.
        top_n: Number of top papers to return.

    Returns:
        Top-N papers sorted by relevance score (highest first).
    """
    all_ranked: list[RankedPaper] = []

    for i in range(0, len(papers), batch_size):
        batch = papers[i : i + batch_size]
        ranked_batch = _rank_batch(batch, profile, llm_config)
        all_ranked.extend(ranked_batch)

    all_ranked.sort(key=lambda r: r.relevance_score, reverse=True)

    # Include all papers tied at the cutoff score rather than arbitrarily dropping some
    if len(all_ranked) > top_n:
        cutoff_score = all_ranked[top_n - 1].relevance_score
        return [r for r in all_ranked if r.relevance_score >= cutoff_score]
    return all_ranked


def _rank_batch(
    papers: list[Paper],
    profile: UserProfile,
    llm_config: LLMConfig,
) -> list[RankedPaper]:
    """Rank a single batch of papers via LLM."""
    prompt = build_ranking_prompt(papers, profile)
    response = call_llm(prompt, llm_config, json_mode=True)

    # Build lookup for papers by source_id
    paper_map = {p.source_id: p for p in papers}

    try:
        data = json.loads(response)
    except json.JSONDecodeError as e:
        print(f"  [WARNING] LLM returned invalid JSON: {e}")
        print(f"  Response preview: {response[:200]}")
        return [
            RankedPaper(paper=p, relevance_score=0, reasoning="LLM returned invalid JSON", summary="")
            for p in papers
        ]

    if "papers" not in data:
        print(f"  [WARNING] LLM response missing 'papers' key. Keys found: {list(data.keys())}")
        return [
            RankedPaper(paper=p, relevance_score=0, reasoning="LLM response missing expected structure", summary="")
            for p in papers
        ]

    results = []
    for idx, item in enumerate(data["papers"]):
        paper_id = item.get("paper_id", "")
        paper = paper_map.get(paper_id)

        if paper is None:
            # Fallback: match by position, but only if ordering looks consistent
            if idx < len(papers):
                paper = papers[idx]
                print(f"  [WARNING] LLM returned unrecognized paper_id '{paper_id}', "
                      f"falling back to positional match (paper {idx + 1}: {paper.title[:60]})")

        if paper is None:
            continue

        # Discard abstract_takeaway if it appears to describe a different paper
        abstract_takeaway = item.get("abstract_takeaway", "")
        if abstract_takeaway and paper.abstract and len(paper.abstract.split()) > 20:
            # Check if the takeaway mentions key terms from the actual abstract
            abstract_words = set(paper.abstract.lower().split())
            takeaway_words = set(abstract_takeaway.lower().split())
            overlap = len(abstract_words & takeaway_words)
            if overlap < 5:
                print(f"  [WARNING] abstract_takeaway for '{paper.title[:50]}' "
                      "may be hallucinated (low overlap), clearing")
                abstract_takeaway = ""

        results.append(RankedPaper(
            paper=paper,
            relevance_score=int(item.get("relevance_score", 0)),
            reasoning=item.get("reasoning", "No reasoning provided"),
            summary=item.get("summary", "No summary provided"),
            abstract_takeaway=abstract_takeaway,
            why_relevant=item.get("why_relevant", ""),
        ))
    return results
