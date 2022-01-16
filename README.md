# Pathfinding-Algorithm-Visualizer
Welcome to my pathfinding algorithm visualizer!
This program is written in Python. Pathfinding is very interesting, worth spending a lot of time building the visualization application.   

You can download the files in the main/ directory to play it in your own PC. (prerequisite: Pygame module) You can also download the exe file in exe/ directory to play.

![A star](https://github.com/Albert-Aiqi-Zhang/Pathfinding-Algorithm-Visualizer/blob/main/imgs/Astar.png)

I implemented the following pathfinding algorithms as well as a maze generator.

## Pathfinding Algorithms
1. A * Algorithm: it calculates heuristic (H score) as well as the current distance from the starting position (G score), and uses their sum (F score) to determine which node to visit next. It can guarantee the shortest path. In my opinion, this is the best pathfinding algorithm among these. In this application, I used a min-heap (priority queue) to implement the algorithm.

2. Dijkstra's Algorithm: it only uses the current distance from the starting position (G score) to determine which node to visit next. Although it also guarantee the shortest path, it is slower than A * algorithm.
 
![Dijkstra](https://github.com/Albert-Aiqi-Zhang/Pathfinding-Algorithm-Visualizer/blob/main/imgs/dijkstra.png)

3. Breadth-First Search Algorithm: it is a classic pathfinding algorithm which also guarantee the shortest path. It neithor uses heuristics nor the current distance form the starting position. In stead, it uses a queue (First In, First Out) to visit nodes in sequence "blindly". Hence, it is slower than A * and Dijkstra's algorithms.

![Breath-first search](https://github.com/Albert-Aiqi-Zhang/Pathfinding-Algorithm-Visualizer/blob/main/imgs/breadth_first_search.png)

4. Depth-First Search Algorithm: actually it is not suitable for pathfinding. It uses a stack (Last In, First Out) to visit nodes. It cannot guarantee the shortest path, nor a fast process.

5. Greedy Best-First Search Algorithm: it is a 'complent' of Dijkstra's algorithm with respect to A * since it only relies on heuristics. In this application I uses Manhattan distance as a heuristic. Although it is often faster than the above algorithms, it cannot guarantee the shortest path, like many other greedy algorithms.

![greedy best-first search](https://github.com/Albert-Aiqi-Zhang/Pathfinding-Algorithm-Visualizer/blob/main/imgs/greedy_best_first.png)

## Manual
Generally you can control the application with a keyboard or a mouse. The shortcuts are shown in the above figure.

### Basic operations
left click (in the grid area): put starting node (purple), ending node(red) and walls (black)  
left click (in the option area): choose corresponding options  
right click: remove the above objects. You can firstly remove the starting node or ending node, and then put it wherever you like.  
SPACE: start pathfinding (You can also click the red title to start)  
R: reset the grids  
E: remove the pathfinding track (from the previous pathfinding process)  

### Choose algorithms
A: A * algorithm  
D: Dijkstra's algorithm  
B: Breadth-first search algorthim  
F: Depth-first search algorithm  
G: Greedy best-first search algorithm   

### Choose Mazes
You can draw walls by dragging the mouse, or use the maze generator. 

M: generate random maze  
H: generate horizontally biased maze   
V: generate vertically biased maze  

![maze](https://github.com/Albert-Aiqi-Zhang/Pathfinding-Algorithm-Visualizer/blob/main/imgs/maze.png)

Enjoy it!




