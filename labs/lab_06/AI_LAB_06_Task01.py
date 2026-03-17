"""
8-Puzzle Solver using Goal-Based Agent with A* Algorithm
Menu-based system with multiple input options and analysis features
"""

import heapq
import copy
import time
import random
from typing import List, Tuple, Optional, Dict
from collections import deque

# ====================== PUZZLE STATE CLASS ======================

class PuzzleState:
    """Represents a state in the 8-puzzle problem"""
    
    def __init__(self, board: List[List[int]], parent=None, move: str = "", depth: int = 0):
        """
        Initialize a puzzle state
        
        Args:
            board: 3x3 grid representing the puzzle
            parent: Parent state (previous state)
            move: Move made to reach this state
            depth: Depth from start state (g(n))
        """
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.blank_pos = self.find_blank()
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.state_id = str(self.board)  # Unique identifier for the state
        
    def find_blank(self) -> Tuple[int, int]:
        """Find the position of the blank (0) tile"""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return (i, j)
        return (0, 0)
    
    def manhattan_distance(self) -> int:
        """
        Calculate Manhattan distance heuristic h(n)
        Sum of distances each tile is from its goal position
        """
        distance = 0
        for i in range(3):
            for j in range(3):
                tile = self.board[i][j]
                if tile != 0:  # Skip blank tile
                    # Find goal position for this tile
                    goal_i = (tile - 1) // 3
                    goal_j = (tile - 1) % 3
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance
    
    def misplaced_tiles(self) -> int:
        """Count misplaced tiles (excluding blank)"""
        count = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0 and self.board[i][j] != self.goal_state[i][j]:
                    count += 1
        return count
    
    def euclidean_distance(self) -> float:
        """Euclidean distance heuristic (rounded)"""
        distance = 0
        for i in range(3):
            for j in range(3):
                tile = self.board[i][j]
                if tile != 0:
                    goal_i = (tile - 1) // 3
                    goal_j = (tile - 1) % 3
                    distance += ((i - goal_i) ** 2 + (j - goal_j) ** 2) ** 0.5
        return round(distance, 2)
    
    def get_f_value(self, heuristic: str = 'manhattan') -> float:
        """Calculate f(n) = g(n) + h(n) with selected heuristic"""
        if heuristic == 'manhattan':
            return self.depth + self.manhattan_distance()
        elif heuristic == 'misplaced':
            return self.depth + self.misplaced_tiles()
        elif heuristic == 'euclidean':
            return self.depth + self.euclidean_distance()
        else:
            return self.depth + self.manhattan_distance()
    
    def is_goal(self) -> bool:
        """Check if current state is goal state"""
        return self.board == self.goal_state
    
    def get_successors(self) -> List['PuzzleState']:
        """
        Generate all valid successor states by moving blank tile
        Returns list of valid next states
        """
        successors = []
        i, j = self.blank_pos
        
        # Possible moves: up, down, left, right
        moves = [
            ((i-1, j), "Up"),
            ((i+1, j), "Down"),
            ((i, j-1), "Left"),
            ((i, j+1), "Right")
        ]
        
        for (new_i, new_j), move_name in moves:
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                # Create new board by swapping blank with adjacent tile
                new_board = copy.deepcopy(self.board)
                new_board[i][j], new_board[new_i][new_j] = new_board[new_i][new_j], new_board[i][j]
                
                # Create new state
                new_state = PuzzleState(new_board, self, move_name, self.depth + 1)
                successors.append(new_state)
        
        return successors
    
    def __lt__(self, other):
        """Less than operator for priority queue"""
        return self.get_f_value() < other.get_f_value()
    
    def __eq__(self, other):
        """Equality operator for comparing states"""
        return self.board == other.board
    
    def __hash__(self):
        """Hash function for using states in sets"""
        return hash(str(self.board))
    
    def display(self):
        """Display the puzzle board with proper formatting"""
        print("+-------+-------+-------+")
        for i, row in enumerate(self.board):
            print("|", end="")
            for j, tile in enumerate(row):
                if tile == 0:
                    print("       |", end="")
                else:
                    print(f"   {tile}   |", end="")
            print()
            if i < 2:
                print("+-------+-------+-------+")
        print("+-------+-------+-------+")
    
    def display_compact(self):
        """Compact display for path visualization"""
        for row in self.board:
            line = "|"
            for tile in row:
                if tile == 0:
                    line += "   |"
                else:
                    line += f" {tile} |"
            print(line)
        print()


# ====================== GOAL-BASED AGENT CLASS ======================

class GoalBasedAgent:
    """
    Goal-based intelligent agent for solving 8-puzzle using A* algorithm
    """
    
    def __init__(self, heuristic: str = 'manhattan'):
        """
        Initialize agent
        
        Args:
            heuristic: Heuristic function to use ('manhattan', 'misplaced', 'euclidean')
        """
        self.heuristic = heuristic
        self.start_state = None
        self.goal_state = None
        self.stats = {
            'nodes_explored': 0,
            'max_queue_size': 0,
            'execution_time': 0,
            'solution_depth': 0,
            'memory_used': 0
        }
        
    def set_start_state(self, board: List[List[int]]):
        """Set the start state"""
        self.start_state = PuzzleState(board)
        self.goal_state = None
        self.reset_stats()
        
    def reset_stats(self):
        """Reset statistics"""
        self.stats = {
            'nodes_explored': 0,
            'max_queue_size': 0,
            'execution_time': 0,
            'solution_depth': 0,
            'memory_used': 0
        }
        
    def solve(self, verbose: bool = True) -> Optional[PuzzleState]:
        """
        Solve the puzzle using A* search
        
        Args:
            verbose: Whether to print progress
            
        Returns:
            Goal state if solution found, None otherwise
        """
        if not self.start_state:
            print("Error: Start state not set!")
            return None
            
        # Check if puzzle is solvable
        if not self.is_solvable(self.start_state.board):
            print("\n" + "!"*50)
            print("This puzzle configuration is NOT SOLVABLE!")
            print("!"*50)
            return None
        
        start_time = time.time()
        
        # Priority queue for open set (states to explore)
        open_set = []
        # Store (f_value, counter, state) to avoid comparing states directly
        counter = 0
        heapq.heappush(open_set, (self.start_state.get_f_value(self.heuristic), counter, self.start_state))
        counter += 1
        
        # Dictionary for quick lookup of states in open set
        open_dict = {self.start_state.state_id: self.start_state}
        
        # Set for closed set (states already explored)
        closed_set = set()
        
        # Dictionary to store best g values
        g_values = {self.start_state.state_id: 0}
        
        if verbose:
            print("\n" + "="*60)
            print(f"STARTING A* SEARCH (Heuristic: {self.heuristic})")
            print("="*60)
            print("Initial state:")
            self.start_state.display()
        
        while open_set:
            # Update max queue size
            self.stats['max_queue_size'] = max(self.stats['max_queue_size'], len(open_set))
            
            # Get state with lowest f value
            _, _, current = heapq.heappop(open_set)
            del open_dict[current.state_id]
            
            self.stats['nodes_explored'] += 1
            
            # Check if we've reached goal
            if current.is_goal():
                self.goal_state = current
                self.stats['execution_time'] = time.time() - start_time
                self.stats['solution_depth'] = current.depth
                
                if verbose:
                    print(f"\n✓ GOAL REACHED!")
                    print(f"  Nodes explored: {self.stats['nodes_explored']}")
                    print(f"  Solution depth: {current.depth}")
                    print(f"  Time taken: {self.stats['execution_time']:.3f} seconds")
                    print(f"  Max queue size: {self.stats['max_queue_size']}")
                
                return current
            
            # Add to closed set
            closed_set.add(current.state_id)
            
            # Generate successors
            for successor in current.get_successors():
                successor_key = successor.state_id
                
                # Skip if already explored
                if successor_key in closed_set:
                    continue
                
                # Calculate new g value
                new_g = current.depth + 1
                
                # If this path to successor is better than previous
                if (successor_key not in g_values or new_g < g_values[successor_key]):
                    g_values[successor_key] = new_g
                    
                    # Calculate f value
                    f_value = successor.get_f_value(self.heuristic)
                    
                    # Add to open set if not already there
                    if successor_key not in open_dict:
                        heapq.heappush(open_set, (f_value, counter, successor))
                        counter += 1
                        open_dict[successor_key] = successor
        
        self.stats['execution_time'] = time.time() - start_time
        
        if verbose:
            print("\n✗ No solution found!")
            print(f"  Nodes explored: {self.stats['nodes_explored']}")
            print(f"  Time taken: {self.stats['execution_time']:.3f} seconds")
        
        return None
    
    def get_solution_path(self) -> List[PuzzleState]:
        """
        Reconstruct solution path from start to goal
        
        Returns:
            List of states from start to goal
        """
        if not self.goal_state:
            return []
        
        path = []
        current = self.goal_state
        
        while current:
            path.append(current)
            current = current.parent
        
        return list(reversed(path))
    
    def display_solution(self):
        """Display the complete solution path"""
        if not self.goal_state:
            print("No solution to display")
            return
        
        path = self.get_solution_path()
        
        print("\n" + "="*60)
        print("SOLUTION PATH")
        print("="*60)
        
        for i, state in enumerate(path):
            if i == 0:
                print(f"\nStep {i}: START")
            else:
                print(f"\nStep {i}: Move {state.move}")
            state.display_compact()
        
        print(f"\n✓ Total moves required: {len(path) - 1}")
        print(f"✓ Solution depth: {self.goal_state.depth}")
        print(f"✓ Nodes explored: {self.stats['nodes_explored']}")
        print(f"✓ Execution time: {self.stats['execution_time']:.3f} seconds")
    
    @staticmethod
    def is_solvable(board: List[List[int]]) -> bool:
        """
        Check if puzzle configuration is solvable
        8-puzzle is solvable if inversion count is even
        """
        # Flatten the board (excluding 0)
        flat = [tile for row in board for tile in row if tile != 0]
        
        # Count inversions
        inversions = 0
        for i in range(len(flat)):
            for j in range(i + 1, len(flat)):
                if flat[i] > flat[j]:
                    inversions += 1
        
        return inversions % 2 == 0
    
    def get_stats(self) -> Dict:
        """Get search statistics"""
        return self.stats


# ====================== MENU SYSTEM ======================

class PuzzleGame:
    """Main menu system for 8-puzzle game"""
    
    def __init__(self):
        self.agent = GoalBasedAgent()
        self.current_board = None
        self.goal_board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        
    def display_main_menu(self):
        """Display main menu with proper alignment"""
        print("\n" + "+" + "="*58 + "+")
        print("|" + " " * 21 + "8-PUZZLE SOLVER" + " " * 22 + "|")
        print("+" + "="*58 + "+")
        print("|  1. Enter custom puzzle                        |")
        print("|  2. Use random puzzle                          |")
        print("|  3. Use predefined puzzles                     |")
        print("|  4. Compare heuristics                         |")
        print("|  5. Manual play mode                           |")
        print("|  6. Analyze puzzle solvability                 |")
        print("|  7. View statistics                            |")
        print("|  8. Exit                                        |")
        print("+" + "="*58 + "+")
        
    def display_heuristic_menu(self):
        """Display heuristic selection menu"""
        print("\n" + "-"*50)
        print("SELECT HEURISTIC FUNCTION:")
        print("-"*50)
        print("1. Manhattan Distance (Recommended)")
        print("2. Misplaced Tiles")
        print("3. Euclidean Distance")
        print("4. Compare all heuristics")
        print("-"*50)
        
    def display_predefined_menu(self):
        """Display predefined puzzles menu"""
        print("\n" + "-"*50)
        print("PREDEFINED PUZZLES:")
        print("-"*50)
        print("1. Easy - Almost solved")
        print("2. Medium - 5 moves away")
        print("3. Hard - 10+ moves away")
        print("4. Very Hard - Challenging")
        print("5. Unsolvable puzzle (demonstration)")
        print("-"*50)
        
    def get_puzzle_input(self) -> List[List[int]]:
        """Get puzzle input from user"""
        print("\n" + "-"*50)
        print("ENTER PUZZLE CONFIGURATION")
        print("-"*50)
        print("Enter numbers row by row (use 0 for blank space)")
        print("Example: Row 1: 1 2 3")
        print("         Row 2: 4 5 6")
        print("         Row 3: 7 8 0")
        print()
        
        board = []
        numbers_used = set()
        
        for i in range(3):
            while True:
                try:
                    row_input = input(f"Row {i+1}: ").strip().split()
                    if len(row_input) != 3:
                        print("Please enter exactly 3 numbers!")
                        continue
                    
                    row = [int(x) for x in row_input]
                    
                    # Check if numbers are valid (0-8)
                    valid = True
                    for num in row:
                        if num < 0 or num > 8:
                            print("Numbers must be between 0 and 8!")
                            valid = False
                            break
                        if num in numbers_used and num != 0:
                            print(f"Number {num} already used!")
                            valid = False
                            break
                        if num == 0 and 0 in numbers_used:
                            print("Only one blank space (0) allowed!")
                            valid = False
                            break
                    
                    if not valid:
                        continue
                    
                    # Add numbers to used set
                    for num in row:
                        numbers_used.add(num)
                    
                    board.append(row)
                    break
                    
                except ValueError:
                    print("Invalid input! Please enter integers.")
        
        return board
    
    def get_random_puzzle(self) -> List[List[int]]:
        """Generate a random solvable puzzle"""
        # Start from goal state and make random moves
        state = PuzzleState([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        
        # Number of random moves (more moves = harder puzzle)
        moves = random.randint(10, 30)
        
        for _ in range(moves):
            successors = state.get_successors()
            state = random.choice(successors)
        
        return state.board
    
    def get_predefined_puzzle(self, choice: int) -> List[List[int]]:
        """Get predefined puzzle based on choice"""
        puzzles = {
            1: [  # Easy
                [1, 2, 3],
                [4, 5, 6],
                [7, 0, 8]
            ],
            2: [  # Medium
                [1, 2, 3],
                [4, 0, 6],
                [7, 5, 8]
            ],
            3: [  # Hard
                [2, 8, 3],
                [1, 6, 4],
                [7, 0, 5]
            ],
            4: [  # Very Hard
                [8, 6, 7],
                [2, 5, 4],
                [3, 0, 1]
            ],
            5: [  # Unsolvable
                [8, 1, 2],
                [0, 4, 3],
                [7, 6, 5]
            ]
        }
        return puzzles.get(choice, puzzles[1])
    
    def compare_heuristics(self, board: List[List[int]]):
        """Compare performance of different heuristics"""
        print("\n" + "="*60)
        print("HEURISTIC COMPARISON")
        print("="*60)
        print("Puzzle configuration:")
        PuzzleState(board).display()
        
        heuristics = ['manhattan', 'misplaced', 'euclidean']
        results = []
        
        for h in heuristics:
            print(f"\nTesting {h} heuristic...")
            agent = GoalBasedAgent(heuristic=h)
            agent.set_start_state(board)
            
            # Solve without verbose output
            agent.solve(verbose=False)
            
            if agent.goal_state:
                results.append({
                    'heuristic': h,
                    'nodes': agent.stats['nodes_explored'],
                    'time': agent.stats['execution_time'],
                    'depth': agent.stats['solution_depth'],
                    'max_queue': agent.stats['max_queue_size']
                })
        
        # Display comparison table
        print("\n" + "="*60)
        print("COMPARISON RESULTS")
        print("="*60)
        print(f"{'Heuristic':<15} {'Nodes':<12} {'Time (s)':<12} {'Depth':<8} {'Max Queue'}")
        print("-"*60)
        
        for r in results:
            print(f"{r['heuristic']:<15} {r['nodes']:<12} {r['time']:.3f}{' ':<9} {r['depth']:<8} {r['max_queue']}")
        
        # Determine best heuristic
        if results:
            best = min(results, key=lambda x: x['nodes'])
            print(f"\n✓ Best heuristic by nodes explored: {best['heuristic']}")
            
            fastest = min(results, key=lambda x: x['time'])
            print(f"✓ Fastest execution: {fastest['heuristic']} ({fastest['time']:.3f}s)")
    
    def manual_play_mode(self):
        """Allow user to play the puzzle manually"""
        if not self.current_board:
            print("\nPlease set up a puzzle first!")
            return
        
        print("\n" + "="*60)
        print("MANUAL PLAY MODE")
        print("="*60)
        print("Goal state:")
        PuzzleState(self.goal_board).display()
        print("\nCurrent state:")
        
        current = PuzzleState(copy.deepcopy(self.current_board))
        moves = 0
        
        while not current.is_goal():
            current.display()
            print(f"\nMoves made: {moves}")
            print("\nAvailable moves:")
            
            # Show available moves
            successors = current.get_successors()
            move_options = {}
            for i, succ in enumerate(successors):
                move_options[i+1] = succ
                print(f"  {i+1}. Move {succ.move}")
            
            print("  0. Exit to menu")
            
            try:
                choice = int(input("\nEnter your choice: "))
                if choice == 0:
                    break
                elif choice in move_options:
                    current = move_options[choice]
                    moves += 1
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Invalid input!")
        
        if current.is_goal():
            print("\n🎉 CONGRATULATIONS! You solved the puzzle!")
            print(f"Total moves: {moves}")
    
    def analyze_solvability(self, board: List[List[int]]):
        """Analyze puzzle solvability"""
        print("\n" + "="*60)
        print("PUZZLE SOLVABILITY ANALYSIS")
        print("="*60)
        
        PuzzleState(board).display()
        
        # Flatten and count inversions
        flat = [tile for row in board for tile in row if tile != 0]
        
        inversions = 0
        for i in range(len(flat)):
            for j in range(i + 1, len(flat)):
                if flat[i] > flat[j]:
                    inversions += 1
        
        print(f"\nPuzzle configuration (flattened, ignoring 0): {flat}")
        print(f"Number of inversions: {inversions}")
        print(f"Inversion parity: {'Even' if inversions % 2 == 0 else 'Odd'}")
        print(f"Solvable: {'✓ YES' if inversions % 2 == 0 else '✗ NO'}")
        
        if inversions % 2 == 0:
            print("\nThis puzzle can be solved!")
        else:
            print("\nThis puzzle is UNSOLVABLE. Try a different configuration.")
    
    def run(self):
        """Main program loop"""
        print("\n" + "+" + "="*58 + "+")
        print("|" + " " * 18 + "WELCOME TO 8-PUZZLE SOLVER" + " " * 18 + "|")
        print("|" + " " * 12 + "Goal-Based Agent with A* Algorithm" + " " * 12 + "|")
        print("+" + "="*58 + "+")
        
        while True:
            self.display_main_menu()
            
            try:
                choice = int(input("\nEnter your choice (1-8): "))
                
                if choice == 1:
                    # Custom puzzle
                    board = self.get_puzzle_input()
                    self.current_board = board
                    
                    self.display_heuristic_menu()
                    h_choice = int(input("\nSelect heuristic (1-4): "))
                    
                    if h_choice == 1:
                        self.agent = GoalBasedAgent(heuristic='manhattan')
                    elif h_choice == 2:
                        self.agent = GoalBasedAgent(heuristic='misplaced')
                    elif h_choice == 3:
                        self.agent = GoalBasedAgent(heuristic='euclidean')
                    elif h_choice == 4:
                        self.compare_heuristics(board)
                        input("\nPress Enter to continue...")
                        continue
                    else:
                        print("Invalid choice! Using Manhattan distance.")
                        self.agent = GoalBasedAgent(heuristic='manhattan')
                    
                    self.agent.set_start_state(board)
                    result = self.agent.solve()
                    
                    if result:
                        self.agent.display_solution()
                    
                elif choice == 2:
                    # Random puzzle
                    board = self.get_random_puzzle()
                    self.current_board = board
                    print("\nGenerated random puzzle:")
                    PuzzleState(board).display()
                    
                    self.display_heuristic_menu()
                    h_choice = int(input("\nSelect heuristic (1-4): "))
                    
                    if h_choice == 1:
                        self.agent = GoalBasedAgent(heuristic='manhattan')
                    elif h_choice == 2:
                        self.agent = GoalBasedAgent(heuristic='misplaced')
                    elif h_choice == 3:
                        self.agent = GoalBasedAgent(heuristic='euclidean')
                    elif h_choice == 4:
                        self.compare_heuristics(board)
                        input("\nPress Enter to continue...")
                        continue
                    
                    self.agent.set_start_state(board)
                    result = self.agent.solve()
                    
                    if result:
                        self.agent.display_solution()
                    
                elif choice == 3:
                    # Predefined puzzles
                    self.display_predefined_menu()
                    p_choice = int(input("\nSelect puzzle (1-5): "))
                    board = self.get_predefined_puzzle(p_choice)
                    self.current_board = board
                    
                    print("\nSelected puzzle:")
                    PuzzleState(board).display()
                    
                    self.display_heuristic_menu()
                    h_choice = int(input("\nSelect heuristic (1-4): "))
                    
                    if h_choice == 1:
                        self.agent = GoalBasedAgent(heuristic='manhattan')
                    elif h_choice == 2:
                        self.agent = GoalBasedAgent(heuristic='misplaced')
                    elif h_choice == 3:
                        self.agent = GoalBasedAgent(heuristic='euclidean')
                    elif h_choice == 4:
                        self.compare_heuristics(board)
                        input("\nPress Enter to continue...")
                        continue
                    
                    self.agent.set_start_state(board)
                    result = self.agent.solve()
                    
                    if result:
                        self.agent.display_solution()
                    
                elif choice == 4:
                    # Compare heuristics
                    if not self.current_board:
                        print("\nPlease set up a puzzle first!")
                        board = self.get_random_puzzle()
                        self.current_board = board
                    
                    self.compare_heuristics(self.current_board)
                    
                elif choice == 5:
                    # Manual play mode
                    if not self.current_board:
                        print("\nPlease set up a puzzle first!")
                        board = self.get_random_puzzle()
                        self.current_board = board
                    
                    self.manual_play_mode()
                    
                elif choice == 6:
                    # Analyze solvability
                    if not self.current_board:
                        print("\nPlease set up a puzzle first!")
                        board = self.get_random_puzzle()
                        self.current_board = board
                    
                    self.analyze_solvability(self.current_board)
                    
                elif choice == 7:
                    # View statistics
                    if self.agent and self.agent.goal_state:
                        print("\n" + "="*60)
                        print("AGENT STATISTICS")
                        print("="*60)
                        print(f"Heuristic used: {self.agent.heuristic}")
                        print(f"Nodes explored: {self.agent.stats['nodes_explored']}")
                        print(f"Solution depth: {self.agent.stats['solution_depth']}")
                        print(f"Execution time: {self.agent.stats['execution_time']:.3f} seconds")
                        print(f"Max queue size: {self.agent.stats['max_queue_size']}")
                    else:
                        print("\nNo puzzle solved yet. Solve a puzzle first!")
                    
                elif choice == 8:
                    # Exit
                    print("\n+" + "="*58 + "+")
                    print("|" + " " * 20 + "Thank you for using" + " " * 20 + "|")
                    print("|" + " " * 22 + "8-Puzzle Solver!" + " " * 22 + "|")
                    print("|" + " " * 26 + "Goodbye!" + " " * 26 + "|")
                    print("+" + "="*58 + "+")
                    break
                    
                else:
                    print("\nInvalid choice! Please enter a number between 1 and 8.")
                    
            except ValueError:
                print("\nInvalid input! Please enter a number.")
            
            if choice != 8:
                input("\nPress Enter to continue...")


# ====================== ADDITIONAL UTILITIES ======================

class PuzzleAnalyzer:
    """Additional analysis tools for 8-puzzle"""
    
    @staticmethod
    def calculate_branching_factor(depth: int, nodes_explored: int) -> float:
        """Calculate effective branching factor"""
        if depth == 0:
            return 0
        # Approximate using nodes ≈ (b^(d+1) - 1)/(b - 1)
        # This is an approximation
        return round(nodes_explored ** (1/depth), 2)
    
    @staticmethod
    def analyze_puzzle_complexity(board: List[List[int]]):
        """Analyze puzzle complexity"""
        state = PuzzleState(board)
        
        print("\n" + "="*60)
        print("PUZZLE COMPLEXITY ANALYSIS")
        print("="*60)
        
        # Manhattan distance from goal
        md = state.manhattan_distance()
        print(f"Manhattan distance from goal: {md}")
        
        # Misplaced tiles
        mt = state.misplaced_tiles()
        print(f"Misplaced tiles: {mt}")
        
        # Estimate difficulty
        if md <= 5:
            difficulty = "Easy"
        elif md <= 10:
            difficulty = "Medium"
        elif md <= 15:
            difficulty = "Hard"
        else:
            difficulty = "Very Hard"
        
        print(f"Estimated difficulty: {difficulty}")
        
        # Number of possible moves from current state
        successors = state.get_successors()
        print(f"Available moves: {len(successors)}")
        print(f"Moves: {[s.move for s in successors]}")


# ====================== MAIN EXECUTION ======================

def main():
    """Main function to run the program"""
    # Create and run the game
    game = PuzzleGame()
    game.run()


if __name__ == "__main__":
    main()
