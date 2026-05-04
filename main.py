from collections import deque
import heapq
import random
import time


GOAL = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0)
)

def print_state(state):
    for row in state:
        print(" ".join(str(x) if x != 0 else "_" for x in row))
    print()

def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def swap(state, r1, c1, r2, c2):
    s = [list(row) for row in state]
    s[r1][c1], s[r2][c2] = s[r2][c2], s[r1][c1]
    return tuple(tuple(row) for row in s)

def neighbors(state):
    r, c = find_zero(state)
    moves = []
    dirs = [(-1,0,"Up"), (1,0,"Down"), (0,-1,"Left"), (0,1,"Right")]

    for dr, dc, name in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            moves.append((name, swap(state, r, c, nr, nc)))

    return moves

def random_start(goal=GOAL, steps=20):
    s = goal
    for _ in range(steps):
        _, s = random.choice(neighbors(s))
    return s

def path_build(parent, action, start, goal):
    p = []
    cur = goal
    while cur != start:
        p.append((action[cur], cur))
        cur = parent[cur]
    p.reverse()
    return p

def misplaced(state):
    c = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != GOAL[i][j]:
                c += 1
    return c

def manhattan(state):
    pos = {}
    for i in range(3):
        for j in range(3):
            pos[GOAL[i][j]] = (i, j)

    d = 0
    for i in range(3):
        for j in range(3):
            v = state[i][j]
            if v != 0:
                gi, gj = pos[v]
                d += abs(i - gi) + abs(j - gj)
    return d


def bfs(start):
    q = deque([start])
    visited = {start}
    parent = {}
    act = {}
    exp = 0

    while q:
        s = q.popleft()
        exp += 1
        if s == GOAL:
            return path_build(parent, act, start, GOAL), exp

        for a, n in neighbors(s):
            if n not in visited:
                visited.add(n)
                parent[n] = s
                act[n] = a
                q.append(n)

    return None, exp


def dfs(start, limit=30):
    stack = [(start, 0)]
    visited = {start}
    parent = {}
    act = {}
    exp = 0

    while stack:
        s, d = stack.pop()
        exp += 1

        if s == GOAL:
            return path_build(parent, act, start, GOAL), exp

        if d < limit:
            for a, n in neighbors(s)[::-1]:
                if n not in visited:
                    visited.add(n)
                    parent[n] = s
                    act[n] = a
                    stack.append((n, d+1))

    return None, exp


def ucs(start):
    pq = [(0, start)]
    parent = {}
    act = {}
    cost = {start: 0}
    exp = 0

    while pq:
        g, s = heapq.heappop(pq)
        exp += 1

        if s == GOAL:
            return path_build(parent, act, start, GOAL), exp

        for a, n in neighbors(s):
            ng = g + 1
            if n not in cost or ng < cost[n]:
                cost[n] = ng
                parent[n] = s
                act[n] = a
                heapq.heappush(pq, (ng, n))

    return None, exp


def ids(start, max_d=30):
    def dls(s, g, limit, parent, act, visited, exp):
        exp[0] += 1
        if s == g:
            return True
        if limit == 0:
            return False

        for a, n in neighbors(s):
            if n not in visited:
                visited.add(n)
                parent[n] = s
                act[n] = a
                if dls(n, g, limit - 1, parent, act, visited, exp):
                    return True
        return False

    total = 0
    for depth in range(max_d + 1):
        parent = {}
        act = {}
        visited = {start}
        exp = [0]

        if dls(start, GOAL, depth, parent, act, visited, exp):
            return path_build(parent, act, start, GOAL), total + exp[0]

        total += exp[0]

    return None, total


def astar(start, h):
    pq = [(h(start), 0, start)]
    parent = {}
    act = {}
    g_cost = {start: 0}
    exp = 0

    while pq:
        f, cost, s = heapq.heappop(pq)
        exp += 1

        if s == GOAL:
            return path_build(parent, act, start, GOAL), exp

        for a, n in neighbors(s):
            ng = cost + 1
            if n not in g_cost or ng < g_cost[n]:
                g_cost[n] = ng
                parent[n] = s
                act[n] = a
                heapq.heappush(pq, (ng + h(n), ng, n))

    return None, exp



def time_run(name, func, start, times):
    t0 = time.time()
    res, exp = func(start)
    t1 = time.time()
    dt = t1 - t0

    print("---------------")
    print(name)
    print("expanded:", exp)
    print("time:", dt, "seconds")

    times[name] = dt

    if res:
        print("steps:", len(res))
    else:
        print("no solution")



def main():
    start = random_start(steps=20)

    print("Start state:")
    print_state(start)

    times = {}

    time_run("BFS", bfs, start, times)
    time_run("DFS", lambda s: dfs(s), start, times)
    time_run("UCS", ucs, start, times)
    time_run("IDS", ids, start, times)
    time_run("A* Manhattan", lambda s: astar(s, manhattan), start, times)
    time_run("A* Misplaced", lambda s: astar(s, misplaced), start, times)

    print("\n==========================")
    print("Summary (seconds):")
    for k, v in times.items():
        print(k, ":", v)



if __name__ == "__main__":
    main()
