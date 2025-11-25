"""
PATTERN: Fast & Slow Pointers (Floyd's Cycle Detection)
DIFFICULTY: Simple
REAL-WORLD SCENARIO: Music Playlist Loop Detection

STORY:
You're building a music streaming app. Due to a bug, a playlist might have created
a loop where a song points back to a previous song instead of moving forward.
Users are stuck hearing the same songs repeatedly. You need to detect if there's
a loop in the playlist.

WHY FAST & SLOW POINTERS?
- Imagine two people running on a circular track at different speeds
- The faster runner will eventually lap the slower runner if there's a loop
- If there's no loop, the fast runner reaches the end first
- This is called "Floyd's Cycle Detection Algorithm" or "Tortoise and Hare"

KEY CONCEPT:
- Slow pointer moves 1 step at a time (🐢 tortoise)
- Fast pointer moves 2 steps at a time (🐰 hare)
- If there's a cycle, they WILL meet inside the cycle
- If no cycle, fast pointer reaches None/end

TIME COMPLEXITY: O(n) - will meet within n steps if cycle exists
SPACE COMPLEXITY: O(1) - only two pointers, no extra data structures
"""

class Song:
    """Represents a song in the playlist."""
    def __init__(self, title: str, artist: str):
        self.title = title
        self.artist = artist
        self.next = None  # Points to next song in playlist
    
    def __repr__(self):
        return f'"{self.title}" by {self.artist}'


def detect_playlist_loop(head: Song) -> tuple[bool, Song | None]:
    """
    Detect if there's a loop in the playlist using Floyd's algorithm.
    
    Args:
        head: First song in the playlist
        
    Returns:
        Tuple of (has_loop, meeting_point_song)
    """
    if not head or not head.next:
        return (False, None)
    
    print("\n🎵 PLAYLIST LOOP DETECTION")
    print("=" * 80)
    
    # Initialize two pointers
    slow = head          # 🐢 Tortoise - moves 1 step
    fast = head          # 🐰 Hare - moves 2 steps
    
    step = 0
    print(f"\n{'Step':<6} {'Slow Pointer (🐢)':<30} {'Fast Pointer (🐰)':<30} {'Status'}")
    print("-" * 80)
    
    # Move pointers until they meet or fast reaches end
    while fast and fast.next:
        # Move slow pointer 1 step
        slow = slow.next
        
        # Move fast pointer 2 steps
        fast = fast.next.next
        
        step += 1
        
        slow_song = slow.title[:25] if slow else "None"
        fast_song = fast.title[:25] if fast else "None"
        
        print(f"{step:<6} {slow_song:<30} {fast_song:<30}", end=" ")
        
        # Check if they met
        if slow == fast:
            print("🔄 LOOP DETECTED!")
            print(f"\n{'='*80}")
            print(f"⚠️  Playlist has a loop! Songs are repeating.")
            print(f"   Meeting point: {slow}")
            return (True, slow)
        else:
            print("➡️  Continue searching")
    
    # Fast reached end without meeting slow
    print(f"\n{'='*80}")
    print("✅ No loop detected - Playlist is valid!")
    return (False, None)


def find_loop_start(head: Song, meeting_point: Song) -> Song:
    """
    Find where the loop starts in the playlist.
    
    MATHEMATICAL PROOF:
    If loop exists, distance from head to loop start = 
    distance from meeting point to loop start (going around the loop)
    
    So we can find loop start by:
    1. Keep one pointer at meeting point
    2. Put another pointer at head
    3. Move both 1 step at a time
    4. They'll meet at the loop start!
    """
    print(f"\n🔍 FINDING LOOP START POINT")
    print("=" * 80)
    
    pointer1 = head
    pointer2 = meeting_point
    
    step = 0
    print(f"\n{'Step':<6} {'From Head':<30} {'From Meeting Point':<30} {'Status'}")
    print("-" * 80)
    
    while pointer1 != pointer2:
        pointer1 = pointer1.next
        pointer2 = pointer2.next
        step += 1
        
        print(f"{step:<6} {pointer1.title[:25]:<30} {pointer2.title[:25]:<30} ➡️  Searching")
    
    print(f"\n{'='*80}")
    print(f"🎯 Loop starts at: {pointer1}")
    return pointer1


def create_playlist_with_loop(songs_data: list[tuple[str, str]], loop_position: int = -1) -> Song:
    """
    Create a linked list of songs, optionally with a loop.
    
    Args:
        songs_data: List of (title, artist) tuples
        loop_position: If >= 0, last song points back to this position
    """
    if not songs_data:
        return None
    
    # Create song nodes
    songs = [Song(title, artist) for title, artist in songs_data]
    
    # Link songs together
    for i in range(len(songs) - 1):
        songs[i].next = songs[i + 1]
    
    # Create loop if specified
    if 0 <= loop_position < len(songs):
        songs[-1].next = songs[loop_position]
        print(f"🔄 Created loop: Last song points back to position {loop_position}")
    else:
        songs[-1].next = None
        print("✅ Created normal playlist (no loop)")
    
    return songs[0]


def print_playlist(head: Song, max_songs: int = 15):
    """Print playlist (limited to prevent infinite loop)."""
    print("\n📝 PLAYLIST STRUCTURE:")
    current = head
    count = 0
    visited = set()
    
    while current and count < max_songs:
        marker = " (🔄 LOOP POINT)" if current in visited else ""
        print(f"   {count + 1}. {current}{marker}")
        
        if current in visited:
            print(f"   ... loops back to song {count - len(visited) + 1}")
            break
        
        visited.add(current)
        current = current.next
        count += 1


# Example usage - Real playlist scenarios
if __name__ == "__main__":
    print("=" * 80)
    print("MUSIC STREAMING APP - PLAYLIST INTEGRITY CHECKER")
    print("=" * 80)
    
    # SCENARIO 1: Playlist with loop (buggy)
    print("\n\n📍 SCENARIO 1: Debugging Corrupted Playlist")
    print("-" * 80)
    
    buggy_playlist_songs = [
        ("Shape of You", "Ed Sheeran"),
        ("Blinding Lights", "The Weeknd"),
        ("Dance Monkey", "Tones and I"),
        ("Someone You Loved", "Lewis Capaldi"),
        ("Señorita", "Shawn Mendes"),
        ("Bad Guy", "Billie Eilish"),
    ]
    
    # Create playlist with loop (last song points to position 2)
    buggy_playlist = create_playlist_with_loop(buggy_playlist_songs, loop_position=2)
    print_playlist(buggy_playlist)
    
    # Detect loop
    has_loop, meeting_point = detect_playlist_loop(buggy_playlist)
    
    if has_loop:
        loop_start = find_loop_start(buggy_playlist, meeting_point)
        print(f"\n📋 DIAGNOSIS: Playlist corrupted")
        print(f"   Problem: Song after '{buggy_playlist_songs[-1][0]}' incorrectly points to '{loop_start.title}'")
        print(f"   Fix: Remove incorrect link and end playlist properly")
    
    # SCENARIO 2: Valid playlist (no loop)
    print("\n\n" + "=" * 80)
    print("\n📍 SCENARIO 2: Validating Normal Playlist")
    print("-" * 80)
    
    normal_playlist_songs = [
        ("Bohemian Rhapsody", "Queen"),
        ("Stairway to Heaven", "Led Zeppelin"),
        ("Hotel California", "Eagles"),
        ("Imagine", "John Lennon"),
    ]
    
    normal_playlist = create_playlist_with_loop(normal_playlist_songs, loop_position=-1)
    print_playlist(normal_playlist)
    
    has_loop, _ = detect_playlist_loop(normal_playlist)
    
    if not has_loop:
        print(f"\n📋 VALIDATION: ✅ Playlist is healthy")
        print(f"   All {len(normal_playlist_songs)} songs properly linked")
        print(f"   Safe to play for users")
    
    print("\n" + "=" * 80)
