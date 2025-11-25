"""
PATTERN: Sliding Window
DIFFICULTY: Hard
REAL-WORLD SCENARIO: Smart Home Energy Management - Minimum Time to Balance Load

STORY:
You're developing software for a smart home energy management system. The home has
solar panels that generate varying power throughout the day. You need to find the
SHORTEST time window where accumulated energy meets or exceeds the daily requirement.
This helps optimize battery storage and grid connection decisions.

WHY THIS IS HARD:
- Variable-size window with MINIMUM length goal (opposite of maximum)
- Need to track cumulative sum within window
- Shrink window as much as possible while maintaining the condition
- Must handle the case where sum might exceed target (need to minimize window)

ADVANCED CONCEPT: Minimum Window Template
- Expand window until condition met
- Once met, try to shrink from left while maintaining condition
- Track minimum window size throughout

TIME COMPLEXITY: O(n) - each element processed at most twice
SPACE COMPLEXITY: O(1) - only variables for tracking
"""

def min_time_to_meet_energy_requirement(
    solar_generation: list[int], 
    energy_requirement: int
) -> tuple[int, int, int, list[int]]:
    """
    Find minimum consecutive time period to generate required energy.
    
    Args:
        solar_generation: Hourly energy generation in kWh
        energy_requirement: Total energy needed in kWh
        
    Returns:
        Tuple of (min_hours, start_hour, end_hour, window_values)
    """
    n = len(solar_generation)
    
    # Initialize window pointers
    left = 0
    current_sum = 0
    
    # Track minimum window
    min_length = float('inf')  # Start with infinity
    best_start = -1
    best_end = -1
    
    print(f"\n⚡ Solar Generation (kWh/hour): {solar_generation}")
    print(f"🎯 Energy Requirement: {energy_requirement} kWh\n")
    
    print(f"{'Step':<6} {'L':<4} {'R':<4} {'Gen[R]':<8} {'Window Sum':<12} "
          f"{'Min Length':<12} {'Action':<40}")
    print("-" * 110)
    
    step = 1
    
    # Expand window with right pointer
    for right in range(n):
        # Add current hour's generation to window
        current_sum += solar_generation[right]
        
        print(f"{step:<6} {left:<4} {right:<4} {solar_generation[right]:<8} {current_sum:<12} "
              f"{min_length if min_length != float('inf') else 'inf':<12} ", end="")
        
        # Try to shrink window while condition is still met
        # This is the KEY difference from medium problem
        while current_sum >= energy_requirement and left <= right:
            # Calculate current window size
            window_length = right - left + 1
            
            # Update minimum if this is smaller
            if window_length < min_length:
                min_length = window_length
                best_start = left
                best_end = right
                print(f"✅ Requirement met, ⭐ NEW MIN: {window_length} hours", end="")
            else:
                print(f"✅ Requirement met, try shrink", end="")
            
            # Try to shrink: remove leftmost element
            print(f" → Remove hour {left} ({solar_generation[left]} kWh)")
            current_sum -= solar_generation[left]
            left += 1
            
            step += 1
            if current_sum >= energy_requirement:
                print(f"{step:<6} {left:<4} {right:<4} {'(shrunk)':<8} {current_sum:<12} "
                      f"{min_length:<12} ", end="")
        
        # If we're here, window is too small again
        if step > 1 and current_sum < energy_requirement:
            print(" → Window too small, continue expanding")
        else:
            print(" → Continue expanding")
        
        step += 1
    
    # Prepare result
    if min_length == float('inf'):
        return (0, -1, -1, [])
    
    window_values = solar_generation[best_start:best_end + 1]
    return (min_length, best_start, best_end, window_values)


def analyze_energy_optimization(generation: list[int], requirement: int,
                               min_hours: int, start: int, end: int, 
                               window_values: list[int]):
    """
    Comprehensive energy management analysis.
    """
    print("\n" + "=" * 110)
    print("🏠 SMART HOME ENERGY MANAGEMENT ANALYSIS")
    print("=" * 110)
    
    if min_hours == 0:
        total_generation = sum(generation)
        print(f"\n❌ INSUFFICIENT SOLAR CAPACITY")
        print(f"   Daily generation: {total_generation} kWh")
        print(f"   Requirement: {requirement} kWh")
        print(f"   Deficit: {requirement - total_generation} kWh")
        print(f"\n📋 RECOMMENDATION: Grid connection required or reduce consumption")
        return
    
    total_generated = sum(window_values)
    excess_energy = total_generated - requirement
    efficiency = (requirement / total_generated) * 100
    
    print(f"\n⚡ OPTIMAL ENERGY GENERATION WINDOW:")
    print(f"   Time Period: Hour {start}:00 to Hour {end}:00")
    print(f"   Duration: {min_hours} hours")
    print(f"   Hourly generation: {window_values} kWh")
    
    print(f"\n📊 ENERGY STATISTICS:")
    print(f"   Required energy: {requirement} kWh")
    print(f"   Generated in window: {total_generated} kWh")
    print(f"   Excess energy: {excess_energy} kWh ({(excess_energy/total_generated)*100:.1f}%)")
    print(f"   Efficiency: {efficiency:.1f}%")
    print(f"   Average generation: {total_generated/min_hours:.2f} kWh/hour")
    
    # Peak hour identification
    peak_hour_idx = window_values.index(max(window_values))
    peak_hour = start + peak_hour_idx
    print(f"\n☀️  PEAK GENERATION:")
    print(f"   Hour {peak_hour}:00 - {max(window_values)} kWh")
    
    # Battery storage recommendation
    print(f"\n🔋 BATTERY STORAGE STRATEGY:")
    print(f"   Minimum battery capacity needed: {requirement} kWh")
    print(f"   Recommended capacity (with buffer): {requirement * 1.2:.1f} kWh")
    
    if excess_energy > requirement * 0.2:
        print(f"   ✅ Significant excess - consider grid sell-back")
        print(f"   💰 Potential revenue: ${excess_energy * 0.12:.2f} (@ $0.12/kWh)")
    
    # Timeline visualization
    print(f"\n📈 GENERATION TIMELINE (24-hour period):")
    visualize_generation_timeline(generation, start, end, requirement)
    
    # Cost analysis
    analyze_cost_savings(requirement, min_hours, generation, start, end)


def visualize_generation_timeline(generation: list[int], start: int, end: int, requirement: int):
    """
    Visual representation of solar generation throughout the day.
    """
    max_gen = max(generation)
    scale = 20 / max_gen if max_gen > 0 else 1
    
    print("\n   kWh")
    for g in range(max(generation), -1, -2):
        print(f"   {g:2d} |", end="")
        for i, val in enumerate(generation):
            if val >= g:
                if start <= i <= end:
                    print("█", end="")  # Optimal window
                else:
                    print("▓", end="")  # Other generation
            else:
                print(" ", end="")
        print()
    
    print("      " + "—" * len(generation))
    print("      " + "".join(str(i % 10) for i in range(len(generation))) + " Hours")
    print(f"\n      Legend: █ = Optimal window, ▓ = Other generation")
    print(f"      Optimal window: Hours {start}-{end} (meets {requirement} kWh requirement)")


def analyze_cost_savings(requirement: int, hours: int, generation: list[int], start: int, end: int):
    """
    Calculate financial benefits of optimal solar utilization.
    """
    grid_cost_per_kwh = 0.15  # $0.15 per kWh from grid
    solar_cost_per_kwh = 0.03  # $0.03 per kWh effective cost (maintenance, amortized)
    
    print(f"\n💰 FINANCIAL ANALYSIS:")
    
    # Cost if using grid
    grid_cost = requirement * grid_cost_per_kwh
    print(f"   Grid electricity cost: ${grid_cost:.2f}")
    
    # Cost using solar
    solar_cost = requirement * solar_cost_per_kwh
    print(f"   Solar electricity cost: ${solar_cost:.2f}")
    
    # Savings
    daily_savings = grid_cost - solar_cost
    print(f"   Daily savings: ${daily_savings:.2f}")
    print(f"   Monthly savings: ${daily_savings * 30:.2f}")
    print(f"   Annual savings: ${daily_savings * 365:.2f}")
    
    # ROI calculation
    system_cost = 15000  # Typical residential solar system
    payback_years = system_cost / (daily_savings * 365)
    print(f"\n   Estimated system cost: ${system_cost}")
    print(f"   Payback period: {payback_years:.1f} years")


# Example usage - Real smart home scenario
if __name__ == "__main__":
    print("=" * 110)
    print("SMART HOME SOLAR ENERGY OPTIMIZATION SYSTEM")
    print("=" * 110)
    
    # Scenario: 24-hour solar generation profile
    print("\n📍 SCENARIO: Residential Solar Panel System")
    print("Homeowner wants to optimize energy storage and minimize battery requirements")
    print("by identifying the shortest high-generation window for daily needs.\n")
    
    # Realistic solar generation pattern (kWh per hour over 24 hours)
    # Night: 0, Morning: increasing, Midday: peak, Evening: decreasing, Night: 0
    solar_hourly_generation = [
        0, 0, 0, 0, 0, 0,           # Hours 0-5: Night
        0.5, 1.2, 2.8, 4.5, 6.2,    # Hours 6-10: Morning ramp-up
        7.8, 8.9, 9.2, 8.7, 7.5,    # Hours 11-15: Midday peak
        6.1, 4.3, 2.7, 1.1,         # Hours 16-19: Evening decline
        0.3, 0, 0, 0                # Hours 20-23: Night
    ]
    
    daily_requirement = 35  # kWh needed per day
    
    print(f"System Specifications:")
    print(f"   - Total daily generation: {sum(solar_hourly_generation)} kWh")
    print(f"   - Daily consumption: {daily_requirement} kWh")
    print(f"   - Peak generation: {max(solar_hourly_generation)} kWh/hour")
    
    # Find optimal window
    min_hours, start_hour, end_hour, window_gen = min_time_to_meet_energy_requirement(
        solar_hourly_generation, daily_requirement
    )
    
    # Comprehensive analysis
    analyze_energy_optimization(
        solar_hourly_generation, daily_requirement,
        min_hours, start_hour, end_hour, window_gen
    )
    
    print("\n" + "=" * 110)
    print("🎯 EXECUTIVE SUMMARY:")
    if min_hours > 0:
        print(f"   ✅ Daily energy requirement achievable in {min_hours}-hour window")
        print(f"   ✅ Optimal battery charging: Hours {start_hour}:00 to {end_hour}:00")
        print(f"   ✅ System efficiency: High - meeting needs in {(min_hours/24)*100:.1f}% of day")
    print("=" * 110)
