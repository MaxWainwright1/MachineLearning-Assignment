import pygame
import sys
from queue import PriorityQueue

# Initialize pygame
pygame.init()

# Constants for the grid
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS

# Color definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)

# Define the grid
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_obstacle = False
        self.is_start = False
        self.is_end = False
        self.color = WHITE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.col * CELL_WIDTH, self.row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

    def make_obstacle(self):
        self.is_obstacle = True
        self.color = BLACK

    def make_start(self):
        self.is_start = True
        self.color = GREEN

    def make_end(self):
        self.is_end = True
        self.color = RED

# Heuristic function for A* (Manhattan distance)
def heuristic(node1, node2):
    return abs(node1.row - node2.row) + abs(node1.col - node2.col)

# A* pathfinding algorithm
def a_star(start_node, end_node, grid):
    open_set = PriorityQueue()
    open_set.put((0, start_node))
    came_from = {}
    
    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start_node] = 0
    
    f_score = {node: float('inf') for row in grid for node in row}
    f_score[start_node] = heuristic(start_node, end_node)
    
    while not open_set.empty():
        current = open_set.get()[1]

        if current == end_node:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(current, grid):
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end_node)

                if (f_score[neighbor], neighbor) not in open_set.queue:
                    open_set.put((f_score[neighbor], neighbor))  # Put as tuple
                    neighbor.color = GRAY  # Mark as visited
                    neighbor.draw(win)
                    pygame.display.update()

    return []  # No path found

# Ensure that 'Node' can be compared based on row and column for better ordering
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_obstacle = False
        self.is_start = False
        self.is_end = False
        self.color = WHITE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.col * CELL_WIDTH, self.row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

    def make_obstacle(self):
        self.is_obstacle = True
        self.color = BLACK

    def make_start(self):
        self.is_start = True
        self.color = GREEN

    def make_end(self):
        self.is_end = True
        self.color = RED

    def __lt__(self, other):
        # This method allows nodes to be compared based on their row and column for PriorityQueue
        return (self.row, self.col) < (other.row, other.col)




# Reconstruct the path from end to start
def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]  # Return reversed path

# Get neighbors for A*
def get_neighbors(node, grid):
    neighbors = []
    row, col = node.row, node.col
    if row < ROWS - 1:  # South
        neighbors.append(grid[row + 1][col])
    if row > 0:  # North
        neighbors.append(grid[row - 1][col])
    if col < COLS - 1:  # East
        neighbors.append(grid[row][col + 1])
    if col > 0:  # West
        neighbors.append(grid[row][col - 1])
    return [n for n in neighbors if not n.is_obstacle]  # Return walkable neighbors

# Main function to run the A* pathfinding
def main():
    global win
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("A* Pathfinding Algorithm Visualization")

    # Create the grid
    grid = [[Node(row, col) for col in range(COLS)] for row in range(ROWS)]

    start_node = None
    end_node = None

    run = True
    while run:
        win.fill(WHITE)
        for row in grid:
            for node in row:
                node.draw(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                pos = pygame.mouse.get_pos()
                col = pos[0] // CELL_WIDTH
                row = pos[1] // CELL_HEIGHT
                node = grid[row][col]
                if not start_node and node != end_node:
                    start_node = node
                    start_node.make_start()
                elif not end_node and node != start_node:
                    end_node = node
                    end_node.make_end()
                elif node != end_node and node != start_node:
                    node.make_obstacle()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_node and end_node:
                    path = a_star(start_node, end_node, grid)
                    for node in path:
                        node.color = BLUE  # Color the path
                        node.draw(win)
                        pygame.display.update()
                        pygame.time.delay(100)  # Delay to visualize path finding

        pygame.display.update()

if __name__ == "__main__":
    main()
