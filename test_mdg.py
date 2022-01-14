# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import pytest
import time
import mdg
from utils import generate_random_problem

A, G, W = generate_random_problem(10)


@pytest.mark.parametrize("solver_type", [mdg.CBC, mdg.BOP, mdg.SAT])
def test_solver(solver_type):
    t0 = time.time()
    status, obj, x, y = mdg.solve(A, G, W, lib=solver_type)
    t1 = time.time() - t0
    print(f'Time: {t1:.2f}s')
    mdg.check(A, G, W, x, y)
    



