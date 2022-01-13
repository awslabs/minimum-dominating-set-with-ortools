import numpy as np


def generate_random_problem(seed=0):

    n = 1000
    m = n // 10
    r = 1.2

    np.random.seed(seed)
    w = (1 + 0.01 * np.random.randn(m)).tolist()

    cr = int(n * r)
    a = [[i] for i in range(n)]

    for i, j in zip(np.random.randint(0, n, cr), np.random.randint(0, n, cr)):
        if j not in a[i]:
            a[i].append(int(j))
            a[j].append(int(i))

    g = [[np.random.randint(0, m)] for i in range(n)]
    gr = int(n * r)
    for i, j in zip(np.random.randint(0, n, gr), np.random.randint(0, m, gr)):
        if j not in g[i]:
            g[i].append(int(j))

    return a, g, w
