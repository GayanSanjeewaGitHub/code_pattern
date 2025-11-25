"""
PATTERN: Sliding Window
DIFFICULTY: Simple
REAL-WORLD SCENARIO: Stock Market Analysis - Maximum Profit in K Days

STORY:
You're a financial analyst at an investment firm. You need to analyze stock price data
to find the best consecutive K-day period that would give maximum profit if someone
bought at the start and sold at the end of that period.

WHY SLIDING WINDOW?
- Instead of recalculating sum for every K-day window (O(n*k) time)
- We maintain a "window" of K days and slide it across the data
- Remove the leftmost element and add new rightmost element
- This gives us O(n) time complexity - single pass through data

TIME COMPLEXITY: O(n) - one pass through the array
SPACE COMPLEXITY: O(1) - only storing window sum and result

WHEN TO USE SLIDING WINDOW:
- Fixed-size or variable-size window
- Need to find something in contiguous subarrays
- Common in: max/min sum, average, substring problems
"""

def find_best_trading_period(stock_prices: list[float], days: int) -> tuple[float, int, list[float]]:
    """
    Find the K-day period with maximum total profit.
    
    Args:
        stock_prices: Daily stock prices
        days: Number of consecutive days to analyze
        
    Returns:
        Tuple of (max_sum, start_index, best_window_prices)
    """
    if len(stock_prices) < days or days <= 0:
        return (0.0, -1, [])
    
    n = len(stock_prices)
    
    # STEP 1: Calculate sum of first window
    print(f"\n📊 Stock Prices: {stock_prices}")
    print(f"🎯 Analysis Period: {days} consecutive days\n")
    
    print("STEP 1: Calculate initial window sum")
    print("-" * 80)
    
    window_sum = 0
    for i in range(days):
        window_sum += stock_prices[i]
        print(f"   Day {i}: ${stock_prices[i]:.2f} → Running sum: ${window_sum:.2f}")
    
    max_sum = window_sum
    max_start_idx = 0
    
    print(f"\n   Initial window [0 to {days-1}]: ${window_sum:.2f} ✅")
    
    # STEP 2: Slide the window across remaining elements
    print(f"\nSTEP 2: Slide window and compare")
    print("-" * 80)
    print(f"{'Window':<12} {'Remove':<10} {'Add':<10} {'New Sum':<12} {'Best So Far':<15} {'Action'}")
    print("-" * 80)
    
    # Slide window from index 'days' to end
    for i in range(days, n):
        # Calculate new window boundaries
        window_start = i - days + 1
        window_end = i
        
        # Remove leftmost element of previous window
        removed = stock_prices[i - days]
        # Add new rightmost element
        added = stock_prices[i]
        
        # Update window sum: subtract left, add right
        window_sum = window_sum - removed + added
        
        # Check if this is the best window so far
        is_better = window_sum > max_sum
        
        print(f"[{window_start:2d} to {window_end:2d}]  "
              f"${removed:<8.2f}  ${added:<8.2f}  ${window_sum:<10.2f}  "
              f"${max_sum:<13.2f}  ", end="")
        
        if is_better:
            max_sum = window_sum
            max_start_idx = window_start
            print("⭐ NEW BEST!")
        else:
            print("   No change")
    
    # Get the best window prices
    best_window = stock_prices[max_start_idx:max_start_idx + days]
    
    return (max_sum, max_start_idx, best_window)


def analyze_investment_opportunity(prices: list[float], period: int):
    """
    Comprehensive analysis of investment opportunity.
    """
    max_profit, start_idx, best_period_prices = find_best_trading_period(prices, period)
    
    if start_idx == -1:
        print("\n❌ Invalid input parameters")
        return
    
    end_idx = start_idx + period - 1
    average = max_profit / period
    
    print("\n" + "=" * 80)
    print("📈 INVESTMENT ANALYSIS REPORT")
    print("=" * 80)
    
    print(f"\n🎯 BEST TRADING PERIOD IDENTIFIED:")
    print(f"   Period: Day {start_idx} to Day {end_idx} ({period} days)")
    print(f"   Prices during this period: {[f'${p:.2f}' for p in best_period_prices]}")
    print(f"   Total value: ${max_profit:.2f}")
    print(f"   Average daily price: ${average:.2f}")
    
    # Calculate potential gains
    buy_price = best_period_prices[0]
    sell_price = best_period_prices[-1]
    gain = sell_price - buy_price
    gain_percentage = (gain / buy_price * 100) if buy_price > 0 else 0
    
    print(f"\n💰 TRADING STRATEGY:")
    print(f"   Buy on Day {start_idx}: ${buy_price:.2f}")
    print(f"   Sell on Day {end_idx}: ${sell_price:.2f}")
    print(f"   {'Profit' if gain > 0 else 'Loss'}: ${abs(gain):.2f} "
          f"({gain_percentage:+.2f}%)")
    
    # Investment recommendation
    print(f"\n📋 RECOMMENDATION:")
    if gain_percentage > 10:
        print("   ✅ STRONG BUY - Excellent profit potential")
    elif gain_percentage > 5:
        print("   ✅ BUY - Good profit opportunity")
    elif gain_percentage > 0:
        print("   ⚠️  HOLD - Moderate gains expected")
    else:
        print("   ❌ AVOID - Projected loss in this period")


# Example usage - Real financial analysis
if __name__ == "__main__":
    print("=" * 80)
    print("STOCK MARKET TRADING PERIOD ANALYZER")
    print("=" * 80)
    
    # Scenario: Tech company stock prices over 15 days
    print("\n📍 SCENARIO: Analyzing TECH Inc. Stock Performance")
    print("An investor wants to identify the best 5-day trading period.")
    
    stock_prices = [45.2, 46.8, 44.5, 47.3, 49.1, 48.6, 51.2, 50.8, 
                    52.4, 54.1, 53.7, 55.3, 54.9, 56.2, 57.1]
    
    analysis_period = 5
    
    analyze_investment_opportunity(stock_prices, analysis_period)
    
    # Additional analysis with different period
    print("\n\n" + "=" * 80)
    print("\n📍 COMPARATIVE ANALYSIS: 3-day vs 7-day periods")
    print("-" * 80)
    
    for period in [3, 7]:
        print(f"\n{'='*40}")
        print(f"Analysis for {period}-day period:")
        print(f"{'='*40}")
        max_val, start, _ = find_best_trading_period(stock_prices, period)
        print(f"Best period: Days {start} to {start+period-1}")
        print(f"Total value: ${max_val:.2f}")
        print(f"Average: ${max_val/period:.2f}/day")
    
    print("\n" + "=" * 80)
