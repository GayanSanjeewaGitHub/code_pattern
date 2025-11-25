"""
DETAILED TRACE: Understanding Why Water = 0 at First Position

Let's trace through: [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
"""

def trace_rainwater_step_by_step():
    elevation = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    
    print("=" * 100)
    print("DETAILED TRACE: Why Water = 0 at First Position is CORRECT")
    print("=" * 100)
    
    print("\nArray: [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]")
    print("Index:  0  1  2  3  4  5  6  7  8  9 10 11\n")
    
    # Simulate first few steps
    left = 0
    right = 11
    left_max = 0
    right_max = 0
    
    print("STEP 1: Processing Position 0 (LEFT EDGE)")
    print("-" * 100)
    left_elevation = elevation[left]
    right_elevation = elevation[right]
    left_max = max(left_max, left_elevation)  # max(0, 0) = 0
    right_max = max(right_max, right_elevation)  # max(0, 1) = 1
    
    print(f"   left = {left}, right = {right}")
    print(f"   elevation[{left}] = {left_elevation}, elevation[{right}] = {right_elevation}")
    print(f"   left_max = {left_max}, right_max = {right_max}")
    print(f"   Since left_max ({left_max}) < right_max ({right_max}), process LEFT side")
    water = left_max - left_elevation
    print(f"   water = left_max - elevation[{left}] = {left_max} - {left_elevation} = {water}")
    print(f"\n   ✅ Water = 0 is CORRECT! Why?")
    print(f"      - Position 0 is at the LEFT EDGE of the roof")
    print(f"      - There's NO wall to the left to hold water")
    print(f"      - Water would just spill off the edge!")
    print(f"      - Visual: [💧➡️]  0  1  0  2  ... (water flows away)")
    left += 1
    
    print("\n" + "=" * 100)
    print("STEP 2: Processing Position 1 (FIRST PEAK)")
    print("-" * 100)
    left_elevation = elevation[left]
    right_elevation = elevation[right]
    left_max = max(left_max, left_elevation)  # max(0, 1) = 1
    right_max = max(right_max, right_elevation)  # max(1, 1) = 1
    
    print(f"   left = {left}, right = {right}")
    print(f"   elevation[{left}] = {left_elevation}, elevation[{right}] = {right_elevation}")
    print(f"   left_max = {left_max}, right_max = {right_max}")
    print(f"   Since left_max ({left_max}) >= right_max ({right_max}), process RIGHT side")
    water = right_max - right_elevation
    print(f"   water = right_max - elevation[{right}] = {right_max} - {right_elevation} = {water}")
    print(f"\n   ✅ Water = 0 is CORRECT! Why?")
    print(f"      - Position 11 is at the RIGHT EDGE of the roof")
    print(f"      - There's NO wall to the right to hold water")
    print(f"      - Visual: ... 1  2  1 [💧➡️] (water flows away)")
    right -= 1
    
    print("\n" + "=" * 100)
    print("STEP 3: Processing Position 10")
    print("-" * 100)
    left_elevation = elevation[left]
    right_elevation = elevation[right]
    left_max = max(left_max, left_elevation)  # max(1, 1) = 1
    right_max = max(right_max, right_elevation)  # max(1, 2) = 2
    
    print(f"   left = {left}, right = {right}")
    print(f"   elevation[{left}] = {left_elevation}, elevation[{right}] = {right_elevation}")
    print(f"   left_max = {left_max}, right_max = {right_max}")
    print(f"   Since left_max ({left_max}) < right_max ({right_max}), process LEFT side")
    water = left_max - left_elevation
    print(f"   water = left_max - elevation[{left}] = {left_max} - {left_elevation} = {water}")
    print(f"\n   ✅ Water = 0 is CORRECT! Why?")
    print(f"      - Position 1 has elevation = 1")
    print(f"      - Maximum wall on left = 1 (same as current)")
    print(f"      - This is a PEAK, water cannot accumulate on top of a peak!")
    print(f"      - Visual: [0][1] ← Peak at same height as left_max")
    left += 1
    
    print("\n" + "=" * 100)
    print("STEP 4: Processing Position 2 (FIRST WATER TRAP!)")
    print("-" * 100)
    left_elevation = elevation[left]
    right_elevation = elevation[right]
    left_max = max(left_max, left_elevation)  # max(1, 0) = 1 (stays 1)
    right_max = max(right_max, right_elevation)  # max(2, 1) = 2
    
    print(f"   left = {left}, right = {right}")
    print(f"   elevation[{left}] = {left_elevation}, elevation[{right}] = {right_elevation}")
    print(f"   left_max = {left_max}, right_max = {right_max}")
    print(f"   Since left_max ({left_max}) < right_max ({right_max}), process LEFT side")
    water = left_max - left_elevation
    print(f"   water = left_max - elevation[{left}] = {left_max} - {left_elevation} = {water}")
    print(f"\n   🎉 Water = 1 TRAPPED! Why?")
    print(f"      - Position 2 has elevation = 0 (a valley)")
    print(f"      - Maximum wall on left = 1 (can hold water up to height 1)")
    print(f"      - There's a wall on the right too (right_max = 2)")
    print(f"      - Water fills the gap: height 1 - elevation 0 = 1 unit of water!")
    print(f"      - Visual: [0][1][≈] where ≈ = water trapped")
    
    print("\n" + "=" * 100)
    print("KEY INSIGHTS:")
    print("=" * 100)
    print("1. ✅ Water = 0 at edges is CORRECT (no walls to contain water)")
    print("2. ✅ Water = 0 at peaks is CORRECT (water can't sit on top of peaks)")
    print("3. ✅ Water > 0 in valleys is CORRECT (trapped between walls)")
    print("4. 🔑 Formula: water = min(left_max, right_max) - current_elevation")
    print("5. 🔑 If current elevation >= left_max or right_max, no water (at edge or peak)")
    print("=" * 100)


if __name__ == "__main__":
    trace_rainwater_step_by_step()
