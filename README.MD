# SAT-NQueens Solver

A professional Python utility designed to encode the classic **N-Queens problem** into a **Boolean Satisfiability (SAT)** formula. The tool generates constraints in the standard **DIMACS CNF** format, making it compatible with modern SAT solvers like MiniSat, Glucose, or Z3.

## Overview

The N-Queens problem involves placing $N$ chess queens on an $N \times N$ chessboard so that no two queens threaten each other. This project provides a robust framework to:
1.  **Generate** SAT constraints for any board size $N$.
2.  **Export** these constraints into a `.cnf` file.
3.  **Verify** the output of a SAT solver against the original constraints.
4.  **Visualize** the solution as a formatted chessboard.

## SAT Encoding

The problem is modeled using $N^2$ boolean variables, where each variable $x_{r,c}$ represents whether a queen is placed at row $r$ and column $c$. The encoding includes:

-   **Row Constraints**: Each row must contain exactly one queen (at least one and at most one).
-   **Column Constraints**: Each column must contain exactly one queen (at least one and at most one).
-   **Diagonal Constraints**: Each diagonal (main and secondary) can contain at most one queen.

## Features

-   **Modular Design**: Clear separation between encoding logic, DIMACS generation, and solution verification.
-   **CLI Interface**: Easily specify the board size and output files via command-line arguments.
-   **Solution Verification**: Validates that the solver's output model actually satisfies all the generated clauses.
-   **Board Visualization**: Automatically decodes the SAT model and prints a human-readable $N \times N$ board.

## Usage

### 1. Generate CNF File
To generate the constraints for a board of size $N=8$:
```bash
python nqueens_solver.py -n 8 -o nqueens_8.cnf
```

### 2. Solve
Use any SAT solver (e.g., [MiniSat.js](https://jgalenson.github.io/research.js/demos/minisat.html)) to solve the generated `.cnf` file. Copy the resulting model (the list of literals).

### 3. Verify and Visualize
Run the script with the `--verify` flag and paste the solver's output when prompted:
```bash
python nqueens_solver.py -n 8 --verify
```

## Example Output (N=4)

```text
. . Q .
Q . . .
. . . Q
. Q . .
```

## Requirements

-   Python 3.x (no external libraries required)

---
*This project was developed as part of the Algorithms and Complexity (ACC) course.*
