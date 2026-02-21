import heapq
from collections import deque
from dataclasses import dataclass, field
from typing import TypeVar, Generic, Dict, List, Set, Optional, Tuple

T = TypeVar('T')

@dataclass(frozen=True)
class Node(Generic[T]):
    """
    An immutable generic node. 
    Frozen is strictly required so the node can be hashed and used 
    as a key in the Graph's adjacency dictionary.
    """
    id: str
    payload: T
    
    def __repr__(self) -> str:
        return f"Node({self.id})"


@dataclass(frozen=True)
class Edge(Generic[T]):
    """Represents a directional connection to another node with a cost."""
    destination: Node[T]
    weight: float = 1.0


class Graph(Generic[T]):
    """
    A generic graph implemented via an Adjacency List.
    Memory efficient for sparse networks (like city maps or state machines).
    """
    def __init__(self):
        # The core adjacency list: Maps a Node to a list of its outgoing Edges
        self._adjacency_list: Dict[Node[T], List[Edge[T]]] = {}

    def add_node(self, node: Node[T]) -> None:
        if node not in self._adjacency_list:
            self._adjacency_list[node] = []

    def add_edge(self, src: Node[T], dest: Node[T], weight: float = 1.0, bidirectional: bool = True) -> None:
        """Connects two nodes. Adds them to the graph if they don't exist yet."""
        self.add_node(src)
        self.add_node(dest)
        
        self._adjacency_list[src].append(Edge(dest, weight))
        if bidirectional:
            self._adjacency_list[dest].append(Edge(src, weight))

    def _reconstruct_path(self, parent_map: Dict[Node[T], Node[T]], current: Node[T]) -> List[Node[T]]:
        """Backtracks from the target to the start using the parent map."""
        path = [current]
        while current in parent_map:
            current = parent_map[current]
            path.append(current)
        path.reverse()
        return path

    def bfs_shortest_path(self, start: Node[T], target: Node[T]) -> Optional[List[Node[T]]]:
        """
        Breadth-First Search (BFS).
        Guarantees the shortest path in an UNWEIGHTED graph.
        Uses a double-ended queue (deque) for O(1) pop operations.
        """
        if start not in self._adjacency_list or target not in self._adjacency_list:
            return None

        queue: deque[Node[T]] = deque([start])
        visited: Set[Node[T]] = {start}
        parent_map: Dict[Node[T], Node[T]] = {}

        while queue:
            # Pop from the left (FIFO)
            current = queue.popleft()

            if current == target:
                return self._reconstruct_path(parent_map, current)

            for edge in self._adjacency_list[current]:
                if edge.destination not in visited:
                    visited.add(edge.destination)
                    parent_map[edge.destination] = current
                    queue.append(edge.destination)

        return None # Target not reachable

    def dfs_path(self, start: Node[T], target: Node[T]) -> Optional[List[Node[T]]]:
        """
        Depth-First Search (DFS).
        Explores as deep as possible before backtracking.
        Uses a Stack (LIFO). Does NOT guarantee the shortest path.
        Implemented iteratively to prevent RecursionError on deep graphs.
        """
        if start not in self._adjacency_list or target not in self._adjacency_list:
            return None

        stack: List[Node[T]] = [start]
        visited: Set[Node[T]] = set()
        parent_map: Dict[Node[T], Node[T]] = {}

        while stack:
            # Pop from the right (LIFO)
            current = stack.pop()

            if current == target:
                return self._reconstruct_path(parent_map, current)

            if current not in visited:
                visited.add(current)
                
                for edge in self._adjacency_list[current]:
                    if edge.destination not in visited:
                        parent_map[edge.destination] = current
                        stack.append(edge.destination)

        return None

    def dijkstra_shortest_path(self, start: Node[T], target: Node[T]) -> Tuple[Optional[List[Node[T]]], float]:
        """
        Dijkstra's Algorithm.
        Finds the absolute shortest path in a WEIGHTED graph.
        Uses a Min-Heap (Priority Queue) to always expand the cheapest node first.
        """
        if start not in self._adjacency_list or target not in self._adjacency_list:
            return None, float('inf')

        # distances tracks the minimum cost to reach each node
        distances: Dict[Node[T], float] = {node: float('inf') for node in self._adjacency_list}
        distances[start] = 0.0
        
        parent_map: Dict[Node[T], Node[T]] = {}
        
        # Priority Queue: stores tuples of (accumulated_cost, tie_breaker_id, Node)
        # The tie_breaker ensures heapq doesn't try to compare Node objects if costs are equal
        pq: List[Tuple[float, int, Node[T]]] = [(0.0, 0, start)]
        tie_breaker = 0

        while pq:
            current_cost, _, current_node = heapq.heappop(pq)

            if current_node == target:
                return self._reconstruct_path(parent_map, current_node), current_cost

            # Optimization: Skip if we already found a cheaper path to this node 
            # while this particular tuple was waiting in the queue
            if current_cost > distances[current_node]:
                continue

            for edge in self._adjacency_list[current_node]:
                new_cost = current_cost + edge.weight

                if new_cost < distances[edge.destination]:
                    distances[edge.destination] = new_cost
                    parent_map[edge.destination] = current_node
                    
                    tie_breaker += 1
                    heapq.heappush(pq, (new_cost, tie_breaker, edge.destination))

        return None, float('inf')


if __name__ == "__main__":
    
    print("--- Building Navigation Graph ---")
    # Instantiating a graph where the payload is just a simple string description
    nav_graph = Graph[str]()
    
    node_A = Node("A", "Warehouse Entrance")
    node_B = Node("B", "Sorting Area")
    node_C = Node("C", "Packaging")
    node_D = Node("D", "Loading Dock")
    node_E = Node("E", "Maintenance")

    # Adding connections with different travel times (weights)
    nav_graph.add_edge(node_A, node_B, weight=2.0)
    nav_graph.add_edge(node_A, node_E, weight=8.0)
    nav_graph.add_edge(node_B, node_C, weight=1.5)
    nav_graph.add_edge(node_C, node_D, weight=3.0)
    nav_graph.add_edge(node_B, node_D, weight=6.0) # Direct but slow path
    nav_graph.add_edge(node_E, node_D, weight=1.0)

    print("[SYSTEM] Graph constructed successfully.")

    print("\n--- 1. Testing BFS (Unweighted Shortest Path) ---")
    # BFS ignores weights. It will find the path with the fewest "hops"
    bfs_path = nav_graph.bfs_shortest_path(node_A, node_D)
    print(f"Path (Fewest Hops): {bfs_path}")

    print("\n--- 2. Testing DFS (Deep Exploration) ---")
    # DFS goes as deep as possible. Output can vary based on adjacency list order.
    dfs_path = nav_graph.dfs_path(node_A, node_D)
    print(f"Path (Exploration): {dfs_path}")

    print("\n--- 3. Testing Dijkstra (Weighted Shortest Path) ---")
    # Dijkstra respects the weights. 
    # Even though A -> B -> D is 2 hops, it costs 8.0.
    # A -> B -> C -> D is 3 hops, but costs only 6.5.
    dijkstra_path, total_cost = nav_graph.dijkstra_shortest_path(node_A, node_D)
    print(f"Path (Lowest Cost): {dijkstra_path}")
    print(f"Total Travel Time: {total_cost:.1f} units")