"""
UNDERSTANDING: What are "elevations" in rainwater harvesting?

This explains what the elevation values represent - they are WALLS, not tanks!
"""

def explain_elevations():
    print("=" * 100)
    print("WHAT DO ELEVATION VALUES REPRESENT?")
    print("=" * 100)
    
    print("\n📦 ELEVATIONS = SOLID WALLS/BLOCKS (not empty tanks!)")
    print("-" * 100)
    
    elevation = [0, 1, 0, 2, 1, 0, 1, 3, 2]
    
    print("\nExample: [0, 1, 0, 2, 1, 0, 1, 3, 2]")
    print("\nPosition 0: elevation = 0")
    print("   → This means: Ground level (no wall)")
    print("   → Physical: Nothing built here, just flat ground")
    
    print("\nPosition 1: elevation = 1")
    print("   → This means: A SOLID WALL 1 meter tall")
    print("   → Physical: █ (solid concrete/brick block)")
    
    print("\nPosition 2: elevation = 0")
    print("   → This means: Ground level again (valley/gap)")
    print("   → Physical: Empty space between position 1 and 3")
    print("   → This is WHERE WATER GETS TRAPPED!")
    
    print("\nPosition 3: elevation = 2")
    print("   → This means: A SOLID WALL 2 meters tall")
    print("   → Physical: ██ (two blocks stacked)")
    
    print("\n" + "=" * 100)
    print("VISUAL BREAKDOWN:")
    print("=" * 100)
    
    # Show the structure
    max_height = max(elevation)
    
    print("\nSOLID STRUCTURE (no water yet):")
    print("-" * 100)
    for h in range(max_height, 0, -1):
        row = f"{h}m | "
        for elev in elevation:
            if elev >= h:
                row += " █  "  # Solid block
            else:
                row += "    "  # Empty air
        print(row)
    
    ground = "0m | "
    for _ in elevation:
        ground += " ─  "
    print(ground)
    
    pos_line = "     "
    for i in range(len(elevation)):
        pos_line += f" {i}  "
    print(pos_line)
    
    print("\n█ = SOLID WALL/BLOCK (the elevation value)")
    print("  = EMPTY AIR SPACE (where water can potentially fill)")
    
    # Now show with water
    print("\n" + "=" * 100)
    print("SAME STRUCTURE WITH WATER TRAPPED:")
    print("=" * 100)
    
    # Calculate water at each position (simplified)
    water_at = []
    for i in range(len(elevation)):
        # Find max height on left
        left_max = max(elevation[:i+1]) if i >= 0 else 0
        # Find max height on right
        right_max = max(elevation[i:]) if i < len(elevation) else 0
        # Water level
        water_level = min(left_max, right_max)
        # Water trapped
        water = max(0, water_level - elevation[i])
        water_at.append(water)
    
    print("\n")
    for h in range(max_height, 0, -1):
        row = f"{h}m | "
        for i, elev in enumerate(elevation):
            total_height = elev + water_at[i]
            if elev >= h:
                row += " █  "  # Solid block
            elif total_height >= h:
                row += " ≈  "  # Water
            else:
                row += "    "  # Empty air
        print(row)
    
    ground = "0m | "
    for _ in elevation:
        ground += " ─  "
    print(ground)
    
    pos_line = "     "
    for i in range(len(elevation)):
        pos_line += f" {i}  "
    print(pos_line)
    
    print("\n█ = SOLID WALL/BLOCK (cannot pass through)")
    print("≈ = WATER (fills gaps between walls)")
    print("  = EMPTY AIR")
    
    # Detailed breakdown
    print("\n" + "=" * 100)
    print("POSITION-BY-POSITION BREAKDOWN:")
    print("=" * 100)
    
    print(f"\n{'Pos':<5} {'Elev':<6} {'Water':<7} {'Total':<7} {'Description':<50}")
    print("-" * 100)
    
    for i in range(len(elevation)):
        elev = elevation[i]
        water = water_at[i]
        total = elev + water
        
        if elev == 0 and water == 0:
            desc = "Ground level, no walls, no water (edge or no containment)"
        elif elev > 0 and water == 0:
            desc = f"Solid wall {elev}m tall, no water on top"
        elif elev == 0 and water > 0:
            desc = f"Valley! No wall, but {water}m water trapped here"
        else:
            desc = f"Wall {elev}m + {water}m water = {total}m total"
        
        print(f"{i:<5} {elev:<6} {water:<7} {total:<7} {desc:<50}")
    
    print("\n" + "=" * 100)
    print("KEY INSIGHTS:")
    print("=" * 100)
    print("1. Elevation value = Height of SOLID structure (walls/blocks)")
    print("2. Water fills EMPTY SPACES between walls")
    print("3. Water cannot penetrate solid walls")
    print("4. Water level = min(left_wall_height, right_wall_height)")
    print("5. Water trapped at position = water_level - elevation")
    print("=" * 100)


def real_world_analogy():
    """
    Real-world analogy to make it crystal clear
    """
    print("\n\n" + "🏗️" * 40)
    print("REAL-WORLD ANALOGY")
    print("🏗️" * 40)
    
    print("""
    Imagine a parking lot with concrete barriers:
    
    Position 0: No barrier (ground = 0m)
    Position 1: Short barrier 1m tall (█)
    Position 2: No barrier, but it's BETWEEN two barriers (valley)
    Position 3: Tall barrier 2m tall (██)
    
    When it rains:
    - Water CANNOT pass through the barriers (they're solid concrete)
    - Water FILLS THE GAPS between barriers
    - Position 2 gets flooded because it's trapped between barriers at positions 1 and 3
    
    Visual:
    2m |        ██           |
    1m |  █  ≈≈ ██           |  ← Water fills the gap at position 2
    0m |__█__≈≈_██___________|
         0  1   2   3
    
    Position 1: SOLID concrete barrier (elevation = 1)
    Position 2: EMPTY space but water trapped (elevation = 0, water = 1)
    Position 3: SOLID concrete barrier (elevation = 2)
    
    The elevation value tells you how much SOLID material is there,
    NOT how much water. Water is CALCULATED based on gaps between solids.
    """)


if __name__ == "__main__":
    explain_elevations()
    real_world_analogy()
    
    print("\n" + "✅" * 40)
    print("SUMMARY: Elevations = SOLID WALLS, Water = FILLS GAPS")
    print("✅" * 40)
