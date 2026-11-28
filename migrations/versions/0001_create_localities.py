"""Create localities and their external identifiers."""

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "localities",
        sa.Column("id", sa.BigInteger(), sa.Identity(), primary_key=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("country_code", sa.String(2), nullable=False),
        sa.Column("subdivision_code", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "country_code ~ '^[A-Z]{2}$'", name="ck_localities_country_code"
        ),
        sa.UniqueConstraint("id", "country_code", name="uq_localities_id_country"),
    )
    op.create_table(
        "locality_external_identifiers",
        sa.Column("locality_id", sa.BigInteger(), nullable=False),
        sa.Column("country_code", sa.String(2), nullable=False),
        sa.Column("identifier_system", sa.Text(), nullable=False),
        sa.Column("identifier_value", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "country_code", "identifier_system", "identifier_value"
        ),
        sa.ForeignKeyConstraint(
            ["locality_id", "country_code"],
            ["localities.id", "localities.country_code"],
            name="fk_locality_external_identifiers_locality",
        ),
    )


def downgrade() -> None:
    op.drop_table("locality_external_identifiers")
    op.drop_table("localities")
