raw_inp = open('input.txt', 'r')
inp = [line.strip() for line in raw_inp]
color_conv = {'red': 'r', 'green': 'g', 'blue':'b'}
games = []
for line in inp:
    new_game = []
    raw_rounds = line.split(':')[1].split(';')
    for raw_round in raw_rounds:
        new_round = []
        raw_draws = raw_round.split(',')
        for raw_draw in raw_draws:
            r_draw = raw_draw.split(' ')[1:]
            try:
                new_round.append([color_conv[r_draw[1]], int(r_draw[0])])
            except:
                print(r_draw)
        new_game.append(new_round)
    games.append(new_game)

def wrapper(_round, isolated_list, color):
    try:
        return _round[isolated_list.index(color)][1]
    except:
        return 0

def part1():
    s = 0
    max_values = {'r':12, 'g':13, 'b':14}
    for indx, game in enumerate(games):
        if all([max([wrapper(_round, [draw[0] for draw in _round], color) for _round in game]) <= max_values[color] for color in max_values.keys()]):
            s += indx + 1
    print(s)
            
part1() #=>2551

def prod(l):
    p = 1
    for x in l:
        p *= x
    return p

def part2():
    s = 0
    for game in games:
        s += prod([max([wrapper(_round, [draw[0] for draw in _round], color) for _round in game]) for color in color_conv.values()])
    print(s)

part2() #=>62811