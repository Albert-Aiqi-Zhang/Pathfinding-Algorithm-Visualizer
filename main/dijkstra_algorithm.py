import pygame
import sys

def dijkstra_algorithm(draw, grid, start, end):
    minDistancesHeap = initializeMinHeap(grid, start)
    came_from = {}
    while not minDistancesHeap.isEmpty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        currentMinDistanceNode = minDistancesHeap.remove()
        # if currentMinDistanceNode == end:
        #     reconstruct_path(came_from, currentMinDistanceNode, draw)
        #     start.make_start()
        #     end.make_end()
        #     break
        # elif currentMinDistanceNode.distance_from_start == float("inf"):
        #     return [] # cannot find a path to the endNode
        if currentMinDistanceNode.distance_from_start == float("inf"):
            return [] # cannot find a path to the endNode
        neighbors = currentMinDistanceNode.neighbors
        for neighbor in neighbors:
            tentativeDistanceToNeighbor = currentMinDistanceNode.distance_from_start + 1
            if tentativeDistanceToNeighbor < neighbor.distance_from_start:
                neighbor.distance_from_start = tentativeDistanceToNeighbor
                came_from[neighbor] = currentMinDistanceNode
                minDistancesHeap.update(neighbor)
                if neighbor == end:
                    close_unrelated_spots(grid, draw)
                    reconstruct_path(came_from, neighbor, start, end, draw)
                    return True
                neighbor.make_open()
        draw()
        if currentMinDistanceNode != start:
            currentMinDistanceNode.make_closed()
    return False
    

def initializeMinHeap(nodes, start):
    nodeArray = [] # squeeze the 2d nodes to a 1d array for 
                   # initialization of min-heap.
    for row in nodes:
        for node in row:
            if node == start:
                node.distance_from_start = 0
            nodeArray.append(node)
    minDistancesHeap = MinHeap(nodeArray)
    return minDistancesHeap

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

class MinHeap:
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
            if (childTwoIdx != -1 and heap[childTwoIdx].distance_from_start < 
                heap[childOneIdx].distance_from_start):
                idxToSwap = childTwoIdx
            else:
                idxToSwap = childOneIdx
            if heap[idxToSwap].distance_from_start < heap[idx].distance_from_start:
                self.swap(idx, idxToSwap, heap)
                idx = idxToSwap
                childOneIdx = idx * 2 + 1
            else:
                break

    def siftUp(self, idx, heap):
        parentIdx = (idx - 1) // 2
        while parentIdx >= 0 and heap[idx].distance_from_start < heap[parentIdx].distance_from_start:
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