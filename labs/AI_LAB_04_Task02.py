from collections import deque
import time

class GraphAlgorithmLab:
    def __init__(self):
        self.graph = {}
        self.default_graph = {
            'A': ['B', 'C'],
            'B': ['C', 'D'],
            'C': ['D'],
            'D': ['C'],
            'E': ['F'],
            'F': ['C']
        }
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*60)
        print("GRAPH ALGORITHMS LAB - BFS & DFS IMPLEMENTATION")
        print("="*60)
        print("1. Use Default Graph")
        print("2. Create Custom Graph")
        print("3. Add Node to Existing Graph")
        print("4. Add Edge to Existing Graph")
        print("5. Display Current Graph")
        print("6. Run BFS Traversal")
        print("7. Run DFS Traversal (Recursive)")
        print("8. Run DFS Traversal (Iterative)")
        print("9. Find Path Between Nodes")
        print("10. Find All Paths Between Nodes")
        print("11. Compare BFS and DFS")
        print("12. Graph Statistics")
        print("13. Reset Graph")
        print("14. Exit")
        print("="*60)
    
    def create_custom_graph(self):
        """Create a custom graph from user input"""
        print("\n--- CREATE CUSTOM GRAPH ---")
        self.graph = {}
        
        while True:
            print("\nOptions:")
            print("1. Add a node")
            print("2. Add an edge")
            print("3. Finish creating graph")
            
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == '1':
                node = input("Enter node name: ").strip()
                if node:
                    if node not in self.graph:
                        self.graph[node] = []
                        print(f"Node '{node}' added successfully!")
                    else:
                        print(f"Node '{node}' already exists!")
                else:
                    print("Invalid node name!")
            
            elif choice == '2':
                if not self.graph:
                    print("Please add nodes first!")
                    continue
                
                print(f"Current nodes: {list(self.graph.keys())}")
                source = input("Enter source node: ").strip()
                destination = input("Enter destination node: ").strip()
                
                if source in self.graph and destination in self.graph:
                    if destination not in self.graph[source]:
                        self.graph[source].append(destination)
                        print(f"Edge from '{source}' to '{destination}' added!")
                    else:
                        print("This edge already exists!")
                else:
                    print("One or both nodes don't exist!")
            
            elif choice == '3':
                print("Custom graph created successfully!")
                self.display_graph()
                break
            else:
                print("Invalid choice!")
    
    def add_node(self):
        """Add a new node to the graph"""
        print("\n--- ADD NODE ---")
        node = input("Enter node name to add: ").strip()
        
        if node:
            if node not in self.graph:
                self.graph[node] = []
                print(f"Node '{node}' added successfully!")
            else:
                print(f"Node '{node}' already exists!")
        else:
            print("Invalid node name!")
    
    def add_edge(self):
        """Add a new edge to the graph"""
        print("\n--- ADD EDGE ---")
        
        if not self.graph:
            print("Graph is empty! Please add nodes first.")
            return
        
        self.display_graph()
        
        source = input("Enter source node: ").strip()
        destination = input("Enter destination node: ").strip()
        
        if source in self.graph and destination in self.graph:
            if destination not in self.graph[source]:
                self.graph[source].append(destination)
                print(f"Edge from '{source}' to '{destination}' added successfully!")
            else:
                print("This edge already exists!")
        else:
            print("One or both nodes don't exist!")
    
    def display_graph(self):
        """Display the current graph structure"""
        print("\n--- CURRENT GRAPH ---")
        if not self.graph:
            print("Graph is empty!")
            return
        
        print("Adjacency List Representation:")
        print("-" * 30)
        for node, neighbors in sorted(self.graph.items()):
            if neighbors:
                print(f"  {node} -> {', '.join(neighbors)}")
            else:
                print(f"  {node} -> (no outgoing edges)")
        
        # Visual representation
        print("\nGraph Visualization:")
        print("-" * 30)
        all_nodes = sorted(self.graph.keys())
        if len(all_nodes) <= 10:  # Only for smaller graphs
            for i, node in enumerate(all_nodes):
                print(f"  [{node}]", end="")
                if i < len(all_nodes) - 1:
                    print(" -- ", end="")
            print()
            
            # Show connections
            for node in all_nodes:
                if self.graph[node]:
                    targets = [n for n in self.graph[node] if n in all_nodes]
                    if targets:
                        print(f"  {node} connects to: {', '.join(targets)}")
    
    def get_graph_statistics(self):
        """Calculate and display graph statistics"""
        print("\n--- GRAPH STATISTICS ---")
        
        if not self.graph:
            print("Graph is empty!")
            return
        
        nodes = list(self.graph.keys())
        edges = sum(len(neighbors) for neighbors in self.graph.values())
        
        print(f"Total Nodes: {len(nodes)}")
        print(f"Total Edges: {edges}")
        print(f"Nodes: {', '.join(sorted(nodes))}")
        
        # Calculate degree for each node
        print("\nNode Degrees:")
        print("-" * 20)
        for node in sorted(nodes):
            out_degree = len(self.graph[node])
            in_degree = sum(1 for n in nodes if node in self.graph[n])
            print(f"  Node {node}: Out-degree = {out_degree}, In-degree = {in_degree}")
        
        # Check if graph is connected
        if nodes:
            reachable = self.bfs_traversal(nodes[0], quiet=True)
            if len(set(reachable)) == len(nodes):
                print("\n Graph is connected (all nodes reachable from first node)")
            else:
                print("\n Graph is not fully connected")
    
    def bfs_traversal(self, start_node, quiet=False):
        """
        Breadth First Search implementation
        Args:
            graph: Dictionary representing the graph
            start_node: Starting node for BFS traversal
            quiet: If True, suppress output (for internal use)
        Returns:
            List of nodes in BFS order
        """
        if start_node not in self.graph:
            if not quiet:
                print(f"Error: Start node '{start_node}' not found in graph!")
            return []
        
        # Create a set to store visited nodes
        visited = set()
        
        # Create a queue for BFS
        queue = deque([start_node])
        
        # Mark the start node as visited
        visited.add(start_node)
        
        # List to store the traversal order
        bfs_order = []
        
        if not quiet:
            print(f"\nStarting BFS from node {start_node}")
            print("-" * 40)
            print(f"Queue: [{start_node}]")
        
        step = 1
        while queue:
            # Dequeue a vertex from queue
            current_node = queue.popleft()
            bfs_order.append(current_node)
            
            if not quiet:
                print(f"\nStep {step}: Dequeue {current_node}")
            
            # Get all adjacent vertices
            neighbors = self.graph.get(current_node, [])
            
            if not quiet:
                print(f"  Neighbors of {current_node}: {neighbors if neighbors else 'None'}")
            
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    if not quiet:
                        print(f"  → Discovered {neighbor}, added to queue")
            
            if not quiet:
                print(f"  Queue now: {list(queue)}")
                print(f"  Visited: {sorted(visited)}")
            
            step += 1
        
        if not quiet:
            print(f"\n BFS traversal complete!")
            print(f"Traversal order: {' → '.join(bfs_order)}")
        
        return bfs_order
    
    def dfs_recursive(self, start_node, visited=None, dfs_order=None, quiet=False, depth=0):
        """
        Depth First Search implementation (recursive)
        """
        if start_node not in self.graph:
            if not quiet:
                print(f"Error: Start node '{start_node}' not found in graph!")
            return []
        
        if visited is None:
            visited = set()
            dfs_order = []
            if not quiet:
                print(f"\nStarting DFS (Recursive) from node {start_node}")
                print("-" * 40)
        
        # Mark the current node as visited
        visited.add(start_node)
        dfs_order.append(start_node)
        
        if not quiet:
            indent = "  " * depth
            print(f"{indent}→ Visiting {start_node}")
        
        # Get all adjacent vertices
        neighbors = self.graph.get(start_node, [])
        
        for neighbor in neighbors:
            if neighbor not in visited:
                if not quiet:
                    print(f"{indent}  Exploring neighbor {neighbor}")
                self.dfs_recursive(neighbor, visited, dfs_order, quiet, depth + 1)
            elif not quiet:
                print(f"{indent}  {neighbor} already visited (skipping)")
        
        if depth == 0 and not quiet:
            print(f"\n DFS traversal complete!")
            print(f"Traversal order: {' → '.join(dfs_order)}")
        
        return dfs_order
    
    def dfs_iterative(self, start_node, quiet=False):
        """
        Depth First Search implementation (iterative using stack)
        """
        if start_node not in self.graph:
            if not quiet:
                print(f"Error: Start node '{start_node}' not found in graph!")
            return []
        
        # Create a set to store visited nodes
        visited = set()
        
        # Create a stack for DFS
        stack = [start_node]
        
        # List to store the traversal order
        dfs_order = []
        
        if not quiet:
            print(f"\nStarting DFS (Iterative) from node {start_node}")
            print("-" * 40)
            print(f"Stack: [{start_node}]")
        
        step = 1
        while stack:
            # Pop a vertex from stack
            current_node = stack.pop()
            
            if not quiet:
                print(f"\nStep {step}: Pop {current_node} from stack")
            
            if current_node not in visited:
                # Mark as visited and add to result
                visited.add(current_node)
                dfs_order.append(current_node)
                
                if not quiet:
                    print(f"  Visiting {current_node}")
                
                # Get all adjacent vertices
                neighbors = self.graph.get(current_node, [])
                
                if not quiet:
                    print(f"  Neighbors: {neighbors if neighbors else 'None'}")
                
                # Add neighbors to stack in reverse order
                for neighbor in reversed(neighbors):
                    if neighbor not in visited:
                        stack.append(neighbor)
                        if not quiet:
                            print(f"  → Pushed {neighbor} to stack")
            
            if not quiet:
                print(f"  Stack now: {stack}")
                print(f"  Visited: {sorted(visited)}")
            
            step += 1
        
        if not quiet:
            print(f"\n DFS traversal complete!")
            print(f"Traversal order: {' → '.join(dfs_order)}")
        
        return dfs_order
    
    def find_path(self, start, end, path=None):
        """
        Find a path from start to end using DFS backtracking
        """
        if path is None:
            path = []
            print(f"\nFinding path from {start} to {end}")
            print("-" * 40)
        
        path = path + [start]
        
        if start == end:
            print(f"✓ Found path: {' → '.join(path)}")
            return path
        
        if start not in self.graph:
            return None
        
        print(f"  At {start}, exploring: {self.graph[start]}")
        
        for node in self.graph[start]:
            if node not in path:
                print(f"    Trying {start} → {node}")
                new_path = self.find_path(node, end, path)
                if new_path:
                    return new_path
        
        if len(path) == 1:
            print(f"✗ No path found from {start} to {end}")
        return None
    
    def find_all_paths_bfs(self, start, end):
        """
        Find all paths from start to end using BFS
        """
        if start not in self.graph or end not in self.graph:
            print("Start or end node not in graph!")
            return []
        
        # Queue will store paths
        queue = deque([[start]])
        all_paths = []
        
        print(f"\nFinding ALL paths from {start} to {end}")
        print("-" * 40)
        
        step = 1
        while queue:
            path = queue.popleft()
            current_node = path[-1]
            
            print(f"\nStep {step}: Exploring path {' → '.join(path)}")
            
            # If we reached the end, add the path to results
            if current_node == end:
                all_paths.append(path)
                print(f"  ✓ Found complete path: {' → '.join(path)}")
                continue
            
            # Explore neighbors
            neighbors = self.graph.get(current_node, [])
            print(f"  From {current_node}, can go to: {neighbors}")
            
            for neighbor in neighbors:
                if neighbor not in path:  # Avoid cycles
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
                    print(f"  → Added new path: {' → '.join(new_path)}")
            
            step += 1
        
        if all_paths:
            print(f"\n Found {len(all_paths)} path(s) from {start} to {end}:")
            for i, path in enumerate(all_paths, 1):
                print(f"  Path {i}: {' → '.join(path)}")
        else:
            print(f"\n✗ No paths found from {start} to {end}")
        
        return all_paths
    
    def compare_algorithms(self):
        """Compare BFS and DFS traversals"""
        print("\n--- COMPARING BFS AND DFS ---")
        
        if not self.graph:
            print("Graph is empty! Please create or load a graph first.")
            return
        
        start_node = input("Enter start node for comparison: ").strip()
        
        if start_node not in self.graph:
            print(f"Node '{start_node}' not found in graph!")
            return
        
        print("\n" + "="*60)
        print("BFS vs DFS COMPARISON")
        print("="*60)
        
        # Time BFS
        print("\n BREADTH-FIRST SEARCH (BFS)")
        print("-" * 30)
        start_time = time.time()
        bfs_result = self.bfs_traversal(start_node, quiet=False)
        bfs_time = time.time() - start_time
        print(f"  Time taken: {bfs_time:.6f} seconds")
        
        # Time DFS Recursive
        print("\n DEPTH-FIRST SEARCH (DFS) - Recursive")
        print("-" * 30)
        start_time = time.time()
        dfs_rec_result = self.dfs_recursive(start_node, quiet=False)
        dfs_rec_time = time.time() - start_time
        print(f"  Time taken: {dfs_rec_time:.6f} seconds")
        
        # Time DFS Iterative
        print("\n DEPTH-FIRST SEARCH (DFS) - Iterative")
        print("-" * 30)
        start_time = time.time()
        dfs_iter_result = self.dfs_iterative(start_node, quiet=False)
        dfs_iter_time = time.time() - start_time
        print(f"  Time taken: {dfs_iter_time:.6f} seconds")
        
        # Comparison Summary
        print("\n" + "="*60)
        print("COMPARISON SUMMARY")
        print("="*60)
        print(f"\nBFS Traversal Order:      {' → '.join(bfs_result)}")
        print(f"DFS Recursive Order:      {' → '.join(dfs_rec_result)}")
        print(f"DFS Iterative Order:      {' → '.join(dfs_iter_result)}")
        
        print("\n KEY DIFFERENCES:")
        print("• BFS explores level by level (uses Queue)")
        print("• DFS explores depth first (uses Stack/Recursion)")
        print("• BFS is better for shortest paths")
        print("• DFS uses less memory on average")
        print("• BFS finds optimal solutions in unweighted graphs")
        print("• DFS is better for topological sorting and cycle detection")
    
    def reset_graph(self):
        """Reset the graph"""
        self.graph = {}
        print("\n Graph has been reset!")
    
    def run(self):
        """Main program loop"""
        print("\n WELCOME TO GRAPH ALGORITHMS LAB (BFS & DFS)")
        print("This program demonstrates Breadth-First Search and Depth-First Search algorithms")
        
        while True:
            self.display_menu()
            
            choice = input("\nEnter your choice (1-14): ").strip()
            
            if choice == '1':
                self.graph = self.default_graph.copy()
                print("\n Default graph loaded!")
                self.display_graph()
            
            elif choice == '2':
                self.create_custom_graph()
            
            elif choice == '3':
                self.add_node()
            
            elif choice == '4':
                self.add_edge()
            
            elif choice == '5':
                self.display_graph()
            
            elif choice == '6':
                if not self.graph:
                    print("Graph is empty! Please create or load a graph first.")
                    continue
                
                self.display_graph()
                start = input("Enter start node for BFS: ").strip()
                self.bfs_traversal(start)
            
            elif choice == '7':
                if not self.graph:
                    print("Graph is empty! Please create or load a graph first.")
                    continue
                
                self.display_graph()
                start = input("Enter start node for DFS (recursive): ").strip()
                self.dfs_recursive(start)
            
            elif choice == '8':
                if not self.graph:
                    print("Graph is empty! Please create or load a graph first.")
                    continue
                
                self.display_graph()
                start = input("Enter start node for DFS (iterative): ").strip()
                self.dfs_iterative(start)
            
            elif choice == '9':
                if not self.graph:
                    print("Graph is empty! Please create or load a graph first.")
                    continue
                
                self.display_graph()
                start = input("Enter start node: ").strip()
                end = input("Enter end node: ").strip()
                
                if start in self.graph and end in self.graph:
                    path = self.find_path(start, end)
                    if path:
                        print(f"\n Path found: {' → '.join(path)}")
                    else:
                        print(f"\n No path found from {start} to {end}")
                else:
                    print("Start or end node not found in graph!")
            
            elif choice == '10':
                if not self.graph:
                    print("Graph is empty! Please create or load a graph first.")
                    continue
                
                self.display_graph()
                start = input("Enter start node: ").strip()
                end = input("Enter end node: ").strip()
                self.find_all_paths_bfs(start, end)
            
            elif choice == '11':
                self.compare_algorithms()
            
            elif choice == '12':
                self.get_graph_statistics()
            
            elif choice == '13':
                self.reset_graph()
            
            elif choice == '14':
                print("\nThank you for using the Graph Algorithms Lab!")
                print("Goodbye!")
                break
            
            else:
                print("\nInvalid choice! Please enter a number between 1 and 14.")
            
            input("\nPress Enter to continue...")


# Additional standalone functions for simple usage
def simple_bfs(graph, start):
    """Simple BFS implementation for quick use"""
    visited = set()
    queue = deque([start])
    visited.add(start)
    
    while queue:
        vertex = queue.popleft()
        print(vertex, end=" ")
        
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)


def simple_dfs(graph, start, visited=None):
    """Simple DFS implementation for quick use"""
    if visited is None:
        visited = set()
    
    visited.add(start)
    print(start, end=" ")
    
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            simple_dfs(graph, neighbor, visited)


# Example usage with predefined graphs
def run_examples():
    """Run some predefined examples"""
    print("\n" + "="*60)
    print("RUNNING PREDEFINED EXAMPLES")
    print("="*60)
    
    # Example 1: Simple graph
    graph1 = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }
    
    print("\nExample 1: Simple Tree-like Graph")
    print("Graph: A->B,C; B->D,E; C->F; E->F")
    print("\nBFS from A: ", end="")
    simple_bfs(graph1, 'A')
    print("\nDFS from A: ", end="")
    simple_dfs(graph1, 'A')
    
    # Example 2: Graph with cycle
    graph2 = {
        '0': ['1', '2'],
        '1': ['2'],
        '2': ['0', '3'],
        '3': ['3']
    }
    
    print("\n\n Example 2: Graph with Cycle")
    print("Graph: 0->1,2; 1->2; 2->0,3; 3->3")
    print("\nBFS from 2: ", end="")
    simple_bfs(graph2, '2')
    print("\nDFS from 2: ", end="")
    simple_dfs(graph2, '2')
    print()


if __name__ == "__main__":
    # Run the interactive lab
    lab = GraphAlgorithmLab()
    lab.run()
    
   # run_examples()