raw_inp = open('input.txt', 'r')
inp = [line.strip() for line in raw_inp]

def input_conversion(inp):
    """
    Converts the basic txt input to 2d array with 0: ground, 1: vertical, 2: horizontal, 3: W-N J, 4: N-E L, 5: E-S F, 6: S-W 7 and 7: Start S
    """
    grid = []
    for line in inp:
        new_row = []
        for c in line:
            new_row.append(convert_char_to_dirint(c))
        grid.append(new_row)
    """
    grid (default):
    [[1, 2, 4, 0, 5, 4, 2, 5, ..., 0, 5, 3, 4, 1, 6]]
    """
    return grid

def convert_char_to_dirint(c):
    char_to_dirint = {'.':0, '|':1, '-':2, 'J':3, 'L':4, 'F':5, '7':6, 'S':7}
    if char_to_dirint.get(c) != None:
        return char_to_dirint[c]
    else:
        print('Unknown Char:',c)
        return None

def convert_dirint_to_char(d):
    dirint_to_char = {0:'.', 1:'|', 2:'-', 3:'J', 4:'L', 5:'F', 6:'7', 7:'S', 8:'X', 9:' ', 10:'I'}
    if dirint_to_char.get(d) != None:
        return dirint_to_char[d]
    else:
        print('Unknown DirInt:',d)
        return None

def convertline(l):
    str_line = ''
    for dirint in l:
        str_line += convert_dirint_to_char(dirint)
    return str_line

def part1(grid):
    loop = generate_loop(grid)
    return int((len(loop)-1)/2)

def generate_loop(grid):
    start_point = find_start_point(grid)
    if start_point[0] == 0 or start_point[0] == len(grid)-1 or start_point[1] == 0 or start_point[1] == len(grid[0])-1:
        return None
    possible_loop_starts = []
    directions = get_directions()
    for direction in directions:
        y, x = start_point[0] + direction[0], start_point[1] + direction[1]
        if grid[y][x] in convert_direction_to_possible_next_dirint(direction):
            possible_loop_starts.append([y,x])
    loops = [[start_point, start] for start in possible_loop_starts]
    #bcs both loops are the same...
    loop = loops[0]
    while not (loop[-1][0] == loop[0][0] and loop[-1][1] == loop[0][1]):
        current_pipe_pos = loop[-1]
        current_pipe = grid[current_pipe_pos[0]][current_pipe_pos[1]]
        adjacent_pipe_relative_pos = convert_dirint_to_possible_direction(current_pipe)
        adjacent_pipe_pos = [[current_pipe_pos[0]+rel_pipe_pos[0], current_pipe_pos[1]+rel_pipe_pos[1]] for rel_pipe_pos in adjacent_pipe_relative_pos]
        prev_pipe_pos = loop[-2]
        if equal_pos(prev_pipe_pos, adjacent_pipe_pos[0]):
            loop.append(adjacent_pipe_pos[1])
        else:
            loop.append(adjacent_pipe_pos[0])
    return loop

def get_directions():
    return [[-1,0],[1,0],[0,-1],[0,1]]

def find_start_point(grid):
    start_point = []
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == 7:
                return [y,x]
    return None

def convert_direction_to_possible_dirint(direction):
    if direction[0] == -1 and direction[1] == 0:
        return [1, 3, 4]
    elif direction[0] == 1 and direction[1] == 0:
        return [1, 5, 6]
    elif direction[0] == 0 and direction[1] == -1:
        return [2, 3, 6]
    elif direction[0] == 0 and direction[1] == 1:
        return [2, 4, 5]
    else:
        print('Unknown direction:', direction)
        return None

def find_dirint_from_directions(directionA, directionB):
    possible_dirintA, possible_dirintB = convert_direction_to_possible_dirint(directionA), convert_direction_to_possible_dirint(directionB)
    return list(set(possible_dirintA) & set(possible_dirintB))[0]

def convert_direction_to_possible_next_dirint(direction):
    if direction[0] == -1 and direction[1] == 0:
        return [1, 5, 6]
    elif direction[0] == 1 and direction[1] == 0:
        return [1, 3, 4]
    elif direction[0] == 0 and direction[1] == -1:
        return [2, 4, 5]
    elif direction[0] == 0 and direction[1] == 1:
        return [2, 3, 6]
    else:
        print('Unknown direction:', direction)
        return None

def convert_dirint_to_possible_direction(dirint):
    conversions = {0:[], 1:[[-1,0],[1,0]], 2:[[0,-1],[0,1]], 3:[[-1,0],[0,-1]], 4:[[-1,0],[0,1]], 5:[[1,0],[0,1]], 6:[[1,0],[0,-1]]}
    if conversions.get(dirint) != None:
        return conversions[dirint]
    else:
        print('Unknown dirint:', dirint)
        return []

def replace_start_point(grid, loop):
    start_point_pos = loop[0]
    attaching_pipes_pos = [loop[-2], loop[1]]
    attaching_pipes_pos_dif = [[attaching_pipes_pos[0][0]-start_point_pos[0],attaching_pipes_pos[0][1]-start_point_pos[1]], [attaching_pipes_pos[1][0]-start_point_pos[0],attaching_pipes_pos[1][1]-start_point_pos[1]]]
    replacing_pipe = find_dirint_from_directions(attaching_pipes_pos_dif[0], attaching_pipes_pos_dif[1])
    grid[start_point_pos[0]][start_point_pos[1]] = replacing_pipe
    return replacing_pipe

def equal_pos(pos1, pos2):
    return pos1[0] == pos2[0] and pos1[1] == pos2[1]

def pos_dif(pos1, pos2, sum=False):
    if not sum:
        return [pos2[0]-pos1[0],pos2[1]-pos1[1]]
    else:
        return [pos2[0]+pos1[0],pos2[1]+pos1[1]]


def part2(grid):
    new_grid = [[0 if x == 0 else 9 for x in line] for line in grid]
    loop = generate_loop(grid)
    
    for pipe_pos in loop:
        y, x = pipe_pos
        new_grid[y][x] = grid[y][x]

    replacing_pipe = replace_start_point(new_grid, loop)
    if replacing_pipe == 3 or replacing_pipe == 6:
        relative_in_between_pos = [[-1,-1],[1,-1]]
    elif replacing_pipe == 4 or replacing_pipe == 5:
        relative_in_between_pos = [[-1,1],[1,1]]
    else:
        relative_in_between_pos = [[-1,-1],[1,1]]

    for ri, relative_pos in enumerate(relative_in_between_pos):
        adjacent_tiles = []
        for x, tile_pos in enumerate(loop):
            if x == 0:
                continue
            prev_tile_pos = loop[x-1]
            prev_tile = new_grid[prev_tile_pos[0]][prev_tile_pos[1]]
            moved_direction = pos_dif(prev_tile_pos, tile_pos)
            if moved_direction[0] == -1 and moved_direction[1] == 0:
                #{'.':0, '|':1, '-':2, 'J':3, 'L':4, 'F':5, '7':6, 'S':7}
                if relative_pos[0] == 1 and relative_pos[1] == -1 and prev_tile == 3:
                    #J or |L
                    adjacent_tiles.extend([pos_dif(x, prev_tile_pos, sum=True) for x in [[1,0],[0,1]]])
                    relative_pos[1] = 1
                elif relative_pos[0] == 1 and relative_pos[1] == 1 and prev_tile == 4:
                    #L or J|
                    adjacent_tiles.extend([pos_dif(x, prev_tile_pos, sum=True) for x in [[1,0],[0,-1]]])
                    relative_pos[1] = -1
                else:
                    if relative_pos[1] == -1:
                        adjacent_tiles.append(pos_dif([0,-1], prev_tile_pos, sum=True))
                    elif relative_pos[1] == 1:
                        adjacent_tiles.append(pos_dif([0,1], prev_tile_pos, sum=True))
                relative_pos[0] = 1
            elif moved_direction[0] == 1 and moved_direction[1] == 0:
                if relative_pos[0] == -1 and relative_pos[1] == -1 and prev_tile == 6:
                    #7 or |F
                    adjacent_tiles.extend([pos_dif(x, prev_tile_pos, sum=True) for x in [[-1,0],[0,1]]])
                    relative_pos[1] = 1
                elif relative_pos[0] == -1 and relative_pos[1] == 1 and prev_tile == 5:
                    #F or 7|
                    adjacent_tiles.extend([pos_dif(x, prev_tile_pos, sum=True) for x in [[-1,0],[0,-1]]])
                    relative_pos[1] = -1
                else:
                    if relative_pos[1] == -1:
                        adjacent_tiles.append(pos_dif([0,-1], prev_tile_pos, sum=True))
                    elif relative_pos[1] == 1:
                        adjacent_tiles.append(pos_dif([0,1], prev_tile_pos, sum=True))
                relative_pos[0] = -1
            elif moved_direction[0] == 0 and moved_direction[1] == -1:
                if relative_pos[0] == -1 and relative_pos[1] == 1 and prev_tile == 3:
                    #J or -7
                    adjacent_tiles.extend([pos_dif(x, prev_tile_pos, sum=True) for x in [[1,0],[0,1]]])
                    relative_pos[0] = 1
                elif relative_pos[0] == 1 and relative_pos[1] == 1 and prev_tile == 6:
                    #7 or J-
                    adjacent_tiles.extend([pos_dif(x, prev_tile_pos, sum=True) for x in [[-1,0],[0,1]]])
                    relative_pos[0] = -1
                else:
                    if relative_pos[0] == -1:
                        adjacent_tiles.append(pos_dif([-1,0], prev_tile_pos, sum=True))
                    elif relative_pos[0] == 1:
                        adjacent_tiles.append(pos_dif([1,0], prev_tile_pos, sum=True))
                relative_pos[1] = 1
            elif moved_direction[0] == 0 and moved_direction[1] == 1:
                if relative_pos[0] == -1 and relative_pos[1] == -1 and prev_tile == 4:
                    #L or -F
                    adjacent_tiles.extend([pos_dif(x, prev_tile_pos, sum=True) for x in [[1,0],[0,-1]]])
                    relative_pos[0] = 1
                elif relative_pos[0] == 1 and relative_pos[1] == -1 and prev_tile == 5:
                    #F or L-
                    adjacent_tiles.extend([pos_dif(x, prev_tile_pos, sum=True) for x in [[-1,0],[0,-1]]])
                    relative_pos[0] = -1
                else:
                    if relative_pos[0] == -1:
                        adjacent_tiles.append(pos_dif([-1,0], prev_tile_pos, sum=True))
                    elif relative_pos[0] == 1:
                        adjacent_tiles.append(pos_dif([1,0], prev_tile_pos, sum=True))
                relative_pos[1] = -1
        adjacent_tiles = remove_duplicate_tiles(new_grid, adjacent_tiles)
        num_ground_tiles = 0
        outside_loop = False
        tiles_to_test = {generate_hash(tile):[True, tile] for tile in adjacent_tiles}
        while sum([test[0] for test in tiles_to_test.values()]) > 0:
            new_tiles_to_test = {}
            for is_open, tile in tiles_to_test.values():
                if not is_open:
                    continue
                tiles_to_test[generate_hash(tile)][0] = False
                y, x = tile
                if new_grid[y][x] == 0 or new_grid[y][x] == 9:
                    num_ground_tiles += 1
                neighbours = [pos_dif(tile, x, sum=True) for x in [[-1,0],[1,0],[0,-1],[0,1]]]
                for neighbour in neighbours:
                    y, x = neighbour
                    if tiles_to_test.get(generate_hash(neighbour)) == None and in_grid(new_grid, neighbour) and (new_grid[y][x] == 0 or new_grid[y][x] == 9):
                        new_tiles_to_test[generate_hash(neighbour)] = [True, neighbour]
                    elif not in_grid(new_grid, neighbour):
                        outside_loop = True
            for k, v in new_tiles_to_test.items():
                tiles_to_test[k] = v
        if not outside_loop:
            return num_ground_tiles
    return None

def remove_duplicate_tiles(grid, tiles):
    unique_tiles = {}
    for t in tiles:
        if unique_tiles.get(generate_hash(t)) == None and in_grid(grid,t):
            if grid[t[0]][t[1]] == 9 or grid[t[0]][t[1]] == 0:
                unique_tiles[generate_hash(t)] = t
    return list(unique_tiles.values())

def in_grid(grid, tile):
    return tile[0] > 0 and tile[1] > 0 and len(grid) > tile[0] and len(grid[0]) > tile[1]

def generate_hash(tile):
    return 1000*tile[0]+tile[1]

grid = input_conversion(inp)
sol1 = part1(grid) #=>7066

grid = input_conversion(inp)
sol2 = part2(grid) #=>401

print(sol1, sol2)