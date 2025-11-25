"""
PATTERN: Two Pointers
DIFFICULTY: Simple
REAL-WORLD SCENARIO: Warehouse Inventory Management

STORY:
You work at an Amazon warehouse. The inventory system stores product weights in sorted order.
A customer ordered two items with a specific combined weight. You need to find if any two 
products in the warehouse match this exact total weight for shipping optimization.

WHY TWO POINTERS?
- Instead of checking every possible pair (O(n²) time), we use two pointers
- One pointer starts at the beginning (lightest item)
- One pointer starts at the end (heaviest item)
- We move pointers based on whether sum is too small or too large
- This reduces time complexity to O(n)

TIME COMPLEXITY: O(n) - single pass through array
SPACE COMPLEXITY: O(1) - only using two pointer variables
"""

def find_products_for_weight(weights: list[int], target_weight: int) -> tuple[int, int] | None:
    """
    Find two products whose combined weight equals the target weight.
    
    Args:
        weights: Sorted list of product weights in kilograms
        target_weight: The target combined weight we need
        
    Returns:
        Tuple of (index1, index2) if found, None otherwise
    """
    # Initialize two pointers
    left = 0                    # Pointer at start (lightest product)
    right = len(weights) - 1    # Pointer at end (heaviest product)
    
    print(f"\n🎯 Target weight: {target_weight} kg")
    print(f"📦 Available products: {weights}")
    print(f"\n{'Step':<6} {'Left':<6} {'Right':<6} {'Weight[L]':<10} {'Weight[R]':<10} {'Sum':<6} {'Action':<20}")
    print("-" * 80)
    
    step = 1
    
    # Keep moving pointers until they meet
    while left < right:
        current_sum = weights[left] + weights[right]
        
        print(f"{step:<6} {left:<6} {right:<6} {weights[left]:<10} {weights[right]:<10} {current_sum:<6}", end=" ")
        
        if current_sum == target_weight:
            # Perfect match! We found two products
            print("✅ MATCH FOUND!")
            print(f"\n✨ Solution: Product at index {left} ({weights[left]} kg) + "
                  f"Product at index {right} ({weights[right]} kg) = {target_weight} kg")
            return (left, right)
        
        elif current_sum < target_weight:
            # Sum is too small, we need heavier products
            # Move left pointer right to get a heavier item
            print("⬆️ Sum too small, move LEFT pointer right")
            left += 1
        
        else:  # current_sum > target_weight
            # Sum is too large, we need lighter products
            # Move right pointer left to get a lighter item
            print("⬇️ Sum too large, move RIGHT pointer left")
            right -= 1
        
        step += 1
    
    # Pointers met without finding a match
    print(f"{step:<6} {left:<6} {right:<6} {'N/A':<10} {'N/A':<10} {'N/A':<6} ❌ No match exists")
    print("\n❌ No two products sum to the target weight")
    return None


# Example usage - Realistic warehouse scenario
if __name__ == "__main__":
    print("=" * 80)
    print("WAREHOUSE INVENTORY MATCHING SYSTEM")
    print("=" * 80)
    
    # Scenario 1: Successful match
    print("\n📍 SCENARIO 1: Finding products for 180 kg shipment")
    warehouse_weights = [45, 52, 67, 73, 89, 95, 107, 128]  # Sorted product weights
    target = 180
    result = find_products_for_weight(warehouse_weights, target)
    
    if result:
        print(f"\n📋 Shipping Instruction: Pack products at positions {result[0]} and {result[1]}")
    
    # Scenario 2: No match exists
    print("\n" + "=" * 80)
    print("\n📍 SCENARIO 2: Finding products for 300 kg shipment")
    target = 300
    result = find_products_for_weight(warehouse_weights, target)
    
    if not result:
        print("\n📋 Recommendation: Split shipment or use single heavier product")
    
    print("\n" + "=" * 80)
