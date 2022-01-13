# Modelization

The "minimum dominating groups" problem can be formalized as below.

Minimize:

$$ \sum_{k \in [1..m]} y_k $$

Subject to:

$$\forall i \in [1..n], \sum_{j \in A_i} x_j \ge 1 $$

$$\forall i \in [1..n], x_i = \prod_{k \in G_i} y_k $$

Given that:

- n is the number of vertices.
- m is the number of groups.
- $x_i \in \{0, 1\}$ indicates if vertex $i$ is part of the dominating vertices.
- $y_k \in \{0, 1\}$ indicates if group $k$ is part of the dominating groups.
- $A_i$ is the closed neighborhood of $i$: the set of vertices directly connected to $i$, including $i$.
- $G_i$ is the set of groups that include $i$.

For implementation in a linear programming framework we rewrite the equality above as two linear inequalities:

$$\forall i, 1 - x_i \leq  \sum_{k \in G_i}(1 - y_k)$$

$$\forall i, \forall k \in G_i, x_i \leq y_k$$

Note that if we define each group to consist of a single vertex, the minimum dominating group problem simplifies into the well known minimum dominating set problem.
