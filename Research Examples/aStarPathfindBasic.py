# https://pypi.org/project/pathfinding/
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

matrix = [
  [1, 1, 1, 1, 1, 1],
  [1, 0, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1]
]

# create a grid
grid = Grid(matrix = matrix)

# create start and end node
start = grid.node(0, 0)
end = grid.node(5, 2)

# create finder with a movement style
finder = AStarFinder(diagonal_movement = DiagonalMovement.always)

# use finder to find the path
path, runs = finder.find_path(start, end, grid)

# print 
print(path)
print(runs)