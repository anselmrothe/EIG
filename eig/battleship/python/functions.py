import numpy as np

def equal(a, b):
    return a == b

def set_equal(s):
    if isinstance(s, set):
        return len(s) == 1
    else:
        t = s[0]
        for i in s:
            if not i == t: return False
        return True
            
def greater(a, b):
    return a > b

def less(a, b):
    return a < b

def plus(a, b):
    return a + b

def minus(a, b):
    return a - b

def sum_op(s):
    return sum(s)

def and_op(a, b):
    return a and b

def or_op(a, b):
    return a or b

def not_op(a):
    return not a

def row(l):
    return l[0]

def col(l):
    return l[1]

def topleft(setl):
    loc = (1000, 1000)
    for l in setl:
        if l[0] < loc[0] or (l[0] == loc[0] and l[1] < loc[1]):
            loc = l
    return loc

def bottomright(setl):
    loc = (0, 0)
    for l in setl:
        if l[0] > loc[0] or (l[0] == loc[0] and l[1] > loc[1]):
            loc = l
    return loc

def set_size(s):
    return len(s)

def is_subset(s1, s2):
    for i in s1:
        if i not in s2:
            return False
    return True

def color_fn(hypothesis, loc):
    return hypothesis.board[loc]

def orient_fn(hypothesis, s):
    for ship in hypothesis.ships:
        if ship.ship_label == s:
            return ship.orientation
    raise ValueError("No ship labeled {} found.".format(s))

def touch_fn(hypothesis, s1, s2):
    ship1, ship2 = None, None
    for ship in hypothesis.ships:
        if ship.ship_label == s1:
            ship1 = ship
        if ship.ship_label == s2:
            ship2 = ship
    if ship1 == None or ship2 == None:
        raise ValueError("No ship labeled {} found.".format(s1 if ship1 is None else s2))
    def ship_tiles(ship):
        locs = [ship.topleft]
        loc = ship.topleft
        if ship.orientation == 'H':
            loc_step = (0, 1)
        elif ship.orientation == 'V':
            loc_step = (1, 0)
        loc = (loc[0] + loc_step[0], loc[1] + loc_step[1])
        for _ in range(ship.size - 1):
            locs.append(loc)
        return locs
    ship1_locs = ship_tiles(ship1)
    ship2_locs = ship_tiles(ship2)
    for t1 in ship1_locs:
        min_dist = 100000
        for t2 in ship2_locs:
            dist = abs(t1[0] - t2[0]) + abs(t1[1] - t2[1])
            min_dist = min(min_dist, dist)
        if min_dist == 1: return True
    return False

def size_fn(hypothesis, s):
    for ship in hypothesis.ships:
        if ship.ship_label == s:
            return ship.size
    raise ValueError("No ship labeled {} found".format(s))

def colored_tiles_fn(hypothesis, s):
    tiles = np.argwhere(hypothesis.board == s)
    return set([(x, y) for x, y in tiles])

def any_op(s):
    print(s)
    return any(s)

def all_op(s):
    return all(s)

def map_op(func, s):
    return [func(x) for x in s]

def set_op(*args):
    return set(args)

def set_diff(s1, s2):
    if isinstance(s1, list): s1 = set(s1)
    if isinstance(s2, list): s2 = set(s2)
    return s1 - s2

def union(s1, s2):
    if isinstance(s1, list): s1 = set(s1)
    if isinstance(s2, list): s2 = set(s2)
    return s1 | s2

def intersect(s1, s2):
    if isinstance(s1, list): s1 = set(s1)
    if isinstance(s2, list): s2 = set(s2)
    return s1 & s2

def unique(s):
    return set(s)