"""A simple implementation Conway's game of life to demonstrate sets and tuples in Python.
This implementation is intentionally kept naive for simplicity."""

BOUND = 15
DELAY = 0.2 #seconds

def iterate(board):
    """ Return the next generation of the passed board. """
    new = set() # If we mutate the set in place we'll screw things up, so we'll add to a new empty set
    for x in range(BOUND):
        for y in range(BOUND):
            is_alive = (x, y) in board
            #import pdb; pdb.set_trace()
            if next_state(is_alive, neighbor_count((x,y), board)):
                new.add((x, y))
    return new

def draw_board(screen, board):
    for x in range(BOUND):
        for y in range(BOUND):
            screen.addstr(y, x, "@" if (x, y) in board else "`")
    screen.refresh()

def next_state(alive, neighbors):
    """ Return True or False depending on whether the given cell should be alive in the next generation.

    Operates according to Conway's original rules (B3/S23).

    >>> next_state(True, 2)
    True

    >>> next_state(True, 3)
    True

    >>> next_state(False, 3)
    True

    >>> next_state(False, 2)
    False

    >>> next_state(False, 4)
    False
    """

    if alive:
        if neighbors in (2, 3):
            return True #STAYALIVE
        else:
            return False #DEATH
    else:
        if neighbors == 3:
            return True #BIRTH
        else:
            return False #STAYDEAD

def neighbor_count(loc, board):
    """ Returns the number of neighbor cells that are "alive" (in the set).

    >>> neighbor_count((1,1), board=set([(0,0), (0,1)]))
    2

    This one tests a board that's fully "alive".  The funny expression on board is a list comprehension we'll learn about later.
    >>> neighbor_count((1,1), board=set([(x, y) for x in (0,1,2) for y in (0,1,2)]))
    8
    """
    count = 0
    for n in get_neighbors(loc):
        if n in board:
            count += 1
    return count

def get_neighbors(loc, bound=BOUND):
    """Returns a tuple of locations that are immediately adjacent to the given location, wrapping around bounds.

    >>> get_neighbors((1,1))
    ((0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2))

    >>> get_neighbors(loc=(0,0), bound=12)
    ((11, 11), (11, 0), (11, 1), (0, 11), (0, 1), (1, 11), (1, 0), (1, 1))
    """
    #TODO: doctest
    # I'm going to use a mutable list to keep track of my neighbors for returning later.
    # Later, we may learn how to use the yield expression and optimize this.
    x, y = loc
    neighbors = []
    for offset_x in (-1, 0, 1):
        for offset_y in (-1, 0, 1):
            nx = (x + offset_x) % bound
            ny = (y + offset_y) % bound
            if (nx, ny) == loc:
                continue # The location we were passed is not a neighbor
            neighbors.append((nx, ny))
    return tuple(neighbors)

def _test():
    import doctest
    print(doctest.testmod())

def _main(stdscr):
    import time

    #Here are three patterns defined as sets
    glider = set([(9, 6), (9, 7), (9, 8), (10, 6), (11, 7)])
    spinner = set([(11, 1), (11, 2), (11, 3)])
    beehive = set([(1, 10), (2, 9), (2, 11), (3, 9), (3, 11), (4, 10)])
    spinnersplosion = set([(6, 7), (7, 7), (8, 7), (7, 9)])

    board = glider
    #board = spinnersplosion
    #board = set.union(glider, beehive, spinner)

    # Start curses and bail on keypress
    stdscr.clear()
    stdscr.nodelay(True)
    while True:
        draw_board(stdscr, board)
        time.sleep(DELAY) #seconds

        board = iterate(board)

        if(stdscr.getch() >= 0):
            break

if __name__ == "__main__":
    from curses import wrapper
    import sys
    sys.exit(wrapper(_main))
