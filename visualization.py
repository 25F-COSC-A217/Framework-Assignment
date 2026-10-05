import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class GridVisualizer:
    """
    Generic visualizer for grid-based search problems.

    The visualizer expects:
        problem.maze or problem.grid
        problem.initial_state
        problem.goal_state

    and uses the Node path returned by the search algorithm.
    """

    def __init__(self, problem, result):

        self.problem = problem
        self.result = result

        self.path = []

        if result.node is not None:
            self.path = [
                node.state
                for node in result.node.path()
            ]

        self.fig = None
        self.ax = None

    def show(self):
        """
        Display the final solution.
        """

        self._create_figure()

        self._draw_grid()

        self._draw_start_goal()

        self._draw_path()

        plt.show()

    def animate(self, interval=300):

        if not self.path:
            print("No solution to animate.")
            return

        self._create_figure()

        self._draw_grid()

        self._draw_start_goal()

        self.position_marker, = self.ax.plot(
            [],
            [],
            marker="o",
            markersize=12,
            linestyle=""
        )

        self.path_line, = self.ax.plot(
            [],
            [],
            linewidth=3
        )

        self.animation = FuncAnimation(
            self.fig,
            self._update,
            frames=len(self.path),
            interval=interval,
            repeat=False
        )

        plt.show()

    def animate_search(self, interval=100):

        if not self.result.explored_order:
            print("No exploration information available.")
            return

        self._create_figure()

        self._draw_grid()
        self._draw_start_goal()

        self.explored_marker, = self.ax.plot(
            [],
            [],
            marker="s",
            markersize=8,
            linestyle=""
        )

        self.solution_line, = self.ax.plot(
            [],
            [],
            linewidth=3
        )

        self.animation = FuncAnimation(
            self.fig,
            self._update_search,
            frames=len(
                self.result.explored_order
            ),
            interval=interval,
            repeat=False
        )

        plt.show()

    def _update_search(self, frame):

        states = self.result.explored_order[
            :frame + 1
        ]

        coordinates = [
            self._state_to_xy(state)
            for state in states
        ]

        x = [p[0] for p in coordinates]
        y = [p[1] for p in coordinates]

        self.explored_marker.set_data(
            x,
            y
        )

        return (
            self.explored_marker,
            self.solution_line
        )

    def _create_figure(self):

        self.fig, self.ax = plt.subplots()

        self.ax.set_aspect("equal")

    def _draw_grid(self):

        grid = getattr(
            self.problem,
            "grid",
            None
        )

        if grid is None:

            grid = getattr(
                self.problem,
                "maze",
                None
            )

        if grid is None:
            return

        rows = len(grid)
        cols = len(grid[0])

        for row in range(rows):

            for col in range(cols):

                cell = grid[row][col]

                # Walls / obstacles
                if cell in ("#", "%", "X"):

                    self.ax.add_patch(
                        plt.Rectangle(
                            (col, rows - row - 1),
                            1,
                            1
                        )
                    )

                # Empty cell
                else:

                    self.ax.add_patch(
                        plt.Rectangle(
                            (col, rows - row - 1),
                            1,
                            1,
                            fill=False
                        )
                    )

        self.ax.set_xlim(0, cols)
        self.ax.set_ylim(0, rows)

        self.ax.set_xticks([])
        self.ax.set_yticks([])

    def _draw_path(self):

        if not self.path:
            return

        coordinates = [
            self._state_to_xy(state)
            for state in self.path
        ]

        x = [p[0] for p in coordinates]
        y = [p[1] for p in coordinates]

        self.ax.plot(
            x,
            y,
            linewidth=3
        )

        self.ax.plot(
            x[0],
            y[0],
            marker="o",
            markersize=12
        )

        self.ax.plot(
            x[-1],
            y[-1],
            marker="*",
            markersize=15
        )

    def _update(self, frame):

        state = self.path[frame]

        x, y = self._state_to_xy(state)

        self.position_marker.set_data(
            [x],
            [y]
        )

        coordinates = [
            self._state_to_xy(
                state
            )
            for state in self.path[:frame + 1]
        ]

        x_values = [
            p[0]
            for p in coordinates
        ]

        y_values = [
            p[1]
            for p in coordinates
        ]

        self.path_line.set_data(
            x_values,
            y_values
        )

        return (
            self.position_marker,
            self.path_line
        )

    def _state_to_xy(self, state):

        row, col = state

        grid = getattr(
            self.problem,
            "grid",
            None
        )

        if grid is None:

            grid = getattr(
                self.problem,
                "maze",
                None
            )

        rows = len(grid)

        x = col + 0.5
        y = rows - row - 0.5

        return x, y

    def _draw_start_goal(self):

        start = self.problem.initial_state
        goal = self.problem.goal_state

        start_x, start_y = self._state_to_xy(start)

        self.ax.plot(
            start_x,
            start_y,
            marker="o",
            markersize=12
        )

        if goal is not None:

            goal_x, goal_y = self._state_to_xy(goal)

            self.ax.plot(
                goal_x,
                goal_y,
                marker="*",
                markersize=15
            )

class PacmanVisualizer(GridVisualizer):

    def _draw_pacman(self, state):

        x, y = self._state_to_xy(state)

        self.ax.plot(
            x,
            y,
            marker="o",
            markersize=18
        )

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class MultiFoodPacmanVisualizer(GridVisualizer):

    def _state_to_xy(self, state):
        return super()._state_to_xy(state[0])

    '''
    def __init__(self, problem, result):

        self.problem = problem
        self.result = result

        # Extract the solution path
        self.path = []

        if result.node is not None:

            self.path = [
                node.state
                for node in result.node.path()
            ]

        self.fig = None
        self.ax = None
    '''
    def animate(self, interval=300):

        if not self.path:

            print("No solution found.")
            return

        self.fig, self.ax = plt.subplots()

        self.ax.set_aspect("equal")

        self._draw_grid()

        # Pacman
        self.pacman, = self.ax.plot(
            [],
            [],
            marker="o",
            markersize=18,
            linestyle=""
        )

        # Path
        self.path_line, = self.ax.plot(
            [],
            [],
            linewidth=2
        )

        # Food markers
        self.food_markers = []

        initial_position, initial_food = (
            self.path[0]
        )

        for food in initial_food:

            marker = self.draw_food(food)

            self.food_markers.append(
                (food, marker)
            )

        self.animation = FuncAnimation(
            self.fig,
            self.update,
            frames=len(self.path),
            interval=interval,
            repeat=False
        )

        plt.show()
    '''
    def draw_board(self):

        grid = self.problem.grid

        rows = len(grid)
        cols = len(grid[0])

        for row in range(rows):

            for col in range(cols):

                x = col
                y = rows - row - 1

                if grid[row][col] == "%":

                    self.ax.add_patch(
                        plt.Rectangle(
                            (x, y),
                            1,
                            1
                        )
                    )

                else:

                    self.ax.add_patch(
                        plt.Rectangle(
                            (x, y),
                            1,
                            1,
                            fill=False
                        )
                    )

        self.ax.set_xlim(0, cols)
        self.ax.set_ylim(0, rows)

        self.ax.set_xticks([])
        self.ax.set_yticks([])
    '''
    def draw_food(self, food):

        row, col = food

        rows = len(self.problem.grid)

        x = col + 0.5
        y = rows - row - 0.5

        marker, = self.ax.plot(
            x,
            y,
            marker="*",
            markersize=14,
            linestyle=""
        )

        return marker

    def update(self, frame):

        position, remaining_food = (
            self.path[frame]
        )

        row, col = position

        rows = len(self.problem.grid)

        x = col + 0.5
        y = rows - row - 0.5

        # Move Pacman

        self.pacman.set_data(
            [x],
            [y]
        )

        # Draw path so far

        path = self.path[:frame + 1]

        x_values = [
            col + 0.5
            for position, food in path
            for row, col in [position]
        ]

        y_values = [
            rows - row - 0.5
            for position, food in path
            for row, col in [position]
        ]

        self.path_line.set_data(
            x_values,
            y_values
        )

        # Remove eaten food

        for food, marker in self.food_markers:

            if food not in remaining_food:

                marker.set_visible(False)

        return (
            self.pacman,
            self.path_line
        )

class DeliveryRobotVisualizer(GridVisualizer):
    def __init__(self, problem, result):

        super().__init__(problem, result)
        self.positions = {

            # Robot area
            "robot": (0, 0),

            # Labs
            "lab_A": (-1, 1),
            "lab_B": (1, 1),
            "lab_D": (-1, 2),
            "lab_C": (1, 2),

            # Offices
            "r101": (-3, -1),
            "r103": (-2, -1),
            "r105": (-1, -1),
            "r107": (0, -1),
            "r109": (1, -1),
            "r111": (2, -1),

            "r113": (3, 1),
            "r115": (3, 2),
            "r117": (3, 3),

            "r119": (2, 4),
            "r121": (1, 4),
            "r123": (0, 4),
            "r125": (-1, 4),
            "r127": (-2, 4),
            "r129": (-3, 4),
            "r131": (-4, 4),

            "main_office": (-5, -1),

            "stairs": (-4, -1)
        }

        self.robot_plot = None
        self.item_plots = {}

        self.states = self.path

    def draw_map(self):

        self.ax.clear()

        # -----------------------------------------
        # Draw connections
        # -----------------------------------------

        for location, neighbors in self.problem.connections.items():

            if location not in self.positions:
                continue

            x1, y1 = self.positions[location]

            for destination in neighbors:

                if destination not in self.positions:
                    continue

                x2, y2 = self.positions[destination]

                self.ax.plot(
                    [x1, x2],
                    [y1, y2],
                    linewidth=2
                )

       # -----------------------------------------
        # Draw rooms
        # -----------------------------------------

        for location, (x, y) in self.positions.items():

            self.ax.text(
                x,
                y,
                location,
                ha="center",
                va="center",
                fontsize=10
            )

        # -----------------------------------------
        # Mark hazardous locations
        # -----------------------------------------

        for location in self.problem.hazardous_locations:

            if location not in self.positions:
                continue

            x, y = self.positions[location]

            self.ax.text(
                x,
                y - 0.25,
                "HAZARD",
                ha="center",
                fontsize=8
            )

        self.ax.set_aspect("equal")

        self.ax.set_xlim(-5, 4)
        self.ax.set_ylim(-2, 5) 

        self.ax.set_xticks([])
        self.ax.set_yticks([])

        self.ax.set_title(
            "Delivery Robot"
        )

    # =================================================
    # GET POSITION
    # =================================================

    def get_position(self, location):

        if location not in self.positions:

            raise ValueError(
                f"No visualization position "
                f"defined for '{location}'"
            )

        return self.positions[location]

    # =================================================
    # ANIMATE SOLUTION
    # =================================================

    def animate_solution(self, interval=800):

        if not self.states:

            print("No solution found.")

            return

        self.fig, self.ax = plt.subplots(
            figsize=(10, 7)
        )

        self.draw_map()

        # -----------------------------------------
        # Robot
        # -----------------------------------------

        self.robot_plot, = self.ax.plot(
            [],
            [],
            marker="o",
            markersize=18,
            linestyle=""
        )
        # -----------------------------------------
        # Items
        # -----------------------------------------

        for item in self.problem.items:

            self.item_plots[item], = self.ax.plot(
                [],
                [],
                marker="s",
                markersize=10,
                linestyle=""
            )

        # -----------------------------------------
        # Animation
        # -----------------------------------------

        self.animation = FuncAnimation(
            self.fig,
            self.update,
            frames=len(self.states),
            interval=interval,
            repeat=False
        )

        plt.show()

    # =================================================
    # UPDATE ANIMATION
    # =================================================

    def update(self, frame):

        state = self.states[frame]

        robot_location = state[0]
        keys = state[2]
        carrying = state[1]
        item_locations = dict(state[3])

        # -----------------------------------------
        # Robot position
        # -----------------------------------------

        x, y = self.get_position(
            robot_location
        )

        self.robot_plot.set_data(
            [x],
            [y]
        )

        # -----------------------------------------
        # Items
        # -----------------------------------------

        for item in self.problem.items:
            location = item_locations[item]

            # -------------------------------------
            # Item is being carried
            # -------------------------------------

            if item in carrying:

                item_x = x
                item_y = y + 0.25

            # -------------------------------------
            # Item is somewhere in building
            # -------------------------------------

            else:

                item_x, item_y = self.get_position(
                    location
                )

            self.item_plots[item].set_data(
                [item_x],
                [item_y]
            )

        # -----------------------------------------
        # Display state information
        # -----------------------------------------

        self.ax.set_title(
            f"Delivery Robot\n"
            f"Step: {frame}/{len(self.states)-1}\n"
            f"Location: {robot_location}\n"
            f"Carrying: {sorted(carrying)}\n"
            f"Keys: {sorted(keys)}"
        )

        return (
            [self.robot_plot]
            + list(self.item_plots.values())
        )

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class CoinFuelVisualizer:

    def __init__(self, problem, result):

        self.problem = problem
        self.result = result

        # ------------------------------------------------
        # Extract solution nodes
        # ------------------------------------------------

        self.nodes = []

        if result.node is not None:

            self.nodes = result.node.path()

        self.states = [
            node.state
            for node in self.nodes
        ]

        self.actions = [
            node.action
            for node in self.nodes
        ]

        self.fig = None
        self.ax = None

        self.agent_plot = None
        self.coin_plots = {}

        self.animation = None

    # ====================================================
    # DRAW THE GRID
    # ====================================================

    def draw_grid(self):

        width = self.problem.width
        height = self.problem.height

        # Draw grid lines

        for x in range(1, width + 1):

            self.ax.plot(
                [x - 0.5, x - 0.5],
                [0.5, height + 0.5],
                linewidth=0.5
            )

        for y in range(1, height + 1):

            self.ax.plot(
                [0.5, width + 0.5],
                [y - 0.5, y - 0.5],
                linewidth=0.5
            )

        # ------------------------------------------------
        # Draw walls
        # ------------------------------------------------

        for x, y in self.problem.walls:

            self.ax.add_patch(
                plt.Rectangle(
                    (x - 0.5, y - 0.5),
                    1,
                    1
                )
            )

        # ------------------------------------------------
        # Draw fuel station
        # ------------------------------------------------

        fx, fy = self.problem.fuel_station

        self.ax.text(
            fx,
            fy,
            "F",
            ha="center",
            va="center",
            fontsize=18
        )

        self.ax.text(
            fx,
            fy - 0.35,
            "Fuel",
            ha="center",
            va="top",
            fontsize=8
        )

        # ------------------------------------------------
        # Draw goal
        # ------------------------------------------------

        gx, gy = self.problem.goal_position

        self.ax.text(
            gx,
            gy,
            "G",
            ha="center",
            va="center",
            fontsize=16
        )

        # ------------------------------------------------
        # Draw coins
        # ------------------------------------------------

        for coin_number, (x, y) in self.problem.coins.items():

            self.coin_plots[coin_number], = self.ax.plot(
                [x],
                [y],
                marker="o",
                markersize=14,
                linestyle=""
            )

            self.ax.text(
                x,
                y,
                str(coin_number),
                ha="center",
                va="center",
                fontsize=8
            )

        # ------------------------------------------------
        # Agent
        # ------------------------------------------------

        self.agent_plot, = self.ax.plot(
            [],
            [],
            marker="o",
            markersize=16,
            linestyle=""
        )

        # ------------------------------------------------
        # Axes
        # ------------------------------------------------

        self.ax.set_xlim(
            0.5,
            width + 0.5
        )

        self.ax.set_ylim(
            0.5,
            height + 0.5
        )

        self.ax.set_aspect("equal")

        self.ax.set_xticks(
            range(1, width + 1)
        )

        self.ax.set_yticks(
            range(1, height + 1)
        )

        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")

    # ====================================================
    # UPDATE FRAME
    # ====================================================

    def update(self, frame):

        state = self.states[frame]

        x, y, fuel, c1, c2, c3, c4 = state

        collected = [
            c1,
            c2,
            c3,
            c4
        ]

        # ------------------------------------------------
        # Move agent
        # ------------------------------------------------

        self.agent_plot.set_data(
            [x],
            [y]
        )

        # ------------------------------------------------
        # Show/hide coins
        # ------------------------------------------------

        for coin_number in range(1, 5):

            if collected[coin_number - 1]:

                self.coin_plots[
                    coin_number
                ].set_visible(False)

            else:

                self.coin_plots[
                    coin_number
                ].set_visible(True)

        # ------------------------------------------------
        # Current action
        # ------------------------------------------------

        if frame < len(self.actions):

            action = self.actions[frame]

        else:

            action = None

        # ------------------------------------------------
        # Count collected coins
        # ------------------------------------------------

        number_collected = sum(
            collected
        )

        # ------------------------------------------------
        # Title
        # ------------------------------------------------

        self.ax.set_title(
            "Example 3.3 — Coin Collection Game\n"
            f"Step: {frame}/{len(self.states) - 1}    "
            f"Position: ({x},{y})    "
            f"Fuel: {fuel}\n"
            f"Coins collected: "
            f"{number_collected}/4    "
            f"Action: {action}"
        )

        return (
            [self.agent_plot]
            +
            list(self.coin_plots.values())
        )

    # ====================================================
    # ANIMATE SOLUTION
    # ====================================================

    def animate_solution(
        self,
        interval=700
    ):

        if not self.states:

            print("No solution found.")
            return

        self.fig, self.ax = plt.subplots(
            figsize=(9, 8)
        )

        self.draw_grid()

        # Initial update
        self.update(0)

        # Create animation
        self.animation = FuncAnimation(
            self.fig,
            self.update,
            frames=len(self.states),
            interval=interval,
            repeat=False
        )

        plt.show()