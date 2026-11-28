"""Store occurrence proposals and their evidence for editorial review."""

import sqlalchemy as sa
from alembic import op

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "occurrence_proposals",
        sa.Column("id", sa.BigInteger(), sa.Identity(), primary_key=True),
        sa.Column("locality_id", sa.BigInteger(), nullable=False),
        sa.Column("event_type", sa.Text(), nullable=False),
        sa.Column("occurred_year", sa.SmallInteger()),
        sa.Column("occurred_month", sa.SmallInteger()),
        sa.Column("occurred_day", sa.SmallInteger()),
        sa.Column("location_label", sa.Text()),
        sa.Column("status", sa.Text(), server_default="pending", nullable=False),
        sa.Column(
            "submitted_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["locality_id"], ["localities.id"], name="fk_occurrence_proposals_locality"
        ),
        sa.CheckConstraint(
            "event_type ~ '[^[:space:]]'", name="ck_occurrence_proposals_event_type"
        ),
        sa.CheckConstraint(
            "status IN ('pending', 'approved', 'rejected')",
            name="ck_occurrence_proposals_status",
        ),
        sa.CheckConstraint(
            "occurred_year BETWEEN 1 AND 9999", name="ck_occurrence_proposals_year"
        ),
        sa.CheckConstraint(
            "occurred_month IS NULL OR "
            "(occurred_year IS NOT NULL AND occurred_month BETWEEN 1 AND 12)",
            name="ck_occurrence_proposals_month",
        ),
        sa.CheckConstraint(
            "CASE WHEN occurred_day IS NULL THEN TRUE "
            "WHEN occurred_year IS NULL OR occurred_month IS NULL THEN FALSE "
            "ELSE make_date(occurred_year, occurred_month, occurred_day) "
            "IS NOT NULL END",
            name="ck_occurrence_proposals_day",
        ),
    )
    op.create_table(
        "proposal_evidence",
        sa.Column("proposal_id", sa.BigInteger(), primary_key=True),
        sa.Column("source_id", sa.BigInteger(), primary_key=True),
        sa.Column("original_url", sa.Text(), primary_key=True),
        sa.ForeignKeyConstraint(
            ["proposal_id"],
            ["occurrence_proposals.id"],
            name="fk_proposal_evidence_proposal",
        ),
        sa.ForeignKeyConstraint(
            ["source_id"], ["sources.id"], name="fk_proposal_evidence_source"
        ),
        sa.CheckConstraint(
            "original_url ~ '[^[:space:]]'", name="ck_proposal_evidence_original_url"
        ),
    )


def downgrade() -> None:
    op.drop_table("proposal_evidence")
    op.drop_table("occurrence_proposals")
