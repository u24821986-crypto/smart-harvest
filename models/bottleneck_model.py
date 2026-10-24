"""
Smart Bottleneck Model

Provides (for Rembander Agribusiness):
- Constraint Identification (Labour vs Transport)
- Vehicle Capacity Gap Analysis
- Bottleneck Severity Classification
- Labour Shortage and Workforce Allocation Analysis

"""

import math

from models.harvest_model import (
    calculate_progress_percentage
)

from models.transport_model import (
    calculate_vehicle_utilisation
)



def identify_constraint(
    progress: float,
    utilisation: float
) -> str:
    """
    Identify whether harvest progress or
    transport utilisation is the primary
    operational constraint.

    Logic
    -----
    If Progress < Utilisation:
        Labour is the constraint.

    If Utilisation < Progress:
        Transport is the constraint.

    Otherwise:
        Harvest and transport capacity
        are balanced.

    Parameters
    ----------
    progress : float
        Harvest completion percentage.

    utilisation : float
        Transport utilisation percentage.

    Returns
    -------
    str
        Constraint classification message.

    Raises
    ------
    ValueError
        If progress is negative.

    ValueError
        If utilisation is negative.
    """

    if progress < 0:
        raise ValueError(
            "progress cannot be negative."
        )

    if utilisation < 0:
        raise ValueError(
            "utilisation cannot be negative."
        )

    if progress < utilisation:
        return (
            "Labour is the constraint."
        )

    elif utilisation < progress:
        return (
            "Transport is the constraint."
        )

    else:
        return (
            "Both are balanced."
        )




def calculate_capacity_gap(
    vehicle_capacity: float,
    crates_loaded: float
) -> float:
    """
    Calculate the unused vehicle capacity
    gap in crates between available
    capacity and loaded crates.

    Formula
    -------
    Capacity Gap =
    Vehicle Capacity − Crates Loaded

    Parameters
    ----------
    vehicle_capacity : float
        Maximum crate capacity of the
        transport vehicle.

    crates_loaded : float
        Actual number of crates loaded
        onto the vehicle.

    Returns
    -------
    float
        Remaining transport capacity.

        Returns 0.0 when crates_loaded
        exceeds vehicle_capacity.

    Raises
    ------
    ValueError
        If vehicle_capacity is negative.

    ValueError
        If crates_loaded is negative.
    """

    if vehicle_capacity < 0:
        raise ValueError(
            "vehicle_capacity cannot be negative."
        )

    if crates_loaded < 0:
        raise ValueError(
            "crates_loaded cannot be negative."
        )

    gap = (
        vehicle_capacity -
        crates_loaded
    )

    return float(
        max(
            0,
            gap
        )
    )




def classify_bottleneck(
    gap: float,
    vehicle_capacity: float
) -> str:
    """
    Classify the severity of a transport
    capacity bottleneck relative to total
    vehicle capacity.

    Logic
    -----
    No Bottleneck:
        Gap = 0

    Minor Bottleneck:
        Gap ≤ 20% of Vehicle Capacity

    Severe Bottleneck:
        Gap > 20% of Vehicle Capacity

    Parameters
    ----------
    gap : float
        Unused vehicle capacity gap
        in crates.

    vehicle_capacity : float
        Maximum crate capacity of the
        transport vehicle.

    Returns
    -------
    str
        Bottleneck severity
        classification message.

    Raises
    ------
    ValueError
        If gap is negative.

    ValueError
        If vehicle_capacity is less than
        or equal to zero.
    """

    if gap < 0:
        raise ValueError(
            "gap cannot be negative."
        )

    if vehicle_capacity <= 0:
        raise ValueError(
            "vehicle_capacity must be greater than zero."
        )

    if gap == 0:
        return (
            "No bottleneck."
        )

    elif gap <= (
        0.2 *
        vehicle_capacity
    ):
        return (
            "Minor bottleneck."
        )

    else:
        return (
            "Severe bottleneck."
        )






def identify_labour_bottleneck(
    block_name: str,
    trees_harvested: float,
    total_trees_in_block: float,
    workers_available: int,
    hours_worked_so_far: float,
    hours_left_in_day: float
) -> str:
    """
    Calculate whether additional harvest
    workers are needed to complete block
    harvest operations within the
    remaining time available.

    Logic
    -----
    1. Calculate current harvest progress.
    2. Estimate current worker productivity.
    3. Determine the remaining trees
       to be harvested.
    4. Estimate remaining harvest capacity.
    5. Calculate any labour shortfall.
    6. Recommend additional workers
       where required.

    Parameters
    ----------
    block_name : str
        Name or identifier of the
        harvest block.

    trees_harvested : float
        Number of trees harvested so far.

    total_trees_in_block : float
        Total number of harvestable trees
        within the block.

    workers_available : int
        Number of workers currently
        assigned to the block.

    hours_worked_so_far : float
        Number of productive hours
        already worked.

    hours_left_in_day : float
        Number of productive hours
        remaining in the day.

    Returns
    -------
    str
        Labour bottleneck assessment and
        workforce recommendation message.

    Raises
    ------
    ValueError
        If trees_harvested is negative.

    ValueError
        If total_trees_in_block is less
        than or equal to zero.

    ValueError
        If workers_available is negative.

    ValueError
        If hours_worked_so_far is negative.

    ValueError
        If hours_left_in_day is negative.
    """

    if trees_harvested < 0:
        raise ValueError(
            "trees_harvested cannot be negative."
        )

    if total_trees_in_block <= 0:
        raise ValueError(
            "total_trees_in_block must be greater than zero."
        )

    if workers_available < 0:
        raise ValueError(
            "workers_available cannot be negative."
        )

    if hours_worked_so_far < 0:
        raise ValueError(
            "hours_worked_so_far cannot be negative."
        )

    if hours_left_in_day < 0:
        raise ValueError(
            "hours_left_in_day cannot be negative."
        )

    progress = calculate_progress_percentage(
        trees_harvested,
        total_trees_in_block
    )

    if (
        hours_worked_so_far > 0 and
        workers_available > 0
    ):
        actual_productivity = (
            trees_harvested /
            workers_available
        ) / hours_worked_so_far
    else:
        actual_productivity = 1.0

    trees_remaining = (
        total_trees_in_block -
        trees_harvested
    )

    projected_capacity = (
        workers_available *
        actual_productivity *
        hours_left_in_day
    )

    gap = (
        trees_remaining -
        projected_capacity
    )

    if (
        gap > 0 and
        hours_left_in_day > 0 and
        actual_productivity > 0
    ):
        extra_workers_needed = math.ceil(
            gap /
            (
                actual_productivity *
                hours_left_in_day
            )
        )

        return (
            f"{block_name}: Progress "
            f"{round(progress, 1)}%. "
            f"Shortage! Add "
            f"{extra_workers_needed} "
            f"more workers."
        )

    else:
        return (
            f"{block_name}: Progress "
            f"{round(progress, 1)}%. "
            f"Labour capacity is sufficient."
        )



