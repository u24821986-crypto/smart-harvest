"""
SmartHarvest Optimisation Model

Provides:
- labour optimisation, 
- workforce allocation, 
- harvest completion forecasting,
- operational risk assessment.

"""


def calculate_block_harvest_rate(
    workers_available: int,
    picker_productivity_rate: float = 12.5
) -> float:
    """
    Calculate total hourly harvesting capacity
    for a block.

    Formula
    -------
    Harvest Rate =
    Workers Available × Picker Productivity Rate

    Parameters
    ----------
    workers_available : int
        Number of active workers assigned
        to the block.

    picker_productivity_rate : float, optional
        Average crates harvested per worker
        per hour. Default is 12.5 crates per
        worker per hour.

    Returns
    -------
    float
        Total harvesting rate in crates
        per hour.

    Raises
    ------
    ValueError
        If workers_available is negative.

    ValueError
        If picker_productivity_rate is less
        than or equal to zero.
    """

    if workers_available < 0:
        raise ValueError(
            "workers_available cannot be negative."
        )

    if picker_productivity_rate <= 0:
        raise ValueError(
            "picker_productivity_rate must be greater than zero."
        )

    harvest_rate = (
        workers_available *
        picker_productivity_rate
    )

    return float(harvest_rate)



def calculate_remaining_harvest_time(
    remaining_crates: int,
    harvest_rate: float
) -> float:
    """
    Calculate the estimated time required
    to harvest the remaining crates
    in a block.

    Formula
    -------
    Remaining Harvest Time =
    Remaining Crates ÷ Harvest Rate

    Parameters
    ----------
    remaining_crates : int
        Number of unharvested crates remaining
        on the block.

    harvest_rate : float
        Total harvesting rate in crates
        per hour.

    Returns
    -------
    float
        Estimated remaining harvest time
        in hours.

    Raises
    ------
    ValueError
        If remaining_crates is negative.

    ValueError
        If harvest_rate is less than
        or equal to zero.
    """

    if remaining_crates < 0:
        raise ValueError(
            "remaining_crates cannot be negative."
        )

    if harvest_rate <= 0:
        raise ValueError(
            "harvest_rate must be greater than zero."
        )

    remaining_time = (
        remaining_crates /
        harvest_rate
    )

    return float(remaining_time)




import math


def calculate_required_workers(
    remaining_crates: int,
    available_hours: float,
    picker_productivity_rate: float = 12.5
) -> int:
    """
    Calculate the minimum number of workers
    required to complete harvesting before
    a target deadline.

    Formula
    -------
    Required Workers =
    Ceiling(
        Remaining Crates ÷
        (Available Hours × Picker Productivity Rate)
    )

    Parameters
    ----------
    remaining_crates : int
        Number of unharvested crates remaining
        on the block.

    available_hours : float
        Time remaining to complete harvesting,
        in hours.

    picker_productivity_rate : float, optional
        Average crates harvested per worker
        per hour. Default is 12.5 crates per
        worker per hour.

    Returns
    -------
    int
        Minimum number of workers required,
        rounded up to the nearest whole worker.

    Raises
    ------
    ValueError
        If remaining_crates is negative.

    ValueError
        If available_hours is less than
        or equal to zero.

    ValueError
        If picker_productivity_rate is less
        than or equal to zero.
    """

    if remaining_crates < 0:
        raise ValueError(
            "remaining_crates cannot be negative."
        )

    if available_hours <= 0:
        raise ValueError(
            "available_hours must be greater than zero."
        )

    if picker_productivity_rate <= 0:
        raise ValueError(
            "picker_productivity_rate must be greater than zero."
        )

    worker_capacity = (
        available_hours *
        picker_productivity_rate
    )

    required_workers = math.ceil(
        remaining_crates /
        worker_capacity
    )

    return int(required_workers)



def evaluate_workforce_deficit(
    required_workers: int,
    available_workers: int
) -> dict:
    """
    Evaluate whether sufficient workers are
    available to complete harvesting within
    the required timeframe.

    Formula
    -------
    Workforce Deficit =
    Required Workers − Available Workers

    Parameters
    ----------
    required_workers : int
        Minimum number of workers required to
        complete harvesting before the target
        deadline.

    available_workers : int
        Number of workers currently available
        for assignment.

    Returns
    -------
    dict
        Dictionary containing:

        has_deficit : bool
            True if additional workers are needed.

        worker_gap : int
            Number of additional workers required.

        message : str
            Human-readable workforce status.

    Raises
    ------
    ValueError
        If required_workers is negative.

    ValueError
        If available_workers is negative.
    """

    if required_workers < 0:
        raise ValueError(
            "required_workers cannot be negative."
        )

    if available_workers < 0:
        raise ValueError(
            "available_workers cannot be negative."
        )

    workforce_deficit = (
        required_workers -
        available_workers
    )

    has_deficit = workforce_deficit > 0

    worker_gap = max(
        0,
        workforce_deficit
    )

    if has_deficit:
        message = (
            f"Workforce Deficit: Shortage of "
            f"{worker_gap} worker(s)."
        )
    else:
        message = (
            "Sufficient workforce available."
        )

    return {
        "has_deficit": has_deficit,
        "worker_gap": worker_gap,
        "message": message
    }



def recommend_worker_transfer(
    worker_gap: int,
    donor_surplus_workers: int
) -> dict:
    """

    Recommend a worker transfer from a donor
    block to a recipient block experiencing
    a labour shortage.

    Formula
    -------
    Transferred Workers =
    Minimum(
        Worker Gap,
        Donor Surplus Workers
    )

    Remaining Deficit =
    Worker Gap − Transferred Workers

    Remaining Surplus =
    Donor Surplus Workers − Transferred Workers

    Parameters
    ----------
    worker_gap : int
        Number of additional workers required.

    donor_surplus_workers : int
        Number of surplus workers available
        for reassignment.

    Returns
    -------
    dict
        Dictionary containing:

        transferred_workers : int
            Number of workers to transfer.

        remaining_deficit : int
            Labour shortage remaining after
            the transfer.

        remaining_surplus : int
            Surplus workers remaining in the
            donor block after the transfer.

        message : str
            Human-readable transfer recommendation.

    Raises
    ------
    ValueError
        If worker_gap is negative.

    ValueError
        If donor_surplus_workers is negative.
    """

    if worker_gap < 0:
        raise ValueError(
            "worker_gap cannot be negative."
        )

    if donor_surplus_workers < 0:
        raise ValueError(
            "donor_surplus_workers cannot be negative."
        )

    transferred_workers = min(
        worker_gap,
        donor_surplus_workers
    )

    remaining_deficit = (
        worker_gap -
        transferred_workers
    )

    remaining_surplus = (
        donor_surplus_workers -
        transferred_workers
    )

    if transferred_workers == 0:
        message = (
            "No worker transfer required."
        )

    elif remaining_deficit == 0:
        message = (
            f"Transfer {transferred_workers} "
            f"worker(s) to eliminate the "
            f"labour shortage."
        )

    else:
        message = (
            f"Transfer {transferred_workers} "
            f"worker(s). Remaining deficit: "
            f"{remaining_deficit} worker(s)."
        )

    return {
        "transferred_workers": transferred_workers,
        "remaining_deficit": remaining_deficit,
        "remaining_surplus": remaining_surplus,
        "message": message
    }



def predict_block_completion_risk(
    remaining_harvest_time: float,
    available_hours: float
) -> dict:
    """
    Predict the risk of failing to complete
    harvesting before the required deadline.

    Formula
    -------
    Time Buffer Hours =
    Available Hours − Remaining Harvest Time

    Classification
    --------------
    GREEN:
        Harvest completion is expected more
        than one hour before the deadline.

    AMBER:
        Harvest completion is expected within
        one hour of the deadline.

    RED:
        Harvest completion exceeds the
        available time window.

    Parameters
    ----------
    remaining_harvest_time : float
        Estimated hours required to complete
        harvesting.

    available_hours : float
        Remaining hours available before
        the deadline.

    Returns
    -------
    dict
        Dictionary containing:

        status : str
            GREEN, AMBER, or RED.

        is_at_risk : bool
            True if status is AMBER or RED.

        time_buffer_hours : float
            Difference between available time
            and required harvest time.

        message : str
            Human-readable risk assessment.

    Raises
    ------
    ValueError
        If remaining_harvest_time is negative.

    ValueError
        If available_hours is less than
        or equal to zero.
    """

    if remaining_harvest_time < 0:
        raise ValueError(
            "remaining_harvest_time cannot be negative."
        )

    if available_hours <= 0:
        raise ValueError(
            "available_hours must be greater than zero."
        )

    time_buffer_hours = (
        available_hours -
        remaining_harvest_time
    )

    if time_buffer_hours < 0:
        status = "RED"
        is_at_risk = True

        overrun_minutes = round(
            abs(time_buffer_hours) * 60
        )

        message = (
            f"CRITICAL: Harvest completion is "
            f"predicted to miss the deadline by "
            f"{overrun_minutes} minute(s)."
        )

    elif time_buffer_hours <= 1:
        status = "AMBER"
        is_at_risk = True

        message = (
            "WARNING: Harvest completion is "
            "predicted within one hour of "
            "the deadline."
        )

    else:
        status = "GREEN"
        is_at_risk = False

        message = (
            "ON TRACK: Harvest completion is "
            "expected comfortably before "
            "the deadline."
        )

    return {
        "status": status,
        "is_at_risk": is_at_risk,
        "time_buffer_hours": round(
            time_buffer_hours,
            2
        ),
        "message": message
    }

