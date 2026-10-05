"""Result container compatible with the supplied search and visualization."""
from dataclasses import dataclass, field


@dataclass
class SearchResult:
    node: object = None
    nodes_expanded: int = 0
    nodes_generated: int = 0
    max_frontier_size: int = 0
    explored_count: int = 0
    execution_time: float = 0.0
    explored_order: list = field(default_factory=list)

    def print_statistics(self):
        print("Solution found:", self.node is not None)
        if self.node is not None:
            print("Path cost:", self.node.path_cost)
            print("Number of actions:", len(self.node.solution()))
        print("Nodes expanded:", self.nodes_expanded)
        print("Nodes generated:", self.nodes_generated)
        print("Maximum frontier size:", self.max_frontier_size)
        print("Explored count:", self.explored_count)
        print(f"Execution time: {self.execution_time:.6f} seconds")
