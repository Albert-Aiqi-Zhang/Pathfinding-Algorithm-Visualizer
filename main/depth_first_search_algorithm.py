import pygame
import sys
import collections

def depth_first_search_algorithm(draw, grid, start, end):
    came_from = {}
    start.distance_from_start = 0
    # start.make_open()
    stackToVisit = [start]
    while stackToVisit:
        currentNode = stackToVisit.pop()
        # if currentNode == end:
        #     reconstruct_path(came_from, currentNode, draw)
        #     start.make_start()
        #     end.make_end()
        #     break
        neighbors = currentNode.neighbors
        for neighbor in neighbors:
            if neighbor.is_closed() or neighbor.is_open() or neighbor == start:
                continue
            came_from[neighbor] = currentNode
            if neighbor == end:
                close_unrelated_spots(grid, draw)
                reconstruct_path(came_from, neighbor, start, end, draw)
                return True
            neighbor.make_open()
            stackToVisit.append(neighbor)
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