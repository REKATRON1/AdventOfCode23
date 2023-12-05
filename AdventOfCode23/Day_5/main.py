from time import perf_counter, sleep

raw_inp = open('input.txt', 'r')
inp = [line.strip() for line in raw_inp]


maps = []
current_map = []
for line in inp:
    if line == '' and len(current_map) != 0:
        if len(current_map) == 1:
            maps.append(current_map[0])
        else:
            maps.append(current_map)
        current_map = []
    else:
        new_range = []
        for number in line.split(' '):
            try:
                new_range.append(int(number))
            except:
                continue
        if len(new_range) >= 3:
            current_map.append(new_range)
if len(current_map) > 1:
    maps.append(current_map)


def mapto(inp, maps):
    outs = []
    for i, x in enumerate(inp):
        for m in maps:
            if m[1] <= x <= m[1]+m[2]-1:
                outs.append(x + (m[0]-m[1]))
                break
        if len(outs) < i+1:
            outs.append(x)
    return outs

def part1():
    t1 = perf_counter()
    seeds = maps[0]
    for m in maps[1:]:
        seeds = mapto(seeds, m)
    t2 = perf_counter()
    print(t2-t1)
    print(min(seeds))

part1() #=>331445006

class mapper():
    def __init__(self, pointer, _conversions):
        conversions = _conversions[pointer]
        self.start_range = conversions[1]
        self.end_range = conversions[1]+conversions[2]-1
        self.converter = conversions[0]-conversions[1]
        self.build_maplist(pointer, _conversions)
    def build_maplist(self, pointer, conversions):
        pointer += 1
        if pointer != len(conversions):
            self.next = mapper(pointer, conversions)
        else:
            self.next = None
    def map_seed(self, inp):
        if self.start_range <= inp <= self.end_range:
            return inp + self.converter
        elif self.next == None:
            return inp
        else:
            return self.next.map_seed(inp)
    def map_seed_range(self, seed_start, seed_end):
        if seed_start > seed_end:
            return []
        elif self.start_range > seed_end or self.end_range < seed_start:
            return self.go_rec(seed_start, seed_end)
        elif self.start_range <= seed_start and self.end_range >= seed_end:
            return [[seed_start + self.converter, seed_end + self.converter]]
        elif self.start_range <= seed_start:
            ret = [[seed_start + self.converter, self.end_range + self.converter]]
            ret.extend(self.go_rec(self.end_range+1, seed_end))
            return ret
        elif self.end_range >= seed_end:
            ret = [[self.start_range + self.converter, seed_end + self.converter]]
            ret.extend(self.go_rec(seed_start, self.start_range-1))
            return ret
        return []
    def go_rec(self, seed_start, seed_end):
        if self.next == None:
            return [[seed_start, seed_end]]
        else:
            return self.next.map_seed_range(seed_start, seed_end)

def part2():
    t1 = perf_counter()
    mappers = []
    for m in maps[1:]:
        mappers.append(mapper(0, m))
    seed_ranges = []
    for x in range(int(len(maps[0])/2)):
        seed_ranges.append([maps[0][2*x], maps[0][2*x]+maps[0][2*x+1]])
    
    for m in mappers:
        new_seed_ranges = []
        for seed_range in seed_ranges:
            new_seed_ranges.extend(m.map_seed_range(seed_range[0], seed_range[1]))
        seed_ranges = new_seed_ranges
    t2 = perf_counter()
    print(t2-t1)
    print(min(seed_ranges, key=lambda x: x[0])[0])

part2() #=>6472060