"""
PATTERN: Two Pointers
DIFFICULTY: Medium
REAL-WORLD SCENARIO: Water Tank Construction Planning

STORY:
You're a civil engineer planning water storage tanks. You have vertical walls of different 
heights along a plot of land. You need to find the maximum water volume that can be stored 
between any two walls. The water level is limited by the shorter wall, and the width is 
the distance between walls.

WHY TWO POINTERS?
- We start with maximum width (leftmost and rightmost walls)
- The water capacity is limited by the shorter wall
- We move the pointer at the shorter wall inward, hoping to find a taller wall
- Moving the taller wall's pointer would only decrease width without potential gain
- This greedy approach ensures we don't miss the optimal solution

TIME COMPLEXITY: O(n) - single pass through array
SPACE COMPLEXITY: O(1) - only using pointer variables
"""

def max_water_storage(wall_heights: list[int]) -> tuple[int, int, int, int]:
    """
    Calculate maximum water storage capacity between two walls.
    
    Args:
        wall_heights: List of wall heights in meters
        
    Returns:
        Tuple of (max_capacity, left_wall_index, right_wall_index, wall_distance)
    """
    if len(wall_heights) < 2:
        return (0, 0, 0, 0)
    
    # Initialize pointers at extreme ends for maximum width
    left = 0
    right = len(wall_heights) - 1
    
    # Track the best configuration found
    max_capacity = 0
    best_left = 0
    best_right = 0
    
    print(f"\n🏗️  Wall Heights: {wall_heights}")
    print(f"\n{'Step':<6} {'L':<4} {'R':<4} {'H[L]':<6} {'H[R]':<6} {'Width':<7} {'Height':<7} {'Capacity':<10} {'Best':<10} {'Action':<25}")
    print("-" * 110)
    
    step = 1
    
    while left < right:
        # Calculate current configuration
        width = right - left
        # Water height limited by shorter wall
        height = min(wall_heights[left], wall_heights[right])
        # Capacity = width × height (area of rectangle)
        current_capacity = width * height
        
        # Track if this is our best solution so far
        is_best = current_capacity > max_capacity
        
        print(f"{step:<6} {left:<4} {right:<4} {wall_heights[left]:<6} {wall_heights[right]:<6} "
              f"{width:<7} {height:<7} {current_capacity:<10} "
              f"{'✨ NEW!' if is_best else max_capacity:<10}", end=" ")
        
        # Update best configuration if current is better
        if current_capacity > max_capacity:
            max_capacity = current_capacity
            best_left = left
            best_right = right
        
        # CRITICAL DECISION: Move the pointer at the shorter wall
        # 
        # ⚠️ IMPORTANT: The array is NOT sorted, so moving left++ doesn't guarantee
        # we'll find a taller wall! The next wall could be shorter, taller, or equal.
        #
        # WHY THIS STRATEGY IS STILL OPTIMAL:
        # 
        # 1. Current capacity is LIMITED by the SHORTER wall (bottleneck principle)
        #    Example: walls of 8m and 11m → water height = min(8,11) = 8m
        # 
        # 2. If we move the TALLER wall's pointer (right):
        #    - Width DECREASES: 8 → 7 (pointers get closer)
        #    - Height CANNOT IMPROVE: still limited by left wall (8m)
        #    - Capacity = 7 × 8 = 56 (was 64) ❌ WORSE GUARANTEED
        #    💡 Why? Even if new right wall is 100m tall, we're still limited by 8m!
        # 
        # 3. If we move the SHORTER wall's pointer (left):
        #    - Width DECREASES: 8 → 7 (pointers get closer)
        #    - Height MIGHT INCREASE: if next wall > 8m ✅ CHANCE TO IMPROVE
        #    - Height MIGHT DECREASE: if next wall < 8m ❌ WILL BE WORSE
        #    
        #    Three scenarios:
        #    a) Next wall = 15m → Capacity = 7 × min(15,11) = 77 ✅ BETTER!
        #    b) Next wall = 6m  → Capacity = 7 × min(6,11) = 42 ❌ WORSE
        #    c) Next wall = 8m  → Capacity = 7 × 8 = 56 ❌ WORSE
        # 
        # 4. THE KEY INSIGHT:
        #    - Moving taller wall = 0% chance to improve
        #    - Moving shorter wall = some chance to improve (even if small)
        #    - We systematically explore ALL configurations where improvement is possible
        #    - We never waste time on configurations that CANNOT improve
        # 
        # 5. PROOF IT'S OPTIMAL:
        #    If we skip checking a configuration by moving the taller wall, we're safe
        #    because that configuration is GUARANTEED to be worse than current one.
        #    The optimal solution MUST involve moving shorter walls until we find it.
        
        if wall_heights[left] < wall_heights[right]:
            # Left wall is shorter - it's the bottleneck, move it inward
            print(f"⬆️ Move L (left={wall_heights[left]}m is shorter than right={wall_heights[right]}m)")
            left += 1
        else:
            # Right wall is shorter or equal - move it inward
            print(f"⬇️ Move R (right={wall_heights[right]}m is shorter/equal to left={wall_heights[left]}m)")
            right -= 1
        
        step += 1
    
    distance = best_right - best_left
    
    print("\n" + "=" * 110)
    print(f"\n🎯 OPTIMAL SOLUTION FOUND:")
    print(f"   Left Wall (Index {best_left}): {wall_heights[best_left]} meters")
    print(f"   Right Wall (Index {best_right}): {wall_heights[best_right]} meters")
    print(f"   Distance: {distance} meters")
    print(f"   Water Height: {min(wall_heights[best_left], wall_heights[best_right])} meters")
    print(f"   💧 Maximum Capacity: {max_capacity} cubic meters")
    
    return (max_capacity, best_left, best_right, distance)


def visualize_tank(wall_heights: list[int], left_idx: int, right_idx: int):
    """
    Create a visual representation of the water tank.
    """
    print("\n📊 VISUAL REPRESENTATION:")
    print("-" * 80)
    
    max_height = max(wall_heights)
    water_level = min(wall_heights[left_idx], wall_heights[right_idx])
    
    # Draw from top to bottom
    for h in range(max_height, 0, -1):
        row = f"{h:2d}m |"
        for i, wall_h in enumerate(wall_heights):
            if i == left_idx or i == right_idx:
                # Mark selected walls
                if wall_h >= h:
                    row += " ║ "
                else:
                    row += "   "
            elif left_idx < i < right_idx:
                # Area between selected walls
                if wall_h >= h:
                    row += " ║ "
                elif h <= water_level:
                    row += " ≈ "  # Water
                else:
                    row += "   "
            else:
                # Other walls
                if wall_h >= h:
                    row += " | "
                else:
                    row += "   "
        print(row)
    
    # Ground level
    print("    " + "—" * (len(wall_heights) * 3 + 1))
    print("      " + "   ".join(str(i) for i in range(len(wall_heights))))
    print("\n    Legend: ║ = Selected walls, ≈ = Water, | = Other walls")


# Example usage - Real engineering scenario
if __name__ == "__main__":
    print("=" * 110)
    print("WATER TANK CONSTRUCTION OPTIMIZATION SYSTEM")
    print("=" * 110)
    
    # Scenario: Multiple wall configurations for a construction site
    print("\n📍 SCENARIO: Optimizing Water Storage Tank Design")
    print("A construction company has 9 pre-built walls of varying heights.")
    print("They need to select 2 walls to maximize rainwater collection capacity.")
    
    # Wall heights in meters at different positions
    walls = [8, 15, 6, 12, 9, 18, 7, 14, 11]
    
    capacity, left, right, distance = max_water_storage(walls)
    
    # Visualize the solution
    visualize_tank(walls, left, right)
    
    # Engineering report
    print("\n" + "=" * 110)
    print("📋 ENGINEERING REPORT:")
    print(f"   Construction Cost per meter: $500")
    print(f"   Wall pair distance: {distance} meters")
    print(f"   Total water storage: {capacity} cubic meters")
    print(f"   Estimated water value (@ $2/m³): ${capacity * 2}")
    print(f"   Estimated excavation cost: ${distance * 500}")
    print(f"   💰 Net benefit: ${(capacity * 2) - (distance * 500)}")
    print("=" * 110)
