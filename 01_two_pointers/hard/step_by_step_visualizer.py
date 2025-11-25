"""
STEP-BY-STEP VARIABLE TRACKER
This tool helps you visualize EVERY variable at EVERY step
Perfect for understanding the algorithm without forgetting anything!
"""

def rainwater_step_by_step_tracker(elevation_blocks: list[int]):
    """
    Shows EVERY variable at EVERY step with color coding and highlights
    """
    n = len(elevation_blocks)
    
    # Initialize all variables
    left = 0
    right = n - 1
    left_max = 0
    right_max = 0
    water_at_position = [0] * n
    total_water = 0
    step = 1
    
    print("=" * 140)
    print("🔍 STEP-BY-STEP VARIABLE TRACKER - RAINWATER TRAPPING")
    print("=" * 140)
    print(f"\nINPUT ARRAY: {elevation_blocks}")
    print(f"ARRAY SIZE: {n}")
    print("\n" + "=" * 140)
    
    # Show initial state
    print(f"\n{'='*140}")
    print(f"INITIAL STATE (Before Loop)")
    print(f"{'='*140}")
    print(f"  left          = {left}")
    print(f"  right         = {right}")
    print(f"  left_max      = {left_max}")
    print(f"  right_max     = {right_max}")
    print(f"  total_water   = {total_water}")
    print(f"  water_at_pos  = {water_at_position}")
    print(f"{'='*140}\n")
    
    input("Press ENTER to start the algorithm...")
    
    # Main loop with detailed tracking
    while left <= right:
        print("\n" + "🔄" * 70)
        print(f"STEP {step}")
        print("🔄" * 70)
        
        # Show current array state with pointers
        print("\n📊 ARRAY STATE:")
        print("   Index:  ", end="")
        for i in range(n):
            print(f"{i:3d} ", end="")
        print()
        
        print("   Height: ", end="")
        for i in range(n):
            print(f"{elevation_blocks[i]:3d} ", end="")
        print()
        
        print("   Pointer:", end="")
        for i in range(n):
            if i == left and i == right:
                print(" L,R", end="")
            elif i == left:
                print("  L ", end="")
            elif i == right:
                print("  R ", end="")
            else:
                print("    ", end="")
        print()
        
        print("   Water:  ", end="")
        for i in range(n):
            if water_at_position[i] > 0:
                print(f"{water_at_position[i]:3d} ", end="")
            else:
                print("  - ", end="")
        print("\n")
        
        # Variables BEFORE processing
        print("📝 VARIABLES BEFORE THIS STEP:")
        print(f"   left          = {left}")
        print(f"   right         = {right}")
        print(f"   left_max      = {left_max}")
        print(f"   right_max     = {right_max}")
        print(f"   total_water   = {total_water}")
        
        # Get current elevations
        left_elevation = elevation_blocks[left]
        right_elevation = elevation_blocks[right]
        
        print(f"\n🔍 READING VALUES:")
        print(f"   elevation_blocks[{left}] = {left_elevation}  ← left_elevation")
        print(f"   elevation_blocks[{right}] = {right_elevation}  ← right_elevation")
        
        # Update maximums
        old_left_max = left_max
        old_right_max = right_max
        left_max = max(left_max, left_elevation)
        right_max = max(right_max, right_elevation)
        
        print(f"\n🔄 UPDATE MAXIMUMS:")
        print(f"   left_max  = max({old_left_max}, {left_elevation}) = {left_max}  {'✓ CHANGED' if left_max != old_left_max else '(no change)'}")
        print(f"   right_max = max({old_right_max}, {right_elevation}) = {right_max}  {'✓ CHANGED' if right_max != old_right_max else '(no change)'}")
        
        # Decision logic
        print(f"\n🤔 DECISION: Which side to process?")
        print(f"   Compare: left_max ({left_max}) vs right_max ({right_max})")
        
        if left_max < right_max:
            print(f"   Result: left_max < right_max → Process LEFT side")
            print(f"\n💧 CALCULATE WATER AT POSITION {left}:")
            print(f"   water = left_max - left_elevation")
            print(f"   water = {left_max} - {left_elevation} = {left_max - left_elevation}")
            
            water = left_max - left_elevation
            water_at_position[left] = water
            old_total = total_water
            total_water += water
            
            print(f"\n✏️ UPDATE VARIABLES:")
            print(f"   water_at_position[{left}] = {water}")
            print(f"   total_water = {old_total} + {water} = {total_water}")
            print(f"   left = {left} + 1 = {left + 1}  ← MOVE LEFT POINTER")
            
            left += 1
            
        else:
            print(f"   Result: left_max >= right_max → Process RIGHT side")
            print(f"\n💧 CALCULATE WATER AT POSITION {right}:")
            print(f"   water = right_max - right_elevation")
            print(f"   water = {right_max} - {right_elevation} = {right_max - right_elevation}")
            
            water = right_max - right_elevation
            water_at_position[right] = water
            old_total = total_water
            total_water += water
            
            print(f"\n✏️ UPDATE VARIABLES:")
            print(f"   water_at_position[{right}] = {water}")
            print(f"   total_water = {old_total} + {water} = {total_water}")
            print(f"   right = {right} - 1 = {right - 1}  ← MOVE RIGHT POINTER")
            
            right -= 1
        
        # Variables AFTER processing
        print(f"\n📝 VARIABLES AFTER THIS STEP:")
        print(f"   left          = {left}")
        print(f"   right         = {right}")
        print(f"   left_max      = {left_max}")
        print(f"   right_max     = {right_max}")
        print(f"   total_water   = {total_water}")
        print(f"   water_at_pos  = {water_at_position}")
        
        # Loop condition check
        print(f"\n🔄 LOOP CONDITION CHECK:")
        print(f"   left <= right → {left} <= {right} → {left <= right}")
        if left <= right:
            print(f"   ✅ Continue to next iteration")
        else:
            print(f"   ❌ Exit loop")
        
        step += 1
        
        if left <= right:
            input("\nPress ENTER for next step...")
    
    # Final summary
    print("\n" + "=" * 140)
    print("🎉 ALGORITHM COMPLETE!")
    print("=" * 140)
    print(f"\n📊 FINAL STATE:")
    print(f"   Total water trapped: {total_water} units")
    print(f"   Water at each position: {water_at_position}")
    print("\n   Visual breakdown:")
    for i in range(n):
        print(f"      Position {i}: elevation={elevation_blocks[i]}, water={water_at_position[i]}, total={elevation_blocks[i] + water_at_position[i]}")
    print("\n" + "=" * 140)
    
    return total_water, water_at_position


def quick_mode(elevation_blocks: list[int]):
    """
    Same visualization but without pausing (for quick review)
    """
    import time
    
    n = len(elevation_blocks)
    left = 0
    right = n - 1
    left_max = 0
    right_max = 0
    water_at_position = [0] * n
    total_water = 0
    step = 1
    
    print("\n" + "=" * 100)
    print("🚀 QUICK MODE - All steps shown automatically")
    print("=" * 100)
    
    while left <= right:
        left_elevation = elevation_blocks[left]
        right_elevation = elevation_blocks[right]
        left_max = max(left_max, left_elevation)
        right_max = max(right_max, right_elevation)
        
        print(f"\nStep {step}: L={left} R={right} | E[L]={left_elevation} E[R]={right_elevation} | Lmax={left_max} Rmax={right_max}", end=" | ")
        
        if left_max < right_max:
            water = left_max - left_elevation
            water_at_position[left] = water
            total_water += water
            print(f"Process LEFT: water={water}, total={total_water}, move L to {left+1}")
            left += 1
        else:
            water = right_max - right_elevation
            water_at_position[right] = water
            total_water += water
            print(f"Process RIGHT: water={water}, total={total_water}, move R to {right-1}")
            right -= 1
        
        step += 1
        time.sleep(0.3)  # Small delay for readability
    
    print(f"\n✅ Total water: {total_water}")
    return total_water, water_at_position


# Example usage
if __name__ == "__main__":
    test_array = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    
    print("\n" + "🎯" * 50)
    print("Choose mode:")
    print("1. Step-by-step (press ENTER for each step)")
    print("2. Quick mode (automatic)")
    choice = input("Enter 1 or 2: ")
    
    if choice == "1":
        rainwater_step_by_step_tracker(test_array)
    else:
        quick_mode(test_array)
