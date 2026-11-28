from argparse import ArgumentParser

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

from app.domain.proposals import OccurrenceProposal, ProposalEvidence
from app.infrastructure.database import database_url
from app.infrastructure.proposals import insert_proposal


def main() -> None:
    parser = ArgumentParser(description="Enviar uma proposta para revisão editorial.")
    parser.add_argument("--locality-id", type=int, required=True)
    parser.add_argument("--event-type", required=True)
    parser.add_argument("--year", type=int)
    parser.add_argument("--month", type=int)
    parser.add_argument("--day", type=int)
    parser.add_argument("--location-label")
    parser.add_argument(
        "--evidence", action="append", nargs=2, metavar=("FONTE", "URL")
    )
    args = parser.parse_args()

    try:
        proposal = OccurrenceProposal(
            locality_id=args.locality_id,
            event_type=args.event_type,
            occurred_year=args.year,
            occurred_month=args.month,
            occurred_day=args.day,
            location_label=args.location_label,
            evidence=tuple(
                ProposalEvidence(int(source_id), url)
                for source_id, url in (args.evidence or [])
            ),
        )
    except ValueError as error:
        parser.error(str(error))

    engine = create_engine(database_url())
    try:
        with engine.begin() as connection:
            proposal_id = insert_proposal(connection, proposal)
    except IntegrityError:
        parser.error("Verifique se a localidade e as fontes informadas existem.")
    finally:
        engine.dispose()

    print(f"Proposta {proposal_id} salva como pendente para revisão.")


if __name__ == "__main__":
    main()
