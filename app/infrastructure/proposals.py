from sqlalchemy import Connection, text

from app.domain.proposals import OccurrenceProposal


def insert_proposal(connection: Connection, proposal: OccurrenceProposal) -> int:
    proposal_id = connection.execute(
        text(
            """
            INSERT INTO occurrence_proposals (
                locality_id, event_type, occurred_year, occurred_month,
                occurred_day, location_label
            ) VALUES (
                :locality_id, :event_type, :occurred_year, :occurred_month,
                :occurred_day, :location_label
            ) RETURNING id
            """
        ),
        {
            "locality_id": proposal.locality_id,
            "event_type": proposal.event_type,
            "occurred_year": proposal.occurred_year,
            "occurred_month": proposal.occurred_month,
            "occurred_day": proposal.occurred_day,
            "location_label": proposal.location_label,
        },
    ).scalar_one()
    if proposal.evidence:
        connection.execute(
            text(
                """
                INSERT INTO proposal_evidence (proposal_id, source_id, original_url)
                VALUES (:proposal_id, :source_id, :original_url)
                ON CONFLICT (proposal_id, source_id, original_url) DO NOTHING
                """
            ),
            [
                {
                    "proposal_id": proposal_id,
                    "source_id": item.source_id,
                    "original_url": item.original_url,
                }
                for item in proposal.evidence
            ],
        )
    return proposal_id
