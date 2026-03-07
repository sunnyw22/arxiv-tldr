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
    return all_ranked[:top_n]


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
        results = []
        for item in data.get("papers", []):
            paper_id = item.get("paper_id", "")
            paper = paper_map.get(paper_id)
            if paper is None:
                # Try matching by position if ID doesn't match
                idx = data["papers"].index(item)
                if idx < len(papers):
                    paper = papers[idx]
                else:
                    continue

            results.append(RankedPaper(
                paper=paper,
                relevance_score=int(item.get("relevance_score", 0)),
                reasoning=item.get("reasoning", ""),
                summary=item.get("summary", ""),
            ))
        return results
    except (json.JSONDecodeError, KeyError, ValueError):
        # If LLM response is unparseable, return papers with score 0
        return [
            RankedPaper(paper=p, relevance_score=0, reasoning="LLM response parsing failed", summary="")
            for p in papers
        ]
