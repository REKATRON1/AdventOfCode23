raw_inp = open('input.txt', 'r')
inp = [line.strip() for line in raw_inp]

def display_idx(l):
    if type(l) == int:
        l = [l]
    st = ''
    for n in range(len(inp[0])):
        if n in l:
            st += '#'
        else:
            st += '.'
    print(st)

def part1():
    s = 0
    for row, line in enumerate(inp):
        counted_indices = set()
        for offset in range(-1,2):
            for idx, c in enumerate(inp[min(max(0,row+offset), len(inp)-1)]):
                try:
                    int(c)
                except:
                    if c != '.':
                        counted_indices.add(max(0,idx-1))
                        counted_indices.add(idx)
                        counted_indices.add(min(idx+1, len(line)-1))
        while len(counted_indices) > 0:
            idx = list(counted_indices)[0]
            try:
                if idx != len(line)-1:
                    int(line[idx])
                    int(line[idx+1])
                    counted_indices.add(idx+1)
                else:
                    int('.')
            except:
                f = 1
                while True:
                    try:
                        s += f*int(line[idx])
                        f *= 10
                        if idx in counted_indices:
                            counted_indices.remove(idx)
                        idx -= 1
                        if idx < 0:
                            break
                    except:
                        break
            if idx in counted_indices:
                counted_indices.remove(idx)
    print(s)

part1() #=>540212


class gear():
    def __init__(self):
        self.ratios = []
    def add_ratio(self, new_ratio):
        if new_ratio != 0:
            self.ratios.append(new_ratio)
    def total_gear_ratio(self):
        if len(self.ratios) != 2:
            return 0
        p = 1
        for ratio in self.ratios:
            p *= ratio
        return p
    def set_set(self, new_set):
        self.indices = set()
        for x in new_set:
            self.indices.add(x)

def part2():
    s = 0
    gears = [{}, {}, {}]
    for row, line in enumerate(inp):
        s += sum([g.total_gear_ratio() for g in gears[0].values()])
        gears = gears[1:]
        gears.append({})
        for offset in range(-1,2):
            for idx, c in enumerate(inp[min(max(0,row+offset), len(inp)-1)]):
                if c == '*':
                    if offset == 1:
                        gears[2][idx] = gear()
                    gears[offset+1][idx].set_set([max(0,idx-1), idx, min(idx+1, len(line)-1)])
        for g_row in gears:
            for g in g_row.values():
                counted_indices = g.indices
                while len(counted_indices) > 0:
                    idx = list(counted_indices)[0]
                    try:
                        if idx != len(line)-1:
                            int(line[idx])
                            int(line[idx+1])
                            counted_indices.add(idx+1)
                        else:
                            int('.')
                    except:
                        number = 0
                        f = 1
                        while True:
                            try:
                                number += f*int(line[idx])
                                f *= 10
                                if idx in counted_indices:
                                    counted_indices.remove(idx)
                                idx -= 1
                                if idx < 0:
                                    break
                            except:
                                break
                        g.add_ratio(number)
                    if idx in counted_indices:
                        counted_indices.remove(idx)
    s += sum([g.total_gear_ratio() for g in gears[0].values()])
    s += sum([g.total_gear_ratio() for g in gears[1].values()])
    s += sum([g.total_gear_ratio() for g in gears[2].values()])
    print(s)

part2() #=>87605697