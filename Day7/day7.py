from operator import itemgetter

def get_input(joker_replacement):
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        temp_list = line.strip().split()
        instructions.append((prepare_card_values(make_card_replacements(list(temp_list[0]), joker_replacement)), int(temp_list[1]), make_card_replacements(list(temp_list[0]), joker_replacement)))
    return instructions

def make_card_replacements(hand, joker_replacement):
    for i in range(len(hand)):
        if hand[i] == "T":
            hand[i] = 10
        elif hand[i] == "J":
            if joker_replacement == False:
                hand[i] = 11
            else:
                hand[i] = 1
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
    for checked_card in instructions:
        if contains_joker(checked_card):
            apply_joker(checked_card)
    return part1(instructions)

def contains_joker(checked_card):
    for key, value in checked_card[0].items():
        if key == 1:
            return True
    return False

def apply_joker(checked_card):
    if is_five(checked_card):
        pass
    else:
        most_frequent_non_joker = find_most_frequent_non_joker(checked_card[0])
        checked_card[0][most_frequent_non_joker] += checked_card[0][1]
        checked_card[0].pop(1)

def find_most_frequent_non_joker(checked_card):
    most_frequent_key, most_frequent_value = None, 0
    for key, value in checked_card.items():
        if value > most_frequent_value and key != 1:
            most_frequent_value = value
            most_frequent_key = key
    return most_frequent_key

def count_card_winnings(sorted_cards):
    winnings = 0
    for i in range(len(sorted_cards)):
        winnings += (sorted_cards[i][-1] * (i+1))
    return winnings

def extract_fives(instructions):
    fives = []
    for checked_card in instructions:
        if is_five(checked_card):
            add_found_card_hand(checked_card, fives)
    return sorted_list(fives)

def is_five(checked_card):
    return len(checked_card[0]) == 1

def extract_fours(instructions):
    fours = []
    for checked_card in instructions:
        if(is_four(checked_card)):
            add_found_card_hand(checked_card, fours)
    return sorted_list(fours)

def is_four(checked_card):
    return len(checked_card[0]) == 2 and 4 in list(checked_card[0].values())

def extract_full_house(instructions):
    full_houses = []
    for checked_card in instructions:
        if(is_full_house(checked_card)):     
            add_found_card_hand(checked_card, full_houses)
    return sorted_list(full_houses)

def is_full_house(checked_card):
    return len(checked_card[0]) == 2 and 3 in list(checked_card[0].values())

def extract_three(instructions):
    threes = []
    for checked_card in instructions:
        if is_three(checked_card):
            add_found_card_hand(checked_card, threes)
    return sorted_list(threes)

def is_three(checked_card):
    return len(checked_card[0]) == 3 and 3 in list(checked_card[0].values())

def extract_two_pairs(instructions):
    two_pairs = []
    for checked_card in instructions:
        if is_two_pairs(checked_card):
            add_found_card_hand(checked_card, two_pairs)
    return sorted_list(two_pairs)

def is_two_pairs(checked_card):
    return len(checked_card[0]) == 3 and 2 in list(checked_card[0].values())

def extract_one_pair(instructions):
    one_pair = []
    for checked_card in instructions:
        if is_one_pair(checked_card):
            add_found_card_hand(checked_card, one_pair)
    return sorted_list(one_pair)

def is_one_pair(checked_card):
    return len(checked_card[0]) == 4

def extract_singles(instructions):
    singles = []
    for checked_card in instructions:
        if is_single(checked_card):
            add_found_card_hand(checked_card, singles)
    return sorted_list(singles)

def is_single(checked_card):
    return len(checked_card[0]) == 5

def sorted_list(list_to_be_sorted):
    return sorted(list_to_be_sorted, key=itemgetter(0,1,2,3,4))

def add_found_card_hand(checked_card, list_of_cards_found):
        found_hand = checked_card[2]
        found_hand.append(checked_card[1])
        list_of_cards_found.append(found_hand)

if __name__ == "__main__":
    instructions = get_input(False)
    print(part1(instructions))
    instructions = get_input(True)
    print(part2(instructions))