"""Record the periods covered by sources for each locality."""

import sqlalchemy as sa
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "source_coverages",
        sa.Column("id", sa.BigInteger(), sa.Identity(), primary_key=True),
        sa.Column("locality_id", sa.BigInteger(), nullable=False),
        sa.Column("source_id", sa.BigInteger(), nullable=False),
        sa.Column("starts_on", sa.Date(), nullable=False),
        sa.Column("ends_on", sa.Date(), nullable=False),
        sa.Column("reference_url", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["locality_id"], ["localities.id"], name="fk_source_coverages_locality"
        ),
        sa.ForeignKeyConstraint(
            ["source_id"], ["sources.id"], name="fk_source_coverages_source"
        ),
        sa.CheckConstraint(
            "ends_on >= starts_on", name="ck_source_coverages_date_order"
        ),
        sa.CheckConstraint(
            "reference_url ~ '[^[:space:]]'", name="ck_source_coverages_reference"
        ),
    )
    op.create_index(
        "ix_source_coverages_locality_dates",
        "source_coverages",
        ["locality_id", "starts_on", "ends_on"],
    )


def downgrade() -> None:
    op.drop_table("source_coverages")
