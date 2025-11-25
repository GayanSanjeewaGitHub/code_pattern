"""
PATTERN: Binary Search
DIFFICULTY: Hard
REAL-WORLD SCENARIO: Warehouse Storage Optimization

Place items with maximum minimum distance between them (aggressive cows problem).
"""

def max_min_distance(positions: list[int], items: int) -> int:
    """Find maximum possible minimum distance between items."""
    positions.sort()
    
    def can_place(min_dist: int) -> bool:
        count = 1
        last_pos = positions[0]
        
        for pos in positions[1:]:
            if pos - last_pos >= min_dist:
                count += 1
                last_pos = pos
                if count >= items:
                    return True
        return False
    
    left, right = 1, positions[-1] - positions[0]
    result = 0
    
    while left <= right:
        mid = (left + right) // 2
        if can_place(mid):
            result = mid
            left = mid + 1
        else:
            right = mid - 1
    
    return result

if __name__ == "__main__":
    print("Warehouse Storage Optimization")
    positions = [1,2,4,8,9]
    print(f"Max minimum distance: {max_min_distance(positions, 3)}")
