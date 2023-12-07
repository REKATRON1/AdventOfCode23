raw_inp = open('input.txt', 'r')
inp = [line.strip() for line in raw_inp]

def input_conversion(inp):
    """
    Converts the basic txt input to list of tuples with the cards and bids for each hand
    """
    hands = []
    for line in inp:
        str_hand = line.split(' ')
        cards, bid = str_hand[0], int(str_hand[1])
        hands.append([cards, bid])
    """
    hands (default):
    [['8444T', 864], ['6TK4Q', 440], ['A5555', 197], ..., ['48744', 976], ['9A9KK', 18], ['TT9T9', 71]]
    """
    return hands

def compare_hands(hand1, hand2, part):
    if not (part == 1 or part == 2):
        return 0
    """
    Compares two "poker hands" by the rules specified in part1/part2 and returns 1 if hand1 > hand2, 0 if hand1 == hand2 and -1 if hand 1 < hand2
    """
    cards1, cards2 = hand1[0], hand2[0]
    if part == 1:
        card_score_conversion = {str(x):x-1 for x in range(2, 10)} | {'T':9, 'J':10, 'Q':11, 'K':12, 'A':13}
        unique_cards1, unique_cards2 = set(cards1), set(cards2)
        num_unique_cards1, num_unique_cards2 = len(unique_cards1), len(unique_cards2)
    elif part == 2:
        card_score_conversion = {str(x):x-1 for x in range(2, 10)} | {'T':9, 'J':0, 'Q':10, 'K':11, 'A':12}
        """
        J are Jokers that can act as any card => just ignore them
        """
        joker_ignored_cards1, joker_ignored_cards2 = [card for card in cards1 if card != 'J'], [card for card in cards2 if card != 'J']
        unique_cards1, unique_cards2 = set(joker_ignored_cards1), set(joker_ignored_cards2)
        #If all joker: no unique_cards...
        num_unique_cards1, num_unique_cards2 = max(1, len(unique_cards1)), max(1, len(unique_cards2))
    
    if num_unique_cards1 == num_unique_cards2:
        """
        Exmpl. (part1) | (part2):
        '22334' (3) and '44599' (3) | '22334' (3) and '44599' (3)
        'KKK44' (2) and 'AAAA2' (2) | 'JJJ44' (1) and 'JJJJ2' (1)
        but
        'KKK23' (3) and '34498' (4) | 'KKK23' (3) and '34498' (4)
                                    | 'AKJJ2' (3) and '34433' (2)
        => fewer unique cards equals better hand
        """
        sum_duplicates1, sum_duplicates2 = sum([cards1.count(card) for card in unique_cards1 if cards1.count(card)>1]), sum([cards2.count(card) for card in unique_cards2 if cards2.count(card)>1])
        if part == 2:
            #Jokers can always be used as duplicate. if so far no duplicates: one card can be copied so its duplace now!
            if cards1.count('J') > 0:
                if sum_duplicates1 == 0:
                    sum_duplicates1 += 1
                sum_duplicates1 += cards1.count('J')
            if cards2.count('J') > 0:
                if sum_duplicates2 == 0:
                    sum_duplicates2 += 1
                sum_duplicates2 += cards2.count('J')
        
        if sum_duplicates1 == sum_duplicates2:
            """
            Exmpl. (part1) | (part2):
            '3444A' (3)   and '56777' (3) | '344JA' (2+1) and '547JJ' (1+2)
            but
            '22233' (3+2) and '55565' (4) | '2J233' (2+2+1) and '55565' (4)
            '22133' (2+2) and '555QK' (3) | '22133' (2+2) and '55JQK' (2+1)
            => fewer duplicate cards equals better hand (if same unique cards)
            => same duplicate cards equals same type of hand (high-card, pair, two-pairs, three, full, four, five)
            """
            for i in range(5):
                cards1_cardI, cards2_cardI = cards1[i], cards2[i]
                if cards1_cardI == cards2_cardI:
                    continue
                else:
                    return (card_score_conversion[cards1_cardI] > card_score_conversion[cards2_cardI])*2-1
            return 0
        else:
            return (sum_duplicates1 < sum_duplicates2)*2-1
    else:
        return (len(unique_cards1) < len(unique_cards2))*2-1

def compare_hands_part1(hand1, hand2):
    return compare_hands(hand1, hand2, part=1)

def compare_hands_part2(hand1, hand2):
    return compare_hands(hand1, hand2, part=2)

import functools

def both_parts(hands, part):
    if not (part == 1 or part == 2):
        return 0
    """
    Find the total winnings of all hands for which the ranking of the hand (1 worst - x best) is multiplied by the bid
    """
    total_winning = 0
    """
    Rank all hands by sorting them:
    Rank = position in sorted list
    """
    if part == 1:
        hands.sort(key=functools.cmp_to_key(compare_hands_part1))
    elif part == 2:
        hands.sort(key=functools.cmp_to_key(compare_hands_part2))

    for ranking, hand in enumerate(hands):
        """
        Multiply hand bid by its position in sorted list (=rank) and add it to total winning
        """
        total_winning += (ranking+1) * hand[1] #enumerate starts at 0
    return total_winning

hands = input_conversion(inp)
sol1 = both_parts(hands, part=1) #=>251106089

hands = input_conversion(inp)
sol2 = both_parts(hands, part=2) #=>249620106

print(sol1, sol2)