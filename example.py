"""
Generate a random problem to solve
A is a list of lists of integers, representing the connected nodes for each node in the graph
G is a list of lists of integers, representing the group memberships for each node in the graph
W is a list of numbers, representing the weight of each group in the minimization
"""
from utils import generate_random_problem
A, G, W = generate_random_problem()

"""
Solve the problem
We simply pass A, G and W and get the results:
    status: 0 if the solution is optimal
    obj   : minimum weighted sum of groups obtained by the solution
    x     : list of 0/1, indicating for each vertex, if it is in the dominating vertices (1) or not (0)
    y     : list of 0/1, indicating for each group, if it is in the dominating groups (1) or not (0)
"""
from mdg import solve
status, obj, x, y = solve(A, G, W)

print(f'{sum(x)} vertices out of {len(x)} are part of the dominating vertices')
print(f'{sum(y)} groups out of {len(y)} are part of the dominating groups')
