# 8-Puzzle Solver: AI Search Algorithms Comparison

This repository contains a comprehensive Python implementation of various artificial intelligence search algorithms to solve the classic **8-Puzzle** problem. The project focuses on comparing performance metrics, specifically execution time and completeness, across different search strategies.

## 🚀 Algorithms Implemented

The project includes both **Uninformed** and **Informed** search strategies:

- **BFS (Breadth-First Search):** Explores all nodes at the current depth before moving deeper. (Optimal for unit step costs).
- **DFS (Depth-First Search):** Explores as far as possible along each branch before backtracking.
- **IDS (Iterative Deepening Search):** Combines the benefits of DFS's space-efficiency and BFS's optimality.
- **UCS (Uniform Cost Search):** Expands the cheapest node, ensuring the optimal path.
- **A* Search (Informed):** Uses heuristics to guide the search efficiently.
  - **Heuristic 1:** Misplaced Tiles (Hamming Distance).
  - **Heuristic 2:** Manhattan Distance (L1 Norm).

## 📊 Performance Analysis
The program is designed to run all implemented algorithms on the same puzzle instance and output a comparative table of execution times. This allows for a clear observation of how informed search (A*) significantly outperforms uninformed search in terms of state-space exploration.

## 🛠️ Installation & Usage

1. **Clone the repository:**
```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   
