from collections import deque
import heapq
import itertools


class FIFOFrontier:

    def __init__(self):
        self.frontier = deque()

    def add(self, node):
        self.frontier.append(node)

    def remove(self):
        return self.frontier.popleft()

    def empty(self):
        return len(self.frontier) == 0


class LIFOFrontier:

    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def remove(self):
        return self.frontier.pop()

    def empty(self):
        return len(self.frontier) == 0


class PriorityFrontier:

    def __init__(self, priority_function):

        self.frontier = []
        self.priority_function = priority_function
        self.counter = itertools.count()

    def add(self, node):

        priority = self.priority_function(node)

        heapq.heappush(
            self.frontier,
            (
                priority,
                next(self.counter),
                node
            )
        )

    def remove(self):

        return heapq.heappop(
            self.frontier
        )[2]

    def empty(self):

        return len(self.frontier) == 0