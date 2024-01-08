from operator import itemgetter

def get_input():
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        temp_list = line.strip().split()
        instructions.append((prepare_card_values(list(temp_list[0])), int(temp_list[1])))
    return instructions

def prepare_card_values(hand):
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
    hand_db = {}
    for elem in hand:
        if elem not in hand_db:
            hand_db[elem] = 0
        hand_db[elem] += 1
    return hand_db

def part1(instructions):
    sorted_cards = []
    fives = extract_fives(instructions, sorted_cards)
    four_of_kind = extract_fours(instructions, sorted_cards)
    full_house = extract_full_house(instructions, sorted_cards)
    three = extract_three(instructions, sorted_cards)
    two_pairs = extract_two_pairs(instructions, sorted_cards)
    one_pair = extract_one_pair(instructions, sorted_cards)
    singles = extract_singles(instructions, sorted_cards)
    return 0

def part2(instructions):
    return 0

def extract_fives(instructions, sorted_cards):
    fives = []
    for checked_card in instructions:
        if len(checked_card[0]) == 1:
            fives_hand = list(checked_card[0].keys())
            fives_hand.append(checked_card[1])
            fives.append(fives_hand)
    fives = sorted(fives, key=itemgetter(0), reverse=True)
    return fives

def extract_fours(instructions, sorted_cards):
    fours = []
    for checked_card in instructions:
        if(len(checked_card[0])) == 2 and 4 in list(checked_card[0].values()):
            fours_hand = [0, 0]
            for key, value in checked_card[0].items():
                if value == 4:
                    fours_hand[0] = key
                elif value == 1:
                    fours_hand[1] = key
            fours_hand.append(checked_card[1])
            fours.append(fours_hand)
    fours = sorted(fours, key=itemgetter(0,1), reverse=True)
    return fours

def extract_full_house(instructions, sorted_cards):
    full_houses = []
    for checked_card in instructions:
        if(len(checked_card[0])) == 2 and 3 in list(checked_card[0].values()):
            full_house_hand = [0,0]
            for key, value in checked_card[0].items():
                if value == 3:
                    full_house_hand[0] = key
                elif value == 2:
                    full_house_hand[1] = key
            full_house_hand.append(checked_card[1])
            full_houses.append(full_house_hand)
    full_houses = sorted(full_houses, key=itemgetter(0,1), reverse=True)
    return full_houses

def extract_three(instructions, sorted_cards):
    threes = []
    for checked_card in instructions:
        if(len(checked_card[0])) == 3 and 3 in list(checked_card[0].values()):
            three_hands = []
            temp_other = []
            for key, value in checked_card[0].items():
                if value == 3:
                    three_hands.append(key)
                else:
                    temp_other.append(key)
            temp_other.sort(reverse=True)
            three_hands += temp_other
            three_hands.append(checked_card[1])
            threes.append(three_hands)
    threes = sorted(threes, key=itemgetter(0,1,2), reverse=True)
    return threes

def extract_two_pairs(instructions, sorted_cards):
    two_pairs = []
    for checked_card in instructions:
        if(len(checked_card[0])) == 3 and 2 in list(checked_card[0].values()):
            two_hands = []
            for key, value in checked_card[0].items():
                if value == 2:
                    two_hands.append(key)
                else:
                    single = key
            two_hands.sort(reverse=True)
            two_hands.append(single)
            two_hands.append(checked_card[1])
            two_pairs.append(two_hands)
    two_pairs = sorted(two_pairs, key=itemgetter(0,1,2), reverse=True)
    return two_pairs

def extract_one_pair(instructions, sorted_cards):
    one_pair = []
    for checked_card in instructions:
        if(len(checked_card[0])) == 4:
            one_pair_hand = []
            single_values = []
            for key, value in checked_card[0].items():
                if value == 2:
                    one_pair_hand.append(key)
                else:
                    single_values.append(key)
            single_values.sort(reverse=True)
            one_pair_hand += single_values
            one_pair_hand.append(checked_card[1])
            one_pair.append(one_pair_hand)
    one_pair = sorted(one_pair, key=itemgetter(0,1,2,3), reverse=True)
    print(one_pair)
    return one_pair

def extract_singles(instructions, sorted_cards):
    singles = []
    for checked_card in instructions:
        if len(checked_card[0]) == 5:
            singles_hand = list(checked_card[0].keys())
            singles_hand.sort(reverse=True)
            singles_hand.append(checked_card[1])
            singles.append(singles_hand)
    singles = sorted(singles, key=itemgetter(0,1,2,3,4), reverse=True)
    return singles

if __name__ == "__main__":
    instructions = get_input()
    print(part1(instructions))
    print(part2(instructions))