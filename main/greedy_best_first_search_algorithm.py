import pygame
import sys

### Similar to A* algorithm, but here it only uses heuristic (h score)
def greedy_best_first_search_algorithm(draw, grid, start, end):
    start.heuristic = getManhattanDistance(start.get_pos(), end.get_pos())
    minHHeap = MinHeapGreedy([start])
    came_from = {}
    while not minHHeap.isEmpty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        currentNode = minHHeap.remove()
        # if currentNode.heuristic == float("inf"):
        #     return [] # cannot find a path to the endNode
        neighbors = currentNode.neighbors
        for neighbor in neighbors:
            if neighbor.is_open() or neighbor.is_closed() or neighbor.is_start():
            # if neighbor.is_closed(): # or neighbor.is_start():
                continue
            tentativeDistance = getManhattanDistance(neighbor.get_pos(), end.get_pos())
            if neighbor.heuristic != tentativeDistance:
                neighbor.heuristic = tentativeDistance
                came_from[neighbor] = currentNode
                minHHeap.insert(neighbor)
            if neighbor == end:
                close_unrelated_spots(grid, draw)
                reconstruct_path(came_from, neighbor, start, end, draw)
                return True
            if not neighbor.is_start():
                neighbor.make_open()
        draw()
        if currentNode != start:
            currentNode.make_closed()
    return False

# def greedy_best_first_search_algorithm(draw, grid, start, end):
#     # print("Hi")
#     # start.heuristic = getManhattanDistance(start.get_pos(), end.get_pos())
#     # minHHeap = MinHeapGreedy([start])
#     minHHeap = initializeMinHeap(grid, start, end)
#     came_from = {}
#     while not minHHeap.isEmpty():
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#         currentNode = minHHeap.remove()
#         # print(currentNode.id)
#         # if currentNode.heuristic == float("inf"):
#         #     return [] # cannot find a path to the endNode
#         neighbors = currentNode.neighbors
#         for neighbor in neighbors:
#             tentativeDistance = getManhattanDistance(neighbor.get_pos(), end.get_pos())
#             if neighbor.heuristic != tentativeDistance:
#                 neighbor.heuristic = tentativeDistance
#                 came_from[neighbor] = currentNode
#                 minHHeap.update(neighbor)
#             if neighbor == end:
#                 close_unrelated_spots(grid, draw)
#                 reconstruct_path(came_from, neighbor, start, end, draw)
#                 return True
#             if not neighbor.is_start():
#                 neighbor.make_open()
#         draw()
#         if currentNode != start:
#             currentNode.make_closed()
#     return False


def initializeMinHeap(nodes, start, end):
    nodeArray = [] # squeeze the 2d nodes to a 1d array for 
                   # initialization of min-heap.
    for row in nodes:
        for node in row:
            if node == start:
                node.heuristic = getManhattanDistance(start.get_pos(), end.get_pos())
            nodeArray.append(node)
    minDistancesHeap = MinHeapGreedy(nodeArray)
    return minDistancesHeap

def getManhattanDistance(pos1, pos2):
    y1, x1 = pos1
    y2, x2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)

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
        if not current.is_start() and not current.is_end():
            current.make_path()
            draw()

class MinHeapGreedy:
    def __init__(self, array):
        self.nodePositionsInHeap = {node.id: idx for idx, node in enumerate(array)}
        self.heap = self.buildHeap(array)
        
    def isEmpty(self):
        return len(self.heap) == 0

    def buildHeap(self, array):
        for i in range(len(array) // 2 - 1, -1, -1):
            self.siftDown(i, array)
        return array

    def siftDown(self, idx, heap):
        childOneIdx = idx * 2 + 1
        while childOneIdx < len(heap):
            childTwoIdx = idx * 2 + 2 if idx * 2 + 2 < len(heap) else -1
            if (childTwoIdx != -1 and heap[childTwoIdx].heuristic < 
                heap[childOneIdx].heuristic):
                idxToSwap = childTwoIdx
            else:
                idxToSwap = childOneIdx
            if heap[idxToSwap].heuristic < heap[idx].heuristic:
                self.swap(idx, idxToSwap, heap)
                idx = idxToSwap
                childOneIdx = idx * 2 + 1
            else:
                break

    def siftUp(self, idx, heap):
        parentIdx = (idx - 1) // 2
        while parentIdx >= 0 and heap[idx].heuristic < heap[parentIdx].heuristic:
            self.swap(parentIdx, idx, heap)
            idx = parentIdx
            parentIdx = (idx - 1) // 2
            
    def swap(self, i, j, heap):
        self.nodePositionsInHeap[heap[i].id] = j
        self.nodePositionsInHeap[heap[j].id] = i
        heap[i], heap[j] = heap[j], heap[i]

    def peek(self):
        return self.heap[0]

    def remove(self):
        if self.isEmpty():
            return
        self.swap(0, len(self.heap) - 1, self.heap)
        node = self.heap.pop()
        del self.nodePositionsInHeap[node.id]
        self.siftDown(0, self.heap)
        return node
    
    def insert(self, node):
        self.heap.append(node)
        self.nodePositionsInHeap[node.id] = len(self.heap) - 1
        self.siftUp(len(self.heap) - 1, self.heap)
    
    def containsNode(self, node):
        return node.id in self.nodePositionsInHeap

    def update(self, node): 
        # When we modify the estimatedDistanceToEnd (make it smaller) 
        # field out of the class,
        # we need to update its position (siftUp)
        self.siftUp(self.nodePositionsInHeap[node.id], self.heap)


