"""
PATTERN: Fast & Slow Pointers
DIFFICULTY: Hard
REAL-WORLD SCENARIO: Finding Duplicate Entry in Database

Given array of n+1 integers where each is between 1 and n, find the duplicate.
Cannot modify array, O(1) space requirement.
"""

def find_duplicate(nums: list[int]) -> int:
    """Find duplicate number using cycle detection."""
    # Treat array as linked list where nums[i] points to nums[nums[i]]
    slow = fast = nums[0]
    
    # Phase 1: Find intersection point
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    
    # Phase 2: Find entrance to cycle (duplicate number)
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    
    return slow

if __name__ == "__main__":
    print("Database Duplicate Entry Finder")
    test = [1,3,4,2,2]
    print(f"Duplicate: {find_duplicate(test)}")
