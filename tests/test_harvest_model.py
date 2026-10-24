"""
test_harvest_model.py

Comprehensive unit test suite for
harvest_model.py using pytest.

Tests:
- Progress percentage calculations
- Harvest rate calculations
- Worker productivity calculations
- Crate rejection rate calculations
- Boundary conditions
- Input validation
- Exception handling
"""

import pytest

from models.harvest_model import (
    calculate_progress_percentage,
    calculate_harvest_rate,
    calculate_worker_productivity,
    calculate_crate_rejection_rate,
)


def test_calculate_progress_percentage():
    """
    Test harvest progress calculations,
    zero-tree boundary conditions,
    and input validation.
    """

    # Standard progress scenario:
    # 75 harvested from 100 total trees
    assert calculate_progress_percentage(
        75,
        100
    ) == 75.0

    # Completed block:
    # 100 harvested from 100 total trees
    assert calculate_progress_percentage(
        100,
        100
    ) == 100.0

    # Zero harvested trees boundary:
    assert calculate_progress_percentage(
        0,
        100
    ) == 0.0

    # Zero-tree guard clause boundary:
    # Prevent division-by-zero
    assert calculate_progress_percentage(
        0,
        0
    ) == 0.0

    assert calculate_progress_percentage(
        50,
        0
    ) == 0.0

    # Defensive validation:
    # Negative harvested trees
    with pytest.raises(
        ValueError,
        match="trees_harvested_per_day cannot be negative."
    ):
        calculate_progress_percentage(
            -10,
            100
        )

    # Defensive validation:
    # Negative total trees
    with pytest.raises(
        ValueError,
        match="total_trees_in_block cannot be negative."
    ):
        calculate_progress_percentage(
            50,
            -100
        )



def test_calculate_harvest_rate():
    """
    Test harvest rate calculations,
    zero-crate boundary conditions,
    and input validation.
    """

    # Standard harvest-rate scenario:
    # 500 crates ÷ 10 hours = 50.0 crates/hour
    assert calculate_harvest_rate(
        500,
        10
    ) == 50.0

    # Fractional harvest-rate scenario:
    # 375 crates ÷ 8 hours = 46.875 crates/hour
    assert calculate_harvest_rate(
        375,
        8
    ) == 46.875

    # Zero crates harvested boundary:
    # 0 crates ÷ 10 hours = 0.0 crates/hour
    assert calculate_harvest_rate(
        0,
        10
    ) == 0.0

    # Defensive validation:
    # Negative total crates harvested
    with pytest.raises(
        ValueError,
        match="total_crates_harvested cannot be negative."
    ):
        calculate_harvest_rate(
            -50,
            10
        )

    # Defensive validation:
    # Zero hours worked
    with pytest.raises(
        ValueError,
        match="hours_worked must be greater than zero."
    ):
        calculate_harvest_rate(
            500,
            0
        )

    # Defensive validation:
    # Negative hours worked
    with pytest.raises(
        ValueError,
        match="hours_worked must be greater than zero."
    ):
        calculate_harvest_rate(
            500,
            -8
        )



def test_calculate_worker_productivity():
    """
    Test worker productivity calculations,
    zero-crate boundary conditions,
    and input validation.
    """

    # Standard worker-productivity scenario:
    # 500 crates ÷ (5 workers × 10 hours)
    # = 500 ÷ 50
    # = 10.0 crates/worker/hour
    assert calculate_worker_productivity(
        500,
        5,
        10
    ) == 10.0

    # Fractional productivity scenario:
    # 375 crates ÷ (4 workers × 8 hours)
    # = 375 ÷ 32
    # = 11.71875 crates/worker/hour
    assert calculate_worker_productivity(
        375,
        4,
        8
    ) == 11.71875

    # Zero crates harvested boundary:
    # 0 crates ÷ (5 workers × 10 hours)
    # = 0.0 crates/worker/hour
    assert calculate_worker_productivity(
        0,
        5,
        10
    ) == 0.0

    # Defensive validation:
    # Negative total crates harvested
    with pytest.raises(
        ValueError,
        match="total_crates_harvested cannot be negative."
    ):
        calculate_worker_productivity(
            -50,
            5,
            10
        )

    # Defensive validation:
    # Zero workers available
    with pytest.raises(
        ValueError,
        match="workers_available must be greater than zero."
    ):
        calculate_worker_productivity(
            500,
            0,
            10
        )

    # Defensive validation:
    # Negative workers available
    with pytest.raises(
        ValueError,
        match="workers_available must be greater than zero."
    ):
        calculate_worker_productivity(
            500,
            -5,
            10
        )

    # Defensive validation:
    # Zero hours worked
    with pytest.raises(
        ValueError,
        match="hours_worked must be greater than zero."
    ):
        calculate_worker_productivity(
            500,
            5,
            0
        )

    # Defensive validation:
    # Negative hours worked
    with pytest.raises(
        ValueError,
        match="hours_worked must be greater than zero."
    ):
        calculate_worker_productivity(
            500,
            5,
            -10
        )




def test_calculate_crate_rejection_rate():
    """
    Test crate rejection-rate calculations,
    dictionary return structure,
    boundary conditions, and
    input validation.
    """

    # Standard rejection-rate scenario:
    # 50 rejected crates out of 500 harvested
    # = 10.0%
    result = calculate_crate_rejection_rate(
        500,
        50
    )

    assert result == {
        "rejection_rate": 10.0
    }

    # Fractional rejection-rate scenario:
    # 15 rejected crates out of 400 harvested
    # = 3.75%
    result = calculate_crate_rejection_rate(
        400,
        15
    )

    assert result == {
        "rejection_rate": 3.75
    }

    # Zero rejected crates boundary:
    # 0 rejected crates out of 500 harvested
    # = 0.0%
    result = calculate_crate_rejection_rate(
        500,
        0
    )

    assert result == {
        "rejection_rate": 0.0
    }

    # Complete rejection scenario:
    # 500 rejected crates out of 500 harvested
    # = 100.0%
    result = calculate_crate_rejection_rate(
        500,
        500
    )

    assert result == {
        "rejection_rate": 100.0
    }

    # Defensive validation:
    # Zero harvested crates
    with pytest.raises(
        ValueError,
        match="total_crates_harvested must be greater than zero."
    ):
        calculate_crate_rejection_rate(
            0,
            0
        )

    # Defensive validation:
    # Negative harvested crates
    with pytest.raises(
        ValueError,
        match="total_crates_harvested must be greater than zero."
    ):
        calculate_crate_rejection_rate(
            -100,
            0
        )

    # Defensive validation:
    # Negative rejected crates
    with pytest.raises(
        ValueError,
        match="total_crates_rejected cannot be negative or exceed the total crates harvested."
    ):
        calculate_crate_rejection_rate(
            500,
            -10
        )

    # Defensive validation:
    # Rejected crates exceed harvested crates
    with pytest.raises(
        ValueError,
        match="total_crates_rejected cannot be negative or exceed the total crates harvested."
    ):
        calculate_crate_rejection_rate(
            500,
            600
        )


