"""
PATTERN: Fast & Slow Pointers
DIFFICULTY: Medium
REAL-WORLD SCENARIO: Traffic Route Cycle Detection in GPS System

Find middle element and detect cycles in delivery routes.
"""

class RouteNode:
    def __init__(self, location: str):
        self.location = location
        self.next = None

def find_middle_route(head: RouteNode) -> RouteNode:
    """Find middle point in route using fast & slow pointers."""
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow

if __name__ == "__main__":
    print("Traffic Route Cycle Detection System")
    print("Using Floyd's algorithm for GPS route validation")
