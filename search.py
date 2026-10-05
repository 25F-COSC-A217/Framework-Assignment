import time 

from node import Node
from frontier import (
    FIFOFrontier,
    LIFOFrontier,
    PriorityFrontier
)

from search_result import SearchResult

def graph_search(problem, frontier):

    start_time = time.perf_counter()

    root = Node(problem.initial_state)

    frontier.add(root)

    explored = set()

    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 1

    explored_order = []

    while not frontier.empty():

        node = frontier.remove()

        if problem.goal_test(node.state):
            execution_time = (
                time.perf_counter() - start_time
            )
            return SearchResult(
                node=node,
                nodes_expanded=nodes_expanded,
                nodes_generated=nodes_generated,
                max_frontier_size=max_frontier_size,
                explored_count=len(explored),
                execution_time=execution_time,
                explored_order=explored_order
            )
            #return node

        if node.state in explored:
            continue

        explored.add(node.state)
        

        explored_order.append(node.state)

        nodes_expanded += 1

        for action in problem.actions(node.state):

            child = node.child_node(
                problem,
                action
            )
            nodes_generated += 1
            if child.state not in explored:
                frontier.add(child)

        max_frontier_size = max(
            max_frontier_size,
            len(frontier.frontier)
        )

    execution_time = (
        time.perf_counter() - start_time
    )
    return SearchResult(
        node=None,
        nodes_expanded=nodes_expanded,
        nodes_generated=nodes_generated,
        max_frontier_size=max_frontier_size,
        explored_count=len(explored),
        execution_time=execution_time,
        explored_order=explored_order
    )   


def breadth_first_search(problem):

    return graph_search(
        problem,
        FIFOFrontier()
    )


def depth_first_search(problem):

    return graph_search(
        problem,
        LIFOFrontier()
    )


def best_first_graph_search(
    problem,
    evaluation_function
):
    start_time = time.perf_counter()
    root = Node(problem.initial_state)

    frontier = PriorityFrontier(
        evaluation_function
    )

    frontier.add(root)

    best_cost = {
        root.state: 0
    }

    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 1
    explored_order = []

    while not frontier.empty():

        node = frontier.remove()

        # Ignore an outdated node
        if node.path_cost > best_cost.get(
            node.state,
            float("inf")
        ):
            continue

        # Goal test
        if problem.goal_test(node.state):
            execution_time = (
                time.perf_counter() - start_time
            )

            return SearchResult(
                node=node,
                nodes_expanded=nodes_expanded,
                nodes_generated=nodes_generated,
                max_frontier_size=max_frontier_size,
                explored_count=len(best_cost),
                execution_time=execution_time,
                explored_order=explored_order
            )
        
        explored_order.append(node.state)
        nodes_expanded += 1
        for action in problem.actions(node.state):

            child = node.child_node(
                problem,
                action
            )

            nodes_generated += 1

            if child.path_cost < best_cost.get(
                child.state,
                float("inf")
            ):

                best_cost[child.state] = (
                    child.path_cost
                )

                frontier.add(child)
        max_frontier_size = max(
            max_frontier_size,
            len(frontier.frontier)
        )

    execution_time = (
        time.perf_counter() - start_time
    )

    return SearchResult(
        node=None,
        nodes_expanded=nodes_expanded,
        nodes_generated=nodes_generated,
        max_frontier_size=max_frontier_size,
        explored_count=len(best_cost),
        execution_time=execution_time,
                explored_order=explored_order
    )
    


def uniform_cost_search(problem):

    return best_first_graph_search(
        problem,
        lambda node: node.path_cost
    )


def greedy_best_first_search(problem):

    return best_first_graph_search(
        problem,
        lambda node:
            problem.heuristic(node.state)
    )


def a_star_search(problem):

    return best_first_graph_search(
        problem,
        lambda node:
            node.path_cost +
            problem.heuristic(node.state)
    )