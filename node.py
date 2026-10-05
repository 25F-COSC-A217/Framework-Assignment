class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0 if parent is None else parent.depth + 1

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        cost = self.path_cost + problem.step_cost(self.state, action, next_state)
        return Node(next_state, self, action, cost)

    def path(self):
        nodes = []
        node = self
        while node is not None:
            nodes.append(node)
            node = node.parent
        return nodes[::-1]

    def solution(self):
        return [node.action for node in self.path()[1:]]
