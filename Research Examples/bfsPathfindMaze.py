from queue import Queue

# define maze as a list:
# "#" are walls, "S" is start node, "X" is goal node
maze = [
  ["#", "#", "#", "#", "#","#", "#", "#", "S","#"],
  ["#", " ", "#", " ", "#"," ", " ", "#", " ","#"],
  ["#", " ", " ", " ", "#"," ", "#", "#", " ","#"],
  ["#", " ", "#", "#", "#"," ", " ", " ", " ","#"],
  ["#", " ", "#", " ", " "," ", " ", "#", " ","#"],
  ["#", " ", "#", " ", " ","#", " ", "#", "#","#"],
  ["#", " ", " ", " ", "#","#", " ", " ", " ","#"],
  ["#", " ", "#", " ", " ","#", " ", "#", " ","#"],
  ["#", " ", "#", " ", " ","#", " ", "#", " ","#"],
  ["#", "X", "#", "#", "#","#", "#", "#", "#","#"]
]

# displays the maze in terminal
def show_maze(maze):
  maze_row = ""

  for row in maze:
    for cell in row:
      maze_row += " " + cell
    print(maze_row)
    maze_row = ""

# finds start and end nodes
def find_node(maze, node):
  maze_size = len(maze)
  row_size = len(maze[0])

  for row in range(maze_size):
    for col in range(row_size):
      if maze[row][col] == node:
        return (row, col)
      
# creates bfs graph of maze
def graph(maze):
  graph = {}
  maze_size = len(maze)
  row_size = len(maze[0])

  for row in range(maze_size):
    for col in range(row_size):
      if maze[row][col] != "#":
        adj_nodes = []

        # checks each direction for empty cells
        if row + 1 < maze_size and maze[row + 1][col] != "#": # South
          adj_nodes.append((row + 1, col))
        if row - 1 >= 0 and maze[row - 1][col] != "#": # North
          adj_nodes.append((row - 1, col))
        if col + 1 < row_size and maze[row][col + 1] != "#": # East
          adj_nodes.append((row, col + 1))
        if col - 1 >= 0 and maze[row][col - 1] != "#": # West
          adj_nodes.append((row, col - 1))

        graph[(row, col)] = adj_nodes

  return graph

# finds path between start and end node
def path(maze, maze_graph, start_node, end_node):
  visited = []
  start_path = [start]
  q = Queue()
  q.put(start_path)

  while not q.empty():
    path = q.get()
    neighbours = maze_graph[path[-1]]

    for n in neighbours:
      if n == end:
        for coordinate in path:
          row, col = coordinate
          maze[row][col] = "X"
        return maze
      if n not in visited:
        visited.append(n)
        new_path = path + [n]
        q.put(new_path)

# finds start and end nodes
start = find_node(maze, "S")
end = find_node(maze, "X")

# create graph of maze
maze_graph = graph(maze)

# finds path from start to end
solved_maze = path(maze, maze_graph, start, end)

# displays maze with shortest path
show_maze(maze)
