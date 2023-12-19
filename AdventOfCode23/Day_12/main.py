raw_inp = open('input.txt', 'r')
inp = [line.strip() for line in raw_inp]

def input_conversion(inp, repetitions=1):
    """
    Converts the basic txt input to array of tuples with the first entry being a list of the condition records: .->0, #->1, ?->2
    and the secound entry being the contiguous damaged group sizes which get duplicated 'repetitions' times
    """
    records = []
    for line in inp:
        condition_records_raw, group_sizes_raw = line.split(' ')
        condition_records, group_sizes = [], []
        for c in condition_records_raw:
            if c == '.':
                condition_records.append(0)
            elif c == '#':
                condition_records.append(1)
            elif c == '?':
                condition_records.append(2)
            else:
                print('Unknown Character')
        for n in group_sizes_raw.split(','):
            group_sizes.append(int(n))
        #Everything times 5
        extended_condition_records, extended_group_sizes = condition_records.copy(), group_sizes.copy()
        for i in range(repetitions-1):
            extended_condition_records.append(2)
            extended_condition_records.extend(condition_records)
            extended_group_sizes.extend(group_sizes)
        records.append((extended_condition_records, extended_group_sizes))
    """
    records (default):
    [([2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 0, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 0, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 0, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 0, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 0, 1, 2, 2, 2, 1, 2, 2, 2], [9, 7, 9, 7, 9, 7, 9, 7, 9, 7]),
     ..., ([2, 2, 2, 2, 1, 1, 2, 2, 1, 1, 0, 2, 2, 2, 2, 1, 0, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 1, 1, 0, 2, 2, 2, 2, 1, 0, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 1, 1, 0, 2, 2, 2, 2, 1, 0, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 1, 1, 0, 2, 2, 2, 2, 1, 0, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 1, 1, 0, 2, 2, 2, 2, 1, 0, 2], [9, 4, 1, 9, 4, 1, 9, 4, 1, 9, 4, 1, 9, 4, 1])]
    """
    return records

def split_at_state(condition_records, state):
    splited_records = []
    new_split = []
    for c in condition_records:
        if c == state and len(new_split) != 0:
            splited_records.append(new_split)
            new_split = []
        elif c != state:
            new_split.append(c)
    if len(new_split) != 0:
        splited_records.append(new_split)
    return splited_records

def split_record_in_possible_groups(record):
    condition_records, group_sizes = record
    split_condition_records_at_operational = split_at_state(condition_records, state=0)
    return split_condition_records_at_operational

def merge_record(split_groups):
    if len(split_groups) == 0:
        return []
    merged = split_groups[0]
    for group in split_groups[1:]:
        merged.append(0)
        merged.extend(group)
    return merged

def try_overlay(cut_record, overlay, index_start=0):
    if len(cut_record) < index_start+len(overlay):
        return False
    for x in range(len(overlay)):
        if (not overlay[x]) and cut_record[x+index_start] == 1:
            return False
        elif overlay[x] and cut_record[x+index_start] == 0:
            return False
    if index_start+len(overlay) < len(cut_record):
        return cut_record[index_start+len(overlay)] != 1
    return True

def generate_hash_rem_index(record, overlay):
    return record * 11113 + overlay

def calculate_permutations_of_subrecord(cut_record, rem_index_record, overlays, rem_index_overlay, dic):
    if len(cut_record) <= rem_index_record:
        return len(overlays) <= rem_index_overlay
    elif len(overlays) <= rem_index_overlay:
        #Missed a 1 at the end
        return try_overlay(cut_record, [0 for x in range(len(cut_record)-rem_index_record)], rem_index_record)
    if dic.get(generate_hash_rem_index(rem_index_record, rem_index_overlay)) != None:
        return dic[generate_hash_rem_index(rem_index_record, rem_index_overlay)]
    permutations = 0
    overlay_size = sum([len(x)+1 for x in overlays[rem_index_overlay:]])-1
    possible_shifts = len(cut_record) - rem_index_record - overlay_size + 1
    next_overlay = overlays[rem_index_overlay]
    for x in range(possible_shifts):
        if x > 0:
            #Check so no 1 gets skipped
            if try_overlay(cut_record, [0 for x in range(x-1)], rem_index_record) and try_overlay(cut_record, next_overlay, rem_index_record+x):
                permutations += calculate_permutations_of_subrecord(cut_record, rem_index_record+len(next_overlay)+x+1, overlays, rem_index_overlay+1, dic)
        else:
            if try_overlay(cut_record, next_overlay, rem_index_record+x):
                permutations += calculate_permutations_of_subrecord(cut_record, rem_index_record+len(next_overlay)+x+1, overlays, rem_index_overlay+1, dic)
    dic[generate_hash_rem_index(rem_index_record, rem_index_overlay)] = permutations
    return permutations

def calculate_permutations_of_record(record):
    cut_record = merge_record(split_record_in_possible_groups(record))
    overlays = [[1 for x in range(s)] for s in record[1]]
    overlay_size = sum([len(x)+1 for x in overlays])-1
    possible_shifts = len(cut_record) - overlay_size
    permutations = calculate_permutations_of_subrecord(cut_record, 0, overlays, 0, {})
    if permutations == 0:
        print('\noverlay', overlays, overlay_size)
        print('record',cut_record, possible_shifts)
        print('permutations:',permutations)
    return permutations

def both_parts(records):
    sum_permutations = 0
    for rec in records:
        sum_permutations += calculate_permutations_of_record(rec)
    return sum_permutations



records = input_conversion(inp)
sol1 = both_parts(records) #=>7633

records = input_conversion(inp, 5)
sol2 = both_parts(records) #=>23903579139437

print(sol1, sol2)