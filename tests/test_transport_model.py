"""
test_transport_model.py

Comprehensive unit test suite for transport_model.py
using pytest.

Tests:
- Normal operational scenarios
- Boundary conditions
- Edge cases
- Input validation
- Exception handling
"""

import pytest

from models.transport_model import (
    calculate_required_trips,
    calculate_transport_capacity,
    calculate_vehicle_utilisation,
    estimate_logistics_completion,
    evaluate_capacity_deficit,
    predict_cutoff_breach,
)


def test_calculate_transport_capacity():
    """
    Test transport capacity calculations and
    input validation.
    """

    # Standard calculation:
    # 150 crates × 2 trips = 300 crates
    assert calculate_transport_capacity(
        150,
        2
    ) == 300

    # Boundary condition:
    # No remaining trips
    assert calculate_transport_capacity(
        150,
        0
    ) == 0

    # Defensive validation:
    # Negative vehicle capacity
    with pytest.raises(
        ValueError,
        match="vehicle_capacity cannot be negative."
    ):
        calculate_transport_capacity(
            -150,
            2
        )

    # Defensive validation:
    # Negative remaining trips
    with pytest.raises(
        ValueError,
        match="remaining_trips cannot be negative."
    ):
        calculate_transport_capacity(
            150,
            -1
        )


def test_calculate_vehicle_utilisation():
    """
    Test vehicle utilisation percentage calculations
    and input validation.
    """

    # Standard partial load:
    # (120 ÷ 150) × 100 = 80.0%
    assert calculate_vehicle_utilisation(
        120,
        150
    ) == 80.0

    # Full utilisation:
    # (150 ÷ 150) × 100 = 100.0%
    assert calculate_vehicle_utilisation(
        150,
        150
    ) == 100.0

    # Empty load boundary:
    # (0 ÷ 150) × 100 = 0.0%
    assert calculate_vehicle_utilisation(
        0,
        150
    ) == 0.0

    # Defensive validation:
    # Negative crates loaded
    with pytest.raises(
        ValueError,
        match="crates_loaded cannot be negative."
    ):
        calculate_vehicle_utilisation(
            -10,
            150
        )

    # Defensive validation:
    # Zero available capacity
    with pytest.raises(
        ValueError,
        match="vehicle_capacity must be greater than zero."
    ):
        calculate_vehicle_utilisation(
            120,
            0
        )

    # Defensive validation:
    # Negative available capacity
    with pytest.raises(
        ValueError,
        match="vehicle_capacity must be greater than zero."
    ):
        calculate_vehicle_utilisation(
            120,
            -150
        )


def test_calculate_required_trips():
    """
    Test trip count calculations (ceiling division)
    and input validation.
    """

    # Exact division:
    # 450 crates ÷ 150 capacity = 3 trips
    assert calculate_required_trips(
        450,
        150
    ) == 3

    # Standard ceiling division:
    # 350 crates ÷ 150 capacity = 2.33 → 3 trips
    assert calculate_required_trips(
        350,
        150
    ) == 3

    # Partial trip required:
    # 520 crates ÷ 150 capacity = 3.47 → 4 trips
    assert calculate_required_trips(
        520,
        150
    ) == 4

    # Zero projected crates boundary:
    # No crates require transport
    assert calculate_required_trips(
        0,
        150
    ) == 0

    # Defensive validation:
    # Negative projected crates
    with pytest.raises(
        ValueError,
        match="projected_crates cannot be negative."
    ):
        calculate_required_trips(
            -100,
            150
        )

    # Defensive validation:
    # Zero vehicle capacity
    with pytest.raises(
        ValueError,
        match="vehicle_capacity must be greater than zero."
    ):
        calculate_required_trips(
            100,
            0
        )

    # Defensive validation:
    # Negative vehicle capacity
    with pytest.raises(
        ValueError,
        match="vehicle_capacity must be greater than zero."
    ):
        calculate_required_trips(
            100,
            -150
        )


def test_evaluate_capacity_deficit():
    """
    Test capacity deficit evaluation logic,
    dictionary structure, and input validation.
    """

    # Deficit scenario:
    # 520 projected crates - 450 capacity = 70 crate deficit
    result = evaluate_capacity_deficit(
        520,
        450
    )

    assert result["has_deficit"] is True
    assert result["capacity_gap"] == 70
    assert result["message"] == (
        "Capacity Shortage: Deficit of 70 crates."
    )

    # Exact match boundary:
    # 450 projected crates - 450 capacity = 0 deficit
    result = evaluate_capacity_deficit(
        450,
        450
    )

    assert result["has_deficit"] is False
    assert result["capacity_gap"] == 0
    assert result["message"] == (
        "Sufficient transport capacity available."
    )

    # Spare capacity scenario:
    # 350 projected crates - 450 capacity = -100
    result = evaluate_capacity_deficit(
        350,
        450
    )

    assert result["has_deficit"] is False
    assert result["capacity_gap"] == 0
    assert result["message"] == (
        "Sufficient transport capacity available."
    )

    # Defensive validation:
    # Negative projected crates
    with pytest.raises(
        ValueError,
        match="projected_crates cannot be negative."
    ):
        evaluate_capacity_deficit(
            -100,
            450
        )

    # Defensive validation:
    # Negative available capacity
    with pytest.raises(
        ValueError,
        match="available_capacity cannot be negative."
    ):
        evaluate_capacity_deficit(
            450,
            -100
        )

def test_estimate_logistics_completion():
    """
    Test logistics completion time estimation,
    default cycle times, time formatting,
    and input validation.
    """

    # Standard operational scenario:
    # 4 trips × 90 minutes = 360 minutes
    # 12:00 + 360 minutes = 18:00
    assert estimate_logistics_completion(
        "12:00",
        4,
        90
    ) == "18:00"

    # Default cycle time:
    # 2 trips × 90 minutes = 180 minutes
    # 08:00 + 180 minutes = 11:00
    assert estimate_logistics_completion(
        "08:00",
        2
    ) == "11:00"

    # Custom cycle time:
    # 1 trip × 45 minutes = 45 minutes
    # 08:00 + 45 minutes = 08:45
    assert estimate_logistics_completion(
        "08:00",
        1,
        45.0
    ) == "08:45"

    # Single-trip scenario:
    # 14:30 + 90 minutes = 16:00
    assert estimate_logistics_completion(
        "14:30",
        1,
        90
    ) == "16:00"

    # Zero-trip boundary:
    # No trips required, completion time remains unchanged
    assert estimate_logistics_completion(
        "12:00",
        0,
        90
    ) == "12:00"

    # Defensive validation:
    # Invalid time format
    with pytest.raises(
        ValueError,
        match="current_time must be in"
    ):
        estimate_logistics_completion(
            "8:00 AM",
            2
        )

    # Defensive validation:
    # Negative trips required
    with pytest.raises(
        ValueError,
        match="trips_required cannot be negative."
    ):
        estimate_logistics_completion(
            "12:00",
            -1,
            90
        )

    # Defensive validation:
    # Invalid cycle time
    with pytest.raises(
        ValueError,
        match="cycle_time_mins must be greater than zero."
    ):
        estimate_logistics_completion(
            "12:00",
            4,
            0
        )

def test_predict_cutoff_breach():
    """
    Test packhouse cut-off breach prediction,
    risk classification, dictionary structure,
    and input validation.
    """

    # GREEN status:
    # Completion time is more than 60 minutes
    # before the cut-off
    result = predict_cutoff_breach(
        "15:00"
    )

    assert result["status"] == "GREEN"
    assert result["is_breached"] is False
    assert result["completion_time"] == "15:00"
    assert result["cutoff_time"] == "17:00"
    assert result["message"] == (
        "ON TRACK: Transport operations are "
        "expected to complete safely before "
        "the cut-off."
    )

    # AMBER status:
    # Completion is within 60 minutes of cut-off
    result = predict_cutoff_breach(
        "16:30"
    )

    assert result["status"] == "AMBER"
    assert result["is_breached"] is False
    assert result["completion_time"] == "16:30"
    assert result["cutoff_time"] == "17:00"
    assert result["message"] == (
        "WARNING: Tight operational window. "
        "Completion is within one hour of "
        "the packhouse cut-off."
    )

    # RED status:
    # Completion exceeds cut-off by 60 minutes
    result = predict_cutoff_breach(
        "18:00"
    )

    assert result["status"] == "RED"
    assert result["is_breached"] is True
    assert result["completion_time"] == "18:00"
    assert result["cutoff_time"] == "17:00"
    assert result["message"] == (
        "CRITICAL: Packhouse cut-off breach "
        "predicted by 60 minutes."
    )

    # Default cut-off time scenario
    result = predict_cutoff_breach(
        "15:00"
    )

    assert result["status"] == "GREEN"
    assert result["cutoff_time"] == "17:00"

    # Defensive validation:
    # Invalid completion time format
    with pytest.raises(
        ValueError,
        match="Times must be in"
    ):
        predict_cutoff_breach(
            "5:00 PM"
        )

    # Defensive validation:
    # Invalid cut-off time format
    with pytest.raises(
        ValueError,
        match="Times must be in"
    ):
        predict_cutoff_breach(
            "15:00",
            "5:00 PM"
        )

