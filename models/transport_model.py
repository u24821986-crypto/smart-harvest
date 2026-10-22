"""
Smart Transport Model

Provides (for Rembander Agribusiness): 
- Transport Planning
- Vehicle Utilisation
- Capacity Forecasting
- Packhouse Cut-off Analysis

"""

import math
from datetime import datetime, timedelta


def calculate_transport_capacity(
    vehicle_capacity: int,
    remaining_trips: int
) -> int:
    
    """

    Calculate total remaining transport capacity for the day in crates.

    
    Formula
    -------
    -> Transport Capacity = Vehicle Capacity × Remaining Trips

    Parameters
    ----------
    -> vehicle_capacity : int
        Number of crates that can be transported
        per trip.

    -> remaining_trips : int
        Number of trips still available.

    Returns
    -------
    -> int
        Total remaining transport capacity in crates.

    Raises
    ------
    -> ValueError
        If vehicle_capacity is negative.

    -> ValueError
        If remaining_trips is negative.
    
    """

    if vehicle_capacity < 0:
        raise ValueError(
            "vehicle_capacity cannot be negative."
        )

    if remaining_trips < 0:
        raise ValueError(
            "remaining_trips cannot be negative."
        )

    transport_capacity = (
        vehicle_capacity *
        remaining_trips
    )

    return transport_capacity


def calculate_vehicle_utilisation(
    crates_loaded: int,
    vehicle_capacity: int
) -> float:
    
    """
    Calculate vehicle utilisation percentage.

    Formula
    -------
    Vehicle Utilisation (%) =
    (Crates Loaded ÷ Vehicle Capacity) × 100

    Parameters
    ----------
    crates_loaded : int
        Number of crates loaded or transported.

    vehicle_capacity : int
        Total available vehicle capacity.

    Returns
    -------
    float
        Vehicle utilisation percentage,
        rounded to 2 decimal places.

    Raises
    ------
    ValueError
        If crates_loaded is negative.

    ValueError
        If vehicle_capacity is less than or equal to zero.
    """

    if crates_loaded < 0:
        raise ValueError(
            "crates_loaded cannot be negative."
        )

    if vehicle_capacity <= 0:
        raise ValueError(
            "vehicle_capacity must be greater than zero."
        )

    utilisation = (
        crates_loaded /
        vehicle_capacity
    ) * 100.0

    return round(utilisation, 2)



def calculate_required_trips(
    projected_crates: int,
    vehicle_capacity: int
) -> int:
    """
    Calculate the number of trips required to
    transport all projected crates.

    Formula
    -------
    Required Trips =
    Ceiling(Projected Crates ÷ Vehicle Capacity)

    Parameters
    ----------
    projected_crates : int
        Total projected crates that require transport.

    vehicle_capacity : int
        Number of crates that can be transported
        per trip.

    Returns
    -------
    int
        Total number of trips required,
        rounded up to the nearest whole trip.

    Raises
    ------
    ValueError
        If projected_crates is negative.

    ValueError
        If vehicle_capacity is less than or equal to zero.
    """

    if projected_crates < 0:
        raise ValueError(
            "projected_crates cannot be negative."
        )

    if vehicle_capacity <= 0:
        raise ValueError(
            "vehicle_capacity must be greater than zero."
        )

    if projected_crates == 0:
        return 0

    required_trips = math.ceil(
        projected_crates /
        vehicle_capacity
    )

    return required_trips



def evaluate_capacity_deficit(
    projected_crates: int,
    available_capacity: int
) -> dict:
    """
    Evaluate whether available transport capacity
    is sufficient to handle the projected harvest.

    Formula
    -------
    Capacity Deficit =
    Projected Crates − Available Capacity

    Parameters
    ----------
    projected_crates : int
        Total projected crates requiring transport.

    available_capacity : int
        Total remaining transport capacity.

    Returns
    -------
    dict
        Dictionary containing:

        has_deficit : bool
            True if projected crates exceed
            available capacity.

        capacity_gap : int
            Number of crates that cannot currently
            be transported.

        message : str
            Human-readable capacity status.

    Raises
    ------
    ValueError
        If projected_crates is negative.

    ValueError
        If available_capacity is negative.
    """

    if projected_crates < 0:
        raise ValueError(
            "projected_crates cannot be negative."
        )

    if available_capacity < 0:
        raise ValueError(
            "available_capacity cannot be negative."
        )

    capacity_deficit = (
        projected_crates -
        available_capacity
    )

    has_deficit = capacity_deficit > 0

    capacity_gap = max(
        0,
        capacity_deficit
    )

    if has_deficit:
        message = (
            f"Capacity Shortage: Deficit of "
            f"{capacity_gap} crates."
        )
    else:
        message = (
            "Sufficient transport capacity available."
        )

    return {
        "has_deficit": has_deficit,
        "capacity_gap": capacity_gap,
        "message": message
    }





def estimate_logistics_completion(
    current_time: str,
    trips_required: int,
    cycle_time_mins: float = 90.0
) -> str:
    """
    Estimate the completion time of transport operations.

    Formula
    -------
    Total Logistics Time =
    Trips Required × Cycle Time

    Estimated Completion Time =
    Current Time + Total Logistics Time

    Parameters
    ----------
    current_time : str
        Current time or dispatch start time
        in HH:MM format.

    trips_required : int
        Number of trips required to transport
        all projected crates.

    cycle_time_mins : float, optional
        Average duration of one complete trip cycle
        in minutes. Default is 90.0 minutes.

    Returns
    -------
    str
        Estimated logistics completion time
        in HH:MM format.

    Raises
    ------
    ValueError
        If trips_required is negative.

    ValueError
        If cycle_time_mins is less than or equal to zero.

    ValueError
        If current_time is not in HH:MM format.
    """

    if trips_required < 0:
        raise ValueError(
            "trips_required cannot be negative."
        )

    if cycle_time_mins <= 0:
        raise ValueError(
            "cycle_time_mins must be greater than zero."
        )

    try:
        start_time = datetime.strptime(
            current_time,
            "%H:%M"
        )
    except ValueError:
        raise ValueError(
            "current_time must be in 'HH:MM' 24-hour format."
        )

    if trips_required == 0:
        return current_time

    total_logistics_time = (
        trips_required *
        cycle_time_mins
    )

    completion_time = (
        start_time +
        timedelta(
            minutes=total_logistics_time
        )
    )

    return completion_time.strftime(
        "%H:%M"
    )



def predict_cutoff_breach(
    completion_time: str,
    cutoff_time: str = "17:00"
) -> dict:
    """
    Predict whether transport operations will breach
    the packhouse cut-off time and assign an
    operational risk status.

    Classification
    --------------
    GREEN:
        Completion time is at least 60 minutes
        before cut-off.

    AMBER:
        Completion time is within 60 minutes
        of cut-off.

    RED:
        Completion time exceeds cut-off.

    Parameters
    ----------
    completion_time : str
        Estimated logistics completion time
        in HH:MM format.

    cutoff_time : str, optional
        Packhouse cut-off time in HH:MM format.
        Default is "17:00".

    Returns
    -------
    dict
        Dictionary containing:

        status : str
            Risk classification
            ("GREEN", "AMBER", or "RED").

        completion_time : str
            Estimated logistics completion time.

        cutoff_time : str
            Target cut-off time.

        is_breached : bool
            True if completion exceeds cut-off.

        message : str
            Human-readable operational assessment.

    Raises
    ------
    ValueError
        If completion_time is not in HH:MM format.

    ValueError
        If cutoff_time is not in HH:MM format.
    """

    try:
        completion = datetime.strptime(
            completion_time,
            "%H:%M"
        )

        cutoff = datetime.strptime(
            cutoff_time,
            "%H:%M"
        )

    except ValueError:
        raise ValueError(
            "Times must be in 'HH:MM' 24-hour format."
        )

    amber_threshold = (
        cutoff -
        timedelta(minutes=60)
    )

    is_breached = completion > cutoff

    if is_breached:
        status = "RED"

        minutes_late = int(
            (completion - cutoff).total_seconds() / 60
        )

        message = (
            f"CRITICAL: Packhouse cut-off breach "
            f"predicted by {minutes_late} minutes."
        )

    elif completion > amber_threshold:
        status = "AMBER"

        message = (
            "WARNING: Tight operational window. "
            "Completion is within one hour of "
            "the packhouse cut-off."
        )

    else:
        status = "GREEN"

        message = (
            "ON TRACK: Transport operations are "
            "expected to complete safely before "
            "the cut-off."
        )

    return {
        "status": status,
        "completion_time": completion_time,
        "cutoff_time": cutoff_time,
        "is_breached": is_breached,
        "message": message
    }



