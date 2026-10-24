"""
test_bottleneck_model.py

Comprehensive unit test suite for
bottleneck_model.py using pytest.

Tests:
- Constraint Identification (Labour vs Transport vs Balanced)
- Vehicle Capacity Gap Calculations
- Bottleneck Severity Classification
- Labour Bottleneck Identification
- Worker Shortage Estimation
- Boundary Conditions and Zero-Value Handling
- Input Validation and Exception Handling
"""

import pytest

from models.bottleneck_model import (
    identify_constraint,
    calculate_capacity_gap,
    classify_bottleneck,
    identify_labour_bottleneck,
)



def test_identify_constraint():
    """
    Test constraint identification logic for
    labour, transport, and balanced scenarios,
    along with input validation.
    """

    # Labour constraint scenario:
    # Progress (40%) < Utilisation (80%)
    assert identify_constraint(
        40.0,
        80.0
    ) == "Labour is the constraint."

    # Transport constraint scenario:
    # Utilisation (50%) < Progress (85%)
    assert identify_constraint(
        85.0,
        50.0
    ) == "Transport is the constraint."

    # Balanced scenario:
    # Progress (75%) == Utilisation (75%)
    assert identify_constraint(
        75.0,
        75.0
    ) == "Both are balanced."

    # Defensive validation:
    # Negative progress
    with pytest.raises(
        ValueError,
        match="progress cannot be negative."
    ):
        identify_constraint(
            -10.0,
            50.0
        )

    # Defensive validation:
    # Negative utilisation
    with pytest.raises(
        ValueError,
        match="utilisation cannot be negative."
    ):
        identify_constraint(
            50.0,
            -5.0
        )



def test_calculate_capacity_gap():
    """
    Test unused vehicle capacity gap calculations,
    boundary conditions, over-capacity handling,
    and input validation.
    """

    # Standard capacity-gap scenario:
    # 150 capacity - 120 loaded = 30.0 crates gap
    assert calculate_capacity_gap(
        150,
        120
    ) == 30.0

    # Full-capacity boundary:
    # 150 capacity - 150 loaded = 0.0 crates gap
    assert calculate_capacity_gap(
        150,
        150
    ) == 0.0

    # Over-capacity safeguard:
    # 150 capacity - 175 loaded = -25
    # max(0, -25) = 0.0
    assert calculate_capacity_gap(
        150,
        175
    ) == 0.0

    # Defensive validation:
    # Negative vehicle capacity
    with pytest.raises(
        ValueError,
        match="vehicle_capacity cannot be negative."
    ):
        calculate_capacity_gap(
            -150,
            100
        )

    # Defensive validation:
    # Negative crates loaded
    with pytest.raises(
        ValueError,
        match="crates_loaded cannot be negative."
    ):
        calculate_capacity_gap(
            150,
            -10
        )



def test_classify_bottleneck():
    """
    Test bottleneck severity classifications,
    boundary conditions, and input validation.
    """

    # No bottleneck scenario:
    # Gap = 0
    assert classify_bottleneck(
        0,
        150
    ) == "No bottleneck."

    # Minor bottleneck scenario:
    # 20% of 150 = 30
    # Gap = 25 <= 30
    assert classify_bottleneck(
        25,
        150
    ) == "Minor bottleneck."

    # Minor bottleneck threshold boundary:
    # Gap = exactly 20% of capacity
    # 30 = 20% of 150
    assert classify_bottleneck(
        30,
        150
    ) == "Minor bottleneck."

    # Severe bottleneck scenario:
    # Gap exceeds 20% of capacity
    # 50 > 30
    assert classify_bottleneck(
        50,
        150
    ) == "Severe bottleneck."

    # Defensive validation:
    # Negative gap
    with pytest.raises(
        ValueError,
        match="gap cannot be negative."
    ):
        classify_bottleneck(
            -10,
            150
        )

    # Defensive validation:
    # Zero vehicle capacity
    with pytest.raises(
        ValueError,
        match="vehicle_capacity must be greater than zero."
    ):
        classify_bottleneck(
            10,
            0
        )

    # Defensive validation:
    # Negative vehicle capacity
    with pytest.raises(
        ValueError,
        match="vehicle_capacity must be greater than zero."
    ):
        classify_bottleneck(
            10,
            -150
        )



def test_identify_labour_bottleneck():
    """
    Test labour bottleneck identification,
    workforce shortage estimations,
    sufficient capacity messaging,
    boundary conditions, and
    input validation.
    """

    # Labour shortage scenario:
    # 200 harvested out of 1000 trees
    # Progress = 20.0%
    result = identify_labour_bottleneck(
        "Block A",
        200,
        1000,
        5,
        4,
        4
    )

    assert (
        "Block A: Progress 20.0%."
        in result
    )

    assert (
        "Shortage! Add"
        in result
    )

    # Labour capacity sufficient scenario:
    # Remaining workload can be completed
    # with the current workforce.
    result = identify_labour_bottleneck(
        "Block B",
        800,
        1000,
        5,
        4,
        4
    )

    assert result == (
        "Block B: Progress 80.0%. "
        "Labour capacity is sufficient."
    )

    # Fallback productivity scenario:
    # No hours worked yet, so default
    # productivity should be applied.
    result = identify_labour_bottleneck(
        "Block C",
        0,
        100,
        2,
        0,
        4
    )

    assert (
        "Block C: Progress 0.0%."
        in result
    )

    assert isinstance(
        result,
        str
    )

    # Defensive validation:
    # Negative trees harvested
    with pytest.raises(
        ValueError,
        match="trees_harvested cannot be negative."
    ):
        identify_labour_bottleneck(
            "Block A",
            -50,
            1000,
            5,
            4,
            4
        )

    # Defensive validation:
    # Zero total trees in block
    with pytest.raises(
        ValueError,
        match="total_trees_in_block must be greater than zero."
    ):
        identify_labour_bottleneck(
            "Block A",
            200,
            0,
            5,
            4,
            4
        )

    # Defensive validation:
    # Negative workers available
    with pytest.raises(
        ValueError,
        match="workers_available cannot be negative."
    ):
        identify_labour_bottleneck(
            "Block A",
            200,
            1000,
            -5,
            4,
            4
        )

    # Defensive validation:
    # Negative hours worked so far
    with pytest.raises(
        ValueError,
        match="hours_worked_so_far cannot be negative."
    ):
        identify_labour_bottleneck(
            "Block A",
            200,
            1000,
            5,
            -4,
            4
        )

    # Defensive validation:
    # Negative hours left in day
    with pytest.raises(
        ValueError,
        match="hours_left_in_day cannot be negative."
    ):
        identify_labour_bottleneck(
            "Block A",
            200,
            1000,
            5,
            4,
            -4
        )


