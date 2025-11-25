"""
PROOF: Why water = left_max - left_elevation (NOT min!)

This demonstrates why using min(left_max, left_elevation) is WRONG
"""

def wrong_formula_min(elevation):
    """WRONG APPROACH - Using min()"""
    left_max = 3
    right_max = 3
    
    print("=" * 80)
    print("❌ WRONG FORMULA: water = min(left_max, left_elevation)")
    print("=" * 80)
    
    total_wrong = 0
    for i, elev in enumerate(elevation):
        # This is WRONG!
        water_wrong = min(left_max, elev)
        total_wrong += water_wrong
        print(f"Position {i}: elevation={elev}, "
              f"water = min({left_max}, {elev}) = {water_wrong}")
    
    print(f"\n❌ Total water (WRONG): {total_wrong} units")
    print("   This makes NO SENSE! We're just copying elevations!")
    return total_wrong


def correct_formula_subtract(elevation):
    """CORRECT APPROACH - Using subtraction"""
    left_max = 3
    right_max = 3
    
    print("\n" + "=" * 80)
    print("✅ CORRECT FORMULA: water = left_max - left_elevation")
    print("=" * 80)
    
    total_correct = 0
    for i, elev in enumerate(elevation):
        # This is CORRECT!
        water_correct = left_max - elev
        total_correct += water_correct
        print(f"Position {i}: elevation={elev}, "
              f"water = {left_max} - {elev} = {water_correct}")
        
        # Visual
        visual = "  " + "█" * elev + "≈" * water_correct
        print(f"           Visual: {visual}")
    
    print(f"\n✅ Total water (CORRECT): {total_correct} units")
    print("   This makes SENSE! Water fills the GAPS!")
    return total_correct


def physical_explanation():
    """
    Physical explanation with ASCII art
    """
    print("\n" + "=" * 80)
    print("🌊 PHYSICAL EXPLANATION")
    print("=" * 80)
    
    print("\nImagine a container with walls:")
    print("""
    Left Wall (3m)                Right Wall (3m)
         █                             █
         █                             █
    3m   █ ← Water fills UP TO here → █
         █                             █
         █   ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈         █
    2m   █   ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈         █
         █                             █
         █   ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈         █
    1m   █   ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈         █
         █                             █
    0m   █___________________________█ (ground)
    
    Ground elevation = 0m
    Left wall height = 3m
    Right wall height = 3m
    
    Water level = min(3m, 3m) = 3m ← This is the CONTAINER HEIGHT
    
    Water trapped = Water level - Ground elevation
                  = 3m - 0m  
                  = 3m ✅
    
    If we used min(left_max, elevation):
        = min(3, 0)
        = 0 ❌ WRONG! Says no water!
    
    """)
    
    print("\n🔑 KEY INSIGHT:")
    print("   - left_max/right_max = HEIGHT of the CONTAINER (walls)")
    print("   - elevation = HEIGHT of the FLOOR")
    print("   - Water fills FROM the floor UP TO the container rim")
    print("   - Amount of water = (rim height) - (floor height)")
    print("   - Formula: water = left_max - elevation ✅")
    print("   - NOT: water = min(left_max, elevation) ❌")


def real_example():
    """
    Real example from rainwater harvesting
    """
    print("\n" + "=" * 80)
    print("📊 REAL EXAMPLE: [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]")
    print("=" * 80)
    
    elevation = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    
    print("\nAt position 2: elevation = 0")
    print("   Left wall (position 1): height = 1")
    print("   Right wall (position 3+): height = 2+")
    print("   left_max = 1, right_max = 2")
    
    print("\n   Using WRONG formula min():")
    print(f"      water = min(1, 0) = 0 ❌")
    print("      Says: NO water trapped!")
    
    print("\n   Using CORRECT formula subtraction:")
    print(f"      water = 1 - 0 = 1 ✅")
    print("      Says: 1 unit of water trapped!")
    
    print("\n   Visual at position 2:")
    print("      [1] [ ] [2]  ← walls")
    print("      [█] [≈] [█]  ← water fills the gap!")
    print("       1   2   3    positions")


if __name__ == "__main__":
    elevation = [0, 1, 0, 1, 0]
    
    print("\n" + "🌟" * 40)
    print("PROOF: Why water = left_max - elevation (NOT min!)")
    print("🌟" * 40)
    
    wrong_formula_min(elevation)
    correct_formula_subtract(elevation)
    physical_explanation()
    real_example()
    
    print("\n" + "=" * 80)
    print("✅ CONCLUSION: water = left_max - left_elevation is CORRECT!")
    print("❌ NEVER use: water = min(left_max, left_elevation)")
    print("=" * 80)
