"""
DEMONSTRATION: Why Sorting Fails for Container With Most Water Problem

This file proves why we CANNOT sort the array before applying the two-pointer technique.
The key insight: POSITION MATTERS because it determines the WIDTH (distance).
"""

def brute_force_solution(heights: list[int]) -> tuple[int, int, int]:
    """
    Brute force: Check ALL possible pairs (this is the TRUE answer)
    Time Complexity: O(n²)
    """
    max_capacity = 0
    best_i = 0
    best_j = 0
    
    for i in range(len(heights)):
        for j in range(i + 1, len(heights)):
            width = j - i
            height = min(heights[i], heights[j])
            capacity = width * height
            if capacity > max_capacity:
                max_capacity = capacity
                best_i = i
                best_j = j
    
    return max_capacity, best_i, best_j


def two_pointer_solution(heights: list[int]) -> tuple[int, int, int]:
    """
    Two pointer solution on ORIGINAL unsorted array
    Time Complexity: O(n)
    """
    left = 0
    right = len(heights) - 1
    max_capacity = 0
    best_left = 0
    best_right = 0
    
    while left < right:
        width = right - left
        height = min(heights[left], heights[right])
        capacity = width * height
        
        if capacity > max_capacity:
            max_capacity = capacity
            best_left = left
            best_right = right
        
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    
    return max_capacity, best_left, best_right


def sorted_two_pointer_attempt(heights: list[int]) -> tuple[int, int, int]:
    """
    WRONG APPROACH: Sorting the array first
    This destroys the position information!
    """
    # Sort the array (THIS IS THE MISTAKE!)
    sorted_heights = sorted(heights)
    
    left = 0
    right = len(sorted_heights) - 1
    max_capacity = 0
    best_left = 0
    best_right = 0
    
    while left < right:
        width = right - left  # ❌ This width is based on SORTED positions, not original!
        height = min(sorted_heights[left], sorted_heights[right])
        capacity = width * height
        
        if capacity > max_capacity:
            max_capacity = capacity
            best_left = left
            best_right = right
    
        if sorted_heights[left] < sorted_heights[right]:
            left += 1
        else:
            right -= 1
    
    return max_capacity, best_left, best_right


def visualize_comparison(heights: list[int]):
    """
    Visual demonstration of why sorting fails
    """
    print("=" * 100)
    print("🧪 EXPERIMENT: Does Sorting Help?")
    print("=" * 100)
    
    print(f"\n📊 ORIGINAL ARRAY: {heights}")
    print(f"   Positions (indices): {list(range(len(heights)))}")
    
    # Show physical layout
    print("\n   Physical Layout (position matters!):")
    print("   " + "-" * 60)
    for i, h in enumerate(heights):
        print(f"   Position {i}: {'█' * h} ({h}m)")
    print("   " + "-" * 60)
    
    # Brute force (TRUE answer)
    print("\n" + "=" * 100)
    print("✅ METHOD 1: BRUTE FORCE (checking all pairs) - THIS IS THE TRUTH")
    print("=" * 100)
    bf_capacity, bf_i, bf_j = brute_force_solution(heights)
    print(f"\n   Best pair found: Index {bf_i} (height={heights[bf_i]}m) and Index {bf_j} (height={heights[bf_j]}m)")
    print(f"   Physical distance: {bf_j - bf_i} meters (this is the REAL distance on land)")
    print(f"   Water height: {min(heights[bf_i], heights[bf_j])} meters")
    print(f"   💧 Maximum capacity: {bf_capacity} cubic meters")
    
    # Two pointer (CORRECT)
    print("\n" + "=" * 100)
    print("✅ METHOD 2: TWO POINTERS on UNSORTED array - O(n) optimized")
    print("=" * 100)
    tp_capacity, tp_i, tp_j = two_pointer_solution(heights)
    print(f"\n   Best pair found: Index {tp_i} (height={heights[tp_i]}m) and Index {tp_j} (height={heights[tp_j]}m)")
    print(f"   Physical distance: {tp_j - tp_i} meters")
    print(f"   Water height: {min(heights[tp_i], heights[tp_j])} meters")
    print(f"   💧 Maximum capacity: {tp_capacity} cubic meters")
    print(f"\n   ✅ Matches brute force: {tp_capacity == bf_capacity}")
    
    # Sorted attempt (WRONG!)
    print("\n" + "=" * 100)
    print("❌ METHOD 3: TWO POINTERS on SORTED array - THIS IS WRONG!")
    print("=" * 100)
    sorted_heights = sorted(heights)
    print(f"\n   Sorted array: {sorted_heights}")
    print(f"   New positions: {list(range(len(sorted_heights)))}")
    print("\n   ⚠️  PROBLEM: After sorting, the positions are meaningless!")
    print("   The distance between indices no longer represents physical distance!")
    
    print("\n   After sorting layout:")
    print("   " + "-" * 60)
    for i, h in enumerate(sorted_heights):
        print(f"   Position {i}: {'█' * h} ({h}m)")
    print("   " + "-" * 60)
    
    st_capacity, st_i, st_j = sorted_two_pointer_attempt(heights)
    print(f"\n   Best pair in sorted array: Index {st_i} and Index {st_j}")
    print(f"   Heights: {sorted_heights[st_i]}m and {sorted_heights[st_j]}m")
    print(f"   ❌ Distance: {st_j - st_i} meters (THIS IS WRONG - not the real distance!)")
    print(f"   💧 Calculated capacity: {st_capacity} cubic meters")
    print(f"\n   ❌ Matches brute force: {st_capacity == bf_capacity}")
    print(f"   ❌ Error: {abs(st_capacity - bf_capacity)} cubic meters difference!")
    
    # Explanation
    print("\n" + "=" * 100)
    print("🎓 WHY SORTING FAILS:")
    print("=" * 100)
    print("""
   1. The POSITION (index) represents the PHYSICAL LOCATION of walls on land
   
   2. The DISTANCE between indices is the ACTUAL DISTANCE between walls:
      - Original: walls at index 1 and 5 → distance = 5-1 = 4 meters ✅
      - After sort: same walls now at index 7 and 8 → distance = 8-7 = 1 meter ❌
   
   3. Sorting DESTROYS the position information:
      - We lose track of where walls are physically located
      - The calculated width becomes meaningless
   
   4. This is NOT like "Two Sum" where only VALUES matter:
      - In Two Sum: We only care about finding two numbers that sum to target
      - In Container: We care about BOTH height AND distance (position)
   
   5. The two-pointer technique works on UNSORTED array because:
      - We need to preserve original positions to calculate real distances
      - We start with maximum width and smartly reduce it
      - We explore all promising configurations without checking all pairs
   
   📌 KEY INSIGHT: Position-dependent problems CANNOT be sorted!
   """)
    print("=" * 100)


# Real-world demonstration
if __name__ == "__main__":
    # Test case 1: Your example
    print("\n🏗️  TEST CASE 1: Construction Site Wall Configuration")
    walls1 = [8, 15, 6, 12, 9, 18, 7, 14, 11]
    visualize_comparison(walls1)
    
    print("\n\n")
    
    # Test case 2: Extreme example
    print("\n🏗️  TEST CASE 2: Extreme Example")
    print("Two very tall walls far apart vs many medium walls close together")
    walls2 = [1, 20, 3, 4, 5, 6, 7, 8, 9, 20]
    visualize_comparison(walls2)
    
    print("\n\n")
    print("=" * 100)
    print("🎯 CONCLUSION:")
    print("=" * 100)
    print("""
The two-pointer technique for 'Container With Most Water' MUST work on the UNSORTED array
because the problem is fundamentally about GEOMETRY - the physical distance between walls.

Sorting would destroy the spatial relationship between walls, making it impossible to
calculate the correct distance (width) between them.

This is different from problems like 'Two Sum' where only the VALUES matter, not their
positions. In those cases, sorting can help. But here, POSITION IS CRITICAL! 🎯
    """)
    print("=" * 100)
