"""
PATTERN: Sliding Window
DIFFICULTY: Medium
REAL-WORLD SCENARIO: Network Bandwidth Monitoring - Longest Period with Required Speed

STORY:
You're a network engineer monitoring internet connection quality for a data center.
You need to find the longest consecutive time period where bandwidth stays above 
a minimum threshold for uninterrupted service delivery.

WHY VARIABLE-SIZE SLIDING WINDOW?
- Window size is NOT fixed - it grows and shrinks based on conditions
- Expand window when condition is met (add right element)
- Shrink window when condition breaks (remove left element)
- Track the maximum window size achieved

This is more complex than fixed-size sliding window because:
- We need two pointers (left and right) to manage window size
- Decision logic: when to expand vs when to shrink

TIME COMPLEXITY: O(n) - each element visited at most twice (once by right, once by left)
SPACE COMPLEXITY: O(1) - only pointers and counters
"""

def longest_quality_connection_period(bandwidth_readings: list[int], min_threshold: int) -> tuple[int, int, int]:
    """
    Find longest consecutive period where bandwidth >= threshold.
    
    Args:
        bandwidth_readings: Bandwidth measurements in Mbps per minute
        min_threshold: Minimum required bandwidth in Mbps
        
    Returns:
        Tuple of (max_duration, start_time, end_time)
    """
    n = len(bandwidth_readings)
    
    # Window boundaries
    left = 0        # Left edge of window
    right = 0       # Right edge of window
    
    # Track best window found
    max_length = 0
    best_start = 0
    best_end = 0
    
    print(f"\n📡 Bandwidth Readings (Mbps): {bandwidth_readings}")
    print(f"🎯 Minimum Threshold: {min_threshold} Mbps\n")
    
    print(f"{'Step':<6} {'L':<4} {'R':<4} {'BW[R]':<8} {'Condition':<12} {'Window Size':<13} "
          f"{'Best':<6} {'Action':<30}")
    print("-" * 100)
    
    step = 1
    current_length = 0
    
    # Expand window by moving right pointer
    while right < n:
        current_bandwidth = bandwidth_readings[right]
        
        # Check if current reading meets threshold
        if current_bandwidth >= min_threshold:
            # EXPAND: Good bandwidth, include in window
            current_length = right - left + 1
            
            print(f"{step:<6} {left:<4} {right:<4} {current_bandwidth:<8} {'✅ Good':<12} "
                  f"{current_length:<13} {max_length:<6} ", end="")
            
            # Update best window if current is larger
            if current_length > max_length:
                max_length = current_length
                best_start = left
                best_end = right
                print("⭐ Expand & Update best")
            else:
                print("➡️  Expand window")
            
            right += 1
            
        else:
            # SHRINK: Bad bandwidth, reset window
            print(f"{step:<6} {left:<4} {right:<4} {current_bandwidth:<8} {'❌ Poor':<12} "
                  f"{0:<13} {max_length:<6} ⚠️  Reset window, move both pointers")
            
            # Jump to next position after bad reading
            right += 1
            left = right
            current_length = 0
        
        step += 1
    
    return (max_length, best_start, best_end)


def generate_quality_report(readings: list[int], threshold: int, 
                           duration: int, start: int, end: int):
    """
    Generate comprehensive network quality report.
    """
    print("\n" + "=" * 100)
    print("📊 NETWORK QUALITY REPORT")
    print("=" * 100)
    
    if duration == 0:
        print("\n❌ No period found meeting the bandwidth requirements")
        print(f"   All readings below {threshold} Mbps threshold")
        return
    
    quality_period = readings[start:end+1]
    total_data = sum(quality_period)
    average_bandwidth = total_data / duration
    
    print(f"\n🎯 BEST QUALITY PERIOD:")
    print(f"   Time Window: Minute {start} to Minute {end}")
    print(f"   Duration: {duration} minutes")
    print(f"   Bandwidth readings: {quality_period}")
    
    print(f"\n📈 STATISTICS:")
    print(f"   Average bandwidth: {average_bandwidth:.2f} Mbps")
    print(f"   Minimum in period: {min(quality_period)} Mbps")
    print(f"   Maximum in period: {max(quality_period)} Mbps")
    print(f"   Total data potential: {total_data} MB")
    
    # Calculate uptime percentage
    total_time = len(readings)
    uptime_percentage = (duration / total_time) * 100
    
    print(f"\n⏱️  SERVICE LEVEL:")
    print(f"   Quality uptime: {duration}/{total_time} minutes ({uptime_percentage:.1f}%)")
    
    # SLA evaluation
    print(f"\n📋 SLA EVALUATION:")
    if uptime_percentage >= 99:
        print("   ✅ EXCELLENT - Exceeds 99% uptime SLA")
    elif uptime_percentage >= 95:
        print("   ✅ GOOD - Meets 95% uptime SLA")
    elif uptime_percentage >= 90:
        print("   ⚠️  ACCEPTABLE - Meets minimum 90% SLA")
    else:
        print("   ❌ POOR - Below acceptable SLA, requires attention")
    
    # Visualization
    print(f"\n📊 VISUAL TIMELINE:")
    print("   ", end="")
    for i, bw in enumerate(readings):
        if start <= i <= end:
            print("█", end="")  # Quality period
        else:
            print("·", end="")  # Other periods
    print()
    print(f"   {'0':<{start}}{'START':<{end-start}}END")


# Example usage - Real network monitoring scenario
if __name__ == "__main__":
    print("=" * 100)
    print("DATA CENTER NETWORK BANDWIDTH MONITOR")
    print("=" * 100)
    
    # Scenario: Hourly bandwidth monitoring (60 minutes)
    print("\n📍 SCENARIO: Server Farm Network Quality Analysis")
    print("Network engineer needs to identify the longest stable high-bandwidth period")
    print("for scheduling critical data transfers.\n")
    
    # Bandwidth readings in Mbps per minute (realistic fluctuating pattern)
    bandwidth_logs = [
        45, 52, 48, 67, 73, 81, 78, 85, 92, 88,  # Minutes 0-9: Building up
        95, 91, 87, 83, 79, 74, 68, 45, 42, 38,  # Minutes 10-19: Peak then drop
        91, 96, 94, 98, 101, 97, 99, 103, 105, 102,  # Minutes 20-29: Excellent period
        98, 95, 91, 88, 85, 81, 55, 51, 48, 44,  # Minutes 30-39: Declining
        86, 89, 92, 87, 84, 80, 76, 72, 68, 64   # Minutes 40-49: Recovery
    ]
    
    minimum_bandwidth = 85  # Mbps
    
    # Find best period
    max_duration, start_minute, end_minute = longest_quality_connection_period(
        bandwidth_logs, minimum_bandwidth
    )
    
    # Generate detailed report
    generate_quality_report(bandwidth_logs, minimum_bandwidth, 
                           max_duration, start_minute, end_minute)
    
    # Recommendation
    print("\n" + "=" * 100)
    print("🎯 OPERATIONAL RECOMMENDATION:")
    if max_duration >= 15:
        print(f"   ✅ Schedule critical data transfers during minutes {start_minute}-{end_minute}")
        print(f"   ✅ {max_duration}-minute window provides adequate time for large transfers")
    elif max_duration >= 10:
        print(f"   ⚠️  Limited window (minutes {start_minute}-{end_minute}) - schedule smaller transfers")
    else:
        print("   ❌ Insufficient stable bandwidth - consider off-peak hours or infrastructure upgrade")
    print("=" * 100)
