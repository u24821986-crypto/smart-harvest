"""
Smart Harvest Model

Provides (for Rembander Agribusiness):
- Block Progress Tracking
- Field Harvest Rate Analysis
- Worker Productivity Evaluation
- Crate Rejection Rate Tracking

"""

import datetime
import math



def calculate_progress_percentage(
    trees_harvested_per_day: float,
    total_trees_in_block: float
) -> float:
    """
    Calculate the percentage of harvest
    progress completed within a block.

    Formula
    -------
    Progress Percentage =
    (Trees Harvested ÷ Total Trees in Block)
    × 100

    Parameters
    ----------
    trees_harvested_per_day : float
        Number of trees harvested in the
        block so far.

    total_trees_in_block : float
        Total number of harvestable trees
        assigned to the block.

    Returns
    -------
    float
        Harvest progress percentage.

    Notes
    -----
    Returns 0.0 when total_trees_in_block
    is zero to prevent division-by-zero
    errors.

    Raises
    ------
    ValueError
        If trees_harvested_per_day is negative.

    ValueError
        If total_trees_in_block is negative.
    """

    if trees_harvested_per_day < 0:
        raise ValueError(
            "trees_harvested_per_day cannot be negative."
        )

    if total_trees_in_block < 0:
        raise ValueError(
            "total_trees_in_block cannot be negative."
        )

    if total_trees_in_block == 0:
        return 0.0

    progress = (
        trees_harvested_per_day /
        total_trees_in_block
    ) * 100

    return float(progress)



def calculate_harvest_rate(
    total_crates_harvested: float,
    hours_worked: float
) -> float:
    """
    Calculate the overall field harvest rate
    in crates per hour.

    Formula
    -------
    Harvest Rate =
    Total Crates Harvested ÷ Hours Worked

    Parameters
    ----------
    total_crates_harvested : float
        Total number of crates harvested
        in the block.

    hours_worked : float
        Total active labour hours worked.

    Returns
    -------
    float
        Field harvest rate in crates
        per hour.

    Raises
    ------
    ValueError
        If total_crates_harvested is negative.

    ValueError
        If hours_worked is less than
        or equal to zero.
    """

    if total_crates_harvested < 0:
        raise ValueError(
            "total_crates_harvested cannot be negative."
        )

    if hours_worked <= 0:
        raise ValueError(
            "hours_worked must be greater than zero."
        )

    harvest_rate = (
        total_crates_harvested /
        hours_worked
    )

    return float(harvest_rate)



def calculate_worker_productivity(
    total_crates_harvested: float,
    workers_available: int,
    hours_worked: float
) -> float:
    """
    Calculate the average worker productivity
    in crates harvested per worker per hour.

    Formula
    -------
    Worker Productivity =
    Total Crates Harvested ÷
    (Workers Available × Hours Worked)

    Parameters
    ----------
    total_crates_harvested : float
        Total number of crates harvested.

    workers_available : int
        Number of active harvest workers
        assigned to operations.

    hours_worked : float
        Total active labour hours worked.

    Returns
    -------
    float
        Average worker productivity in
        crates per worker per hour.

    Raises
    ------
    ValueError
        If total_crates_harvested is negative.

    ValueError
        If workers_available is less than
        or equal to zero.

    ValueError
        If hours_worked is less than
        or equal to zero.
    """

    if total_crates_harvested < 0:
        raise ValueError(
            "total_crates_harvested cannot be negative."
        )

    if workers_available <= 0:
        raise ValueError(
            "workers_available must be greater than zero."
        )

    if hours_worked <= 0:
        raise ValueError(
            "hours_worked must be greater than zero."
        )

    productivity = (
        total_crates_harvested /
        (
            workers_available *
            hours_worked
        )
    )

    return float(productivity)



def calculate_crate_rejection_rate(
    total_crates_harvested: float,
    total_crates_rejected: float
) -> dict:
    """
    Calculate the percentage rejection rate
    of harvested crates.

    Formula
    -------
    Rejection Rate =
    (Total Crates Rejected ÷
    Total Crates Harvested)
    × 100

    Parameters
    ----------
    total_crates_harvested : float
        Total number of crates harvested.

    total_crates_rejected : float
        Total number of crates rejected
        during quality inspection.

    Returns
    -------
    dict
        Dictionary containing:

        rejection_rate : float
            Percentage of harvested crates
            that were rejected.

    Raises
    ------
    ValueError
        If total_crates_harvested is less
        than or equal to zero.

    ValueError
        If total_crates_rejected is negative.

    ValueError
        If total_crates_rejected exceeds
        total_crates_harvested.
    """

    if total_crates_harvested <= 0:
        raise ValueError(
            "total_crates_harvested must be greater than zero."
        )

    if (
        total_crates_rejected < 0 or
        total_crates_rejected >
        total_crates_harvested
    ):
        raise ValueError(
            "total_crates_rejected cannot be "
            "negative or exceed the total "
            "crates harvested."
        )

    rejection_rate = (
        total_crates_rejected /
        total_crates_harvested
    ) * 100

    return {
        "rejection_rate": float(
            rejection_rate
        )
    }
