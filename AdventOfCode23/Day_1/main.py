raw_inp = open('input.txt', 'r')
inp = [line.strip() for line in raw_inp]

def part1():
    s = 0
    for line in inp:
        for c in line:
            try:
                s += 10*int(c)
                break
            except:
                continue
        for c in line[::-1]:
            try:
                s += int(c)
                break
            except:
                continue

    print(s)

part1() #=>55816 

def part2():
    s = 0
    numbers = ['one','two','three','four','five','six','seven','eight','nine']
    for line in inp:
        for i, c in enumerate(line):
            try:
                s += 10*int(c)
                break
            except:
                if any([x in line[i:i+len(x)] for x in numbers]):
                    s += 10*([x in line[i:i+len(x)] for x in numbers].index(True)+1)
                    break
        for i, c in enumerate(line[::-1]):
            try:
                s += int(c)
                break
            except:
                if any([x in line[::-1][i:i+len(x)][::-1] for x in numbers]):
                    s += ([x in line[::-1][i:i+len(x)][::-1] for x in numbers].index(True)+1)
                    break
    print(s)

part2() #=>54980