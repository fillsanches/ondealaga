from enum import StrEnum


class ProposalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ReviewOutcome(StrEnum):
    APPROVE = "approve"
    REJECT = "reject"


def review_proposal(
    status: ProposalStatus,
    outcome: ReviewOutcome,
    *,
    has_evidence: bool,
    reason: str,
) -> ProposalStatus:
    """Apply the rules for deciding a pending occurrence proposal."""
    if status is not ProposalStatus.PENDING:
        raise ValueError("Only pending proposals can be reviewed.")
    if not reason.strip():
        raise ValueError("A review reason is required.")
    if outcome is ReviewOutcome.REJECT:
        return ProposalStatus.REJECTED
    if outcome is ReviewOutcome.APPROVE:
        if not has_evidence:
            raise ValueError("Evidence is required to approve a proposal.")
        return ProposalStatus.APPROVED
    raise ValueError("Invalid review outcome.")
