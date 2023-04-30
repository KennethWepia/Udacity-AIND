from collections import defaultdict


rows = 'ABCDEFGHI'
cols = '123456789'
boxes = [r + c for r in rows for c in cols]
history = {}  # history must be declared here so that it exists in the assign_values scope


def extract_units(unitlist, boxes):
    
    unitlist(list)
        a list containing "units" (rows, columns, diagonals, etc.) of boxes

    boxes(list)
        a list of strings identifying each box on a sudoku board (e.g., "A1", "C7", etc.)

    Returns
    -------
    dict
        a dictionary with a key for each box (string) whose value is a list
        containing the units that the box belongs to (i.e., the "member units")
    
    units = defaultdict(list)
    for current_box in boxes:
        for unit in unitlist:
            if current_box in unit:
                # defaultdict avoids this raising a KeyError when new keys are added
                units[current_box].append(unit)
    return units


def extract_peers(units, boxes):
    
    units(dict)
        a dictionary with a key for each box (string) whose value is a list
        containing the units that the box belongs to (i.e., the "member units")

    boxes(list)
        a list of strings identifying each box on a sudoku board (e.g., "A1", "C7", etc.)

   
    # the value for keys that aren't in the dictionary are initialized as an empty list
    peers = defaultdict(set)  # set avoids duplicates
    for key_box in boxes:
        for unit in units[key_box]:
            for peer_box in unit:
                if peer_box != key_box:
                    # defaultdict avoids this raising a KeyError when new keys are added
                    peers[key_box].add(peer_box)
    return peers


def assign_value(values, box, value):
   
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    prev = values2grid(values)
    values[box] = value
    if len(value) == 1:
        history[values2grid(values)] = (prev, (box, value))
    return values

def cross(A, B):
    """Cross product of elements in A and elements in B """
    return [x+y for x in A for y in B]


def values2grid(values):
    
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

   
    res = []
    for r in rows:
        for c in cols:
            v = values[r + c]
            res.append(v if len(v) == 1 else '.')
    return ''.join(res)


def grid2values(grid):
    
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    
    
    sudoku_grid = {}
    for val, key in zip(grid, boxes):
        if val == '.':
            sudoku_grid[key] = '123456789'
        else:
            sudoku_grid[key] = val
    return sudoku_grid


def display(values):
    
        values(dict): The sudoku in dictionary form
    
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print()


def reconstruct(values, history):
   
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    history(dict)
        
    path = []
    prev = values2grid(values)
    while prev in history:
        prev, step = history[prev]
        path.append(step)
    return path[::-1]
