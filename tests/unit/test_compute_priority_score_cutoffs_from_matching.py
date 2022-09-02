import pytest

from python.compute_priority_score_cutoffs_from_matching import (
    compute_priority_score_cutoffs_from_matching,
)
from python.contract import Contract


contracts = {"C1": Contract("C1"), "C2": Contract("C2"), "C3": Contract("C3")}
contracts["C1"].score_dictionary = {"A1": 10.1, "A2": 10.2}
contracts["C2"].score_dictionary = {"A1": 10.1, "A2": 10.2}

use_cases = [
    {"matching": {"A1": None, "A2": None}, "expected": {"C1": 0, "C2": 0, "C3": 0}},
    {
        "matching": {"A1": "C1", "A2": "C2"},
        "expected": {"C1": 10.1, "C2": 10.2, "C3": 0},
    },
    {"matching": {"A1": "C1", "A2": "C1"}, "expected": {"C1": 10.1, "C2": 0, "C3": 0}},
]


@pytest.mark.parametrize("use_case", use_cases)
def test__compute_priority_score_cutoffs__normal_matching__returns_right_cutoffs(
    use_case,
):
    matching = use_case["matching"]

    priority_score_cutoffs = compute_priority_score_cutoffs_from_matching(
        matching, contracts
    )

    assert priority_score_cutoffs == use_case["expected"]
