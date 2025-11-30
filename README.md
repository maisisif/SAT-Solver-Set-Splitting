 # **Set Splitting SAT Solver**

This project builds a solver for the Set Splitting problem by reducing it to the Boolean Satisfiability Problem (SAT). The main logic is written in Python and encodes the input problem into CNF (Conjunctive Normal Form) before using the Glucose 4.2 SAT solver to get a solution.



 ## Problem description

Given a family $X$ of subsets of a finite set $S$, decide whether there exists a partition of S into two subsets $S_1$, $S_2$ such that all elements of F are split by this partition.

The goal is to partition the elements of X into two disjoint sets: $S_1$ and $S_2$. Such that no subset $X_i$ is entirely contained within $S_1$ or $S_2$. Basically showing that every subset $X_i$ must be split between the two groups.

An example of a valid input format is:

```text
6 2
1 2 3
2 3 4
```

Where the first line contains n and m:
- n stands for number of elements
- m stands for number of sets (each contain space seperated elements of set)


## Encoding

To encode the problem, items are directly mapped to boolean variables.

Start by defining a variable $x_i$ for each element $i \in \{1, \dots, n\}$.
Next step is to identify where the element belongs to:
- If $x_i$ is True, element $i$ belongs to set $S_1$.
- If $x_i$ is False, element $i$ belongs to set $S_2$.

For each set $X \in \mathcal{X}$, we require that neither $S_1$ nor $S_2$ can have all of its items. This ensures that splitting is correct. This results in:
- At least one element must be in $S_1$:
                            ($x_1$ ∨ $x_2$​ ∨ $x_3$ ​∨ …)
  
- At least one element must be in $S_2$:
                            ($¬x_1$ ​∨ $¬x_2$​ ∨ $¬x_3$ ​∨ …)


The CNF is written in the standard DIMACS format.

## User documentation
Basic usage:
```text
set_splitting.py [-h] [-i INPUT] [-o OUTPUT] [-s SOLVER] [-v {0,1}]
```
Command-line options:

- h, --help
Show a help message and exit.

- i INPUT, --input INPUT
The instance file for the Set Splitting problem.
Default: "instances/small-sat.in".

- o OUTPUT, --output OUTPUT
Output file for the DIMACS CNF formula.
Default: "formula.cnf".

- s SOLVER, --solver SOLVER
The SAT solver to be used (compiled Glucose binary).
Default: "glucose".

- v {0,1}, --verb {0,1}
Verbosity level of the SAT solver (0 = quiet, 1 = default).
Default: 1.

## Example instances
- small-sat.in: A small satifiasble instance
- small-unsat.in: A small unsatifiable instance
- medium-sat.in: A medium satisfiable instance
- slow-hard.in: A slow and hard instance


## Experiments
Experiments were run on a MacBook Pro 14-inch (2023) equipped with an Apple M3 Pro chip and 18 GB of RAM. Time was measured with hyperfine.

For the small and medium files, experiments were ran almost immediately. So I will focus on the slow-hard example.
```text
Benchmark 1: python3 set_splitting.py -i instances/slow-hard.in -o formula.cnf -s glucose
  Time (mean ± σ):      28.5 ms ±   4.2 ms    [User: 20.7 ms, System: 6.6 ms]
  Range (min … max):    26.4 ms …  56.6 ms    50 runs
```

I tried making bigger and bigger instances to slow the solver down, but Glucose still solves them almost immediately and it was not easy to create such instances. For Set Splitting the conditions are easy, so even if I use very large inputs, they do not create enough difficulty for the solver to hit those 10 seconds.
As a result, the biggest instance I made is included, but it still solves very fast.

