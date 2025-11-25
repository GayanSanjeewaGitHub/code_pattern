"""
PATTERN: Dynamic Programming
DIFFICULTY: Hard
REAL-WORLD SCENARIO: Document Formatting Cost Minimization

Justify text by minimizing total cost of extra spaces.
"""

def min_cost_justification(words: list[str], width: int) -> int:
    """Calculate minimum cost to justify text."""
    n = len(words)
    INF = float('inf')
    
    # Calculate cost of putting words[i:j+1] on one line
    def line_cost(i: int, j: int) -> int:
        length = sum(len(words[k]) for k in range(i, j+1)) + (j - i)
        if length > width:
            return INF
        return (width - length) ** 2
    
    dp = [INF] * (n + 1)
    dp[0] = 0
    
    for i in range(1, n + 1):
        for j in range(i):
            cost = line_cost(j, i - 1)
            if cost != INF:
                dp[i] = min(dp[i], dp[j] + cost)
    
    return dp[n]

if __name__ == "__main__":
    print("Document Formatting Optimizer")
    words = ["This", "is", "an", "example", "of", "text"]
    print(f"Minimum cost: {min_cost_justification(words, 16)}")
