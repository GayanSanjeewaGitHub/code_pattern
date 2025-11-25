"""
PATTERN: Dynamic Programming
DIFFICULTY: Medium
REAL-WORLD SCENARIO: Stock Trading with Cooldown Period

After selling stock, must wait one day before buying again.
State machine DP: track states (holding, sold, cooldown).
"""

def max_profit_with_cooldown(prices: list[int]) -> int:
    """Calculate maximum profit with cooldown constraint."""
    if not prices or len(prices) < 2:
        return 0
    
    n = len(prices)
    hold = [-prices[0]] + [0] * (n - 1)    # Holding stock
    sold = [0] * n                           # Just sold
    rest = [0] * n                           # Resting/cooldown
    
    for i in range(1, n):
        hold[i] = max(hold[i-1], rest[i-1] - prices[i])
        sold[i] = hold[i-1] + prices[i]
        rest[i] = max(rest[i-1], sold[i-1])
    
    return max(sold[-1], rest[-1])

if __name__ == "__main__":
    print("Stock Trading with Cooldown")
    prices = [1,2,3,0,2]
    print(f"Maximum profit: ${max_profit_with_cooldown(prices)}")
