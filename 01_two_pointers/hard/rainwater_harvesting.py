"""
PATTERN: Two Pointers
DIFFICULTY: Hard
REAL-WORLD SCENARIO: Rainwater Harvesting System Design

STORY:
You're designing a rainwater harvesting system for a building complex. The roof has 
elevation blocks of different heights. During rain, water gets trapped between the blocks.
Calculate total water volume that can be collected for the building's water conservation system.

WHY THIS IS HARD:
- Unlike simple container problem, water can be trapped at multiple locations
- Need to consider the maximum heights on BOTH left and right sides of each position
- Water level at any position = min(max_left, max_right) - current_height
- We use two pointers with auxiliary tracking of maximum heights

ALGORITHM INSIGHT:
- Process from both ends simultaneously
- Track the maximum height seen so far from left and right
- The side with smaller max height determines water level for that position
- Move pointer from the side with smaller max height

TIME COMPLEXITY: O(n) - single pass
SPACE COMPLEXITY: O(1) - only pointer and max height variables
"""

def trap_rainwater(elevation_blocks: list[int]) -> tuple[int, list[int]]:
    """
    Calculate trapped rainwater volume in a rooftop with varying elevations.
    
    Args:
        elevation_blocks: List of elevation heights in decimeters
        
    Returns:
        Tuple of (total_water_trapped, water_at_each_position)
    """
    if not elevation_blocks or len(elevation_blocks) < 3:
        return (0, [0] * len(elevation_blocks))
    
    n = len(elevation_blocks)
    
    # Two pointers starting from both ends
    left = 0
    right = n - 1
    
    # Track maximum heights seen from left and right
    left_max = 0
    right_max = 0
    
    # Store water trapped at each position for visualization
    water_at_position = [0] * n
    total_water = 0
    
    print(f"\n🏢 Rooftop Elevation Blocks: {elevation_blocks}")
    print(f"\n{'Step':<6} {'L':<4} {'R':<4} {'E[L]':<6} {'E[R]':<6} {'L_Max':<7} {'R_Max':<7} "
          f"{'Process':<8} {'Water':<7} {'Total':<7} {'Reason':<40}")
    print("-" * 120)
    
    step = 1
    
    # Process until pointers meet
    while left <= right:
        # Get current elevations
        left_elevation = elevation_blocks[left]
        right_elevation = elevation_blocks[right]
        
        # Update maximum heights seen so far
        left_max = max(left_max, left_elevation)
        right_max = max(right_max, right_elevation)
        
        print(f"{step:<6} {left:<4} {right:<4} {left_elevation:<6} {right_elevation:<6} "
              f"{left_max:<7} {right_max:<7}", end=" ")
        
        # CRITICAL DECISION: Process the side with smaller maximum height
        # Why? Because that side's water level is already determined
        # The water level cannot be higher than the smaller of the two max heights
        
        if left_max < right_max:
            # Process left side
            # Water trapped = max height on left - current elevation
            # NOTE: If left_max == left_elevation, water = 0 (no trapping, at edge or peak)
            # This is CORRECT! Water can only be trapped BETWEEN walls, not at edges.
            water = left_max - left_elevation
            water_at_position[left] = water
            total_water += water
            
            print(f"{'Left':<8} {water:<7} {total_water:<7} "
                  f"L_max < R_max: water = {left_max} - {left_elevation}")
            left += 1
        else:
            # Process right side
            # Water trapped = max height on right - current elevation
            water = right_max - right_elevation
            water_at_position[right] = water
            total_water += water
            
            print(f"{'Right':<8} {water:<7} {total_water:<7} "
                  f"R_max >= L_max: water = {right_max} - {right_elevation}")
            right -= 1
        
        step += 1
    
    return (total_water, water_at_position)


def visualize_rainwater_system(elevation_blocks: list[int], water_at_position: list[int]):
    """
    Create a visual representation of the rainwater harvesting system.
    """
    print("\n" + "=" * 120)
    print("📊 RAINWATER HARVESTING VISUALIZATION")
    print("=" * 120)
    
    max_height = max(max(elevation_blocks), max(elevation_blocks[i] + water_at_position[i] 
                     for i in range(len(elevation_blocks))))
    
    # Draw from top to bottom
    for h in range(max_height, 0, -1):
        row = f"{h:2d} dm |"
        for i in range(len(elevation_blocks)):
            block_height = elevation_blocks[i]
            water_height = water_at_position[i]
            total_height = block_height + water_height
            
            if h <= block_height:
                row += " ██ "  # Solid block
            elif h <= total_height:
                row += " ≈≈ "  # Water
            else:
                row += "    "  # Empty air
        row += "|"
        print(row)
    
    # Ground line
    print("     " + "—" * (len(elevation_blocks) * 4 + 1))
    
    # Position numbers
    position_line = "       "
    for i in range(len(elevation_blocks)):
        position_line += f"{i:2d}  "
    print(position_line)
    
    print("\n    Legend: ██ = Roof Block, ≈≈ = Trapped Water")
    
    # Detailed breakdown
    print("\n📋 POSITION-WISE BREAKDOWN:")
    print(f"{'Position':<10} {'Elevation':<12} {'Water':<12} {'Total Height':<15}")
    print("-" * 50)
    for i in range(len(elevation_blocks)):
        print(f"{i:<10} {elevation_blocks[i]:<12} {water_at_position[i]:<12} "
              f"{elevation_blocks[i] + water_at_position[i]:<15}")


def calculate_water_value(total_water: int, cost_per_unit: float):
    """
    Calculate the economic value of harvested rainwater.
    """
    print("\n" + "=" * 120)
    print("💰 ECONOMIC ANALYSIS")
    print("=" * 120)
    
    # Convert from cubic decimeters to liters (1 dm³ = 1 liter)
    liters = total_water
    gallons = liters * 0.264172
    
    print(f"   Total Water Harvested: {total_water} dm³ = {liters} liters = {gallons:.2f} gallons")
    print(f"   Municipal Water Cost: ${cost_per_unit} per liter")
    print(f"   💧 Annual Savings (assuming monthly collection): ${liters * cost_per_unit * 12:.2f}")
    print(f"   🌍 Environmental Impact: {liters * 12} liters saved from municipal supply/year")
    
    # CO2 savings (water treatment and distribution)
    co2_saved = (liters * 12 * 0.0003)  # kg CO2 per liter
    print(f"   🌱 CO2 Emissions Prevented: {co2_saved:.2f} kg/year")


# Example usage - Real building management scenario
if __name__ == "__main__":
    print("=" * 120)
    print("SMART BUILDING RAINWATER HARVESTING SYSTEM")
    print("=" * 120)
    
    # Scenario: Office building rooftop with irregular elevation
    print("\n📍 SCENARIO: Office Complex Rooftop Water Collection")
    print("Building Manager wants to calculate potential rainwater collection capacity")
    print("for sustainable water management and cost reduction.\n")
    
    # Rooftop elevation blocks (in decimeters) - realistic irregular pattern
    rooftop_elevations = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    
    print("Building Specifications:")
    print(f"   - Number of elevation sections: {len(rooftop_elevations)}")
    print(f"   - Each section width: 1 meter")
    print(f"   - Total rooftop length: {len(rooftop_elevations)} meters")
    
    # Calculate trapped water
    total_water, water_distribution = trap_rainwater(rooftop_elevations)
    
    # Visualize the system
    visualize_rainwater_system(rooftop_elevations, water_distribution)
    
    # Economic analysis
    cost_per_liter = 0.005  # $0.005 per liter (typical municipal water cost)
    calculate_water_value(total_water, cost_per_liter)
    
    # Summary
    print("\n" + "=" * 120)
    print("📊 EXECUTIVE SUMMARY:")
    print(f"   ✅ Feasibility: {'Highly Recommended' if total_water > 5 else 'Consider Alternative Design'}")
    print(f"   ✅ Total Collection Capacity: {total_water} liters per rainfall event")
    print(f"   ✅ ROI Period: ~2-3 years (including installation costs)")
    print(f"   ✅ Sustainability Rating: ⭐⭐⭐⭐{'⭐' if total_water > 5 else ''}")
    print("=" * 120)
