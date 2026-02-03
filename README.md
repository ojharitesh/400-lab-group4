# Lab Activity: Performance Analysis of File Allocation Strategies

## Objective

Measure and compare the performance of **naive (first-fit)** and **FFS-inspired (block group)** allocation strategies on simulated workloads, focusing on seeks, fragmentation, allocation time, and space utilization.

## Background

### The Problem

When storing files on a disk, the operating system must decide where to place file blocks. Different allocation strategies have different performance characteristics:

- **Naive (First-Fit)**: Allocates the first available blocks anywhere on the disk
- **FFS-Inspired (Block Groups)**: Tries to keep each file's blocks together within the same block group

### Why It Matters

On real hard drives, the disk head must physically move to read data. This movement (called a "seek") is slow. By keeping related data together, we can reduce seeks and improve performance.

## Setup

### Disk Model

- **200 blocks** total
- Divided into **4 block groups** (50 blocks each)
  - Group 0: blocks 0-49
  - Group 1: blocks 50-99
  - Group 2: blocks 100-149
  - Group 3: blocks 150-199

### Workload

- **40 files** to allocate
- Each file has a **random size between 2 and 20 blocks**

## Implementation Tasks

### Task 1: Implement Allocation Functions

You need to implement two allocation functions:

1. **`naive_allocate(bitmap, size)`**
   - Takes a bitmap (list of 0/1) and number of blocks needed
   - Returns a list of block indices (first available blocks)
   - Returns `None` if not enough space

2. **`ffs_allocate(bitmap, size, group)`**
   - Takes a bitmap, size, and block group number (0-3)
   - Returns a list of block indices within that group
   - Returns `None` if not enough space in that group

### Task 2: Implement Simulation Function

Create a `simulate(strategy)` function that:

- Takes 'naive' or 'ffs' as the strategy
- For each file:
  - Measures allocation time
  - Allocates blocks using the chosen strategy
  - Marks blocks as used in the bitmap
  - Calculates seeks (non-contiguous jumps between blocks)
  - Calculates fragmentation (max distance between blocks)
- Returns a dictionary with:
  - `seeks`: total seeks across all files
  - `fragmentation`: total fragmentation
  - `allocation_time`: average allocation time (ms)
  - `space_util`: space utilization (0.0 to 1.0)

### Task 3: Metrics to Calculate

**Seeks**: Count how many times blocks are non-contiguous

```python
# Example: blocks [5, 6, 8, 9] has 1 seek (jump from 6 to 8)
seek_count = sum(1 for i in range(1, len(blocks)) 
                 if blocks[i] != blocks[i-1] + 1)
```

**Fragmentation**: Max distance between blocks in a file

```python
# Example: blocks [5, 6, 8, 9] has fragmentation = 9 - 5 = 4
frag = max(blocks) - min(blocks) if blocks else 0
```

### Task 4: Visualization

Create bar charts comparing the two strategies for:

- Total seeks (lower is better)
- Total fragmentation (lower is better)
- Average allocation time (lower is better)
- Space utilization (higher is better)

#### How to implement `visualize_comparison(naive_results, ffs_results)`

In `performance_analysis_starter.py`, fill in the `visualize_comparison()` function to generate the bar chart.

**Step-by-step checklist:**

1. **Create labels**
   - Use 4 labels (one per metric):
     - `"Total Seeks"`
     - `"Total Fragmentation"`
     - `"Avg Alloc Time (ms)"`
     - `"Space Utilization"`

2. **Create the values for each strategy**
   - `naive_vals` should be a list of 4 numbers pulled from `naive_results`
   - `ffs_vals` should be a list of 4 numbers pulled from `ffs_results`
   - **Important:** For the bar chart, multiply space utilization by 1000 so it’s visible on the same plot:
     - `naive_results['space_util'] * 1000`
     - `ffs_results['space_util'] * 1000`

3. **Make side-by-side bars**
   - Use `x = range(len(labels))` and `width = 0.35`
   - Create two `plt.bar(...)` calls (one for naive, one for FFS) with x-offsets:
     - naive bars at `[i - width/2 for i in x]`
     - ffs bars at `[i + width/2 for i in x]`

4. **Add plot formatting**
   - Title, axis labels, legend
   - Set the x-tick labels to your `labels` list

5. **Save the figure**
   - Save to **`allocation_comparison.png`** using `plt.savefig(...)`
   - Then call `plt.show()` (optional, but helpful if running locally)

**Reminder:** If matplotlib is not installed, the starter code will skip visualization. Install it with `pip install matplotlib`.

## Deliverables

1. **Complete Python script** (`performance_analysis_starter.py`) with:
   - Both allocation functions
   - Simulation function
   - Visualization code
   - Main function that runs both strategies and displays results

2. **Output**:
   - Console output showing metrics for both strategies
   - Comparison summary table
   - Bar chart visualization (saved as PNG)

3. **Short report** (1-2 pages) answering:
   - Which strategy resulted in fewer seeks and lower fragmentation?
   - How did allocation time compare?
   - What happens to performance as the disk fills up?
   - How does this demonstrate the importance of file system design?

## Getting Started

1. Open `performance_analysis_starter.py`
2. Set up the configuration:

   ```python
   NUM_BLOCKS = 200
   BLOCK_GROUP_SIZE = 50
   NUM_FILES = 40
   MIN_FILE_SIZE = 2
   MAX_FILE_SIZE = 20
   ```

3. Generate random file sizes (use a seed for reproducibility)
4. Implement the allocation functions
5. Implement the simulation function
6. Add visualization using matplotlib
7. Test and compare results

## Hints

- Use a list of 0/1 to represent the bitmap (0 = free, 1 = used)
- For FFS, try the preferred group first, then fall back to other groups if needed
- Use `time.time()` to measure allocation time
- Use `matplotlib.pyplot` for bar charts
- Make sure to handle cases where allocation fails (not enough space)

## Submission

Submit:

1. Your Python script (`performance_analysis_starter.py`)
2. The generated visualization image (`allocation_comparison.png`)
3. A brief report with your analysis and answers to the questions

## Grading Rubric

- **Implementation (40%)**: Correct allocation functions and simulation
- **Metrics (30%)**: Accurate calculation of seeks, fragmentation, time, utilization
- **Visualization (20%)**: Clear, labeled bar charts
- **Analysis (10%)**: Thoughtful answers to reflection questions

## Resources

- Python documentation: `https://docs.python.org/3/`
- Matplotlib tutorial: `https://matplotlib.org/stable/tutorials/index.html`
- File system concepts from lecture notes

---

**Good luck!** Start with the allocation functions, then build up to the full simulation.
