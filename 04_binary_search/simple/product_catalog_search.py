"""
PATTERN: Binary Search
DIFFICULTY: Simple
REAL-WORLD SCENARIO: E-Commerce Product Catalog Search

STORY:
You work at an e-commerce company. Products are stored sorted by price in a database.
A customer wants to find if a product with exact price exists. Binary search allows
you to find it in logarithmic time instead of checking every product.

WHY BINARY SEARCH?
- Linear search checks every element: O(n) time
- Binary search eliminates half the search space each step: O(log n) time
- For 1 million products: Linear = 1,000,000 checks, Binary = only 20 checks!

HOW IT WORKS:
1. Start with entire sorted array
2. Check middle element
3. If target is smaller, search left half
4. If target is larger, search right half
5. Repeat until found or search space exhausted

REQUIREMENTS:
- Array MUST be sorted
- Random access to elements (arrays, not linked lists)

TIME COMPLEXITY: O(log n)
SPACE COMPLEXITY: O(1) iterative, O(log n) recursive (call stack)
"""

def binary_search_product(prices: list[float], target_price: float) -> int:
    """
    Search for a product with exact price using binary search.
    
    Args:
        prices: Sorted list of product prices
        target_price: Price to search for
        
    Returns:
        Index of product if found, -1 if not found
    """
    left = 0                    # Start of search space
    right = len(prices) - 1     # End of search space
    
    print(f"\n🔍 BINARY SEARCH FOR PRICE: ${target_price}")
    print(f"📦 Product Catalog (sorted by price): {prices}")
    print(f"📊 Total products: {len(prices)}\n")
    
    print(f"{'Step':<6} {'Left':<6} {'Right':<6} {'Mid':<6} {'Price[Mid]':<12} {'Search Space':<15} {'Action':<30}")
    print("-" * 100)
    
    step = 1
    
    # Continue while there's still a search space
    while left <= right:
        # Calculate middle index
        # Using (left + right) // 2 can overflow for large numbers
        # Safer: left + (right - left) // 2
        mid = left + (right - left) // 2
        mid_price = prices[mid]
        
        # Visualize current search space
        search_space = f"[{left}...{right}]"
        space_size = right - left + 1
        
        print(f"{step:<6} {left:<6} {right:<6} {mid:<6} ${mid_price:<11.2f} {search_space:<15}", end=" ")
        
        # Check if we found the target
        if mid_price == target_price:
            print(f"✅ FOUND at index {mid}!")
            print(f"\n{'='*100}")
            print(f"🎯 SUCCESS: Product found at position {mid}")
            print(f"   Price: ${mid_price:.2f}")
            print(f"   Search efficiency: Checked {step} out of {len(prices)} products")
            print(f"   Time saved: {((len(prices) - step) / len(prices) * 100):.1f}%")
            return mid
        
        elif mid_price < target_price:
            # Target is in right half
            print(f"⬆️  ${mid_price:.2f} < ${target_price:.2f}, search RIGHT")
            left = mid + 1  # Eliminate left half including mid
        
        else:  # mid_price > target_price
            # Target is in left half
            print(f"⬇️  ${mid_price:.2f} > ${target_price:.2f}, search LEFT")
            right = mid - 1  # Eliminate right half including mid
        
        step += 1
    
    # Target not found
    print(f"\n{'='*100}")
    print(f"❌ NOT FOUND: No product with price ${target_price:.2f}")
    print(f"   Checked {step - 1} positions in {len(prices)} products")
    print(f"   Closest lower price: ${prices[right]:.2f} at index {right}" if right >= 0 else "   All prices higher")
    print(f"   Closest higher price: ${prices[left]:.2f} at index {left}" if left < len(prices) else "   All prices lower")
    
    return -1


def find_insert_position(prices: list[float], new_price: float) -> int:
    """
    Find the position where new product should be inserted to maintain sorted order.
    
    This is a VARIANT of binary search - instead of finding exact match,
    we find the insertion point.
    """
    left = 0
    right = len(prices)  # Note: len(prices), not len(prices) - 1
    
    print(f"\n📥 FINDING INSERT POSITION FOR: ${new_price:.2f}")
    print(f"{'Step':<6} {'Left':<6} {'Right':<6} {'Mid':<6} {'Price[Mid]':<12} {'Action':<30}")
    print("-" * 90)
    
    step = 1
    
    while left < right:  # Note: <, not <=
        mid = left + (right - left) // 2
        
        if mid < len(prices):
            mid_price = prices[mid]
            print(f"{step:<6} {left:<6} {right:<6} {mid:<6} ${mid_price:<11.2f}", end=" ")
            
            if mid_price < new_price:
                print(f"${mid_price:.2f} < ${new_price:.2f}, move left pointer")
                left = mid + 1
            else:
                print(f"${mid_price:.2f} >= ${new_price:.2f}, move right pointer")
                right = mid
        
        step += 1
    
    print(f"\n✅ Insert position: {left}")
    return left


# Example usage - E-commerce scenarios
if __name__ == "__main__":
    print("=" * 100)
    print("E-COMMERCE PRODUCT CATALOG SEARCH SYSTEM")
    print("=" * 100)
    
    # Product catalog sorted by price
    product_prices = [9.99, 14.99, 19.99, 24.99, 29.99, 34.99, 39.99, 
                     44.99, 49.99, 59.99, 69.99, 79.99, 89.99, 99.99]
    
    # SCENARIO 1: Customer searches for existing product
    print("\n📍 SCENARIO 1: Customer Search - Existing Product")
    print("-" * 100)
    customer_budget = 49.99
    result = binary_search_product(product_prices, customer_budget)
    
    if result != -1:
        print(f"\n📋 RECOMMENDATION: Show product at index {result} to customer")
    
    # SCENARIO 2: Customer searches for non-existing price
    print("\n\n" + "=" * 100)
    print("\n📍 SCENARIO 2: Customer Search - Price Not Available")
    print("-" * 100)
    customer_budget = 42.50
    result = binary_search_product(product_prices, customer_budget)
    
    if result == -1:
        print(f"\n📋 RECOMMENDATION: Show nearby products or suggest alternatives")
    
    # SCENARIO 3: Adding new product to catalog
    print("\n\n" + "=" * 100)
    print("\n📍 SCENARIO 3: Admin - Adding New Product to Catalog")
    print("-" * 100)
    new_product_price = 54.99
    insert_pos = find_insert_position(product_prices, new_product_price)
    
    print(f"\n📊 BEFORE: {product_prices}")
    product_prices.insert(insert_pos, new_product_price)
    print(f"📊 AFTER:  {product_prices}")
    print(f"\n✅ Catalog updated, sort order maintained")
    
    # Performance comparison
    print("\n\n" + "=" * 100)
    print("⚡ PERFORMANCE COMPARISON: Binary Search vs Linear Search")
    print("=" * 100)
    
    import math
    for n in [100, 1000, 10000, 100000, 1000000]:
        linear = n
        binary = math.ceil(math.log2(n))
        improvement = (linear - binary) / linear * 100
        
        print(f"   {n:,} products:")
        print(f"      Linear Search: {linear:,} checks")
        print(f"      Binary Search: {binary} checks")
        print(f"      Improvement: {improvement:.2f}% faster ⚡")
        print()
    
    print("=" * 100)
