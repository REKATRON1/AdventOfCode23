raw_inp = open('input.txt', 'r')
inp = [line.strip() for line in raw_inp]

def input_conversion(inp):
    """
    Converts the basic txt input to list of sequences
    """
    sequences = []
    for line in inp:
        str_sequence = line.split()
        sequences.append([int(x) for x in str_sequence])
    """
    sequences (default):
    [[21, 32, 43, 50, 52, 63, 128, 354, 980, 2536, 6198, 14571, 33400, 75257, 167315, 367301, 795349, 1696172, 3558635, 7344376, 14925482], ..., 
    [24, 32, 35, 33, 26, 14, -3, -25, -52, -84, -121, -163, -210, -262, -319, -381, -448, -520, -597, -679, -766]]
    """
    return sequences

def both_parts(sequences, part):
    if part != 1 and part != 2:
        return 0
    sum_of_next_sequence_value = 0
    for sequence in sequences:
        if part == 1:
            sum_of_next_sequence_value += generate_next_sequence_value(sequence)
        elif part == 2:
            sum_of_next_sequence_value += generate_next_sequence_value(sequence, reverse=True)
    return sum_of_next_sequence_value

def generate_next_sequence_value(sequence, reverse=False):
    sequence_differences = [sequence]
    while not all_zeros(sequence_differences[-1]):
        sequence_differences.append(get_sequence_differences(sequence_differences[-1]))
    if not reverse:
        for x in range(len(sequence_differences)-2, -1, -1):
            seq_dif = sequence_differences[x]
            sequence_differences[x].append(seq_dif[-1] + sequence_differences[x+1][-1])
        return sequence_differences[0][-1]
    else:
        for x in range(len(sequence_differences)-2, -1, -1):
            seq_dif = [sequence_differences[x][0] - sequence_differences[x+1][0]]
            seq_dif.extend(sequence_differences[x])
            sequence_differences[x] = seq_dif
        return sequence_differences[0][0]

def all_zeros(sequence):
    for x in sequence:
        if x != 0:
            return False
    return True

def get_sequence_differences(sequence):
    return [sequence[i+1]-sequence[i] for i in range(len(sequence)-1)]

sequences = input_conversion(inp)
sol1 = both_parts(sequences, part=1) #=>2038472161

sequences = input_conversion(inp)
sol2 = both_parts(sequences, part=2) #=>2038472161

print(sol1, sol2)