raw_inp = open('input.txt', 'r')
inp = [line.strip() for line in raw_inp]

def input_conversion(inp):
    """
    Converts the basic txt input to 2d array with 0: void, 1: galaxy
    """
    grid = []
    for line in inp:
        new_row = []
        for c in line:
            if c == '.':
                new_row.append(0)
            elif c == '#':
                new_row.append(1)
            else:
                print(c)
        grid.append(new_row)
    """
    grid (default):
    [[0, 0, 1, 0, 0, ..., 0, 0, 0, 0, 0]]
    """
    return grid

def get_empty_rows(raw_universe):
    empty_indices = []
    for index, row in enumerate(raw_universe):
        is_empty = True
        for c in row:
            if c != 0:
                is_empty = False
                break
        if is_empty:
            empty_indices.append(index)
    return empty_indices

def get_empty_columns(raw_universe):
    empty_indices = []
    for index in range(len(raw_universe[0])):
        is_empty = True
        for row in raw_universe:
            if row[index] != 0:
                is_empty = False
                break
        if is_empty:
            empty_indices.append(index)
    return empty_indices

def expand_universe(raw_universe):
    empty_rows = get_empty_rows(raw_universe)
    empty_colums = get_empty_columns(raw_universe)
    new_num_rows, new_num_columns = len(raw_universe)+len(empty_rows), len(raw_universe[0])+len(empty_colums)
    expanded_universe = []
    for row_index, row in enumerate(raw_universe):
        if not row_index in empty_rows:
            new_row = []
            for column_index, c in enumerate(row):
                new_row.append(c)
                if column_index in empty_colums:
                    new_row.append(0)
            expanded_universe.append(new_row)
        else:
            expanded_universe.append([0 for x in range(new_num_columns)])
            expanded_universe.append([0 for x in range(new_num_columns)])
    if len(expanded_universe) != new_num_rows:
        print('universe too small')
    return expanded_universe

def get_galaxy_positions(expanded_universe):
    galaxy_positions = []
    for y, row in enumerate(expanded_universe):
        for x, c in enumerate(row):
            if c == 1:
                galaxy_positions.append([y,x])
    return galaxy_positions

def distance_between_points(a, b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def get_sum_distances_between_galaxy(galaxy_position, list_galaxy_positions):
    s = 0
    for compare_galaxy in list_galaxy_positions:
        s += distance_between_points(galaxy_position, compare_galaxy)
    return s

def part1(raw_universe):
    expanded_universe = expand_universe(raw_universe)
    galaxy_positions = get_galaxy_positions(expanded_universe)
    total_distances = 0
    for x, galaxy in enumerate(galaxy_positions):
        total_distances += get_sum_distances_between_galaxy(galaxy, galaxy_positions[x+1:])
    return total_distances

def count_traversing_empty_rows(galaxyA, galaxyB, empty_rows):
    if galaxyA[0] == galaxyB[0]:
        return 0
    elif galaxyA[0] > galaxyB[0]:
        (galaxyA, galaxyB) = (galaxyB, galaxyA)
    counter = 0
    for x in range(galaxyA[0]+1,galaxyB[0]):
        if x in empty_rows:
            counter += 1
    return counter

def count_traversing_empty_columns(galaxyA, galaxyB, empty_columns):
    if galaxyA[1] == galaxyB[1]:
        return 0
    elif galaxyA[1] > galaxyB[1]:
        (galaxyA, galaxyB) = (galaxyB, galaxyA)
    counter = 0
    for x in range(galaxyA[1]+1,galaxyB[1]):
        if x in empty_columns:
            counter += 1
    return counter

def distance_between_expanded_points(a, b, empty_rows, empty_columns, expansion_factor):
    #expansion_factor-1 bcs distance_between_points includes empty rows/columns and expansion_factor does too
    return distance_between_points(a,b) + (expansion_factor-1)*(count_traversing_empty_rows(a,b,empty_rows)+count_traversing_empty_columns(a,b,empty_columns))

def get_sum_distances_between_expanding_galaxy(galaxy_position, list_galaxy_positions, empty_rows, empty_columns, expansion_factor):
    s = 0
    for compare_galaxy in list_galaxy_positions:
        s += distance_between_expanded_points(galaxy_position, compare_galaxy, empty_rows, empty_columns, expansion_factor)
    return s

def part2(raw_universe):
    empty_rows, empty_columns = get_empty_rows(raw_universe), get_empty_columns(raw_universe)
    expansion_factor = 1_000_000
    galaxy_positions = get_galaxy_positions(raw_universe)
    total_distances = 0
    for x, galaxy in enumerate(galaxy_positions):
        total_distances += get_sum_distances_between_expanding_galaxy(galaxy, galaxy_positions[x+1:], empty_rows, empty_columns, expansion_factor)
    return total_distances


universe = input_conversion(inp)
sol1 = part1(universe) #=>9550717

universe = input_conversion(inp)
sol2 = part2(universe) #=>648_458_253_817

print(sol1, sol2)