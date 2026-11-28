import os

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

from app.domain.proposals import OccurrenceProposal, ProposalEvidence
from app.infrastructure.database import database_url
from app.infrastructure.proposals import insert_proposal


@pytest.mark.parametrize("parts", [{"occurred_month": 3}, {"occurred_day": 3}])
def test_proposal_requires_date_components_in_order(parts: dict[str, int]) -> None:
    with pytest.raises(ValueError, match="quando houver"):
        OccurrenceProposal(locality_id=1, event_type="flood", **parts)


def test_proposal_rejects_invalid_calendar_date() -> None:
    with pytest.raises(ValueError, match="data de ocorrência válida"):
        OccurrenceProposal(1, "flood", 2026, 2, 29)


@pytest.mark.skipif(
    os.getenv("POSTGRES_HOST") != "checks-db",
    reason="Run with the isolated Compose checks database.",
)
def test_insert_proposal_keeps_evidence_and_leaves_occurrences_empty() -> None:
    engine = create_engine(database_url())
    try:
        with engine.connect() as connection:
            locality = connection.execute(
                text(
                    "INSERT INTO localities (name, country_code) "
                    "VALUES ('Editorial test', 'BR') RETURNING id"
                )
            ).scalar_one()
            source = connection.execute(
                text("INSERT INTO sources (name) VALUES ('Test source') RETURNING id")
            ).scalar_one()
            item = ProposalEvidence(source, "https://example.org/report")
            proposal = OccurrenceProposal(
                locality, "flood", 2026, 3, evidence=(item, item)
            )
            proposal_id = insert_proposal(connection, proposal)

            saved = connection.execute(
                text(
                    "SELECT status, occurred_year, occurred_month, occurred_day "
                    "FROM occurrence_proposals WHERE id = :id"
                ),
                {"id": proposal_id},
            ).one()
            assert saved == ("pending", 2026, 3, None)

            original_url = connection.execute(
                text(
                    "SELECT original_url FROM proposal_evidence WHERE proposal_id = :id"
                ),
                {"id": proposal_id},
            ).scalar_one()
            assert original_url == item.original_url

            published_count = connection.execute(
                text("SELECT count(*) FROM occurrences WHERE locality_id = :locality"),
                {"locality": locality},
            ).scalar_one()
            assert published_count == 0

            assert insert_proposal(connection, OccurrenceProposal(locality, "flood"))
            with pytest.raises(IntegrityError), connection.begin_nested():
                insert_proposal(
                    connection,
                    OccurrenceProposal(
                        locality,
                        "flood",
                        evidence=(ProposalEvidence(0, "https://example.org/missing"),),
                    ),
                )
            proposal_count = connection.execute(
                text(
                    "SELECT count(*) FROM occurrence_proposals "
                    "WHERE locality_id = :locality"
                ),
                {"locality": locality},
            ).scalar_one()
            assert proposal_count == 2
    finally:
        engine.dispose()
