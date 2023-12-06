raw_inp = open('input.txt', 'r')
inp = [line.strip() for line in raw_inp]

def input_conversion_part1(inp):
    """
    Converts the basic txt input to list of tuples with the time and record for each race
    """
    line1, line2 = inp[0], inp[1]

    race_time_record_tuples = []

    race_times = [int(x) for x in line1.split()[1:]] #Ignore 'Time:'
    race_recors = [int(x) for x in line2.split()[1:]] #Ignore 'Distance:'

    for race_num in range(len(race_times)):
        race_time_record_tuples.append([race_times[race_num], race_recors[race_num]])

    """
    race_time_record_tuples (default):
    [[35, 213], [69, 1168], [68, 1086], [87, 1248]]
    """
    return race_time_record_tuples

def input_conversion_part2(inp):
    """
    Converts the basic txt input to a list with one tuple with the time and record for the race
    Wrapping -> reusing the code from part1
    """
    line1, line2 = inp[0], inp[1]

    race_time_record_tuples = [['', '']]

    race_times_split = line1.split()[1:] #Ignore 'Time:'
    race_recors_split = line2.split()[1:] #Ignore 'Distance:'

    for num in range(len(race_times_split)):
        race_time_record_tuples[0][0] += race_times_split[num]
        race_time_record_tuples[0][1] += race_recors_split[num]

    race_time_record_tuples =[[int(race[0]), int(race[1])] for race in race_time_record_tuples]

    """
    race_time_record_tuples (default):
    [[35696887, 213116810861248]]
    """
    return race_time_record_tuples

import numpy as np
def quadratic_roots(factors):
    """
    Calculates roots of normalized (a=1) quadratic polynomial.
    factors: [c, b, a] := ax^2+bx+c=0
    """
    D = (factors[1]/2)**2-factors[0]
    if D > 0:
        d_sqrt = np.sqrt(D)
        sols = [-factors[1]/2-d_sqrt, -factors[1]/2+d_sqrt]
    elif D == 0:
        sols = [-factors[1]/2]
    else:
        sols = []
    return sols


def both_parts(races):
    """
    Find the product of the amount of record-beating-charge-times from all races.
    The distance traveled equals the charge-time c times the remaining time t-c of the race:
    d(c)=c*(t-c)
    """
    
    product_amount_record_beating_times = 1
    for race in races:
        """
        Calculate for which charge time the driven distance matches record.
        Due to the function being a parabola (with negative leading term) all values
        between the two intersections beat the record.
        For charge time c, total time t and record r:
        d(c)=c*(t-c)=r <=> -c^2+tc-r=0 <=> c^2-tc+r=0
        """
        matching_record_times = quadratic_roots([race[1], -race[0], 1])

        if len(matching_record_times) == 2:
            matching_record_times_round_inwards = [int(np.ceil(matching_record_times[0])), int(np.floor(matching_record_times[1]))]
            #No need for accounting sols being outside the definition-range bcs these distances would be negative
            product_amount_record_beating_times *= len(list(range(matching_record_times_round_inwards[0], matching_record_times_round_inwards[1]+1)))
        else:
            product_amount_record_beating_times *= 0
            #Cannot be anything else but 0 bcs a*0=0
            break

    return product_amount_record_beating_times

race_time_record_tuples_part1 = input_conversion_part1(inp)
print(both_parts(race_time_record_tuples_part1)) #=>170000

race_time_record_tuples_part2 = input_conversion_part2(inp)
print(both_parts(race_time_record_tuples_part2)) #=>20537782
