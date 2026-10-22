import math

from harvest_model import calculate_progress_percentage
from transport_model import calculate_vehicle_utilisation
def identify_constraint(progress, utilisation):
    """Identify the constraint based on progress and utilisation."""
    if progress < utilisation:
        return "Labour is the constraint." # Or "Progress is the constraint"
    elif utilisation < progress:
        return "Transport is the constraint." # Or "Utilisation is the constraint"
    else:
        return "Both are balanced."

    
def calculate_capacity_gap(total_truck_capacity, crates_loaded):
    """Calculate the capacity gap between total and actual capacities."""
    gap = total_truck_capacity - crates_loaded
    return max(0, gap)  # Ensure the gap is not negative    


def classify_bottleneck(gap):
    """Classify the severity of the gap."""
    if gap == 0:
        return "No bottleneck."
    elif gap <= (0.2 * total_truck_capacity):
        return "Minor bottleneck."
    else:
        return "Severe bottleneck."


import math

def identify_labour_bottleneck(block_name, trees_harvested, total_trees_in_block, workers_available, hours_worked_so_far, hours_left_in_day):
    """
    Calculates how many MORE workers are needed based on current progress.
    """
    
    # 1. Calculate progress using your function
    progress = calculate_progress_percentage(trees_harvested, total_trees_in_block)
    
    # 2. Figure out how fast they are ACTUALLY working right now
    if hours_worked_so_far > 0 and workers_available > 0:
        actual_productivity = (trees_harvested / workers_available) / hours_worked_so_far
    else:
        actual_productivity = 1.0 # Fallback if they just started
        
    # 3. How many trees are left to hit 100%?
    trees_remaining = total_trees_in_block - trees_harvested
    
    # 4. How many trees can the current team pick in the remaining hours?
    projected_capacity = workers_available * actual_productivity * hours_left_in_day
    
    # 5. Compare them and find the gap
    gap = trees_remaining - projected_capacity
    
    if gap > 0:
        # 6. Calculate exactly how many EXTRA workers are needed
        # (Divide the gap by how much one worker can do in the remaining time)
        extra_workers_needed = math.ceil(gap / (actual_productivity * hours_left_in_day))
        return f"{block_name}: Progress {round(progress, 1)}%. Shortage! Add {extra_workers_needed} more workers."
    else:
        return f"{block_name}: Progress {round(progress, 1)}%. Labour capacity is sufficient."


