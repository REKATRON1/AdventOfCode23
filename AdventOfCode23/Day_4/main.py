raw_inp = open('input.txt', 'r')
inp = [line.strip() for line in raw_inp]

cards = []
for line in inp:
    numbers = [x.split(' ') for x in line.split(':')[1].split('|')]
    card = []
    for numberlist in numbers:
        new_numberlist = []
        for n in numberlist:
            if n != '':
                try:
                    new_numberlist.append(int(n))
                except:
                    print(n)
        card.append(new_numberlist)
    cards.append(card)

def number_of_duplicates(l1, l2):
    combined_list = l1.copy()
    combined_list.extend(l2)
    total_numbers = len(combined_list)
    rem_dupl = list(set(combined_list))
    unique_numbers = len(rem_dupl)
    duplicates = total_numbers - unique_numbers
    return duplicates

def part1():
    total_score = 0
    for card in cards:
        duplicates = number_of_duplicates(card[0], card[1])
        if duplicates > 0:
            total_score += 2 ** (duplicates-1)
    print(total_score)

part1()

def part2():
    total_cards = {x: 1 for x in range(len(cards))}
    for idx, card in enumerate(cards):
        duplicates = number_of_duplicates(card[0], card[1])
        if duplicates > 0:
            card_amount = total_cards[idx]
            for x in range(1, duplicates+1):
                if idx + x < len(cards):
                    total_cards[idx+x] += card_amount
    sum_cards = sum(list(total_cards.values()))
    print(sum_cards)

part2() #=>6874754