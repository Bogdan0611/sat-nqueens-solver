import itertools
import argparse
import sys

class NQueensSAT:
    """
    A class to encode the N-Queens problem into a Boolean Satisfiability (SAT) formula 
    in Conjunctive Normal Form (CNF) and visualize its solutions.
    """
    def __init__(self, size):
        self.n = size
        self.clauses = []
        self.num_vars = size * size

    def _get_var(self, r, c):
        """Map (row, col) to a unique variable ID (1 to N^2)."""
        return (r - 1) * self.n + c

    def _at_most_one(self, vars_list):
        """Add clauses to ensure at most one variable in the list is true."""
        for v1, v2 in itertools.combinations(vars_list, 2):
            self.clauses.append([-v1, -v2])

    def generate_cnf(self):
        """Generates the SAT constraints for the N-Queens problem."""
        self.clauses = []
        
        # 1. Row constraints: Each row must have exactly one queen.
        for i in range(1, self.n + 1):
            row_vars = [self._get_var(i, j) for j in range(1, self.n + 1)]
            self.clauses.append(row_vars)  # At least one
            self._at_most_one(row_vars)    # At most one

        # 2. Column constraints: Each column must have exactly one queen.
        for i in range(1, self.n + 1):
            col_vars = [self._get_var(j, i) for j in range(1, self.n + 1)]
            self.clauses.append(col_vars)  # At least one
            self._at_most_one(col_vars)    # At most one

        # 3. Diagonal constraints: Each diagonal can have at most one queen.
        d_main = {}
        d_sec = {}
        for r in range(1, self.n + 1):
            for c in range(1, self.n + 1):
                v = self._get_var(r, c)
                d_main.setdefault(r - c, []).append(v)
                d_sec.setdefault(r + c, []).append(v)

        for diag in d_main.values():
            if len(diag) > 1:
                self._at_most_one(diag)
                
        for diag in d_sec.values():
            if len(diag) > 1:
                self._at_most_one(diag)

    def save_dimacs(self, filename):
        """Saves the generated clauses in the standard DIMACS format."""
        with open(filename, 'w') as f:
            f.write(f"c N-Queens SAT encoding for N={self.n}\n")
            f.write(f"p cnf {self.num_vars} {len(self.clauses)}\n")
            for clause in self.clauses:
                f.write(" ".join(map(str, clause)) + " 0\n")

    def verify_solution(self, model):
        """Verifies if a given assignment satisfies all CNF clauses."""
        model_set = set(model)
        for clause in self.clauses:
            if not any(lit in model_set for lit in clause):
                return False
        return True

    def print_board(self, model):
        """Prints the N-Queens board based on the SAT solver's output model."""
        queens = [v for v in model if v > 0]
        board = [['.' for _ in range(self.n)] for _ in range(self.n)]
        
        for q in queens:
            r = (q - 1) // self.n
            c = (q - 1) % self.n
            board[r][c] = 'Q'
            
        for row in board:
            print(" ".join(row))
        print()

def parse_model(model_str):
    """Parses a space-separated string of literals into a list of integers."""
    try:
        return [int(x) for x in model_str.split() if int(x) != 0]
    except ValueError:
        return None

def main():
    parser = argparse.ArgumentParser(description="N-Queens SAT Solver Utility")
    parser.add_argument("-n", "--size", type=int, default=8, help="Size of the board (N)")
    parser.add_argument("-o", "--output", type=str, help="Output CNF filename")
    parser.add_argument("-v", "--verify", action="store_true", help="Verify a solution model")
    
    args = parser.parse_args()

    n_queens = NQueensSAT(args.size)
    n_queens.generate_cnf()

    if args.output:
        n_queens.save_dimacs(args.output)
        print(f"CNF file saved to {args.output}")
    elif not args.verify:
        # Default behavior: save to a default filename if no specific action is requested
        default_file = f"nqueens_{args.size}.cnf"
        n_queens.save_dimacs(default_file)
        print(f"Generated {default_file} for N={args.size}")

    if args.verify:
        print(f"\nEnter the SAT solver output (space-separated literals) for N={args.size}:")
        print("(Or type 'UNSAT' if no solution was found)")
        user_input = sys.stdin.read().strip()
        
        if user_input.upper() == "UNSAT":
            if args.size in [2, 3]:
                print(f"Correct: N={args.size} is indeed unsatisfiable.")
            else:
                print(f"Warning: N={args.size} should be satisfiable. Check your solver output.")
        else:
            model = parse_model(user_input)
            if model is not None:
                if n_queens.verify_solution(model):
                    print("\nSuccess: Solution verified against all clauses!")
                    print("Visualized Board:")
                    n_queens.print_board(model)
                else:
                    print("\nError: The provided solution does not satisfy the constraints.")
            else:
                print("\nInvalid input format. Expected space-separated integers.")

if __name__ == "__main__":
    main()
