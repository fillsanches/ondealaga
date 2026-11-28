"""Create flood occurrences, sources, and evidence."""

import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "sources",
        sa.Column("id", sa.BigInteger(), sa.Identity(), primary_key=True),
        sa.Column("name", sa.Text(), nullable=False),
    )
    op.create_table(
        "occurrences",
        sa.Column("id", sa.BigInteger(), sa.Identity(), primary_key=True),
        sa.Column("locality_id", sa.BigInteger(), nullable=False),
        sa.Column("event_type", sa.Text(), nullable=False),
        sa.Column("occurred_year", sa.SmallInteger(), nullable=True),
        sa.Column("occurred_month", sa.SmallInteger(), nullable=True),
        sa.Column("occurred_day", sa.SmallInteger(), nullable=True),
        sa.Column("location_label", sa.Text(), nullable=True),
        sa.Column("location_precision", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["locality_id"], ["localities.id"], name="fk_occurrences_locality"
        ),
        sa.CheckConstraint(
            "occurred_year BETWEEN 1 AND 9999",
            name="ck_occurrences_year",
        ),
        sa.CheckConstraint(
            "occurred_month IS NULL OR "
            "(occurred_year IS NOT NULL AND occurred_month BETWEEN 1 AND 12)",
            name="ck_occurrences_month",
        ),
        sa.CheckConstraint(
            "CASE WHEN occurred_day IS NULL THEN TRUE "
            "WHEN occurred_year IS NULL OR occurred_month IS NULL THEN FALSE "
            "ELSE make_date(occurred_year, occurred_month, occurred_day) "
            "IS NOT NULL END",
            name="ck_occurrences_day",
        ),
    )
    op.execute("ALTER TABLE occurrences ADD COLUMN location geography(Geometry, 4326)")
    op.create_check_constraint(
        "ck_occurrences_location_precision",
        "occurrences",
        "(location IS NULL AND location_precision IS NULL) OR "
        "(location IS NOT NULL AND location_precision IS NOT NULL "
        "AND location_precision IN ('exact', 'approximate') "
        "AND GeometryType(location::geometry) IN ('POINT', 'POLYGON', 'MULTIPOLYGON') "
        "AND NOT ST_IsEmpty(location::geometry))",
    )
    op.create_index(
        "ix_occurrences_location", "occurrences", ["location"], postgresql_using="gist"
    )
    op.create_index(
        "ix_occurrences_locality_date",
        "occurrences",
        ["locality_id", "occurred_year", "occurred_month", "occurred_day"],
    )

    op.create_table(
        "evidence",
        sa.Column("id", sa.BigInteger(), sa.Identity(), primary_key=True),
        sa.Column("occurrence_id", sa.BigInteger(), nullable=False),
        sa.Column("source_id", sa.BigInteger(), nullable=False),
        sa.Column("original_url", sa.Text(), nullable=False),
        sa.Column("published_on", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(
            ["occurrence_id"], ["occurrences.id"], name="fk_evidence_occurrence"
        ),
        sa.ForeignKeyConstraint(
            ["source_id"], ["sources.id"], name="fk_evidence_source"
        ),
        sa.UniqueConstraint(
            "occurrence_id",
            "source_id",
            "original_url",
            name="uq_evidence_occurrence_url",
        ),
    )


def downgrade() -> None:
    op.drop_table("evidence")
    op.drop_table("occurrences")
    op.drop_table("sources")
