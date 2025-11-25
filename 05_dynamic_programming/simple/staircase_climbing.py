"""
PATTERN: Dynamic Programming
DIFFICULTY: Simple
REAL-WORLD SCENARIO: Building Staircase - Count Ways to Climb

STORY:
You're a fitness app developer. Users can climb stairs by taking 1 or 2 steps at a time.
You need to calculate how many different ways a user can climb N stairs for gamification.
This is a classic DP problem similar to Fibonacci.

WHY DYNAMIC PROGRAMMING?
- Naive recursion recalculates same subproblems many times
- For stairs(5): calculates stairs(3) multiple times, stairs(2) even more
- DP stores results of subproblems to avoid recalculation
- Turns exponential O(2^n) into linear O(n)!

DP CHARACTERISTICS:
1. Optimal Substructure: Solution built from smaller subproblems
2. Overlapping Subproblems: Same problems solved repeatedly
3. Memoization (top-down) or Tabulation (bottom-up)

RECURRENCE RELATION:
ways(n) = ways(n-1) + ways(n-2)
Base cases: ways(0) = 1, ways(1) = 1

TIME COMPLEXITY: O(n)
SPACE COMPLEXITY: O(n) with array, O(1) with variables
"""

def count_ways_recursive_naive(n: int, depth: int = 0) -> int:
    """
    Naive recursive solution - for comparison (SLOW).
    Shows why we need DP.
    """
    indent = "  " * depth
    print(f"{indent}📞 ways({n})")
    
    if n == 0 or n == 1:
        print(f"{indent}   ✅ Base case: return 1")
        return 1
    
    # Notice: We calculate ways(n-1) and ways(n-2)
    # These recursive calls will also calculate their subproblems
    # Leading to MASSIVE redundant calculations
    left = count_ways_recursive_naive(n - 1, depth + 1)
    right = count_ways_recursive_naive(n - 2, depth + 1)
    
    result = left + right
    print(f"{indent}   ↩️  ways({n}) = ways({n-1}) + ways({n-2}) = {left} + {right} = {result}")
    return result


def count_ways_dp_memoization(n: int, memo: dict = None, depth: int = 0) -> int:
    """
    DP Solution using Memoization (Top-Down approach).
    Store calculated results to avoid recalculation.
    """
    if memo is None:
        memo = {}
    
    indent = "  " * depth
    
    # Check if we've already calculated this
    if n in memo:
        print(f"{indent}📝 ways({n}) = {memo[n]} (from cache)")
        return memo[n]
    
    print(f"{indent}📞 ways({n})")
    
    # Base cases
    if n == 0 or n == 1:
        print(f"{indent}   ✅ Base case: return 1")
        return 1
    
    # Calculate and store result
    result = (count_ways_dp_memoization(n - 1, memo, depth + 1) + 
              count_ways_dp_memoization(n - 2, memo, depth + 1))
    
    memo[n] = result
    print(f"{indent}   💾 Storing ways({n}) = {result}")
    return result


def count_ways_dp_tabulation(n: int) -> int:
    """
    DP Solution using Tabulation (Bottom-Up approach).
    Build solution from smallest subproblems upward.
    """
    if n == 0 or n == 1:
        return 1
    
    # Create table to store results
    dp = [0] * (n + 1)
    
    # Base cases
    dp[0] = 1  # 0 stairs: 1 way (don't climb)
    dp[1] = 1  # 1 stair: 1 way (single step)
    
    print(f"\n📊 BUILDING DP TABLE")
    print(f"{'Stairs':<8} {'Ways':<8} {'Calculation':<30} {'DP Table'}")
    print("-" * 80)
    
    print(f"{0:<8} {dp[0]:<8} {'Base case':<30} {dp[:2]}")
    print(f"{1:<8} {dp[1]:<8} {'Base case':<30} {dp[:2]}")
    
    # Fill table from bottom up
    for i in range(2, n + 1):
        # Current ways = ways to reach (i-1) + ways to reach (i-2)
        # Because from (i-1) we take 1 step, from (i-2) we take 2 steps
        dp[i] = dp[i-1] + dp[i-2]
        
        calculation = f"dp[{i-1}] + dp[{i-2}] = {dp[i-1]} + {dp[i-2]}"
        print(f"{i:<8} {dp[i]:<8} {calculation:<30} {dp[:min(i+1, 10)]}")
    
    return dp[n]


def count_ways_optimized(n: int) -> int:
    """
    Space-optimized DP solution.
    We only need last 2 values, not entire array!
    """
    if n == 0 or n == 1:
        return 1
    
    # Only keep track of last two values
    prev2 = 1  # ways(i-2)
    prev1 = 1  # ways(i-1)
    
    print(f"\n🎯 SPACE-OPTIMIZED DP")
    print(f"{'Stairs':<8} {'prev2':<8} {'prev1':<8} {'current':<10} {'Calculation'}")
    print("-" * 70)
    
    print(f"{0:<8} {'-':<8} {prev2:<8} {'-':<10}")
    print(f"{1:<8} {prev2:<8} {prev1:<8} {'-':<10}")
    
    for i in range(2, n + 1):
        current = prev1 + prev2
        print(f"{i:<8} {prev2:<8} {prev1:<8} {current:<10} {prev1} + {prev2}")
        
        # Shift values for next iteration
        prev2 = prev1
        prev1 = current
    
    return prev1


def analyze_fitness_gamification(stairs: int, ways: int):
    """
    Analyze fitness gamification data.
    """
    print(f"\n{'='*80}")
    print(f"🏃 FITNESS APP GAMIFICATION ANALYSIS")
    print(f"{'='*80}")
    
    print(f"\n📊 CHALLENGE: Climb {stairs} stairs")
    print(f"   Total unique climbing patterns: {ways:,}")
    
    # Calculate variety score
    if ways < 10:
        variety = "Low"
        engagement = "Basic"
    elif ways < 100:
        variety = "Medium"
        engagement = "Good"
    elif ways < 1000:
        variety = "High"
        engagement = "Excellent"
    else:
        variety = "Very High"
        engagement = "Outstanding"
    
    print(f"   Variety Score: {variety}")
    print(f"   User Engagement Level: {engagement}")
    
    # Gamification suggestions
    print(f"\n🎮 GAMIFICATION FEATURES:")
    print(f"   ✅ Achievement: Unlock 'Master Climber' badge")
    print(f"   ✅ Challenge: 'Try all {ways} different patterns'")
    print(f"   ✅ Leaderboard: Track unique patterns discovered")
    print(f"   ✅ Daily Quest: 'Discover 5 new climbing patterns'")
    
    # Calorie estimation (rough approximation)
    calories_per_stair = 0.15
    total_calories = stairs * calories_per_stair
    print(f"\n🔥 FITNESS METRICS:")
    print(f"   Calories burned per climb: ~{total_calories:.1f} kcal")
    print(f"   Total calorie potential (all patterns): ~{total_calories * ways:.0f} kcal")


# Example usage - Fitness app scenarios
if __name__ == "__main__":
    print("=" * 80)
    print("FITNESS APP: STAIRCASE CLIMBING CHALLENGE")
    print("=" * 80)
    
    # SCENARIO 1: Small example with naive recursion (to show problem)
    print("\n📍 SCENARIO 1: Naive Recursion - Why It's Slow")
    print("-" * 80)
    print("⚠️  Watch how many redundant calculations occur!\n")
    
    stairs = 5
    result_naive = count_ways_recursive_naive(stairs)
    print(f"\n✅ Result: {result_naive} ways to climb {stairs} stairs")
    print(f"⚠️  Notice: Same subproblems calculated many times!")
    
    # SCENARIO 2: Memoization (Top-Down DP)
    print("\n\n" + "=" * 80)
    print("\n📍 SCENARIO 2: Memoization - Optimized Recursion")
    print("-" * 80)
    print("✅ Each subproblem calculated only ONCE!\n")
    
    result_memo = count_ways_dp_memoization(stairs)
    print(f"\n✅ Result: {result_memo} ways (same answer, much faster!)")
    
    # SCENARIO 3: Tabulation (Bottom-Up DP)
    print("\n\n" + "=" * 80)
    print("\n📍 SCENARIO 3: Tabulation - Building From Bottom")
    print("-" * 80)
    
    stairs = 10
    result_tab = count_ways_dp_tabulation(stairs)
    print(f"\n✅ Result: {result_tab} ways to climb {stairs} stairs")
    
    # SCENARIO 4: Space-Optimized
    print("\n\n" + "=" * 80)
    print("\n📍 SCENARIO 4: Space-Optimized DP")
    print("-" * 80)
    
    result_opt = count_ways_optimized(stairs)
    print(f"\n✅ Result: {result_opt} ways (using O(1) space!)")
    
    # Analyze for gamification
    analyze_fitness_gamification(stairs, result_opt)
    
    # Performance comparison
    print("\n\n" + "=" * 80)
    print("⚡ COMPLEXITY COMPARISON")
    print("=" * 80)
    
    print("\nApproach          | Time Complexity | Space Complexity | Note")
    print("-" * 80)
    print("Naive Recursion   | O(2^n)         | O(n) stack      | ❌ Too slow!")
    print("Memoization       | O(n)           | O(n)            | ✅ Fast, top-down")
    print("Tabulation        | O(n)           | O(n)            | ✅ Fast, bottom-up")
    print("Space-Optimized   | O(n)           | O(1)            | ✅ Fastest, minimal space")
    
    print("\n" + "=" * 80)
