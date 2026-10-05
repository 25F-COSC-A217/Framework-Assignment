from problem.pacman2 import MultiFoodPacmanProblem
from search import a_star_search
from visualization import MultiFoodPacmanVisualizer

from search_result import SearchResult

grid = [
    "%%%%%%%%%%%%%%%%%%%%",
    "%                  %",
    "% %%%%%% %%%%%%%%  %",
    "% %                %",
    "% % %%%%%%%%%%%%%% %",
    "% %                %",
    "% %%%%%%%%%%%%%%%  %",
    "%                  %",
    "%%%%%%%%%%%%%%%%%%%%"
]


food_locations = [
    (1, 10),
    (3, 17),
    (5, 5),
    (7, 15)
]



problem = MultiFoodPacmanProblem(
    grid,
    pacman_start=(1, 1),
    food_locations=food_locations
)


result = a_star_search(problem)

result.print_statistics()

visualizer = MultiFoodPacmanVisualizer(
    problem,
    result
)


visualizer.animate(
    interval=300
)

visualizer.animate_search()

