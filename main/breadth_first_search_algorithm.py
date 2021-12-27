import pygame
import sys
import collections

def breadth_first_search_algorithm(draw, grid, start, end):
    start.distance_from_start = 0
    queue = collections.deque([start])
    came_from = {}
    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        currentNode = queue.popleft()
        neighbors = currentNode.neighbors
        for neighbor in neighbors:
            if neighbor.is_open() or neighbor.is_closed():
                continue
            queue.append(neighbor)
            tentativeDistanceToNeighbor = currentNode.distance_from_start + 1
            if tentativeDistanceToNeighbor < neighbor.distance_from_start:
                neighbor.distance_from_start = tentativeDistanceToNeighbor
                came_from[neighbor] = currentNode
                if neighbor == end:
                    close_unrelated_spots(grid, draw)
                    reconstruct_path(came_from, neighbor, start, end, draw)
                    return True
                neighbor.make_open()
        draw()
        if currentNode != start:
            currentNode.make_closed()
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

