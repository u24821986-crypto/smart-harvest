"""
test_optimisation_model.py

Comprehensive unit test suite for
optimisation_model.py using pytest.

Tests:
- Normal operational scenarios
- Boundary conditions
- Edge cases
- Input validation
- Exception handling
"""

import pytest

from models.optimisation_model import (
    calculate_block_harvest_rate,
    calculate_remaining_harvest_time,
    calculate_required_workers,
    evaluate_workforce_deficit,
    recommend_worker_transfer,
    predict_block_completion_risk,
)


def test_calculate_block_harvest_rate():
    """
    Test block harvest rate calculations,
    default productivity rates, and
    input validation.
    """

    # Standard operational scenario:
    # 10 workers × 12.5 crates/hour = 125.0
    assert calculate_block_harvest_rate(
        10
    ) == 125.0

    # Custom productivity rate:
    # 8 workers × 15.0 crates/hour = 120.0
    assert calculate_block_harvest_rate(
        8,
        15.0
    ) == 120.0

    # Zero workers boundary:
    # 0 workers × 12.5 crates/hour = 0.0
    assert calculate_block_harvest_rate(
        0
    ) == 0.0

    # Defensive validation:
    # Negative active workers
    with pytest.raises(
        ValueError,
        match="active_workers cannot be negative."
    ):
        calculate_block_harvest_rate(
            -5
        )

    # Defensive validation:
    # Zero productivity rate
    with pytest.raises(
        ValueError,
        match="picker_productivity_rate must be greater than zero."
    ):
        calculate_block_harvest_rate(
            10,
            0.0
        )

    # Defensive validation:
    # Negative productivity rate
    with pytest.raises(
        ValueError,
        match="picker_productivity_rate must be greater than zero."
    ):
        calculate_block_harvest_rate(
            10,
            -12.5
        )


def test_calculate_remaining_harvest_time():
    """
    Test remaining harvest time calculations,
    fractional durations, zero-crate boundaries,
    and input validation.
    """

    # Standard operational scenario:
    # 1000 crates ÷ 125 crates/hour = 8.0 hours
    assert calculate_remaining_harvest_time(
        1000,
        125
    ) == 8.0

    # Fractional time scenario:
    # 500 crates ÷ 80 crates/hour = 6.25 hours
    assert calculate_remaining_harvest_time(
        500,
        80
    ) == 6.25

    # Alternative operational scenario:
    # 250 crates ÷ 125 crates/hour = 2.0 hours
    assert calculate_remaining_harvest_time(
        250,
        125.0
    ) == 2.0

    # Zero remaining crates boundary:
    # No harvest remaining
    assert calculate_remaining_harvest_time(
        0,
        125
    ) == 0.0

    # Defensive validation:
    # Negative remaining crates
    with pytest.raises(
        ValueError,
        match="remaining_crates cannot be negative."
    ):
        calculate_remaining_harvest_time(
            -100,
            125
        )

    # Defensive validation:
    # Zero harvest rate
    with pytest.raises(
        ValueError,
        match="harvest_rate must be greater than zero."
    ):
        calculate_remaining_harvest_time(
            1000,
            0
        )

    # Defensive validation:
    # Negative harvest rate
    with pytest.raises(
        ValueError,
        match="harvest_rate must be greater than zero."
    ):
        calculate_remaining_harvest_time(
            1000,
            -125
        )


def test_calculate_required_workers():
    """
    Test required worker calculations,
    ceiling division behaviour, default
    productivity rates, and input validation.
    """

    # Standard operational scenario:
    # 1000 crates ÷ (10 hours × 12.5 crates/hour)
    # = 1000 ÷ 125
    # = 8 workers
    assert calculate_required_workers(
        1000,
        10
    ) == 8

    # Ceiling division scenario:
    # 260 crates ÷ (2 hours × 12.5 crates/hour)
    # = 260 ÷ 25
    # = 10.4 → 11 workers
    assert calculate_required_workers(
        260,
        2
    ) == 11

    # Exact division boundary:
    # 250 crates ÷ (2 hours × 12.5 crates/hour)
    # = 250 ÷ 25
    # = 10 workers
    assert calculate_required_workers(
        250,
        2
    ) == 10

    # Custom productivity rate:
    # 600 crates ÷ (8 hours × 15 crates/hour)
    # = 600 ÷ 120
    # = 5 workers
    assert calculate_required_workers(
        600,
        8,
        15.0
    ) == 5

    # Zero remaining crates boundary:
    # No harvest remaining
    assert calculate_required_workers(
        0,
        10
    ) == 0

    # Defensive validation:
    # Negative remaining crates
    with pytest.raises(
        ValueError,
        match="remaining_crates cannot be negative."
    ):
        calculate_required_workers(
            -100,
            10
        )

    # Defensive validation:
    # Zero available hours
    with pytest.raises(
        ValueError,
        match="available_hours must be greater than zero."
    ):
        calculate_required_workers(
            1000,
            0
        )

    # Defensive validation:
    # Negative available hours
    with pytest.raises(
        ValueError,
        match="available_hours must be greater than zero."
    ):
        calculate_required_workers(
            1000,
            -5
        )

    # Defensive validation:
    # Zero productivity rate
    with pytest.raises(
        ValueError,
        match="picker_productivity_rate must be greater than zero."
    ):
        calculate_required_workers(
            1000,
            10,
            0
        )

    # Defensive validation:
    # Negative productivity rate
    with pytest.raises(
        ValueError,
        match="picker_productivity_rate must be greater than zero."
    ):
        calculate_required_workers(
            1000,
            10,
            -12.5
        )



def test_evaluate_workforce_deficit():
    """
    Test workforce deficit evaluation logic,
    dictionary return structure, workforce
    surplus handling, and input validation.
    """

    # Workforce deficit scenario:
    # 12 required workers - 8 available workers
    # = 4 worker shortage
    result = evaluate_workforce_deficit(
        12,
        8
    )

    assert result["has_deficit"] is True
    assert result["worker_gap"] == 4
    assert result["message"] == (
        "Workforce Deficit: Shortage of 4 worker(s)."
    )

    # Exact workforce match boundary:
    # 10 required workers - 10 available workers
    # = 0 gap
    result = evaluate_workforce_deficit(
        10,
        10
    )

    assert result["has_deficit"] is False
    assert result["worker_gap"] == 0
    assert result["message"] == (
        "Sufficient workforce available."
    )

    # Workforce surplus scenario:
    # 8 required workers - 12 available workers
    # = surplus labour available
    result = evaluate_workforce_deficit(
        8,
        12
    )

    assert result["has_deficit"] is False
    assert result["worker_gap"] == 0
    assert result["message"] == (
        "Sufficient workforce available."
    )

    # Defensive validation:
    # Negative required workers
    with pytest.raises(
        ValueError,
        match="required_workers cannot be negative."
    ):
        evaluate_workforce_deficit(
            -5,
            10
        )

    # Defensive validation:
    # Negative available workers
    with pytest.raises(
        ValueError,
        match="available_workers cannot be negative."
    ):
        evaluate_workforce_deficit(
            10,
            -5
        )


def test_recommend_worker_transfer():
    """
    Test worker transfer recommendation logic,
    full and partial deficit resolution,
    zero-transfer boundaries, dictionary
    structure, and input validation.
    """

    # Full deficit resolution:
    # Worker gap = 4, donor surplus = 6
    # Transfer 4 workers, leaving a surplus of 2
    result = recommend_worker_transfer(
        4,
        6
    )

    assert result["transferred_workers"] == 4
    assert result["remaining_deficit"] == 0
    assert result["remaining_surplus"] == 2
    assert result["message"] == (
        "Transfer 4 worker(s) to eliminate the "
        "labour shortage."
    )

    # Partial deficit resolution:
    # Worker gap = 5, donor surplus = 3
    # Transfer 3 workers, leaving a deficit of 2
    result = recommend_worker_transfer(
        5,
        3
    )

    assert result["transferred_workers"] == 3
    assert result["remaining_deficit"] == 2
    assert result["remaining_surplus"] == 0
    assert result["message"] == (
        "Transfer 3 worker(s). Remaining deficit: "
        "2 worker(s)."
    )

    # Zero worker-gap boundary:
    # No labour shortage exists
    result = recommend_worker_transfer(
        0,
        5
    )

    assert result["transferred_workers"] == 0
    assert result["remaining_deficit"] == 0
    assert result["remaining_surplus"] == 5
    assert result["message"] == (
        "No worker transfer required."
    )

    # Zero donor-surplus boundary:
    # A deficit exists, but no workers are available
    # for transfer
    result = recommend_worker_transfer(
        4,
        0
    )

    assert result["transferred_workers"] == 0
    assert result["remaining_deficit"] == 4
    assert result["remaining_surplus"] == 0
    assert result["message"] == (
        "No worker transfer required."
    )

    # Defensive validation:
    # Negative worker gap
    with pytest.raises(
        ValueError,
        match="worker_gap cannot be negative."
    ):
        recommend_worker_transfer(
            -2,
            5
        )

    # Defensive validation:
    # Negative donor surplus
    with pytest.raises(
        ValueError,
        match="donor_surplus_workers cannot be negative."
    ):
        recommend_worker_transfer(
            4,
            -3
        )


def test_predict_block_completion_risk():
    """
    Test block completion risk predictions,
    GREEN/AMBER/RED risk classifications,
    time-buffer calculations, deadline
    boundaries, and input validation.
    """

    # GREEN status scenario:
    # 6 hours required, 10 hours available
    # Buffer = 4.0 hours
    result = predict_block_completion_risk(
        6,
        10
    )

    assert result["status"] == "GREEN"
    assert result["is_at_risk"] is False
    assert result["time_buffer_hours"] == 4.0
    assert result["message"] == (
        "ON TRACK: Harvest completion is "
        "expected comfortably before "
        "the deadline."
    )

    # AMBER status scenario:
    # 9.5 hours required, 10 hours available
    # Buffer = 0.5 hours
    result = predict_block_completion_risk(
        9.5,
        10
    )

    assert result["status"] == "AMBER"
    assert result["is_at_risk"] is True
    assert result["time_buffer_hours"] == 0.5
    assert result["message"] == (
        "WARNING: Harvest completion is "
        "predicted within one hour of "
        "the deadline."
    )

    # RED status scenario:
    # 12 hours required, 10 hours available
    # Overrun = 2 hours = 120 minutes
    result = predict_block_completion_risk(
        12,
        10
    )

    assert result["status"] == "RED"
    assert result["is_at_risk"] is True
    assert result["time_buffer_hours"] == -2.0
    assert result["message"] == (
        "CRITICAL: Harvest completion is "
        "predicted to miss the deadline by "
        "120 minute(s)."
    )

    # Exact deadline boundary:
    # 10 hours required, 10 hours available
    # Buffer = 0.0 hours
    result = predict_block_completion_risk(
        10,
        10
    )

    assert result["status"] == "AMBER"
    assert result["is_at_risk"] is True
    assert result["time_buffer_hours"] == 0.0

    # Defensive validation:
    # Negative remaining harvest time
    with pytest.raises(
        ValueError,
        match="remaining_harvest_time cannot be negative."
    ):
        predict_block_completion_risk(
            -1,
            10
        )

    # Defensive validation:
    # Zero available hours
    with pytest.raises(
        ValueError,
        match="available_hours must be greater than zero."
    ):
        predict_block_completion_risk(
            5,
            0
        )

    # Defensive validation:
    # Negative available hours
    with pytest.raises(
        ValueError,
        match="available_hours must be greater than zero."
    ):
        predict_block_completion_risk(
            5,
            -2
        )



