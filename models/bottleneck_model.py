import math

from harvest_model import calculate_daily_labour_capacity
from transport_model import calculate_daily_transport_capacity
def identify_constraint(labour_capacity, transport_capacity):
    """Identify the constraint based on labour and transport capacities."""
    if labour_capacity < transport_capacity:
        return "Labour is the constraint."
    elif transport_capacity < labour_capacity:
        return "Transport is the constraint."
    else:
        return "Both labour and transport are balanced."

   
from transport_model import calculate_daily_transport_capacity 
def calculate_capacity_gap(required_capacity, actual_capacity):
    """Calculate the capacity gap between required and actual capacities."""
    gap = required_capacity - actual_capacity
    return max(0, gap)  # Ensure the gap is not negative    
def evaluate_transport_bottleneck(crates_harvested_today, number_of_trucks, capacity_per_truck, trips_per_day):
    """
    Evaluates if there is a transport bottleneck based on the number of crates harvested today
    and the transport capacity.
    """
    # Calculate the total transport capacity for the day
    total_transport_capacity = calculate_daily_transport_capacity(number_of_trucks, capacity_per_truck, trips_per_day)
    
    # Calculate the gap between harvested crates and transport capacity
    transport_gap = calculate_capacity_gap(crates_harvested_today, total_transport_capacity)
    
    return transport_gap

def classify_bottleneck(gap):
    """Classify the severity of the gap."""
    if gap == 0:
        return "No bottleneck."
    elif gap <= 200:
        return "Minor bottleneck."
    else:
        return "Severe bottleneck."

def rank_constraints(labour_gap, transport_gap):
    """Ranks which bottle neck is the most urgent to fix."""
    if labour_gap > transport_gap:
        return "Labour is the primary constraint."
    elif transport_gap > labour_gap:
        return "Transport is the primary constraint."
    else:
        return "Both constraints are equally significant."


from harvest_model import calculate_daily_labour_capacity

def identify_labour_bottleneck(block_name, tree_target, workers_available, actual_productivity, hours_in_day=8):
    """
    Calculates if there is a labour bottleneck.
    It pulls the capacity calculation from the harvest_model.
    """
    
    # 1. Ask the harvest model to do the math
    labour_capacity = calculate_daily_labour_capacity(workers_available, actual_productivity, hours_in_day)
    
    # 2. Compare capacity to the target
    gap = tree_target - labour_capacity
    
    if gap > 0:
        # Calculate how many extra workers are needed to close the gap
        extra_workers_needed = math.ceil(gap / (actual_productivity * hours_in_day))
        return f"{block_name}: Shortage! Need {extra_workers_needed} more workers to hit the target."
    else:
        return f"{block_name}: Labour capacity is sufficient."

def identify_transport_bottleneck(trips_needed, trips_available):
    """Identify if there is a transport bottleneck based on trips needed and available."""
    shortage = trips_needed - trips_available
    if shortage > 0:
        return f" Shortage of {math.ceil(shortage)} trips."
    else:
        return f" Transport capacity is sufficient."

def run_master_diagnostic(block_name, workers_needed, workers_available, crates_harvested_today, number_of_trucks, capacity_per_truck, trips_per_day):
    
    # 1. Evaluate Transport (From your code)
    transport_gap = evaluate_transport_bottleneck(crates_harvested_today, number_of_trucks, capacity_per_truck, trips_per_day)
    
    # Calculate trips needed for the transport bottleneck message
    trips_needed = math.ceil(crates_harvested_today / capacity_per_truck)
    transport_msg = identify_transport_bottleneck(trips_needed, trips_per_day)
    
    # 2. Evaluate Labour (From your code)
    labour_gap = max(0, workers_needed - workers_available)
    labour_msg = identify_labour_bottleneck(block_name, workers_needed, workers_available, actual_productivity=2, hours_in_day=8)
    
    # 3. Rank and Classify (From your code)
    rank_msg = rank_constraints(labour_gap, transport_gap)
    severity_msg = classify_bottleneck(max(labour_gap, transport_gap))
    
    # 4. Return the report
    return {
        "Block Status": labour_msg,
        "Transport Status": transport_msg,
        "Primary Constraint": rank_msg,
        "Severity": severity_msg
    }


