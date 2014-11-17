"""A simple implementation Conway's game of life to demonstrate sets and tuples in Python.
This implementation is intentionally kept naive for simplicity."""

__author__ = "Hovis <hovis_biddle@symantec.com>"

# CONSTANTS
# I'm bounding the world to keep logic and display trivial, but using
#  a set for state allows practically unlimited board size!
BOUND = 15
DELAY = 1 #seconds

# GLOBALS

# These are some pre-defined patterns
spinner = set([(1, 0), (1, 1), (1, 2)])
glider = set([(9, 6), (9, 7), (9, 8), (10, 6), (11, 7)])
beehive = set([(1, 10), (2, 9), (2, 11), (3, 9), (3, 11), (4, 10)])
spinnersplosion = set([(6, 7), (7, 7), (8, 7), (7, 9)])

globalboard = spinner.union(glider)


def iterate(board):
    """ Return the next generation of the passed board.
    
    >>> spinner = set([(1, 0), (1, 1), (1, 2)])
    >>> iterate(spinner)
    set((0, 1), (1, 1), (2, 1))
    """
    # Sets are mutable, if we edit it directly we'll screw things up because
    # LIFE is supposed to iterate a whole universe at a time
    next_board = set()

    # Let's get our locations using a comprehension instead of nested loops.
    # The comprehension evaluates to a generator that returns tuples.
    # If we made a list from the generator, it would look like: [(0,0), (0,1), (0,2), ..., (14, 14)]
    for location in ((x, y) for x in range(BOUND) for y in range(BOUND)):
        # location is a 2-tuple that corresponds to an x, y coordinate
        if cell_next_state( is_alive(location), neighbor_count(location) ):
            next_board.add(location)
    return next_board

def cell_next_state(alive, neighbors):
    """ Return True or False depending on whether the given cell should be alive in the next generation.

    Operates according to Conway's original rules (B3/S23).
    These rules mean that an dead cell should become alive if it has 3 live neighbors, 
    and an alive cell should stay alive if it has 2 or 3 live neighbors,  otherwise the live cell should die.
    
    Examples:

    >>> cell_next_state(alive=True, neighbors=2)
    True

    >>> cell_next_state(alive=True, neighbors=3)
    True

    >>> cell_next_state(alive=False, neighbors=3)
    True

    >>> cell_next_state(alive=False, neighbors=2)
    False

    >>> cell_next_state(alive=False, neighbors=4)
    False
    """

    # There are shorter ways of structuring this logic, but this more closely
    # represents the description of the logic ("B3/S23")
    if alive:
        return neighbors in (2, 3)
        #return neighbors == 2 or neighbors == 3
    else:
        return neighbors == 3

# board=globalboard means to use the global variable board if we don't explicitly pass one
# We're using this little hack so that I can write doctests for a function that uses global vars
# In real life, we really don't want to use global variables and we shouldn't need to do this here.
def neighbor_count(location, board=globalboard):
    """ Returns the number of neighbor cells that are "alive" (in the set).

    >>> testboard = set([(0,0), (2,1)])
    >>> neighbor_count((1,1), testboard)
    2

    The board is generated using a comprehension. Yay for expressiveness!
    >>> testboard = set([(x, y) for x in (0,1,2) for y in (0,1,2)])
    >>> neighbor_count((1,1), testboard)
    8
    """
    count = 0
    for neighbor in get_neighbors(location):
        if is_alive(neighbor, board): #If we don't pass the board through, the tests will fail. (more hacks because global state sucks)
            count += 1
    return count

def is_alive(location, board=globalboard):
    """ Return True if the cell in location is alive, False if dead

    >>> testboard = set([(0,0)])

    >>> location = 0, 0
    >>> is_alive(location, testboard)
    True

    >>> location = 0, 1
    >>> is_alive(location, testboard)
    False
    """
    # Our board is a set of all the "alive" cell locations. 
    # Any cell locations not in the set are implicitly "dead".
    return location in board

def get_neighbors(location, bound=BOUND):
    """Returns a tuple of locations that are immediately adjacent to the given location, wrapping around bounds.

    >>> get_neighbors((1,1))
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]

    >>> get_neighbors(location=(0,0), bound=12)
    [(11, 11), (11, 0), (11, 1), (0, 11), (0, 1), (1, 11), (1, 0), (1, 1)]
    """
    # I'm going to use a mutable list to keep track of my neighbors, and then return it
    # This can absolutely be optimized with a generator, we should do that later
    x, y = location
    neighbors = []
    for offset_x in (-1, 0, 1):
        for offset_y in (-1, 0, 1):
            nx = (x + offset_x) % bound
            ny = (y + offset_y) % bound
            if (nx, ny) == location:
                continue # The location we were passed is not a neighbor
            neighbors.append((nx, ny))
    return neighbors

def neighbors_generator(location, bound=BOUND):
    """
    Like get_neighbors(), but return a generator instead

    For testing, we'll pass the generator to tuple() to see what it yields.
    >>> loc = 1, 1
    >>> tuple(neighbors_generator(loc))
    ((0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2))

    >>> loc = 0, 0
    >>> tuple(neighbors_generator(loc, bound=12))
    ((11, 11), (11, 0), (11, 1), (0, 11), (0, 1), (1, 11), (1, 0), (1, 1))
    """
    x, y = location
    return (
            ( (x + offset_x) % bound, (y + offset_y) % bound ) # tuple specification
            for offset_x in (-1, 0, 1)
            for offset_y in (-1, 0, 1)
            if not (offset_x == 0 and offset_y == 0) # exclude the center
        )

def _test():
    import doctest
    print(doctest.testmod())

def _main():
    import time

    global globalboard
    # Draw stuff, break on Ctrl-C
    while True:
        draw_board(globalboard)
        time.sleep(DELAY) #seconds
        globalboard = iterate(globalboard)

def draw_board(screen, board=globalboard):
    for x in range(BOUND):
        for y in range(BOUND):
            print( "@" if is_alive((x,y)) else "`", end='')
        print() #need that newline
    print()

if __name__ == "__main__":
    import sys
    sys.exit(_main())
