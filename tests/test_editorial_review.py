import pytest

from app.domain.editorial_review import ProposalStatus, ReviewOutcome, review_proposal


def test_approve_pending_proposal_with_evidence() -> None:
    status = review_proposal(
        ProposalStatus.PENDING,
        ReviewOutcome.APPROVE,
        has_evidence=True,
        reason="The report confirms the location and date.",
    )

    assert status is ProposalStatus.APPROVED


def test_reject_pending_proposal_without_evidence() -> None:
    status = review_proposal(
        ProposalStatus.PENDING,
        ReviewOutcome.REJECT,
        has_evidence=False,
        reason="The report provides no evidence.",
    )

    assert status is ProposalStatus.REJECTED


def test_approve_requires_evidence() -> None:
    with pytest.raises(ValueError, match="Evidence is required"):
        review_proposal(
            ProposalStatus.PENDING,
            ReviewOutcome.APPROVE,
            has_evidence=False,
            reason="The location was reported.",
        )


@pytest.mark.parametrize("outcome", list(ReviewOutcome))
def test_review_requires_a_reason(outcome: ReviewOutcome) -> None:
    with pytest.raises(ValueError, match="review reason is required"):
        review_proposal(ProposalStatus.PENDING, outcome, has_evidence=True, reason="  ")


@pytest.mark.parametrize("status", [ProposalStatus.APPROVED, ProposalStatus.REJECTED])
def test_review_requires_a_pending_proposal(status: ProposalStatus) -> None:
    with pytest.raises(ValueError, match="Only pending proposals"):
        review_proposal(
            status, ReviewOutcome.REJECT, has_evidence=True, reason="Duplicate event."
        )
