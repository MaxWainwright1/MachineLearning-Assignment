from pyamaze import maze, agent, textLabel
from queue import PriorityQueue


# Heuristic function: Manhattan distance between two cells
def heuristic(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)

# A* algorithm for finding shortest path in the maze
def a_star_search(maze_obj):
    start = (maze_obj.rows, maze_obj.cols)  # Start from bottom-right corner
    goal = (1, 1)  # Goal is at top-left corner
    
    # Initialize g_score and f_score dictionaries with infinity for all cells
    g_score = {cell: float('inf') for cell in maze_obj.grid}
    g_score[start] = 0  # Distance from start to start is 0
    f_score = {cell: float('inf') for cell in maze_obj.grid}
    f_score[start] = heuristic(start, goal)  # Estimate distance to goal from start

    # Priority queue to store cells to be explored, starting with the start cell
    open_set = PriorityQueue()
    open_set.put((f_score[start], heuristic(start, goal), start))

    # Dictionary to store the most efficient path to each cell
    came_from = {}
    
    # Start exploring cells in the maze
    while not open_set.empty():
        current_cell = open_set.get()[2]

        # Delay node movement
        # time.sleep(0.3)

        # If we reached the goal, stop
        if current_cell == goal:
            break
        
        # Check neighbors (East, South, West, North) for possible moves
        for direction in 'ESNW':
            if maze_obj.maze_map[current_cell][direction]:
                if direction == 'E':
                    neighbor = (current_cell[0], current_cell[1] + 1)
                elif direction == 'W':
                    neighbor = (current_cell[0], current_cell[1] - 1)
                elif direction == 'N':
                    neighbor = (current_cell[0] - 1, current_cell[1])
                elif direction == 'S':
                    neighbor = (current_cell[0] + 1, current_cell[1])

                # Tentative g_score for the neighbor
                temp_g_score = g_score[current_cell] + 1
                temp_f_score = temp_g_score + heuristic(neighbor, goal)

                # If this path is better, update path information
                if temp_f_score < f_score[neighbor]:
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_f_score
                    open_set.put((temp_f_score, heuristic(neighbor, goal), neighbor))
                    came_from[neighbor] = current_cell

    # Reconstruct path from goal to start
    path = {}
    cell = goal
    while cell != start:
        path[came_from[cell]] = cell
        cell = came_from[cell]
    return path

if __name__ == '__main__':
    
    # Create a x by x maze
    m = maze(8, 8)
    m.CreateMaze()  # Generate a random maze structure

    # Run A* search and retrieve the path
    path = a_star_search(m)

    # Initialize agent and display path in the maze
    agent_obj = agent(m, footprints=True, color="yellow")
    m.tracePath({agent_obj: path})
    
    # Display the length of the path
    path_length = len(path) + 1  # Including the start cell
    label = textLabel(m, 'A* Path Length', path_length)

    # Run the visualization in Pyamaze
    m.run()
