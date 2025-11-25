# Getting Started with Competitive Programming Patterns

## Project Overview

This repository contains **54 complete Python implementations** of competitive programming patterns:
- **18 patterns** covering all major algorithm categories
- **3 difficulty levels** (simple, medium, hard) for each pattern
- **Realistic scenarios** with extensive comments and logging
- **Python 3.13** compatible with modern type hints

## Project Structure

```
code_pattern/
├── 01_two_pointers/        # Two pointer technique
├── 02_sliding_window/       # Sliding window pattern
├── 03_fast_slow_pointers/   # Floyd's cycle detection
├── 04_binary_search/        # Binary search variations
├── 05_dynamic_programming/  # DP problems
├── 06_greedy/               # Greedy algorithms
├── 07_divide_conquer/       # Divide & conquer
├── 08_backtracking/         # Backtracking solutions
├── 09_graph_algorithms/     # Graph problems
├── 10_tree_patterns/        # Tree algorithms
├── 11_bit_manipulation/     # Bit operations
├── 12_prefix_sum/           # Prefix sum technique
├── 13_monotonic_stack_queue/# Monotonic structures
├── 14_trie/                 # Trie data structure
├── 15_segment_tree/         # Segment tree
├── 16_line_sweep/           # Line sweep algorithm
├── 17_string_matching/      # String algorithms
└── 18_hashing/              # Hash-based solutions
```

Each folder contains:
- `simple/` - Introductory level with detailed explanations
- `medium/` - Intermediate level with optimizations
- `hard/` - Advanced level with complex scenarios

## Quick Start

### Prerequisites
- Python 3.13 (or Python 3.10+)
- No external dependencies required (pure Python standard library)

### Running Examples

**Method 1: Direct execution**
```bash
cd code_pattern
python 01_two_pointers/simple/warehouse_inventory_match.py
```

**Method 2: Using the index**
```bash
python index.py
# Follow interactive menu
```

**Method 3: List all patterns**
```bash
python index.py list
```

**Method 4: See recommended starting points**
```bash
python index.py quick
```

## Recommended Learning Path

### Week 1-2: Foundation Patterns
Start with these essential patterns that appear in 60% of problems:

1. **Two Pointers** (`01_two_pointers/simple/`)
   - Learn: Moving pointers from both ends
   - Try: Warehouse inventory matching
   
2. **Sliding Window** (`02_sliding_window/simple/`)
   - Learn: Fixed and variable window sizes
   - Try: Stock trading analyzer

3. **Hashing** (`18_hashing/simple/`)
   - Learn: O(1) lookups with hash maps
   - Try: Two sum problem

4. **Binary Search** (`04_binary_search/simple/`)
   - Learn: O(log n) search in sorted data
   - Try: Product catalog search

### Week 3-4: Core Algorithms

5. **Dynamic Programming** (`05_dynamic_programming/simple/`)
   - Learn: Memoization and tabulation
   - Try: Staircase climbing

6. **Greedy** (`06_greedy/simple/`)
   - Learn: Locally optimal choices
   - Try: Meeting room scheduler

7. **Prefix Sum** (`12_prefix_sum/simple/`)
   - Learn: Precompute for O(1) queries
   - Try: Sales report analysis

### Week 5-6: Advanced Patterns

8. **Fast & Slow Pointers** (`03_fast_slow_pointers/simple/`)
   - Learn: Cycle detection (Floyd's algorithm)
   - Try: Playlist loop detection

9. **Graph Algorithms** (`09_graph_algorithms/simple/`)
   - Learn: BFS/DFS traversal
   - Try: Social network exploration

10. **Tree Patterns** (`10_tree_patterns/simple/`)
    - Learn: Tree traversal and recursion
    - Try: File system tree

### Week 7-8: Specialized Patterns

11. **Backtracking** (`08_backtracking/simple/`)
12. **Divide & Conquer** (`07_divide_conquer/simple/`)
13. **Monotonic Stack/Queue** (`13_monotonic_stack_queue/simple/`)
14. **Bit Manipulation** (`11_bit_manipulation/simple/`)

### Week 9-10: Expert Patterns

15. **Trie** (`14_trie/simple/`)
16. **Segment Tree** (`15_segment_tree/simple/`)
17. **Line Sweep** (`16_line_sweep/simple/`)
18. **String Matching** (`17_string_matching/simple/`)

## Understanding the Code Structure

Every file follows this template:

```python
"""
PATTERN: [Pattern Name]
DIFFICULTY: [Simple/Medium/Hard]
REAL-WORLD SCENARIO: [Realistic Use Case]

STORY:
[Context explaining the real-world problem]

WHY THIS PATTERN?
[Explanation of why this approach is optimal]

TIME COMPLEXITY: [Big-O notation]
SPACE COMPLEXITY: [Big-O notation]
"""

def main_algorithm(params):
    """
    [Description]
    
    Args:
        [Parameters with types]
        
    Returns:
        [Return value description]
    """
    # Detailed implementation with comments
    # Step-by-step logging
    # Intermediate results printed
    pass

# Example usage with realistic data
if __name__ == "__main__":
    # Multiple scenarios demonstrating the pattern
    pass
```

## Key Features

### 1. Extensive Comments
Every algorithm includes:
- **Why comments**: Explaining why we do each step
- **What comments**: What each variable/function does
- **How comments**: How the algorithm progresses

### 2. Step-by-Step Logging
Watch the algorithm work in real-time:
```
Step 1: Checking element at index 5...
Step 2: Found match! Moving pointer...
Step 3: Final result: [...]
```

### 3. Realistic Scenarios
Instead of abstract array problems, you'll solve:
- Warehouse inventory management
- Energy system optimization
- Music playlist validation
- Network quality monitoring
- And 50+ more real scenarios!

### 4. Visual Output
Many implementations include ASCII visualizations:
```
Timeline:  ████░░░░████░░
           0   5   10  15
```

## Pattern Recognition Guide

Use this quick reference to identify which pattern to use:

### Problem → Pattern Mapping

| Problem Characteristic | Pattern to Use |
|----------------------|----------------|
| Sorted array + find pairs/triplets | Two Pointers |
| Contiguous subarray/substring | Sliding Window |
| Linked list cycle detection | Fast & Slow Pointers |
| Search in sorted space | Binary Search |
| Optimization with subproblems | Dynamic Programming |
| Locally optimal → globally optimal | Greedy |
| All possible combinations | Backtracking |
| Connected elements/paths | Graph Algorithms |
| Hierarchical data | Tree Patterns |
| Bit-level optimization | Bit Manipulation |
| Range queries on arrays | Prefix Sum |
| Next greater/smaller element | Monotonic Stack |
| Prefix matching | Trie |
| Range queries with updates | Segment Tree |
| Interval/event problems | Line Sweep |
| Pattern in text | String Matching |
| Fast lookups/duplicates | Hashing |

## Complexity Cheat Sheet

Common time complexities in competitive programming:

- **O(1)**: Hash map lookup, array access
- **O(log n)**: Binary search, balanced tree operations
- **O(n)**: Linear scan, two pointers, sliding window
- **O(n log n)**: Efficient sorting, heap operations
- **O(n²)**: Nested loops, some DP problems
- **O(2ⁿ)**: Brute force combinations (avoid!)
- **O(n!)**: Permutations (only for small n)

## Testing Your Understanding

After studying each pattern, you should be able to:

1. ✅ Explain when to use this pattern (in your own words)
2. ✅ Identify the pattern from a problem description
3. ✅ Implement the basic version from memory
4. ✅ Analyze time and space complexity
5. ✅ Solve similar LeetCode/Codeforces problems

## Common Pitfalls to Avoid

1. **Off-by-one errors**: Pay attention to `<=` vs `<`
2. **Integer overflow**: Use Python (auto big-int) or check bounds
3. **Not handling edge cases**: Empty input, single element, etc.
4. **Wrong complexity**: Make sure your solution is fast enough
5. **Modifying while iterating**: Create copies when needed

## Resources for Practice

After mastering these patterns, practice on:

- **LeetCode**: Filter by pattern tags
- **Codeforces**: Contests and problem sets
- **HackerRank**: Algorithm challenges
- **AtCoder**: Educational contests
- **Project Euler**: Mathematical problems

## Contribution Guidelines

Want to add more examples?
- Keep the realistic scenario theme
- Add extensive comments explaining WHY
- Include step-by-step logging
- Follow Python 3.13 style guidelines
- Add type hints

## Troubleshooting

### Encoding Issues (Windows)
If you see Unicode errors with emojis:
```bash
# Set environment variable
$env:PYTHONIOENCODING="utf-8"
# Then run the script
python pattern_file.py
```

Or modify scripts to remove emojis if needed.

### Import Errors
All scripts use only Python standard library. No pip installs needed!

### Performance Issues
For learning, we prioritize clarity over performance. Production code should be further optimized.

## Next Steps

1. ✅ Clone/download this repository
2. ✅ Start with recommended learning path (Week 1-2)
3. ✅ Run each example and read ALL comments
4. ✅ Try modifying inputs to see different scenarios
5. ✅ Implement variations without looking at code
6. ✅ Practice on coding platforms
7. ✅ Teach someone else (best way to learn!)

## Summary Statistics

- **Total Files**: 54+ Python files
- **Total Patterns**: 18 major patterns
- **Lines of Code**: ~10,000+ LOC
- **Comments**: Extensive documentation in every file
- **Real-World Scenarios**: 54 unique scenarios
- **Difficulty Levels**: 3 per pattern (simple, medium, hard)

---

**Ready to master competitive programming? Start with Week 1-2 patterns now!**

Good luck on your coding journey! 🚀
