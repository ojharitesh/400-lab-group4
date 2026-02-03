"""
Lab Activity: Performance Analysis of File Allocation Strategies
STARTER TEMPLATE - Complete the TODO sections
"""

import random
import time

# Try to import matplotlib for visualization
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Warning: matplotlib not available. Install with: pip install matplotlib")

# Configuration
NUM_BLOCKS = 200
BLOCK_GROUP_SIZE = 50
NUM_GROUPS = NUM_BLOCKS // BLOCK_GROUP_SIZE  # 4 groups
NUM_FILES = 40
MIN_FILE_SIZE = 2
MAX_FILE_SIZE = 20

# Generate random file sizes (use seed for reproducibility)
random.seed(42)
FILE_SIZES = [random.randint(MIN_FILE_SIZE, MAX_FILE_SIZE) for _ in range(NUM_FILES)]


def naive_allocate(bitmap, size):
    """
    TODO: Implement naive (first-fit) allocation.
    
    Args:
        bitmap: List of 0/1 indicating free/used blocks (0 = free, 1 = used)
        size: Number of blocks needed
    
    Returns:
        List of block indices if allocation succeeds, None otherwise
    
    HINTS:
    Step 1: Create a list to store free block indices
    Step 2: Loop through bitmap, find all indices where bitmap[i] == 0
    Step 3: Check if you found enough free blocks (len(free_blocks) >= size)
    Step 4: If yes, return first 'size' blocks. If no, return None
    
    Example:
        bitmap = [1, 0, 0, 1, 0, 0, 0]
        size = 2
        Should return [1, 2] (first 2 free blocks)
    """
    # Step 1: Find all free blocks (where bitmap[i] == 0)
    free_blocks = []  # TODO: Create list comprehension: [i for i, b in enumerate(bitmap) if b == 0]
    
    # Step 2: Check if we have enough free blocks
    if len(free_blocks) < size:
        return None  # Not enough space
    
    # Step 3: Return the first 'size' free blocks
    return None  # TODO: Return free_blocks[:size]


def ffs_allocate(bitmap, size, group):
    """
    TODO: Implement FFS-inspired allocation within a block group.
    
    Args:
        bitmap: List of 0/1 indicating free/used blocks
        size: Number of blocks needed
        group: Block group number (0-3)
    
    Returns:
        List of block indices within the group if allocation succeeds, None otherwise
    
    Example:
        group = 1, BLOCK_GROUP_SIZE = 50
        start = 50, end = 100
        Look for free blocks between indices 50-99
    """
    # Step 1: Calculate the range for this group
    start = None  # TODO: group * BLOCK_GROUP_SIZE
    end = None    # TODO: start + BLOCK_GROUP_SIZE
    
    # Step 2: Find free blocks only within this group's range
    free_blocks = []  # TODO: [i for i in range(start, end) if bitmap[i] == 0]
    
    # Step 3: Check if we have enough free blocks
    if len(free_blocks) < size:
        return None  # Not enough space in this group
    
    # Step 4: Return the first 'size' free blocks
    return None  # TODO: Return free_blocks[:size]


def simulate(strategy):
    """
    TODO: Implement the simulation function.
    
    Args:
        strategy: 'naive' or 'ffs'
    
    Returns:
        Dictionary with performance metrics:
        {
            'seeks': total_seeks,
            'fragmentation': total_fragmentation,
            'allocation_time': average_time_ms,
            'space_util': utilization_ratio,
            'files': list of allocated file block lists,
            'used_blocks': number of blocks used
        }
    """
    bitmap = [0] * NUM_BLOCKS  # 0 = free, 1 = used
    files = []
    seeks = []
    fragmentation = []
    allocation_times = []
    used_blocks = 0
    
    for idx, size in enumerate(FILE_SIZES):
        # TODO: Measure allocation time
        t0 = time.time()
        
        # TODO: Allocate blocks based on strategy
        if strategy == 'naive':
            blocks = None  # TODO: Call naive_allocate(bitmap, size)
        else:  # ffs
            # Step 1: Assign file to a group using round-robin
            preferred_group = None  # TODO: idx % NUM_GROUPS
            
            # Step 2: Try to allocate in preferred group
            blocks = None  # TODO: Call ffs_allocate(bitmap, size, preferred_group)
            
            # Step 3: If preferred group is full, try other groups
            if blocks is None:
                for alt_group in range(NUM_GROUPS):
                    if alt_group != preferred_group:
                        blocks = None  # TODO: Call ffs_allocate(bitmap, size, alt_group)
                        if blocks is not None:
                            break  # Found space in alternative group
        
        t1 = time.time()
        allocation_times.append((t1 - t0) * 1000)  # Convert to milliseconds
        
        if not blocks:
            # Allocation failed
            files.append([])
            seeks.append(0)
            fragmentation.append(0)
            continue
        
        # Step 1: Mark blocks as used in bitmap (set bitmap[b] = 1 for each block)
        # TODO: Loop through blocks and set bitmap[b] = 1
        for b in blocks:  # blocks is a list, so this will work once you implement allocation
            bitmap[b] = 1  # TODO: Uncomment this line once blocks is not None
        
        # Step 2: Add blocks to files list
        files.append(blocks)  # Already done!
        
        # Step 3: Update used_blocks counter
        used_blocks += None  # TODO: Add len(blocks)
        
        # Step 4: Calculate seeks (non-contiguous jumps)
        # Example: blocks [5, 6, 8, 9] has 1 seek (jump from 6 to 8)
        # Loop through blocks starting at index 1, count when blocks[i] != blocks[i-1] + 1
        seek_count = 0  # TODO: sum(1 for i in range(1, len(blocks)) if blocks[i] != blocks[i-1] + 1)
        seeks.append(seek_count)
        
        # Step 5: Calculate fragmentation (max distance between blocks)
        # Example: blocks [5, 6, 8, 9] has fragmentation = 9 - 5 = 4
        frag = 0  # TODO: max(blocks) - min(blocks) if blocks else 0
        fragmentation.append(frag)
    
    # Step 1: Calculate totals and averages
    total_seeks = 0  # TODO: sum(seeks)
    total_frag = 0  # TODO: sum(fragmentation)
    avg_alloc_time = 0  # TODO: sum(allocation_times) / len(allocation_times) if allocation_times else 0
    space_util = 0  # TODO: used_blocks / NUM_BLOCKS
    
    return {
        'seeks': total_seeks,
        'fragmentation': total_frag,
        'allocation_time': avg_alloc_time,
        'space_util': space_util,
        'files': files,
        'used_blocks': used_blocks
    }


def visualize_comparison(naive_results, ffs_results):
    """
    TODO: Create bar charts comparing the two strategies.
    
    Create a bar chart with 4 bars:
    1. Total Seeks
    2. Total Fragmentation
    3. Average Allocation Time (ms)
    4. Space Utilization (scale by 1000 for visibility)
    
    HINTS:
    Step 1: Create labels list: ['Total Seeks', 'Total Fragmentation', 'Avg Alloc Time (ms)', 'Space Utilization']
    Step 2: Create naive_vals list with 4 values from naive_results
    Step 3: Create ffs_vals list with 4 values from ffs_results (scale space_util by 1000)
    Step 4: Use plt.bar() to create side-by-side bars
    Step 5: Add labels, title, legend with plt.xlabel(), plt.title(), plt.legend()
    Step 6: Save with plt.savefig('allocation_comparison.png')
    """
    if not HAS_MATPLOTLIB:
        print("Cannot visualize: matplotlib not available")
        return
    
    # Step 1: Set up labels
    labels = []  # TODO: ['Total Seeks', 'Total Fragmentation', 'Avg Alloc Time (ms)', 'Space Utilization']
    
    # Step 2: Set up values (scale space utilization by 1000 for visibility)
    # Note: These variables will be used in the plotting code below
    naive_vals = []  # TODO: [naive_results['seeks'], naive_results['fragmentation'], 
                     #       naive_results['allocation_time'], naive_results['space_util'] * 1000]
    ffs_vals = []    # TODO: [ffs_results['seeks'], ffs_results['fragmentation'],
                     #       ffs_results['allocation_time'], ffs_results['space_util'] * 1000]
    
    # Step 3: Create bar chart
    # Note: These variables will be used in the plotting code below
    x = range(len(labels))  # TODO: Uncomment once labels is defined
    width = 0.35  # Width of bars
    
    # Step 4: Create the actual plot
    # TODO: Uncomment and complete these lines:
    # fig, ax = plt.subplots(figsize=(12, 6))
    # bars1 = ax.bar([i - width/2 for i in x], naive_vals, width, label='Naive', color='#ff7f0e', alpha=0.8)
    # bars2 = ax.bar([i + width/2 for i in x], ffs_vals, width, label='FFS', color='#2ca02c', alpha=0.8)
    # ax.set_xlabel('Metrics', fontsize=12)
    # ax.set_ylabel('Value', fontsize=12)
    # ax.set_title('Performance Comparison: Naive vs. FFS Allocation Strategies', fontsize=14, fontweight='bold')
    # ax.set_xticks(x)
    # ax.set_xticklabels(labels)
    # ax.legend()
    # ax.grid(axis='y', alpha=0.3)
    # 
    # Step 5: Add value labels on top of bars (optional but nice!)
    # for bars in [bars1, bars2]:
    #     for bar in bars:
    #         height = bar.get_height()
    #         # Format differently for space utilization (4th bar, index 3)
    #         if bar.get_x() == x[3]:  # Space utilization bar
    #             label = f'{height/1000:.2%}'  # Convert back to percentage
    #         else:
    #             label = f'{int(height)}'  # Show integer for other metrics
    #         ax.text(bar.get_x() + bar.get_width()/2., height,
    #                label, ha='center', va='bottom', fontsize=9)
    # 
    # plt.tight_layout()
    # plt.savefig('allocation_comparison.png', dpi=150, bbox_inches='tight')
    # print("Visualization saved as 'allocation_comparison.png'")
    # plt.show()
    
    # Placeholder to prevent errors - remove this once you implement the plotting code above
    print("TODO: Implement visualization code above")


def print_results(results, strategy_name):
    """Helper function to print results for a strategy."""
    print(f"\n{strategy_name.upper()} Strategy Results:")
    print("-" * 60)
    print(f"  Total seeks:           {results['seeks']}")
    print(f"  Total fragmentation:   {results['fragmentation']}")
    print(f"  Avg allocation time:   {results['allocation_time']:.6f} ms")
    print(f"  Space utilization:     {results['space_util']:.2%}")
    print(f"  Blocks used:           {results['used_blocks']} / {NUM_BLOCKS}")
    allocated = len([f for f in results['files'] if f])
    print(f"  Files allocated:       {allocated} / {NUM_FILES}")


def main():
    """Main function to run the performance analysis."""
    print("=" * 80)
    print("Performance Analysis of File Allocation Strategies")
    print("=" * 80)
    print("\nConfiguration:")
    print(f"  - Total blocks: {NUM_BLOCKS}")
    print(f"  - Block groups: {NUM_GROUPS} (each with {BLOCK_GROUP_SIZE} blocks)")
    print(f"  - Number of files: {NUM_FILES}")
    print(f"  - File sizes: {MIN_FILE_SIZE} to {MAX_FILE_SIZE} blocks")
    
    print("\n" + "=" * 80)
    print("Running simulations...")
    print("=" * 80)
    
    # Run both simulations
    print("\nSimulating Naive (First-Fit) allocation...")
    naive_results = simulate('naive')
    print_results(naive_results, 'Naive (First-Fit)')
    
    print("\nSimulating FFS-Inspired allocation...")
    ffs_results = simulate('ffs')
    print_results(ffs_results, 'FFS-Inspired')
    
    # Comparison summary
    print("\n" + "=" * 80)
    print("COMPARISON SUMMARY")
    print("=" * 80)
    print(f"\n{'Metric':<30} {'Naive':<20} {'FFS':<20} {'Winner'}")
    print("-" * 80)
    
    # Seeks (lower is better)
    if ffs_results['seeks'] < naive_results['seeks']:
        seeks_winner = "FFS"
    elif naive_results['seeks'] < ffs_results['seeks']:
        seeks_winner = "Naive"
    else:
        seeks_winner = "Tie"
    print(f"{'Total Seeks':<30} {naive_results['seeks']:<20} {ffs_results['seeks']:<20} {seeks_winner}")
    
    # Fragmentation (lower is better)
    if ffs_results['fragmentation'] < naive_results['fragmentation']:
        frag_winner = "FFS"
    elif naive_results['fragmentation'] < ffs_results['fragmentation']:
        frag_winner = "Naive"
    else:
        frag_winner = "Tie"
    print(f"{'Total Fragmentation':<30} {naive_results['fragmentation']:<20} {ffs_results['fragmentation']:<20} {frag_winner}")
    
    # Allocation time (lower is better)
    if ffs_results['allocation_time'] < naive_results['allocation_time']:
        time_winner = "FFS"
    elif naive_results['allocation_time'] < ffs_results['allocation_time']:
        time_winner = "Naive"
    else:
        time_winner = "Tie"
    print(f"{'Avg Allocation Time (ms)':<30} {naive_results['allocation_time']:<20.6f} {ffs_results['allocation_time']:<20.6f} {time_winner}")
    
    # Space utilization (higher is better)
    if ffs_results['space_util'] > naive_results['space_util']:
        util_winner = "FFS"
    elif naive_results['space_util'] > ffs_results['space_util']:
        util_winner = "Naive"
    else:
        util_winner = "Tie"
    print(f"{'Space Utilization':<30} {naive_results['space_util']:<20.2%} {ffs_results['space_util']:<20.2%} {util_winner}")
    
    # Generate visualization
    if HAS_MATPLOTLIB:
        print("\n" + "=" * 80)
        print("Generating visualization...")
        print("=" * 80)
        visualize_comparison(naive_results, ffs_results)
        print("Visualization saved as 'allocation_comparison.png'")
    else:
        print("\n" + "=" * 80)
        print("Visualization skipped (matplotlib not available)")
        print("=" * 80)
    
    print("\nDone!")


if __name__ == "__main__":
    main()

