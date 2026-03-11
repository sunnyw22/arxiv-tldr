from src.core.models import Paper
from src.profiles.schema import UserProfile
from src.ranking.keyword import ScoredPaper, score_paper


def rank_papers(
    papers: list[Paper],
    profile: UserProfile,
    max_papers: int = 10,
    min_score: float = 0.0,
) -> list[ScoredPaper]:
    """Score, filter, and rank papers against a user profile.

    Args:
        papers: List of candidate papers.
        profile: User research profile.
        max_papers: Maximum number of papers to return.
        min_score: Minimum score threshold (papers below this are excluded).

    Returns:
        Sorted list of ScoredPaper, highest score first, capped at max_papers.
    """
    scored = []
    for paper in papers:
        result = score_paper(paper, profile)
        if result is not None and result.score >= min_score:
            scored.append(result)

    scored.sort(key=lambda s: s.score, reverse=True)
    return scored[:max_papers]
