"""
PATTERN: Binary Search
DIFFICULTY: Medium
REAL-WORLD SCENARIO: Find Minimum Server Capacity for Peak Load

Binary search on answer space - find minimum capacity that satisfies conditions.
"""

def min_server_capacity(workloads: list[int], max_servers: int) -> int:
    """Find minimum capacity per server to handle all workloads."""
    def can_distribute(capacity: int) -> bool:
        servers_needed = 1
        current_load = 0
        
        for workload in workloads:
            if current_load + workload > capacity:
                servers_needed += 1
                current_load = workload
                if servers_needed > max_servers:
                    return False
            else:
                current_load += workload
        
        return True
    
    left, right = max(workloads), sum(workloads)
    result = right
    
    while left <= right:
        mid = (left + right) // 2
        if can_distribute(mid):
            result = mid
            right = mid - 1
        else:
            left = mid + 1
    
    return result

if __name__ == "__main__":
    print("Server Capacity Planning System")
    workloads = [7,2,5,10,8]
    print(f"Minimum capacity needed: {min_server_capacity(workloads, 2)}")
