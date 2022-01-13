# Minimum Dominating Groups

Here we address an extension of the minimum [dominating set](https://en.wikipedia.org/wiki/Dominating_set) problem to groups of vertices. The idea is to look for the minimum dominating set, but the choice of vertices is restricted: we cannot select vertices directly, we select groups, and the vertices are determined by the selected groups. For the precise formulation please see [modelization.pdf](modelization.pdf).

A potential application is the optimization of manufacturing tests. Output test parameters belong to groups corresponding to the physical tests that generate them. Correlations and redundancies between test parameters can be represented by a graph. Minimizing the number of physical tests is a minimum dominating group problem.

[mdg.py](mdg.py) is a Python module that solves the minimum dominating groups problem using integer linear programming.

The main requirement is [OR-Tools](https://developers.google.com/optimization):

```shell
pip install ortools
```

You will need [Numpy](https://numpy.org/) to run the example or unit tests:

```shell
pip install numpy
```

Usage (from [example.py](example.py)):

```python
from utils import generate_random_problem
A, G, W = generate_random_problem()

from mdg import solve
status, obj, x, y = solve(A, G, W)

print(f'{sum(x)} vertices out of {len(x)} are part of the dominating vertices')
print(f'{sum(y)} groups out of {len(y)} are part of the dominating groups')
```

Output:

```
Using OR-Tools API with solver CBC
Solving with 1000 vertices and 100 groups
Number of constraints = 4185
Status    = 0 (optimal)
Objective = 95.058
905 vertices out of 1000 are part of the dominating vertices
95 groups out of 100 are part of the dominating groups
```

Nota Bene:

- We observed fast and optimal solutions in our tests, but this is not 
  guaranteed due to the complexity of the problem.
- For a vertex to be selected, all its groups must be selected (AND formulation). An OR formulation is possible (at least one of the group must be selected) and leads to a similar but different solution.
- We implemented the weighted version of the minimization: each group 
  is associated with a weight, and the weighted sum is minimized.
- The input parameter A is a list of lists, representing the adjacency 
  matrix of the graph in a sparse way, and it may be asymmetric if the 
  graph is directed.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is licensed under the Apache-2.0 License.
