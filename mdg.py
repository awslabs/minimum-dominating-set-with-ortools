# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from typing import List
from ortools.linear_solver import pywraplp
from operator import mul
from functools import reduce

BOP = pywraplp.Solver.BOP_INTEGER_PROGRAMMING
CBC = pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING
SAT = pywraplp.Solver.SAT_INTEGER_PROGRAMMING

SOLVER_NAMES = {
    BOP: 'BOP',
    CBC: 'CBC',
    SAT: 'SAT',
}


def solve(a: List[List[int]], g: List[List[int]], w: List[float], lib: int = CBC) -> (int, float, List[int], List[int]):
    """
    ARGUMENTS

        a: a[i] is the list of vertices directly connected to vertex i, including i.
        g: g[i] is the list of groups that include vertex i.
        w: w[k] is the weight applied to group k in the minimization.

    RETURNS

        status: 0 if the problem is solved optimally.
        objective: the optimal value of the objective.
        x: list of 0/1. x[i] indicates if the vertex i is part of the dominating set.
        y: list of 0/1. y[k] indicates if the group k is part of the dominating group.
    """

    # number of vertices and groups
    n, m = len(a), len(w)
    
    print(f'Using OR-Tools API with solver {SOLVER_NAMES[lib]}')
    print(f'Solving with {n} vertices and {m} groups')

    solver = pywraplp.Solver('mdg', lib)

    # define the problem decision variables for vertices and groups
    x = {i: solver.IntVar(0, 1, f'x{i}') for i in range(n)}
    y = {k: solver.IntVar(0, 1, f'y{k}') for k in range(m)}

    # define the objective function
    objective = solver.Objective()
    objective.SetMinimization()
    for k in range(m):
        objective.SetCoefficient(y[k], float(w[k]))

    # define the constraints
    for i in range(n):
        r2 = solver.Constraint(1, n, f'A_{i}')
        for j in a[i]:
            r2.SetCoefficient(x[j], 1)
            
        gs = solver.Constraint(1 - len(g[i]), 1, f'G_{i}_SUM')
        gs.SetCoefficient(x[i], 1)
        for k in g[i]:
            gs.SetCoefficient(y[k], -1)
            
        for k in g[i]:
            gk = solver.Constraint(0, 1, f'G_{i}_{k}')
            gk.SetCoefficient(y[k], 1)
            gk.SetCoefficient(x[i], -1)

    print('Number of constraints =', solver.NumConstraints())

    # solve
    status = solver.Solve()
    status_name = 'optimal' if status == solver.OPTIMAL else 'not optimal'
    objective = objective.Value()
    print(f'Status    = {status} ({status_name})')
    print(f'Objective = {objective:.3f}')

    return status, objective, _solutions(x), _solutions(y)


def _solutions(x):
    return [int(x[i].solution_value()) for i in range(len(x))]


def check(a, g, w, x, y):
    """Checks the results from the optimizer."""

    n, m = len(a), len(w)
    
    metrics = [
        ('Number of vertices', sum(x), n),
        ('Number of groups', sum(y), m),
        ('Weighted groups', sum([w[k]*y[k] for k in range(m)]), sum(w))
    ]
    
    for name, z, Z in metrics:
        print(f'{name :<20} {z:>8.1f}/{Z:>8.1f} = {100*z/Z:.1f}%')
        
    dominated_set = {i for i in range(n) if x[i] == 0}
    dominant_set = {i for i in range(n) if x[i] == 1}

    # check that the solution is a dominant set
    for i in dominated_set:
        assert len(dominant_set & set(a[i])) >= 1

    # check that x[i] = product of y[j] for j in groups[i]
    for i in range(n):
        assert x[i] == reduce(mul, [y[j] for j in g[i]])    
