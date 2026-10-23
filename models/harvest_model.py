import datetime
import math

def calculate_progress_percentage(trees_harvested_per_day, total_trees_in_block):
    """Calculates how much of the block is finished."""
    if total_trees_in_block == 0:
        return 0
        
    progress = (trees_harvested_per_day / total_trees_in_block) * 100
    return progress

def calculate_harvest_rate(total_crates_harvested, hours_worked):
    """
    Calculates the harvest rate in crates per hour.
    """
    if hours_worked <= 0:
        raise ValueError("Hours worked must be greater than zero.")
    return total_crates_harvested / hours_worked

def calculate_worker_productivity(total_crates_harvested, workers_available, hours_worked):
    """
    Calculates the productivity of each worker in crates per hour.
    """
    if workers_available <= 0:
        raise ValueError("Workers available must be greater than zero.")
    if hours_worked <= 0:
        raise ValueError("Hours worked must be greater than zero.")
    return total_crates_harvested / (workers_available * hours_worked)

def calculate_crate_rejection_rate(total_crates_harvested, total_crates_rejected):
    """
    Calculates the rejection rate of harvested crates.
    """
    if total_crates_harvested <= 0:
        raise ValueError("Total crates harvested must be greater than zero.")
    if total_crates_rejected < 0 or total_crates_rejected > total_crates_harvested:
        raise ValueError("Total crates rejected cannot be negative or exceed the total crates harvested.")
    return { "rejection_rate": (total_crates_rejected / total_crates_harvested) * 100 }

