from collections.abc import Iterable
from datetime import date
from enum import StrEnum


class CoverageStatus(StrEnum):
    UNKNOWN = "unknown"
    PARTIAL = "partial"
    FULL = "full"


def classify_coverage(
    starts_on: date, ends_on: date, intervals: Iterable[tuple[date, date]]
) -> CoverageStatus:
    """Classify coverage over inclusive dates for a single locality."""
    if ends_on < starts_on:
        raise ValueError("The query end date must be on or after the start date.")

    first_day = starts_on.toordinal()
    last_day = ends_on.toordinal()
    next_uncovered_day = first_day

    for covered_from, covered_through in sorted(intervals):
        if covered_through < starts_on:
            continue
        if covered_from > ends_on:
            break
        if covered_from.toordinal() > next_uncovered_day:
            return CoverageStatus.PARTIAL

        next_uncovered_day = max(next_uncovered_day, covered_through.toordinal() + 1)
        if next_uncovered_day > last_day:
            return CoverageStatus.FULL

    if next_uncovered_day == first_day:
        return CoverageStatus.UNKNOWN
    return CoverageStatus.PARTIAL
