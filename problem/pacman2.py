from problem import Problem


class MultiFoodPacmanProblem(Problem):

    def __init__(
        self,
        grid,
        pacman_start,
        food_locations
    ):

        initial_state = (
            pacman_start,
            frozenset(food_locations)
        )

        super().__init__(
            initial_state,
            None
        )

        self.grid = grid

        self.rows = len(grid)
        self.cols = len(grid[0])

    def actions(self, state):

        position, food = state

        row, col = position

        directions = {
            "NORTH": (-1, 0),
            "SOUTH": (1, 0),
            "WEST": (0, -1),
            "EAST": (0, 1)
        }

        actions = []

        for action, (dr, dc) in directions.items():

            new_row = row + dr
            new_col = col + dc

            if self.valid_position(
                new_row,
                new_col
            ):
                actions.append(action)

        return actions

    def result(self, state, action):

        position, food = state

        row, col = position

        directions = {
            "NORTH": (-1, 0),
            "SOUTH": (1, 0),
            "WEST": (0, -1),
            "EAST": (0, 1)
        }

        dr, dc = directions[action]

        new_position = (
            row + dr,
            col + dc
        )

        new_food = food

        if new_position in food:
            new_food = food - {
                new_position
            }

        return (
            new_position,
            frozenset(new_food)
        )

    def goal_test(self, state):

        position, food = state

        return len(food) == 0

    def valid_position(self, row, col):

        if row < 0 or row >= self.rows:
            return False

        if col < 0 or col >= self.cols:
            return False

        return self.grid[row][col] != "%"

    def step_cost(
        self,
        state,
        action,
        next_state
    ):

        return 1

    def heuristic1(self, state):

        position, food = state

        if not food:
            return 0

        return min(
            abs(position[0] - f[0]) +
            abs(position[1] - f[1])
            for f in food
        )

    def heuristic(self, state):

        position, food = state

        if not food:
            return 0

        total = 0
        current = position

        remaining = set(food)

        while remaining:

            closest = min(
                remaining,
                key=lambda f:
                    abs(current[0] - f[0]) +
                    abs(current[1] - f[1])
            )

            distance = (
                abs(current[0] - closest[0]) +
                abs(current[1] - closest[1])
            )

            total += distance

            current = closest

            remaining.remove(closest)

        return total

    