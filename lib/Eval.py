from math import log

WGT_ALIVE = 40000
WGT_MERGE = 0.450
WGT_LEVEL = 0.045
WGT_ORDER = 1.000
WGT_VALUE = 0.133

##############################################################################
# MAIN EVALUATION FUNCTION
# Row- and column-based weighted combination of heuristics
##############################################################################

def eval(grid, over):
    lines = []

    for i in xrange(4):
        row = [tile for tile in grid.map[i] if tile]
        lines.append(row)

    for j in xrange(4):
        col = [row[j] for row in grid.map if row[j]]
        lines.append(col)

    score = 0

    for index, line in enumerate(lines):
        score += (
            WGT_ALIVE / 8  * (1 - over) + \
            WGT_LEVEL * evalLevel(line) + \
            WGT_ORDER * evalOrder(line) + \
            WGT_MERGE * evalMerge(line) + \
            WGT_VALUE * evalValue(line) * \
            (index % 4 - index / 4 - 1)   \
        )

    return score

##############################################################################
# (1) LEVEL EVALUATION
# Penalizes differences in value levels between adjacent tiles
##############################################################################

def evalLevel(line):
    return reduce(lambda s, (i, j): \
        s - abs(rank(j) ** 2 - rank(i) ** 2), \
    zip(line, line[1:]), 0)

##############################################################################
# (2) ORDER EVALUATION
# Penalizes violations of monotonic order along a row or column
##############################################################################

def evalOrder(line):
    return reduce(lambda s, (i, j): \
        s - max(0, rank(i) ** 2 - rank(j) ** 2), \
    zip(line, line[1:]), 0)

##############################################################################
# (3) MERGE EVALUATION
# Rewards value-adjusted potential merges betewen adjacent tiles
##############################################################################

def evalMerge(line):
    return reduce(lambda s, (i, j): \
        s + (i == j) * i, \
    zip(line, line[1:]), 0)

##############################################################################
# (4) VALUE EVALUATION
# Rewards values, which are then scaled along a diagonal gradient
##############################################################################

def evalValue(line):
    return reduce(lambda s, i: \
        s + i, \
    line, 0)

##############################################################################
# LOG BASE 2 HELPER
##############################################################################

def rank(num):
    return log(num, 2)
