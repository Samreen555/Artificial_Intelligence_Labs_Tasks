from collections import deque

# Graph representation from the lab (based on the graph shown)
graph = {
    'A': ['B', 'C'],
    'B': ['C', 'D'],
    'C': ['D'],
    'D': ['C'],
    'E': ['F'],
    'F': ['C']
}

graph_alternative = {
    '0': ['1', '2'],
    '1': ['2'],
    '2': ['0', '3'],
    '3': ['3']
}

def bfs(graph, start_node):
    """
    Breadth First Search implementation
    Args:
        graph: Dictionary representing the graph
        start_node: Starting node for BFS traversal
    Returns:
        List of nodes in BFS order
    """
    # Create a set to store visited nodes
    visited = set()
    
    # Create a queue for BFS (using deque for efficient pop from left)
    queue = deque([start_node])
    
    # Mark the start node as visited
    visited.add(start_node)
    
    # List to store the traversal order
    bfs_order = []
    
    print(f"Starting BFS from node {start_node}")
    print("-" * 40)
    
    while queue:
        # Dequeue a vertex from queue
        current_node = queue.popleft()
        bfs_order.append(current_node)
        print(f"Visited: {current_node}")
        
        # Get all adjacent vertices of the dequeued vertex
        # If the current node doesn't exist in graph, treat it as having no neighbors
        neighbors = graph.get(current_node, [])
        
        for neighbor in neighbors:
            if neighbor not in visited:
                # Mark as visited and enqueue
                visited.add(neighbor)
                queue.append(neighbor)
                print(f"  Added {neighbor} to queue")
    
    return bfs_order


def dfs(graph, start_node, visited=None, dfs_order=None):
    """
    Depth First Search implementation (recursive)
    Args:
        graph: Dictionary representing the graph
        start_node: Starting node for DFS traversal
        visited: Set of visited nodes (used in recursion)
        dfs_order: List to store the traversal order
    Returns:
        List of nodes in DFS order
    """
    if visited is None:
        visited = set()
        dfs_order = []
        print(f"Starting DFS from node {start_node}")
        print("-" * 40)
    
    # Mark the current node as visited and print it
    visited.add(start_node)
    dfs_order.append(start_node)
    print(f"Visited: {start_node}")
    
    # Get all adjacent vertices of the current node
    neighbors = graph.get(start_node, [])
    
    for neighbor in neighbors:
        if neighbor not in visited:
            # Recursively visit the neighbor
            dfs(graph, neighbor, visited, dfs_order)
    
    return dfs_order


def dfs_iterative(graph, start_node):
    """
    Depth First Search implementation (iterative using stack)
    Args:
        graph: Dictionary representing the graph
        start_node: Starting node for DFS traversal
    Returns:
        List of nodes in DFS order
    """
    # Create a set to store visited nodes
    visited = set()
    
    # Create a stack for DFS
    stack = [start_node]
    
    # List to store the traversal order
    dfs_order = []
    
    print(f"Starting DFS (iterative) from node {start_node}")
    print("-" * 40)
    
    while stack:
        # Pop a vertex from stack
        current_node = stack.pop()
        
        if current_node not in visited:
            # Mark as visited and add to result
            visited.add(current_node)
            dfs_order.append(current_node)
            print(f"Visited: {current_node}")
            
            # Get all adjacent vertices
            # Add them to stack in reverse order to simulate recursion
            neighbors = graph.get(current_node, [])
            
            # Add neighbors to stack in reverse order
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    stack.append(neighbor)
                    print(f"  Added {neighbor} to stack")
    
    return dfs_order


def find_all_paths_bfs(graph, start, end):
    """
    Find all paths from start to end using BFS approach
    Args:
        graph: Dictionary representing the graph
        start: Starting node
        end: Ending node
    Returns:
        List of all paths from start to end
    """
    # Queue will store paths
    queue = deque([[start]])
    all_paths = []
    
    print(f"Finding all paths from {start} to {end}")
    print("-" * 40)
    
    while queue:
        path = queue.popleft()
        current_node = path[-1]
        
        # If we reached the end, add the path to results
        if current_node == end:
            all_paths.append(path)
            print(f"Found path: {' -> '.join(path)}")
            continue
        
        # Explore neighbors
        neighbors = graph.get(current_node, [])
        for neighbor in neighbors:
            if neighbor not in path:  # Avoid cycles
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
    
    return all_paths


def find_path_dfs(graph, start, end, path=None):
    """
    Find a path from start to end using DFS (backtracking)
    This is similar to the example in your lab
    """
    if path is None:
        path = []
    
    path = path + [start]
    
    if start == end:
        return path
    
    if start not in graph:
        return None
    
    for node in graph[start]:
        if node not in path:
            new_path = find_path_dfs(graph, node, end, path)
            if new_path:
                return new_path
    
    return None


def print_graph_info(graph):
    """Print information about the graph"""
    print("Graph Representation:")
    print("-" * 20)
    for node, neighbors in graph.items():
        print(f"Node {node} -> {neighbors}")
    
    # Count nodes and edges
    nodes = list(graph.keys())
    edges = sum(len(neighbors) for neighbors in graph.values())
    print(f"\nTotal Nodes: {len(nodes)}")
    print(f"Total Edges: {edges}")
    print(f"Nodes: {nodes}")
    print()


# Test the implementations
if __name__ == "__main__":
    # Print graph information
    print_graph_info(graph)
    
    # Test BFS
    print("\n" + "="*50)
    print("BFS TRAVERSAL")
    print("="*50)
    bfs_result = bfs(graph, 'A')
    print(f"\nBFS traversal order: {' -> '.join(bfs_result)}")
    
    # Test DFS (recursive)
    print("\n" + "="*50)
    print("DFS TRAVERSAL (RECURSIVE)")
    print("="*50)
    dfs_result = dfs(graph, 'A')
    print(f"\nDFS traversal order: {' -> '.join(dfs_result)}")
    
    # Test DFS (iterative)
    print("\n" + "="*50)
    print("DFS TRAVERSAL (ITERATIVE)")
    print("="*50)
    dfs_iter_result = dfs_iterative(graph, 'A')
    print(f"\nDFS traversal order: {' -> '.join(dfs_iter_result)}")
    
    # Test finding paths
    print("\n" + "="*50)
    print("FINDING PATHS")
    print("="*50)
    
    # Find a single path using DFS backtracking (like in the lab example)
    path = find_path_dfs(graph, 'A', 'D')
    print(f"\nPath from A to D (DFS backtracking): {' -> '.join(path) if path else 'No path found'}")
    
    # Find all paths using BFS
    all_paths = find_all_paths_bfs(graph, 'A', 'D')
    print(f"\nAll paths from A to D:")
    for i, path in enumerate(all_paths, 1):
        print(f"  Path {i}: {' -> '.join(path)}")
    
    # Test with different start nodes
    print("\n" + "="*50)
    print("TRAVERSALS FROM DIFFERENT START NODES")
    print("="*50)
    
    for start in ['C', 'E', 'F']:
        print(f"\nBFS from {start}: {' -> '.join(bfs(graph, start))}")
        print(f"DFS from {start}: {' -> '.join(dfs(graph, start))}")
        print()
