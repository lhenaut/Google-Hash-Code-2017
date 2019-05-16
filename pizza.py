import numpy as np

def process_input():
    #input: R C L H, then R lines with C chars
    r,c,l,h = map(int, input().strip().split(' '))
    pizza = []
    for ri in range(r):
        pizza.append(list(input().strip()))

    # print(r,c,l,h)
    # print(np.array(pizza))
    return r, c, l, h, pizza

# output: number of slices, coordinates
# coordinate: r1 c1 r2 c2


def bigh(pizza, l, max_size, square):
    """
    find the biggest possible slice between max_size and min
    size and recursively find biggest possible slices to left
    over parts.
    return: list of slices [slice1, slice2, ...]
            where slice = (sr1, sc1, sr2, sc2)
    """

    r1, c1, r2, c2 = square  # get the square corners
    # Base case: empty square
    if r1 > r2 or c1 > c2:
        return []

    # try to find a solution with size max_size or less
    limit_size = min(max_size, (r2-r1)*(c2-c1)) # check if max_size is not bigger than remaining pizza
    for sol_size in range(limit_size, 2*l, -1):
        # try to find a (or all) piece of size sol_size

        # iterate over all possible positions of the grid, left to right
        for pos_r in range(r1, r2):
            for pos_c in range(c1, c2):
                # iterate over all rectangles with size sol_size
                factors = [i for i in range(1, sol_size+1) if not sol_size%i]
                for f in factors:
                    # print(sol_size, pos_r, pos_c, f)
                    # try to fit each possible slice
                    piece = (pos_r, pos_c, pos_r+f, pos_c+sol_size//f)
                    if valid_slice(pizza, l, piece, square):
                        # find the 4 left overs (check) and their solutions
                        fixed_piece = (pos_r, pos_c, pos_r+f-1, pos_c+sol_size//f-1)
                        solution = [fixed_piece]
                        for lo_sq in left_overs(square, piece):
                            solution += bigh(pizza, l, max_size, lo_sq)
                        return solution  # TODO: should wait for best possible?

    # case no slice was ever found, return empty (0 slices)
    return []


def valid_slice(pizza, l, piece, square):
    """
    check if a piece with coordinates r1, c1, r2, c2 is valid inside
    square (sr1, sc1, sr2, sc2)
    return True or False
    """

    (r1, c1, r2, c2) = piece
    (sr1, sc1, sr2, sc2) = square
    # first check if dimensions fit
    if (r2 > sr2 or c2 > sc2 or r1 < sr1 or c1 < sc1):
        return False

    # check if number of elements make sense
    ms = 0
    ts = 0
    for r in range(r1, r2):
        for c in range(c1, c2):
            if pizza[r][c] == "M":
                ms += 1
            elif pizza[r][c] == "T":
                ts += 1

    if ms >= l and ts >= l:
        return True
    else:
        # print("False because:", ms, ts)
        return False


def left_overs(square, hole):
    """
    given a hole in a square, return the left over parts
    """

    (sr1, sc1, sr2, sc2) = square
    (hr1, hc1, hr2, hc2) = hole

    # do vertical cuts

    return [(sr1, sc1, sr2, hc1),  # left
            (sr1, hc1, hr1, hc2),  # up
            (hr2, hc1, sr2, hc2),  # down
            (sr1, hc2, sr2, sc2)]  # right
    # TODO: test other solutions (horizontal), 8 spaces
# validate slices


def points(solution):
    return sum((r2-r1)*(c2-c1) for (r1, c1, r2, c2) in solution)


def google_print(solution):
    print(len(solution))
    for s in solution:
        print(str(s)[1:-1])


if __name__ == '__main__':
    r, c, l, h, pizza = process_input()
    # find solution
    solution = bigh(pizza, l, h, (0, 0, r, c))
    # print(solution)
    # print(points(solution))
    google_print(solution)

# TODO: validate
