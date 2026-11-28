from datetime import date

import pytest

from app.domain.coverage import CoverageStatus, classify_coverage


@pytest.mark.parametrize(
    ("intervals", "expected"),
    [
        ([], CoverageStatus.UNKNOWN),
        ([(1, 9), (21, 30)], CoverageStatus.UNKNOWN),
        ([(11, 20)], CoverageStatus.PARTIAL),
        ([(10, 19)], CoverageStatus.PARTIAL),
        ([(1, 13), (15, 30)], CoverageStatus.PARTIAL),
        ([(14, 30), (1, 13)], CoverageStatus.FULL),
        ([(13, 16), (15, 30), (1, 14)], CoverageStatus.FULL),
        ([(1, 30), (1, 30)], CoverageStatus.FULL),
    ],
)
def test_classify_coverage(
    intervals: list[tuple[int, int]], expected: CoverageStatus
) -> None:
    assert (
        classify_coverage(
            date(2026, 3, 10),
            date(2026, 3, 20),
            ((date(2026, 3, start), date(2026, 3, end)) for start, end in intervals),
        )
        == expected
    )


def test_classify_coverage_includes_end_dates() -> None:
    coverage = classify_coverage(date.max, date.max, [(date.max, date.max)])
    assert coverage == CoverageStatus.FULL


def test_classify_coverage_rejects_reversed_query() -> None:
    with pytest.raises(ValueError, match="end date"):
        classify_coverage(date(2026, 3, 20), date(2026, 3, 10), [])
