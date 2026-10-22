import datetime
import math

def calculate_progress_percentage(trees_harvested_per_day, total_trees_in_block):
    """Calculates how much of the block is finished."""
    if total_trees_in_block == 0:
        return 0
        
    progress = (trees_harvested_per_day / total_trees_in_block) * 100
    return progress

def calculate_daily_labour_capacity(total_workers, productivity_per_worker_hour, hours_in_day, crates_per_tree=10):
    """
    Calculates the maximum number of crates the workforce can harvest in one day.
    (Based on the proposal: 1 tree = 10-20 crates. We use 10 as a baseline).
    """
    # 1. How many trees can all the workers pick in one hour?
    trees_per_hour = total_workers * productivity_per_worker_hour
    
    # 2. How many trees in a full day?
    trees_per_day = trees_per_hour * hours_in_day
    
    # 3. Convert trees to crates (The farm's unit of transport)
    total_crates = trees_per_day * crates_per_tree
    
    return total_crates

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

