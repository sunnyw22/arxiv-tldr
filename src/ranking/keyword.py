from dataclasses import dataclass, field

from src.core.models import Paper
from src.profiles.schema import UserProfile


@dataclass
class ScoredPaper:
    """A paper with its relevance score and match reasons."""

    paper: Paper
    score: float
    matched_interests: list[str] = field(default_factory=list)
    matched_signals: list[str] = field(default_factory=list)


def score_paper(paper: Paper, profile: UserProfile) -> ScoredPaper | None:
    """Score a single paper against the user profile.

    Returns None if the paper matches any negative filter (hard reject).
    """
    text = f"{paper.title} {paper.abstract}".lower()

    # Hard reject on negative filters
    for neg in profile.negative_filters:
        if neg.lower() in text:
            return None

    score = 0.0
    matched_interests = []
    matched_signals = []

    # Topic interests: +1.0 per match
    for interest in profile.topic_interests:
        if interest.lower() in text:
            score += 1.0
            matched_interests.append(interest)

    # Required signals: +0.5 bonus per match
    for signal in profile.required_signals:
        if signal.lower() in text:
            score += 0.5
            matched_signals.append(signal)

    # Reject papers with no keyword matches at all
    if score == 0.0:
        return None

    return ScoredPaper(
        paper=paper,
        score=score,
        matched_interests=matched_interests,
        matched_signals=matched_signals,
    )
