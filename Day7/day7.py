from operator import itemgetter

def get_input():
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        temp_list = line.strip().split()
        instructions.append((prepare_card_values(make_card_replacements(list(temp_list[0]))), int(temp_list[1]), make_card_replacements(list(temp_list[0]))))
    return instructions

def make_card_replacements(hand):
    for i in range(len(hand)):
        if hand[i] == "T":
            hand[i] = 10
        elif hand[i] == "J":
            hand[i] = 11
        elif hand[i] == "Q":
            hand[i] = 12
        elif hand[i] == "K":
            hand[i] = 13
        elif hand[i] == "A":
            hand[i] = 14
        else:
            hand[i] = int(hand[i])
    return hand

def prepare_card_values(hand):
    hand_db = {}
    for elem in hand:
        if elem not in hand_db:
            hand_db[elem] = 0
        hand_db[elem] += 1
    return hand_db

def part1(instructions):
    sorted_cards = []
    sorted_cards += extract_singles(instructions)
    sorted_cards += extract_one_pair(instructions)
    sorted_cards += extract_two_pairs(instructions)
    sorted_cards += extract_three(instructions)
    sorted_cards += extract_full_house(instructions)
    sorted_cards += extract_fours(instructions)
    sorted_cards += extract_fives(instructions)
    return count_card_winnings(sorted_cards)

def part2(instructions):
    return 0

def count_card_winnings(sorted_cards):
    winnings = 0
    for i in range(len(sorted_cards)):
        winnings += (sorted_cards[i][-1] * (i+1))
    return winnings

def extract_fives(instructions):
    fives = []
    for checked_card in instructions:
        if len(checked_card[0]) == 1:
            add_found_card_hand(checked_card, fives)
    return sorted_list(fives)

def extract_fours(instructions):
    fours = []
    for checked_card in instructions:
        if(len(checked_card[0])) == 2 and 4 in list(checked_card[0].values()):
            add_found_card_hand(checked_card, fours)
    return sorted_list(fours)

def extract_full_house(instructions):
    full_houses = []
    for checked_card in instructions:
        if(len(checked_card[0])) == 2 and 3 in list(checked_card[0].values()):     
            add_found_card_hand(checked_card, full_houses)
    return sorted_list(full_houses)

def extract_three(instructions):
    threes = []
    for checked_card in instructions:
        if(len(checked_card[0])) == 3 and 3 in list(checked_card[0].values()):
            add_found_card_hand(checked_card, threes)
    return sorted_list(threes)

def extract_two_pairs(instructions):
    two_pairs = []
    for checked_card in instructions:
        if(len(checked_card[0])) == 3 and 2 in list(checked_card[0].values()):
            add_found_card_hand(checked_card, two_pairs)
    return sorted_list(two_pairs)

def extract_one_pair(instructions):
    one_pair = []
    for checked_card in instructions:
        if(len(checked_card[0])) == 4:
            add_found_card_hand(checked_card, one_pair)
    return sorted_list(one_pair)

def extract_singles(instructions):
    singles = []
    for checked_card in instructions:
        if len(checked_card[0]) == 5:
            add_found_card_hand(checked_card, singles)
    return sorted_list(singles)

def sorted_list(list_to_be_sorted):
    return sorted(list_to_be_sorted, key=itemgetter(0,1,2,3,4))

def add_found_card_hand(checked_card, list_of_cards_found):
        found_hand = checked_card[2]
        found_hand.append(checked_card[1])
        list_of_cards_found.append(found_hand)

if __name__ == "__main__":
    instructions = get_input()
    print(part1(instructions))
    print(part2(instructions))