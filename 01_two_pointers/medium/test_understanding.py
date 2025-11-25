"""
DEMONSTRATION: Why moving the shorter pointer works even in unsorted arrays

This script proves that the two-pointer algorithm is optimal even though:
1. The array is NOT sorted
2. Moving the shorter pointer doesn't guarantee finding a taller wall
"""

def demonstrate_why_it_works():
    """
    Show step-by-step why we move the shorter pointer
    """
    walls = [8, 15, 6, 12, 9, 18, 7, 14, 11]
    
    print("=" * 100)
    print("DEMONSTRATION: Why We Move the SHORTER Wall (Even in Unsorted Array)")
    print("=" * 100)
    
    print(f"\nArray: {walls}")
    print("Indices: 0   1   2   3   4   5   6   7   8")
    print("\n" + "=" * 100)
    
    # Step 1: Initial configuration
    print("\n📍 STEP 1: Initial Configuration")
    print("-" * 100)
    left, right = 0, 8
    print(f"Left pointer = {left} (height = {walls[left]}m)")
    print(f"Right pointer = {right} (height = {walls[right]}m)")
    
    width = right - left
    height = min(walls[left], walls[right])
    capacity = width * height
    
    print(f"\n📊 Current Capacity:")
    print(f"   Width = {right} - {left} = {width}m")
    print(f"   Height = min({walls[left]}, {walls[right]}) = {height}m (limited by SHORTER wall)")
    print(f"   Capacity = {width} × {height} = {capacity} cubic meters")
    
    # Now we have a choice
    print("\n" + "=" * 100)
    print("🤔 DECISION TIME: Which pointer should we move?")
    print("=" * 100)
    
    # Option A: Move the SHORTER wall (left)
    print("\n✅ OPTION A: Move the SHORTER wall pointer (left++)")
    print("-" * 100)
    print(f"Current left = {left} (height = {walls[left]}m) ← This is the BOTTLENECK")
    print(f"Next left = {left + 1} (height = {walls[left + 1]}m)")
    
    new_left = left + 1
    new_width = right - new_left
    new_height = min(walls[new_left], walls[right])
    new_capacity = new_width * new_height
    
    print(f"\n📊 If we move left pointer:")
    print(f"   Width = {right} - {new_left} = {new_width}m (decreased by 1)")
    print(f"   Height = min({walls[new_left]}, {walls[right]}) = {new_height}m")
    print(f"   Capacity = {new_width} × {new_height} = {new_capacity} cubic meters")
    
    improvement_a = new_capacity - capacity
    print(f"\n{'🎉' if improvement_a > 0 else '❌'} Result: {'+' if improvement_a > 0 else ''}{improvement_a} cubic meters")
    print(f"   Explanation: Next wall ({walls[new_left]}m) is TALLER than current bottleneck ({walls[left]}m)")
    print(f"                So even though width decreased, the HEIGHT increased from {height}m to {new_height}m!")
    
    # Option B: Move the TALLER wall (right)
    print("\n" + "-" * 100)
    print("❌ OPTION B: Move the TALLER wall pointer (right--)")
    print("-" * 100)
    print(f"Current right = {right} (height = {walls[right]}m)")
    print(f"Next right = {right - 1} (height = {walls[right - 1]}m)")
    
    new_right = right - 1
    new_width_b = new_right - left
    new_height_b = min(walls[left], walls[new_right])
    new_capacity_b = new_width_b * new_height_b
    
    print(f"\n📊 If we move right pointer:")
    print(f"   Width = {new_right} - {left} = {new_width_b}m (decreased by 1)")
    print(f"   Height = min({walls[left]}, {walls[new_right]}) = {new_height_b}m")
    print(f"   Capacity = {new_width_b} × {new_height_b} = {new_capacity_b} cubic meters")
    
    improvement_b = new_capacity_b - capacity
    print(f"\n{'🎉' if improvement_b > 0 else '❌'} Result: {'+' if improvement_b > 0 else ''}{improvement_b} cubic meters")
    print(f"   Explanation: We're still limited by the left wall ({walls[left]}m)")
    print(f"                New right wall ({walls[new_right]}m) doesn't help - bottleneck is still {walls[left]}m!")
    print(f"                Width decreased but height stayed at {height}m → WORSE capacity!")
    
    # Comparison
    print("\n" + "=" * 100)
    print("📊 COMPARISON:")
    print("=" * 100)
    print(f"Original capacity: {capacity} cubic meters")
    print(f"Option A (move shorter/left): {new_capacity} cubic meters ({'+' if improvement_a > 0 else ''}{improvement_a}) {'✅ BETTER' if improvement_a > 0 else '❌'}")
    print(f"Option B (move taller/right): {new_capacity_b} cubic meters ({'+' if improvement_b > 0 else ''}{improvement_b}) {'✅ BETTER' if improvement_b > 0 else '❌'}")
    
    print("\n" + "=" * 100)
    print("💡 CONCLUSION:")
    print("=" * 100)
    print("Even though the array is UNSORTED and moving left++ doesn't GUARANTEE")
    print("finding a taller wall, it's still the ONLY choice with potential to improve!")
    print("")
    print("Moving the taller wall pointer is ALWAYS worse because:")
    print("  • Width decreases")
    print("  • Height cannot improve (still limited by the shorter wall)")
    print("")
    print("Moving the shorter wall pointer gives us a CHANCE to improve:")
    print("  • Width decreases (unavoidable)")
    print("  • Height MIGHT increase (if we find a taller wall)")
    print("  • Net result MIGHT be positive (trading width for height)")
    print("=" * 100)


if __name__ == "__main__":
    demonstrate_why_it_works()
