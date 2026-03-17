import heapq
from collections import deque

class Graph:
    def __init__(self):
        # (1) Represent the graph as adjacency list
        # Format: {node: [(neighbor, weight), ...]}
        self.graph = {
            'S': [('B_top', 4), ('B_bottom', 3), ('E', 2)],
            'B_top': [('C', 2), ('G', 5)],
            'B_bottom': [('C', 1), ('F', 4)],
            'C': [('G', 3)],
            'E': [('F', 3)],
            'F': [('G', 2)],
            'G': []
        }
        
        # For unweighted traversal (DFS/BFS), we'll use the same structure but ignore weights
        self.unweighted_graph = {
            node: [neighbor for neighbor, _ in edges] 
            for node, edges in self.graph.items()
        }
        
        # Heuristic function for A* (estimated straight-line distance to G)
        # Based on approximate positions if we imagine the graph layout
        # These are admissible (never overestimate) and consistent
        self.heuristic = {
            'S': 6,      # S is far from G
            'B_top': 4,  # Top B is moderately far
            'B_bottom': 3,  # Bottom B is closer
            'C': 2,      # C is close to G
            'E': 4,      # E is moderate
            'F': 1,      # F is very close to G
            'G': 0       # Goal has heuristic 0
        }
        
        # Justification for heuristic:
        # These values represent estimated minimum remaining cost to reach G
        # They are admissible because actual minimum costs:
        # S->G: min(4+2+3=9, 4+5=9, 3+1+3=7, 3+4+2=9, 2+3+2=7) = 7, heuristic=6 ✓
        # B_top->G: min(2+3=5, 5=5) = 5, heuristic=4 ✓
        # B_bottom->G: min(1+3=4, 4+2=6) = 4, heuristic=3 ✓
        # C->G: 3, heuristic=2 ✓
        # E->G: 3+2=5, heuristic=4 ✓
        # F->G: 2, heuristic=1 ✓
        # All heuristics are less than or equal to actual minimum cost
    
    def display_graph_structure(self):
        """Display the graph structure in text format"""
        print("\n" + "="*50)
        print("GRAPH STRUCTURE (Directed Weighted Graph)")
        print("="*50)
        print("\nAdjacency List with Weights:")
        for node, edges in self.graph.items():
            if edges:
                edges_str = ", ".join([f"{neighbor}({weight})" for neighbor, weight in edges])
                print(f"  {node} -> {edges_str}")
            else:
                print(f"  {node} -> (no outgoing edges)")
        
        print("\n" + "="*50)
        print("HEURISTIC VALUES (h) for A*")
        print("="*50)
        print("These are estimated costs from each node to goal G")
        print("Justification: Admissible (never overestimate actual cost)")
        for node, h_value in sorted(self.heuristic.items()):
            print(f"  h({node}) = {h_value}")
        
        # Calculate and show actual minimum costs for verification
        print("\n" + "="*50)
        print("VERIFICATION OF ADMISSIBLE HEURISTIC")
        print("="*50)
        actual_min_costs = self.calculate_actual_min_costs('G')
        for node in sorted(self.heuristic.keys()):
            if node != 'G':
                actual = actual_min_costs.get(node, float('inf'))
                heuristic = self.heuristic[node]
                status = "✓" if heuristic <= actual else "✗ (Not admissible!)"
                print(f"  {node}: heuristic={heuristic}, actual min cost={actual} {status}")
    
    def calculate_actual_min_costs(self, goal):
        """Calculate actual minimum costs from each node to goal using Dijkstra-like approach"""
        # Simple Dijkstra from each node to goal (for verification only)
        costs = {}
        for start in self.graph.keys():
            if start == goal:
                costs[start] = 0
                continue
                
            # Initialize distances
            dist = {node: float('inf') for node in self.graph.keys()}
            dist[start] = 0
            pq = [(0, start)]
            visited = set()
            
            while pq:
                current_dist, current = heapq.heappop(pq)
                if current in visited:
                    continue
                visited.add(current)
                
                if current == goal:
                    break
                
                for neighbor, weight in self.graph.get(current, []):
                    new_dist = current_dist + weight
                    if new_dist < dist[neighbor]:
                        dist[neighbor] = new_dist
                        heapq.heappush(pq, (new_dist, neighbor))
            
            costs[start] = dist[goal] if dist[goal] != float('inf') else None
        
        return costs
    
    def dfs(self, start, goal):
        """
        Depth-First Search implementation
        Uses stack data structure (LIFO)
        """
        print("\n" + "="*60)
        print("DFS (Depth-First Search) IMPLEMENTATION")
        print("="*60)
        print("Data Structure: Stack (LIFO)")
        print("Treating edges as unweighted")
        print("-" * 40)
        
        # Stack stores (node, path, visited_set for this path)
        stack = [(start, [start], {start})]
        expanded_nodes = 0
        nodes_explored_order = []
        
        while stack:
            current_node, path, path_visited = stack.pop()
            nodes_explored_order.append(current_node)
            expanded_nodes += 1
            
            print(f"\nStep {expanded_nodes}: Expanding {current_node}")
            print(f"  Path so far: {' -> '.join(path)}")
            
            if current_node == goal:
                print(f"\n GOAL FOUND!")
                print(f"  Final Path: {' -> '.join(path)}")
                print(f"  Number of expanded nodes: {expanded_nodes}")
                print(f"  Nodes explored in order: {' -> '.join(nodes_explored_order)}")
                return path, expanded_nodes
            
            # Get neighbors
            neighbors = self.unweighted_graph.get(current_node, [])
            print(f"  Neighbors: {neighbors}")
            
            # Add unvisited neighbors to stack
            added_count = 0
            for neighbor in reversed(neighbors):  # reversed for typical DFS order
                if neighbor not in path_visited:
                    new_path = path + [neighbor]
                    new_visited = path_visited | {neighbor}
                    stack.append((neighbor, new_path, new_visited))
                    added_count += 1
                    print(f"  Added {neighbor} to stack")
            
            if added_count == 0:
                print("  No unvisited neighbors - backtracking")
        
        print(f"\n No path found from {start} to {goal}")
        return None, expanded_nodes
    
    def bfs(self, start, goal):
        """
        Breadth-First Search implementation
        Uses queue data structure (FIFO)
        """
        print("\n" + "="*60)
        print("BFS (Breadth-First Search) IMPLEMENTATION")
        print("="*60)
        print("Data Structure: Queue (FIFO)")
        print("Treating edges as unweighted")
        print("-" * 40)
        
        # Queue stores (node, path)
        queue = deque([(start, [start])])
        visited = set([start])
        expanded_nodes = 0
        nodes_explored_order = []
        
        while queue:
            current_node, path = queue.popleft()
            nodes_explored_order.append(current_node)
            expanded_nodes += 1
            
            print(f"\nStep {expanded_nodes}: Expanding {current_node}")
            print(f"  Path so far: {' -> '.join(path)}")
            
            if current_node == goal:
                print(f"\n GOAL FOUND!")
                print(f"  Final Path: {' -> '.join(path)}")
                print(f"  Number of expanded nodes: {expanded_nodes}")
                print(f"  Nodes explored in order: {' -> '.join(nodes_explored_order)}")
                return path, expanded_nodes
            
            # Get neighbors
            neighbors = self.unweighted_graph.get(current_node, [])
            print(f"  Neighbors: {neighbors}")
            
            # Add unvisited neighbors to queue
            added_count = 0
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
                    added_count += 1
                    print(f"  Added {neighbor} to queue")
            
            if added_count == 0:
                print("  No unvisited neighbors")
        
        print(f"\n No path found from {start} to {goal}")
        return None, expanded_nodes
    
    def a_star(self, start, goal):
        """
        A* Search implementation
        Uses priority queue (min-heap) based on f(n) = g(n) + h(n)
        """
        print("\n" + "="*60)
        print("A* (A-Star) IMPLEMENTATION")
        print("="*60)
        print("Data Structure: Priority Queue (Min-Heap)")
        print("f(n) = g(n) + h(n) where:")
        print("  g(n) = actual cost from start to n")
        print("  h(n) = heuristic estimate from n to goal")
        print("-" * 40)
        
        # Priority queue stores (f_score, unique_id, node, path, g_score)
        # Using unique_id to break ties and prevent comparison issues
        counter = 0
        
        # Initialize with start node
        g_score = {start: 0}
        f_score = {start: self.heuristic[start]}
        
        # Priority queue entries: (f_score, counter, node, path, g_score)
        open_set = [(f_score[start], counter, start, [start], 0)]
        # Set to keep track of nodes in open set (for quick lookup)
        open_set_nodes = {start}
        # Dictionary for best g_scores
        best_g = {start: 0}
        # Set for closed/expanded nodes
        closed_set = set()
        expanded_nodes = 0
        nodes_explored_order = []
        
        print(f"\nInitial state:")
        print(f"  Start node: {start}, Goal node: {goal}")
        print(f"  h({start}) = {self.heuristic[start]}")
        print(f"  Initial f({start}) = 0 + {self.heuristic[start]} = {f_score[start]}")
        
        while open_set:
            # Pop node with smallest f_score
            current_f, _, current_node, path, current_g = heapq.heappop(open_set)
            open_set_nodes.remove(current_node)
            nodes_explored_order.append(current_node)
            expanded_nodes += 1
            
            print(f"\n{'='*40}")
            print(f"Step {expanded_nodes}: Expanding {current_node}")
            print(f"  Path: {' -> '.join(path)}")
            print(f"  g({current_node}) = {current_g}")
            print(f"  h({current_node}) = {self.heuristic[current_node]}")
            print(f"  f({current_node}) = {current_g} + {self.heuristic[current_node]} = {current_f}")
            
            if current_node == goal:
                print(f"\n{''*20}")
                print(f"GOAL FOUND!")
                print(f"  Final Path: {' -> '.join(path)}")
                print(f"  Total Path Cost: {current_g}")
                print(f"  Number of expanded nodes: {expanded_nodes}")
                print(f"  Nodes explored in order: {' -> '.join(nodes_explored_order)}")
                return path, expanded_nodes, current_g
            
            closed_set.add(current_node)
            
            # Explore neighbors
            neighbors = self.graph.get(current_node, [])
            print(f"  Neighbors: {[(n, w) for n, w in neighbors]}")
            
            if not neighbors:
                print("  No outgoing edges from this node")
            
            for neighbor, weight in neighbors:
                if neighbor in closed_set:
                    print(f"  ⏭️  {neighbor} already expanded (in closed set)")
                    continue
                
                # Calculate tentative g_score for neighbor
                tentative_g = current_g + weight
                
                print(f"  Checking {neighbor}:")
                print(f"    Edge weight: {weight}")
                print(f"    Tentative g({neighbor}) = {current_g} + {weight} = {tentative_g}")
                
                # If neighbor not in open set or we found a better path
                if neighbor not in best_g or tentative_g < best_g[neighbor]:
                    # Update scores
                    best_g[neighbor] = tentative_g
                    f = tentative_g + self.heuristic[neighbor]
                    
                    # Add to open set
                    counter += 1
                    heapq.heappush(open_set, (f, counter, neighbor, path + [neighbor], tentative_g))
                    open_set_nodes.add(neighbor)
                    
                    print(f"     Added to open set:")
                    print(f"       g({neighbor}) = {tentative_g}")
                    print(f"       h({neighbor}) = {self.heuristic[neighbor]}")
                    print(f"       f({neighbor}) = {tentative_g} + {self.heuristic[neighbor]} = {f}")
                else:
                    print(f"     Not better than current best g({neighbor}) = {best_g[neighbor]}")
            
            # Show current open set
            if open_set:
                print(f"\n  Current Open Set (f values):")
                sorted_open = sorted([(f, n) for f, _, n, _, _ in open_set])
                for f_val, node in sorted_open[:3]:  # Show top 3
                    print(f"    {node}: f={f_val}")
                if len(sorted_open) > 3:
                    print(f"    ... and {len(sorted_open)-3} more")
        
        print(f"\n No path found from {start} to {goal}")
        return None, expanded_nodes, None

def clear_screen():
    """Clear the console screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Main menu-driven program"""
    graph = Graph()
    
    while True:
        clear_screen()
        print("\n" + "="*60)
        print("            GRAPH ALGORITHMS IMPLEMENTATION")
        print("="*60)
        print("Nodes: S, B_top, B_bottom, C, E, F, G")
        print("Goal: Find path from S to G")
        print("-" * 60)
        print("1. Run DFS (Depth-First Search)")
        print("2. Run BFS (Breadth-First Search)")
        print("3. Run A* (A-Star Search)")
        print("4. Run All Algorithms (Compare)")
        print("5. Show Graph Structure & Heuristics")
        print("6. Exit")
        print("="*60)
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            clear_screen()
            path, expanded = graph.dfs('S', 'G')
            input("\n\nPress Enter to continue...")
        
        elif choice == '2':
            clear_screen()
            path, expanded = graph.bfs('S', 'G')
            input("\n\nPress Enter to continue...")
        
        elif choice == '3':
            clear_screen()
            path, expanded, cost = graph.a_star('S', 'G')
            input("\n\nPress Enter to continue...")
        
        elif choice == '4':
            clear_screen()
            print("\n" + "#"*70)
            print("RUNNING ALL ALGORITHMS - COMPARISON")
            print("#"*70)
            
            dfs_path, dfs_exp = graph.dfs('S', 'G')
            print("\n" + "-"*50)
            bfs_path, bfs_exp = graph.bfs('S', 'G')
            print("\n" + "-"*50)
            astar_path, astar_exp, astar_cost = graph.a_star('S', 'G')
            
            print("\n" + "="*70)
            print("SUMMARY COMPARISON")
            print("="*70)
            print(f"{'Algorithm':<15} {'Path Found':<30} {'Expanded Nodes':<15} {'Cost':<10}")
            print("-"*70)
            print(f"{'DFS':<15} {str(' -> '.join(dfs_path) if dfs_path else 'No path'):<30} {dfs_exp:<15} {'N/A':<10}")
            print(f"{'BFS':<15} {str(' -> '.join(bfs_path) if bfs_path else 'No path'):<30} {bfs_exp:<15} {'N/A':<10}")
            print(f"{'A*':<15} {str(' -> '.join(astar_path) if astar_path else 'No path'):<30} {astar_exp:<15} {astar_cost if astar_cost else 'N/A':<10}")
            
            input("\n\nPress Enter to continue...")
        
        elif choice == '5':
            clear_screen()
            graph.display_graph_structure()
            input("\n\nPress Enter to continue...")
        
        elif choice == '6':
            print("\nExiting program. Goodbye!")
            break
        
        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()