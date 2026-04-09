"""
Lab 07: Implementing Sorting Algorithms - Smart Sorting Framework
================================================================
A framework that analyzes input data and automatically selects
the most suitable sorting algorithm.
User provides input array - no hardcoded test data.
"""

import heapq
import time
import random

# ============================================================================
# PART 1: SORTING ALGORITHM IMPLEMENTATIONS
# ============================================================================

def bubble_sort(arr):
    """
    Bubble Sort: O(n²)
    Repeatedly steps through the list, compares adjacent elements
    and swaps them if they're in the wrong order.
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def selection_sort(arr):
    """
    Selection Sort: O(n²)
    Divides the list into sorted and unsorted parts.
    Repeatedly finds the minimum element from unsorted part
    and places it at the end of sorted part.
    """
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr


def insertion_sort(arr):
    """
    Insertion Sort: O(n²) worst case, O(n) best case
    Builds the final sorted array one item at a time.
    Very efficient for small or nearly-sorted datasets.
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def heap_sort(arr):
    """
    Heap Sort: O(n log n)
    Converts the array into a heap data structure, then repeatedly
    extracts the maximum element to build the sorted array.
    """
    heap = arr.copy()
    heapq.heapify(heap)
    sorted_list = []
    while heap:
        sorted_list.append(heapq.heappop(heap))
    return sorted_list


def merge_sort(arr):
    """
    Merge Sort: O(n log n)
    Divide and conquer algorithm that splits the array in half,
    recursively sorts each half, then merges them back together.
    Stable sort with guaranteed O(n log n) performance.
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    merged = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quick_sort(arr):
    """
    Quick Sort: O(n log n) average, O(n²) worst case
    Divide and conquer algorithm that selects a pivot element
    and partitions the array around it. Very fast in practice.
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return left + middle + right


# ============================================================================
# PART 2: DATA ANALYSIS FUNCTIONS
# ============================================================================

def analyze_data(arr):
    """
    Analyzes the input array and returns its characteristics.
    
    Parameters:
        arr (list): The input array to analyze
    
    Returns:
        dict: Dictionary containing array characteristics
    """
    if len(arr) == 0:
        return {
            'size': 0,
            'is_sorted': True,
            'is_reverse_sorted': True,
            'sortedness': 1.0,
            'unique_ratio': 0.0,
            'data_type': None
        }
    
    n = len(arr)
    
    # Check if array is already sorted
    is_sorted = all(arr[i] <= arr[i+1] for i in range(n-1))
    
    # Check if array is reverse sorted
    is_reverse_sorted = all(arr[i] >= arr[i+1] for i in range(n-1))
    
    # Count inversions (pairs out of order) - sample for efficiency
    sample_size = min(n, 100)
    inversions = 0
    for i in range(sample_size):
        for j in range(i+1, sample_size):
            if arr[i] > arr[j]:
                inversions += 1
    
    # Calculate "sortedness" percentage
    if sample_size <= 1:
        sortedness = 1.0
    else:
        max_inversions = (sample_size * (sample_size - 1)) // 2
        sortedness = 1 - (inversions / max_inversions) if max_inversions > 0 else 1
    
    # Check for small range of values
    sample_for_unique = arr[:min(n, 1000)]
    unique_values = len(set(sample_for_unique))
    unique_ratio = unique_values / len(sample_for_unique)
    
    return {
        'size': n,
        'is_sorted': is_sorted,
        'is_reverse_sorted': is_reverse_sorted,
        'sortedness': sortedness,
        'unique_ratio': unique_ratio,
        'data_type': type(arr[0]).__name__
    }


# ============================================================================
# PART 3: SMART SORTING FRAMEWORK
# ============================================================================

class SmartSortingFramework:
    """
    A smart sorting framework that automatically selects the best 
    sorting algorithm based on input data characteristics.
    """
    
    def __init__(self):
        """Initialize the framework with available sorting algorithms."""
        self.algorithms = {
            'bubble': bubble_sort,
            'selection': selection_sort,
            'insertion': insertion_sort,
            'heap': heap_sort,
            'merge': merge_sort,
            'quick': quick_sort,
            'built-in': sorted
        }
        
        self.algorithm_names = {
            'bubble': 'Bubble Sort',
            'selection': 'Selection Sort',
            'insertion': 'Insertion Sort',
            'heap': 'Heap Sort',
            'merge': 'Merge Sort',
            'quick': 'Quick Sort',
            'built-in': 'Python Built-in Sort (Timsort)'
        }
        
        self.complexities = {
            'bubble': 'O(n²)',
            'selection': 'O(n²)',
            'insertion': 'O(n²) worst, O(n) best',
            'heap': 'O(n log n)',
            'merge': 'O(n log n)',
            'quick': 'O(n log n) avg, O(n²) worst',
            'built-in': 'O(n log n)'
        }
    
    def select_algorithm(self, arr):
        """
        Selects the most appropriate sorting algorithm based on data analysis.
        """
        if len(arr) == 0:
            return 'built-in'
        
        analysis = analyze_data(arr)
        n = analysis['size']
        
        # Already sorted - built-in is highly optimized
        if analysis['is_sorted']:
            return 'built-in'
        
        # Very small arrays - Insertion Sort has lowest overhead
        if n < 30:
            return 'insertion'
        
        # Small to medium arrays
        if n < 1000:
            if analysis['sortedness'] > 0.7:
                return 'insertion'
            else:
                return 'quick'
        
        # Large arrays
        else:
            if analysis['sortedness'] > 0.8:
                return 'insertion'
            elif analysis['unique_ratio'] < 0.1:
                return 'quick'
            else:
                return 'merge'
    
    def sort(self, arr, algorithm=None, verbose=True):
        """
        Sort the array using selected or specified algorithm.
        """
        if algorithm is None:
            algorithm = self.select_algorithm(arr)
        
        # Make a copy to avoid modifying original
        arr_copy = arr.copy()
        
        start_time = time.perf_counter()
        sorted_arr = self.algorithms[algorithm](arr_copy)
        end_time = time.perf_counter()
        
        execution_time = (end_time - start_time) * 1000
        
        if verbose:
            print(f"\n{'='*60}")
            print(f" SORTING RESULTS")
            print(f"{'='*60}")
            print(f"Algorithm Used: {self.algorithm_names[algorithm]}")
            print(f"Time Complexity: {self.complexities[algorithm]}")
            print(f"Input Size: {len(arr)} elements")
            print(f"Execution Time: {execution_time:.6f} ms")
            print(f"{'='*60}")
        
        return {
            'sorted_array': sorted_arr,
            'algorithm_used': self.algorithm_names[algorithm],
            'algorithm_key': algorithm,
            'execution_time_ms': execution_time,
            'input_size': len(arr)
        }
    
    def compare_all_algorithms(self, arr):
        """
        Compare performance of all algorithms on the given array.
        """
        results = {}
        
        for algo_name, algo_func in self.algorithms.items():
            arr_copy = arr.copy()
            
            start_time = time.perf_counter()
            sorted_arr = algo_func(arr_copy)
            end_time = time.perf_counter()
            
            results[algo_name] = {
                'name': self.algorithm_names[algo_name],
                'time_ms': (end_time - start_time) * 1000,
                'complexity': self.complexities[algo_name],
                'correct': sorted_arr == sorted(arr)
            }
        
        return results


# ============================================================================
# PART 4: USER INPUT FUNCTIONS
# ============================================================================

def get_user_array():
    """
    Get array input from user with multiple input methods.
    """
    print("\n" + "="*60)
    print("ARRAY INPUT OPTIONS")
    print("="*60)
    print("1. Enter numbers manually (space-separated)")
    print("2. Generate random array")
    print("3. Generate nearly sorted array")
    print("4. Generate reverse sorted array")
    print("5. Generate array with duplicates")
    print("="*60)
    
    while True:
        choice = input("\nSelect input method (1-5): ").strip()
        
        if choice == '1':
            # Manual input
            while True:
                try:
                    nums = input("\nEnter numbers separated by spaces: ").strip()
                    if not nums:
                        print(" Please enter some numbers.")
                        continue
                    arr = [int(x) for x in nums.split()]
                    print(f"✓ Array accepted: {arr}")
                    return arr
                except ValueError:
                    print(" Invalid input. Please enter numbers only (e.g., 5 2 8 1 9).")
        
        elif choice == '2':
            # Random array
            try:
                size = int(input("Enter array size: "))
                if size <= 0:
                    print(" Size must be positive.")
                    continue
                min_val = int(input("Enter minimum value (default 1): ") or "1")
                max_val = int(input("Enter maximum value (default 100): ") or "100")
                
                arr = [random.randint(min_val, max_val) for _ in range(size)]
                print(f"\nGenerated array ({size} elements):")
                print(f"First 20 elements: {arr[:20]}{'...' if size > 20 else ''}")
                return arr
            except ValueError:
                print(" Please enter valid numbers.")
        
        elif choice == '3':
            # Nearly sorted array
            try:
                size = int(input("Enter array size: "))
                if size <= 0:
                    print(" Size must be positive.")
                    continue
                swaps = int(input("Enter number of random swaps (default 5): ") or "5")
                
                arr = list(range(size))
                for _ in range(swaps):
                    i, j = random.randint(0, size-1), random.randint(0, size-1)
                    arr[i], arr[j] = arr[j], arr[i]
                
                print(f"\nGenerated nearly sorted array ({size} elements with {swaps} swaps):")
                print(f"First 20 elements: {arr[:20]}{'...' if size > 20 else ''}")
                return arr
            except ValueError:
                print(" Please enter valid numbers.")
        
        elif choice == '4':
            # Reverse sorted array
            try:
                size = int(input("Enter array size: "))
                if size <= 0:
                    print(" Size must be positive.")
                    continue
                
                arr = list(range(size, 0, -1))
                print(f"\nGenerated reverse sorted array ({size} elements):")
                print(f"First 20 elements: {arr[:20]}{'...' if size > 20 else ''}")
                return arr
            except ValueError:
                print(" Please enter valid numbers.")
        
        elif choice == '5':
            # Array with duplicates
            try:
                size = int(input("Enter array size: "))
                if size <= 0:
                    print(" Size must be positive.")
                    continue
                unique_vals = int(input("Enter number of unique values (default 5): ") or "5")
                max_val = int(input("Enter maximum value (default 100): ") or "100")
                
                values = [random.randint(1, max_val) for _ in range(unique_vals)]
                arr = [random.choice(values) for _ in range(size)]
                
                print(f"\nGenerated array with duplicates ({size} elements, {unique_vals} unique values):")
                print(f"First 20 elements: {arr[:20]}{'...' if size > 20 else ''}")
                print(f"Unique values in array: {set(arr)}")
                return arr
            except ValueError:
                print(" Please enter valid numbers.")
        
        else:
            print(" Invalid choice. Please enter 1-5.")


def display_analysis(analysis):
    """
    Display data analysis results.
    """
    print("\n" + "="*60)
    print("DATA ANALYSIS RESULTS")
    print("="*60)
    print(f"Array Size: {analysis['size']} elements")
    print(f"Data Type: {analysis['data_type']}")
    print(f"Already Sorted: {'✓ Yes' if analysis['is_sorted'] else '✗ No'}")
    print(f"Reverse Sorted: {'✓ Yes' if analysis['is_reverse_sorted'] else '✗ No'}")
    print(f"Sortedness: {analysis['sortedness']*100:.2f}%")
    print(f"Unique Value Ratio: {analysis['unique_ratio']*100:.2f}%")
    print("="*60)


# ============================================================================
# PART 5: MAIN EXECUTION
# ============================================================================

def main():
    """
    Main function - takes user input and executes the sorting framework.
    """
    print("\n")
    print("*" * 80)
    print("*" + " " * 78 + "*")
    print("*" + "    LAB 07: SMART SORTING FRAMEWORK".center(78) + "*")
    print("*" + "    Implementing and Comparing Sorting Algorithms".center(78) + "*")
    print("*" + " " * 78 + "*")
    print("*" * 80)
    
    framework = SmartSortingFramework()
    
    while True:
        # Get array from user
        arr = get_user_array()
        
        if len(arr) == 0:
            print("\n Array is empty. Please enter some data.")
            continue
        
        # Analyze the data
        analysis = analyze_data(arr)
        display_analysis(analysis)
        
        # Let user choose what to do
        print("\n" + "="*60)
        print("SORTING OPTIONS")
        print("="*60)
        print("1. Use SMART selection (framework chooses best algorithm)")
        print("2. Choose specific algorithm manually")
        print("3. Compare ALL algorithms")
        print("4. Enter new array")
        print("5. Exit")
        print("="*60)
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            # Smart selection
            selected = framework.select_algorithm(arr)
            print(f"\n SMART SELECTION: {framework.algorithm_names[selected]}")
            print(f"   Reason: Based on array size ({len(arr)}) and sortedness ({analysis['sortedness']*100:.1f}%)")
            
            result = framework.sort(arr)
            print(f"\n✓ Original array: {arr[:20]}{'...' if len(arr) > 20 else ''}")
            print(f"✓ Sorted array:   {result['sorted_array'][:20]}{'...' if len(arr) > 20 else ''}")
            
            # Verify correctness
            is_correct = result['sorted_array'] == sorted(arr)
            print(f"✓ Correctly sorted: {'Yes' if is_correct else 'No'}")
        
        elif choice == '2':
            # Manual algorithm selection
            print("\n" + "="*60)
            print("AVAILABLE ALGORITHMS")
            print("="*60)
            
            algos = list(framework.algorithms.keys())
            for i, algo in enumerate(algos, 1):
                print(f"{i}. {framework.algorithm_names[algo]} - {framework.complexities[algo]}")
            
            try:
                algo_choice = int(input(f"\nSelect algorithm (1-{len(algos)}): ").strip())
                if 1 <= algo_choice <= len(algos):
                    selected_algo = algos[algo_choice - 1]
                    result = framework.sort(arr, algorithm=selected_algo)
                    
                    print(f"\n✓ Original array: {arr[:20]}{'...' if len(arr) > 20 else ''}")
                    print(f"✓ Sorted array:   {result['sorted_array'][:20]}{'...' if len(arr) > 20 else ''}")
                    
                    is_correct = result['sorted_array'] == sorted(arr)
                    print(f"✓ Correctly sorted: {'Yes' if is_correct else 'No'}")
                else:
                    print(" Invalid selection.")
            except ValueError:
                print(" Please enter a valid number.")
        
        elif choice == '3':
            # Compare all algorithms
            print("\n" + "="*70)
            print("COMPARING ALL SORTING ALGORITHMS")
            print("="*70)
            
            results = framework.compare_all_algorithms(arr)
            
            print(f"\n{'Algorithm':<25} {'Time (ms)':<15} {'Complexity':<22} {'Status':<10}")
            print("-" * 75)
            
            sorted_results = sorted(results.items(), key=lambda x: x[1]['time_ms'])
            
            for algo, data in sorted_results:
                status = "✓" if data['correct'] else "✗"
                print(f"{data['name']:<25} {data['time_ms']:<15.6f} {data['complexity']:<22} {status:<10}")
            
            # Show fastest algorithm
            fastest = sorted_results[0]
            print(f"\n Fastest Algorithm: {fastest[1]['name']} ({fastest[1]['time_ms']:.6f} ms)")
            
            # Compare with smart selection
            smart_choice = framework.select_algorithm(arr)
            print(f" Smart Selection would choose: {framework.algorithm_names[smart_choice]}")
        
        elif choice == '4':
            # Enter new array
            continue
        
        elif choice == '5':
            # Exit
            print("\n" + "="*60)
            print("LAB COMPLETED SUCCESSFULLY!")
            print("="*60)
            print("\n Summary of Sorting Algorithms:")
            print("   • Bubble Sort:    Simple but slow O(n²) - Educational use")
            print("   • Selection Sort: Minimal swaps O(n²) - Small arrays")
            print("   • Insertion Sort: Fast for nearly-sorted data")
            print("   • Heap Sort:      Guaranteed O(n log n)")
            print("   • Merge Sort:     Stable O(n log n) - Large datasets")
            print("   • Quick Sort:     Fast average case - General purpose")
            print("   • Built-in Sort:  Best for production Python code!")
            print("\nThank you for completing Lab 07!")
            break
        
        else:
            print(" Invalid choice. Please enter 1-5.")
        
        # Ask if user wants to continue
        if choice != '4':
            print("\n" + "-"*40)
            continue_choice = input("Continue with same array? (y/n): ").strip().lower()
            if continue_choice != 'y':
                continue


# Fix for the typo in heap_sort
def heap_sort(arr):
    """Fixed heap sort implementation."""
    import heapq
    heap = arr.copy()
    heapq.heapify(heap)
    sorted_list = []
    while heap:
        sorted_list.append(heapq.heappop(heap))
    return sorted_list


if __name__ == "__main__":
    main()