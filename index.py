"""
COMPETITIVE PROGRAMMING PATTERNS - QUICK START GUIDE

This file helps you navigate and run all 54 pattern implementations.
Each pattern folder contains: simple/, medium/, and hard/ difficulty levels.
"""

import os
import sys

# Pattern catalog with descriptions
PATTERNS = {
    "01_two_pointers": {
        "name": "Two Pointers",
        "when_to_use": "Sorted arrays, finding pairs, palindromes",
        "files": {
            "simple": "warehouse_inventory_match.py - Find pair with target sum",
            "medium": "container_water_optimization.py - Maximum water container",
            "hard": "rainwater_harvesting.py - Trapping rainwater problem"
        }
    },
    "02_sliding_window": {
        "name": "Sliding Window",
        "when_to_use": "Contiguous subarrays, substring problems",
        "files": {
            "simple": "stock_trading_analyzer.py - Maximum sum of K elements",
            "medium": "network_quality_monitor.py - Longest subarray with condition",
            "hard": "smart_home_energy_optimizer.py - Minimum window substring"
        }
    },
    "03_fast_slow_pointers": {
        "name": "Fast & Slow Pointers",
        "when_to_use": "Cycle detection, middle element, linked lists",
        "files": {
            "simple": "playlist_loop_detection.py - Detect cycle in linked list",
            "medium": "traffic_cycle_detection.py - Find middle element",
            "hard": "duplicate_finder.py - Find duplicate in array"
        }
    },
    "04_binary_search": {
        "name": "Binary Search",
        "when_to_use": "Sorted data, search space optimization",
        "files": {
            "simple": "product_catalog_search.py - Search in sorted array",
            "medium": "server_capacity_planning.py - Binary search on answer",
            "hard": "aggressive_cows.py - Maximize minimum distance"
        }
    },
    "05_dynamic_programming": {
        "name": "Dynamic Programming",
        "when_to_use": "Optimization, overlapping subproblems",
        "files": {
            "simple": "staircase_climbing.py - Count ways (Fibonacci variant)",
            "medium": "stock_trading_cooldown.py - State machine DP",
            "hard": "text_justification.py - Minimize cost DP"
        }
    },
    "06_greedy": {
        "name": "Greedy Algorithms",
        "when_to_use": "Local optimum leads to global optimum",
        "files": {
            "simple": "meeting_scheduler.py - Activity selection",
            "medium": "gas_station.py - Circuit completion",
            "hard": "job_scheduling.py - Weighted job scheduling"
        }
    },
    "07_divide_conquer": {
        "name": "Divide & Conquer",
        "when_to_use": "Breaking into independent subproblems",
        "files": {
            "simple": "merge_sort.py - Sorting algorithm",
            "medium": "count_inversions.py - Count inversions",
            "hard": "median_two_arrays.py - Median of sorted arrays"
        }
    },
    "08_backtracking": {
        "name": "Backtracking",
        "when_to_use": "Exploring all solutions with pruning",
        "files": {
            "simple": "sudoku_solver.py - Constraint satisfaction",
            "medium": "n_queens.py - N-Queens placement",
            "hard": "word_break_ii.py - All possible solutions"
        }
    },
    "09_graph_algorithms": {
        "name": "Graph Algorithms",
        "when_to_use": "Networks, connections, paths",
        "files": {
            "simple": "social_network_bfs.py - BFS traversal",
            "medium": "package_delivery.py - Dijkstra shortest path",
            "hard": "flight_optimization.py - Bellman-Ford algorithm"
        }
    },
    "10_tree_patterns": {
        "name": "Tree Patterns",
        "when_to_use": "Hierarchical data, BST operations",
        "files": {
            "simple": "file_system_tree.py - Tree traversal",
            "medium": "bst_validation.py - Validate BST",
            "hard": "serialize_tree.py - Serialize/deserialize"
        }
    },
    "11_bit_manipulation": {
        "name": "Bit Manipulation",
        "when_to_use": "Low-level operations, optimization",
        "files": {
            "simple": "access_control.py - Permission bits",
            "medium": "single_number.py - XOR properties",
            "hard": "max_xor_subarray.py - Maximum XOR"
        }
    },
    "12_prefix_sum": {
        "name": "Prefix Sum",
        "when_to_use": "Range queries, cumulative sums",
        "files": {
            "simple": "sales_analysis.py - Range sum query",
            "medium": "subarray_sum_k.py - Subarray with target sum",
            "hard": "matrix_region_sum.py - 2D prefix sum"
        }
    },
    "13_monotonic_stack_queue": {
        "name": "Monotonic Stack/Queue",
        "when_to_use": "Next greater/smaller, range queries",
        "files": {
            "simple": "stock_span.py - Stock price span",
            "medium": "next_greater.py - Next greater element",
            "hard": "largest_rectangle.py - Largest rectangle"
        }
    },
    "14_trie": {
        "name": "Trie (Prefix Tree)",
        "when_to_use": "Prefix searches, autocomplete",
        "files": {
            "simple": "autocomplete.py - Autocomplete system",
            "medium": "word_search_ii.py - Word search in grid",
            "hard": "palindrome_pairs.py - Find palindrome pairs"
        }
    },
    "15_segment_tree": {
        "name": "Segment Tree",
        "when_to_use": "Range queries with updates",
        "files": {
            "simple": "range_query.py - Range min/max/sum",
            "medium": "range_update.py - Point and range updates",
            "hard": "lazy_propagation.py - Lazy propagation"
        }
    },
    "16_line_sweep": {
        "name": "Line Sweep",
        "when_to_use": "Interval problems, events",
        "files": {
            "simple": "meeting_conflicts.py - Interval overlaps",
            "medium": "skyline_problem.py - Building skyline",
            "hard": "rectangle_area.py - Rectangle union area"
        }
    },
    "17_string_matching": {
        "name": "String Matching",
        "when_to_use": "Pattern search in text",
        "files": {
            "simple": "kmp_search.py - KMP algorithm",
            "medium": "rabin_karp.py - Rolling hash search",
            "hard": "multiple_patterns.py - Multiple pattern matching"
        }
    },
    "18_hashing": {
        "name": "Hashing",
        "when_to_use": "Fast lookups, duplicates",
        "files": {
            "simple": "two_sum.py - Two sum problem",
            "medium": "group_anagrams.py - Group anagrams",
            "hard": "longest_consecutive.py - Longest consecutive sequence"
        }
    }
}


def print_pattern_catalog():
    """Display all available patterns."""
    print("=" * 100)
    print("COMPETITIVE PROGRAMMING PATTERNS CATALOG")
    print("=" * 100)
    print()
    
    for pattern_id, info in PATTERNS.items():
        print(f"📁 {pattern_id.upper()}: {info['name']}")
        print(f"   💡 Use when: {info['when_to_use']}")
        print(f"   📄 Files:")
        for difficulty, description in info['files'].items():
            print(f"      • {difficulty:<8} - {description}")
        print()


def run_example(pattern_id: str, difficulty: str):
    """Run a specific pattern example."""
    if pattern_id not in PATTERNS:
        print(f"❌ Pattern {pattern_id} not found!")
        return
    
    if difficulty not in PATTERNS[pattern_id]['files']:
        print(f"❌ Difficulty {difficulty} not found for pattern {pattern_id}!")
        return
    
    # Get filename from description
    filename = PATTERNS[pattern_id]['files'][difficulty].split(' - ')[0]
    filepath = os.path.join(pattern_id, difficulty, filename)
    
    if not os.path.exists(filepath):
        print(f"❌ File {filepath} not found!")
        return
    
    print(f"🚀 Running: {filepath}")
    print("=" * 100)
    os.system(f"python {filepath}")


def interactive_menu():
    """Interactive menu for exploring patterns."""
    while True:
        print("\n" + "=" * 100)
        print("INTERACTIVE PATTERN EXPLORER")
        print("=" * 100)
        print("\nOptions:")
        print("  1. View all patterns")
        print("  2. Run a pattern example")
        print("  3. Search patterns by use case")
        print("  4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            print_pattern_catalog()
        
        elif choice == "2":
            print("\nEnter pattern ID (e.g., 01_two_pointers): ", end="")
            pattern_id = input().strip()
            print("Enter difficulty (simple/medium/hard): ", end="")
            difficulty = input().strip()
            run_example(pattern_id, difficulty)
        
        elif choice == "3":
            keyword = input("\nEnter keyword (e.g., 'sorted', 'cycle', 'optimization'): ").strip().lower()
            print(f"\n🔍 Patterns matching '{keyword}':")
            found = False
            for pattern_id, info in PATTERNS.items():
                if keyword in info['when_to_use'].lower() or keyword in info['name'].lower():
                    print(f"   • {pattern_id}: {info['name']} - {info['when_to_use']}")
                    found = True
            if not found:
                print(f"   No patterns found matching '{keyword}'")
        
        elif choice == "4":
            print("\n👋 Happy coding!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-4.")


# Quick start examples
def quick_start():
    """Show quick start examples."""
    print("\n" + "=" * 100)
    print("QUICK START - Try These Examples First!")
    print("=" * 100)
    
    recommended = [
        ("01_two_pointers", "simple", "Perfect introduction to two pointers pattern"),
        ("02_sliding_window", "simple", "Learn sliding window with stock analysis"),
        ("04_binary_search", "simple", "Classic binary search with e-commerce"),
        ("05_dynamic_programming", "simple", "DP fundamentals with stairs problem"),
        ("18_hashing", "simple", "Essential hashing pattern - two sum"),
    ]
    
    print("\n📚 Recommended Learning Path:")
    for i, (pattern_id, difficulty, description) in enumerate(recommended, 1):
        filename = PATTERNS[pattern_id]['files'][difficulty].split(' - ')[0]
        print(f"\n{i}. {PATTERNS[pattern_id]['name']} ({difficulty})")
        print(f"   {description}")
        print(f"   Run: python {pattern_id}/{difficulty}/{filename}")


if __name__ == "__main__":
    print("=" * 100)
    print("COMPETITIVE PROGRAMMING PATTERNS - PYTHON 3.13")
    print("=" * 100)
    
    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == "list":
            print_pattern_catalog()
        elif sys.argv[1] == "quick":
            quick_start()
        else:
            print("Usage: python index.py [list|quick]")
            print("   Or run without arguments for interactive mode")
    else:
        # Interactive mode
        quick_start()
        print("\n")
        interactive_menu()
