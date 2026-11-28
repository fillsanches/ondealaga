from dataclasses import dataclass
from datetime import date
from urllib.parse import urlsplit


@dataclass(frozen=True, slots=True)
class ProposalEvidence:
    source_id: int
    original_url: str

    def __post_init__(self) -> None:
        url = urlsplit(self.original_url)
        if url.scheme not in ("http", "https") or not url.hostname:
            raise ValueError("Informe uma URL HTTP ou HTTPS para a evidência.")


@dataclass(frozen=True, slots=True)
class OccurrenceProposal:
    locality_id: int
    event_type: str
    occurred_year: int | None = None
    occurred_month: int | None = None
    occurred_day: int | None = None
    location_label: str | None = None
    evidence: tuple[ProposalEvidence, ...] = ()

    def __post_init__(self) -> None:
        if not self.event_type.strip():
            raise ValueError("Informe o tipo de ocorrência.")
        if self.occurred_month is not None and self.occurred_year is None:
            raise ValueError("Informe o ano quando houver um mês.")
        if self.occurred_day is not None and self.occurred_month is None:
            raise ValueError("Informe o mês quando houver um dia.")
        if self.occurred_year is not None:
            try:
                date(
                    self.occurred_year,
                    1 if self.occurred_month is None else self.occurred_month,
                    1 if self.occurred_day is None else self.occurred_day,
                )
            except ValueError as error:
                raise ValueError("Informe uma data de ocorrência válida.") from error
