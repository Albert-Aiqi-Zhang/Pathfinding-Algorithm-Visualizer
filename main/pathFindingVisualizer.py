import pygame
import math
from queue import PriorityQueue
import sys
import os
sys.path.append(os.getcwd())
# from drop_down import * # a class of drop down bottons
from AStar_algorithm import *
from dijkstra_algorithm import *
from breadth_first_search_algorithm import *
from depth_first_search_algorithm import *
from greedy_best_first_search_algorithm import *
from maze_algorithm import *
pygame.init()

TOTAL_WIDTH = 1200
TOTAL_HEIGHT = 780
WIDTH = 1200
HEIGHT = 600
# WIN = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
pygame.display.set_caption("Path Finding Visualizer")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 203, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
SHALLOW_BLUE = (135, 206, 235)

### OPTION positions:
LINE_1 = (45, 70)
LINE_2 = (70, 95)
LINE_3 = (95, 120)
LINE_4 = (120, 145)
LINE_5 = (145, 170)
COL_1 = (30, 250)
COL_2 = (TOTAL_WIDTH / 2 - 100, TOTAL_WIDTH / 2 + 150)
COL_3 = (TOTAL_WIDTH - 250, TOTAL_WIDTH - 50)


# COLOR_INACTIVE = (100, 80, 255)
# COLOR_ACTIVE = (100, 200, 255)
# COLOR_LIST_INACTIVE = (255, 100, 100)
# COLOR_LIST_ACTIVE = (255, 150, 150)

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    BLUE = 0, 0, 255
    RED = 255, 0, 0
    GREY = 128, 128, 128
    YELLOW = 255, 250, 100
    PINK = 255, 192, 203
    BACKGROUND_COLOR = WHITE

    FONT = pygame.font.SysFont("Times", 25)
    LARGE_FONT = pygame.font.SysFont("arial", 35)
    SIDE_PAD = 100
    TOP_PAD = 150

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pathfinding Algorithm Visualizer")


class Spot:
    def __init__(self, row, col, height, width, total_rows, total_cols):
        self.row = row
        self.col = col
        self.id = str(row) + "-" + str(col)
        self.y = row * width + TOTAL_HEIGHT - HEIGHT
        self.x = col * height
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.height = height
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.distance_from_start = float("inf")
        self.heuristic = float("inf")

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == BLUE

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == PURPLE

    def is_end(self):
        return self.color == RED

    def is_path(self):
        return self.color == YELLOW

    def reset(self):
        self.color = WHITE

    def reset_value(self):
        self.distance_from_start = float("inf")
        self.heuristic = float("inf")

    def make_start(self):
        self.color = PURPLE

    def make_closed(self):
        self.color = BLUE

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = RED
    
    def make_path(self):
        self.color = YELLOW

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def update_neighbors(self, grid):
        ### ATTENTION: self.total_rows may be wrong here
        self.neighbors = []
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

    def __lt__(self, other):
        return False


def make_grid(cols, width, HEIGHT, TOTAL_HEIGHT):
    grid = []
    gap = width // cols
    rows = HEIGHT // gap # actual row number
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            spot = Spot(i, j, gap, gap, rows, cols)
            grid[i].append(spot)
    return grid

def draw_grid(win, cols, width):
    gap = width // cols
    rows = HEIGHT // gap
    for i in range(rows):
        # pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        pygame.draw.line(win, SHALLOW_BLUE, (0, i * gap + TOTAL_HEIGHT - HEIGHT), (width, i * gap + TOTAL_HEIGHT - HEIGHT))
        for j in range(cols):
            pygame.draw.line(win, SHALLOW_BLUE, (j * gap, TOTAL_HEIGHT - HEIGHT), (j * gap, TOTAL_HEIGHT))

def draw(draw_info, grid, rows, width, algo_name):
    win = draw_info.window
    # win.fill(WHITE)
    win.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(algo_name, 1, RED)
    win.blit(title, (width/2 - title.get_width()/2 , 5))

    ### Manual:
    controls = draw_info.FONT.render("SPACE - Start", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (30 , 45))
    controls = draw_info.FONT.render("R - Reset", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (30 , 70))
    controls = draw_info.FONT.render("E - Remove Track", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (30 , 95))
    controls = draw_info.FONT.render("Left Click - Put Obejects", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (30 , 120))
    controls = draw_info.FONT.render("Right Click - Remove Obejects", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (30 , 145))

    controls = draw_info.FONT.render("A - A * Algorithm", 1, draw_info.BLUE)
    draw_info.window.blit(controls, (draw_info.width / 2 - 100, 45))
    controls = draw_info.FONT.render("D - Dijkstra's Algorithm", 1, draw_info.BLUE)
    draw_info.window.blit(controls, (draw_info.width / 2 - 100, 70))
    controls = draw_info.FONT.render("B - Breadth First Search", 1, draw_info.BLUE)
    draw_info.window.blit(controls, (draw_info.width / 2 - 100, 95))
    sorting = draw_info.FONT.render("F - Depth First Search", 1, draw_info.BLUE)
    draw_info.window.blit(sorting, (draw_info.width / 2 - 100, 120))
    sorting = draw_info.FONT.render("G - Greedy Best First", 1, draw_info.BLUE)
    draw_info.window.blit(sorting, (draw_info.width / 2 - 100, 145))

    controls = draw_info.FONT.render("M - Generate Maze", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width - 250, 45))
    controls = draw_info.FONT.render("H - Horizontal Maze", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width - 250, 70))
    controls = draw_info.FONT.render("V - Vertical Maze", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width - 250, 95))

    # controls = draw_info.FONT.render("R - Reset | E - Remove Track | SPACE - Start PathFinding | M - Create Random Maze", 1, draw_info.BLACK)
    # draw_info.window.blit(controls, (0 , 70))

    # controls = draw_info.FONT.render("R - Reset | E - Remove Track | SPACE - Start PathFinding | M - Create Random Maze", 1, draw_info.BLACK)
    # draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

    # controls = draw_info.FONT.render("H - Horizontal Skewed Maze | V - Vertical Skwed Maze", 1, draw_info.BLACK)
    # draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 70))

    # controls = draw_info.FONT.render("A - A* Algorithm | D - Dijkstra's Algorithm | B - Breadth First Search", 1, draw_info.BLUE)
    # draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 95))

    # sorting = draw_info.FONT.render("F - Depth First Search | G - Greedy Best First Search", 1, draw_info.BLUE)
    # draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 120))

    # sorting = draw_info.FONT.render("Q - Quick Sort | H - Heap Sort | M - Merge Sort", 1, draw_info.BLUE)
    # draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 120))

    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def clear_last_track(grid, draw):
    for row in grid:
        for spot in row:
            spot.reset_value()
            if spot.is_barrier() or spot.is_start() or spot.is_end():
                continue
            spot.reset()
    draw()

def get_clicked_pos(pos, cols, width):
    gap = width // cols
    x, y = pos
    row = (y - (TOTAL_HEIGHT - HEIGHT)) // gap
    # row = y // gap
    col = x // gap
    return row, col

def switch_option(pos): # click options to do something
    x, y = pos
    if 0 < y < 45 and  TOTAL_WIDTH / 2 - 200 < x < TOTAL_WIDTH / 2 + 200:
        ### Special: click title and start
        return "SPACE"
    elif isInside(x, COL_1):
        if isInside(y, LINE_1):
            return "SPACE"
        elif isInside(y, LINE_2):
            return "R"
        elif isInside(y, LINE_3):
            return "E"
    elif isInside(x, COL_2):
        if isInside(y, LINE_1):
            return "A"
        elif isInside(y, LINE_2):
            return "D"
        elif isInside(y, LINE_3):
            return "B"
        elif isInside(y, LINE_4):
            return "F"
        elif isInside(y, LINE_5):
            return "G"
    elif isInside(x, COL_3):
        if isInside(y, LINE_1):
            return "M"
        elif isInside(y, LINE_2):
            return "H"
        elif isInside(y, LINE_3):
            return "V"

def isInside(x, LINE):
    return LINE[0] < x < LINE[1]

def main():
    width = WIDTH
    ROWS = 40 # change it to 40
    COLS = 40 # change it to 40
    grid = make_grid(COLS, width, HEIGHT, TOTAL_HEIGHT)
    draw_info = DrawInformation(TOTAL_WIDTH, TOTAL_HEIGHT)

    numRows, numCols = len(grid), len(grid[0])
    start, end = None, None
    # default setting
    start = grid[numRows // 3][numCols // 5]
    start.make_start()
    end = grid[numRows // 3][3 * numCols // 5]
    end.make_end()


    pathfinding_algorithm = a_star_algorithm
    algo_name = "A* algorithm"


    option = None
    run = True
    while run:
        draw(draw_info, grid, ROWS, width, algo_name)

        # event_list = pygame.event.get()
        # selected_option = list1.update(event_list)
        # if selected_option >= 0:
        #     list1.main = list1.options[selected_option]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # left click
                pos = pygame.mouse.get_pos()
                if pos[1] >= TOTAL_HEIGHT - HEIGHT: # inside the grid zone
                    row, col = get_clicked_pos(pos, COLS, width)
                    spot = grid[row][col]
                    if not start and spot != end: # set start node
                        start = spot
                        start.make_start()
                    elif not end and spot != start:
                        end = spot # set end node
                        end.make_end()
                    elif spot != end and spot != start: # set barrier node
                        spot.make_barrier()
                else:
                    pass # ToDo

            elif pygame.mouse.get_pressed()[2]: # right click
                pos = pygame.mouse.get_pos()
                if pos[1] >= TOTAL_HEIGHT - HEIGHT: # inside the grid zone
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None
                else:
                    pass # ToDo

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                option = switch_option(pos)
                if option == "SPACE" and start and end : # press SPACE
                    clear_last_track(grid, lambda: draw(draw_info, grid, ROWS, width, algo_name))
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    pathfinding_algorithm(lambda: draw(draw_info, grid, ROWS, width, algo_name), grid, start, end)
                elif option == "R": # press r to reset
                    grid = make_grid(ROWS, width, HEIGHT, TOTAL_HEIGHT)
                    # default setting
                    start = grid[numRows // 3][numCols // 5]
                    start.make_start()
                    end = grid[numRows // 3][3 * numCols // 5]
                    end.make_end()
                # elif option == ""
                elif option == "E":  # press E to remove the algorithm track
                    for row in grid:
                        for spot in row:
                            if not spot.is_start() and not spot.is_end() and spot.is_closed() or spot.is_path():
                                spot.reset()
                elif option == "A": # press a for A * algorithm
                    clear_last_track(grid, lambda: draw(draw_info, grid, ROWS, width, algo_name))
                    pathfinding_algorithm = a_star_algorithm
                    algo_name = "A* Algorithm"
                elif option == "D": # press d for Dijkstra's algorithm
                    clear_last_track(grid, lambda: draw(draw_info, grid, ROWS, width, algo_name))
                    pathfinding_algorithm = dijkstra_algorithm
                    algo_name = "Dijkstra's Algorithm"
                elif option == "B": # press b for breadth first search algorithm
                    clear_last_track(grid, lambda: draw(draw_info, grid, ROWS, width, algo_name))
                    pathfinding_algorithm = breadth_first_search_algorithm
                    algo_name = "Breadth First Search Algorithm"
                elif option == "F": # press f for Depth first search algorithm
                    clear_last_track(grid, lambda: draw(draw_info, grid, ROWS, width, algo_name))
                    pathfinding_algorithm = depth_first_search_algorithm
                    algo_name = "Depth First Search Algorithm"
                elif option == "G": # press g for greedy best first search algorithm
                    clear_last_track(grid, lambda: draw(draw_info, grid, ROWS, width, algo_name))
                    pathfinding_algorithm = greedy_best_first_search_algorithm
                    algo_name = "Greedy Best First Search Algorithm"
                elif option == "M": # press m to create random maze
                    create_random_maze(lambda: draw(draw_info, grid, ROWS, width, algo_name), grid)
                elif option == "H": # press h to create horizontally skewed maze
                    create_recursive_skewed_maze(lambda: draw(draw_info, grid, ROWS, width, algo_name), grid, "horizontal")
                elif option == "V": # press v to create vertically skewed maze
                    create_recursive_skewed_maze(lambda: draw(draw_info, grid, ROWS, width, algo_name), grid, "vertical")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: # press a for A * algorithm
                    clear_last_track(grid, lambda: draw(draw_info, grid, ROWS, width, algo_name))
                    pathfinding_algorithm = a_star_algorithm
                    algo_name = "A* Algorithm"
                if event.key == pygame.K_d: # press d for Dijkstra's algorithm
                    clear_last_track(grid, lambda: draw(draw_info, grid, ROWS, width, algo_name))
                    pathfinding_algorithm = dijkstra_algorithm
                    algo_name = "Dijkstra's Algorithm"
                if event.key == pygame.K_b: # press b for breadth first search algorithm
                    clear_last_track(grid, lambda: draw(draw_info, grid, ROWS, width, algo_name))
                    pathfinding_algorithm = breadth_first_search_algorithm
                    algo_name = "Breadth First Search Algorithm"
                if event.key == pygame.K_f: # press f for Depth first search algorithm
                    clear_last_track(grid, lambda: draw(draw_info, grid, ROWS, width, algo_name))
                    pathfinding_algorithm = depth_first_search_algorithm
                    algo_name = "Depth First Search Algorithm"
                if event.key == pygame.K_g: # press g for greedy best first search algorithm
                    clear_last_track(grid, lambda: draw(draw_info, grid, ROWS, width, algo_name))
                    pathfinding_algorithm = greedy_best_first_search_algorithm
                    algo_name = "Greedy Best First Search Algorithm"

                if event.key == pygame.K_m: # press m to create random maze
                    create_random_maze(lambda: draw(draw_info, grid, ROWS, width, algo_name), grid)
                if event.key == pygame.K_v: # press v to create vertically skewed maze
                    # create_vertical_skewed_maze(lambda: draw(draw_info, grid, ROWS, width, algo_name), grid)
                    create_recursive_skewed_maze(lambda: draw(draw_info, grid, ROWS, width, algo_name), grid, "vertical")
                if event.key == pygame.K_h: # press h to create horizontally skewed maze
                    # create_horizontal_skewed_maze(lambda: draw(draw_info, grid, ROWS, width, algo_name), grid)
                    create_recursive_skewed_maze(lambda: draw(draw_info, grid, ROWS, width, algo_name), grid, "horizontal")


                if event.key == pygame.K_SPACE and start and end : # press SPACE
                    clear_last_track(grid, lambda: draw(draw_info, grid, ROWS, width, algo_name))
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    pathfinding_algorithm(lambda: draw(draw_info, grid, ROWS, width, algo_name), grid, start, end)

                if event.key == pygame.K_r: # press r to reset
                    # start = None
                    # end = None
                    grid = make_grid(ROWS, width, HEIGHT, TOTAL_HEIGHT)
                    # default setting
                    start = grid[numRows // 3][numCols // 5]
                    start.make_start()
                    end = grid[numRows // 3][3 * numCols // 5]
                    end.make_end()
                if event.key == pygame.K_e: # press E to remove the algorithm track
                    for row in grid:
                        for spot in row:
                            spot.reset_value()
                            if not spot.is_start() and not spot.is_end() and (spot.is_closed() or spot.is_path() or spot.is_open()):
                                spot.reset()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

