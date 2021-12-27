# Pathfinding-Algorithm-Visualizer
Welcome to my pathfinding algorithm visualizer!
This program is written in Python. Pathfinding is very interesting, worth spending a lot of time building the visualization application. You can download the files in the main/ directory to play it in your own PC. (prerequisite: Pygame module)

![A star](https://github.com/Albert-Aiqi-Zhang/Pathfinding-Algorithm-Visualizer/blob/main/imgs/Astar.png)

This application is inspired by a Youtuber, Tech with Tim. He has a tutorial of visualization of A* algorthim. Inspired by his work, I implemented these pathfinding algorithms as well as a maze generator.

## Pathfinding Algorithms
1. A * Algorithm: it calculates heuristic (H score) as well as the current distance from the starting position (G score), and uses their sum (F score) to determine which node to visit next. It can guarantee the shortest path. In my opinion, this is the best pathfinding algorithm among these.

2. Dijkstra's Algorithm: it only uses the current distance from the starting position (G score) to determine which node to visit next. Although it also guarantee the shortest path, it is slower than A * algorithm.
 
![Dijkstra](https://github.com/Albert-Aiqi-Zhang/Pathfinding-Algorithm-Visualizer/blob/main/imgs/dijkstra.png)

3. Breadth-First Search Algorithm: it is a classic pathfinding algorithm which also guarantee the shortest path. It neithor uses heuristics nor the current distance form the starting position. In stead, it uses a queue (First In, First Out) to visit nodes in sequence "blindly". Hence, it is slower than A * and Dijkstra's algorithms.

![Breath-first search](https://github.com/Albert-Aiqi-Zhang/Pathfinding-Algorithm-Visualizer/blob/main/imgs/breadth_first_search.png)

4. Depth-First Search Algorithm: actually it is not suitable for pathfinding. It uses a stack (Last In, First Out) to visit nodes. It cannot guarantee the shortest path, nor a fast process.

5. Greedy Best-First Search Algorithm: it is a 'complent' of Dijkstra's algorithm with respect to A * since it only relies on heuristics. In this application I uses Manhattan distance as a heuristic. Although it is often faster than the above algorithms, it canonot guarantee the shortest path, like many other greedy algorithms.

![greedy best-first search](https://github.com/Albert-Aiqi-Zhang/Pathfinding-Algorithm-Visualizer/blob/main/imgs/greedy_best_first.png)

