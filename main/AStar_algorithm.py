from queue import PriorityQueue
import pygame
import sys

def a_star_algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        current = open_set.get()[2]
        open_set_hash.remove(current)
        # if current == end:
        #     reconstruct_path(came_from, current, draw)
        #     start.make_start()
        #     end.make_end()
        #     return True # make path
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                if neighbor == end:
                    close_unrelated_spots(grid, draw)
                    reconstruct_path(came_from, neighbor, start, end, draw)
                    return True
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start:
            current.make_closed()
    return False

def close_unrelated_spots(grid, draw):
    for row in grid:
        for spot in row:
            if spot.is_open():
                spot.make_closed()
                draw()

def reconstruct_path(came_from, current, start, end, draw):
    reversedNodes = []
    while current in came_from:
        reversedNodes.append(current)
        current = came_from[current]
    for current in reversedNodes[::-1]:
        if current not in (start, end):
            current.make_path()
            draw()

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)