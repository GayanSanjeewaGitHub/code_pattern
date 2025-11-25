"""
PATTERN: Greedy Algorithm
DIFFICULTY: Simple
REAL-WORLD SCENARIO: Meeting Room Scheduler - Maximum Meetings

Schedule maximum number of non-overlapping meetings in a conference room.
"""

def schedule_meetings(meetings: list[tuple[str, int, int]]) -> list:
    """Schedule maximum non-overlapping meetings."""
    # Sort by end time - greedy choice
    sorted_meetings = sorted(meetings, key=lambda x: x[2])
    
    scheduled = [sorted_meetings[0]]
    last_end = sorted_meetings[0][2]
    
    for name, start, end in sorted_meetings[1:]:
        if start >= last_end:  # No overlap
            scheduled.append((name, start, end))
            last_end = end
    
    return scheduled

if __name__ == "__main__":
    print("Meeting Room Scheduler - Greedy Algorithm")
    meetings = [
        ("Team Standup", 9, 10),
        ("Client Meeting", 10, 12),
        ("Lunch", 12, 13),
        ("Code Review", 13, 15),
    ]
    result = schedule_meetings(meetings)
    print(f"Scheduled {len(result)} meetings: {result}")