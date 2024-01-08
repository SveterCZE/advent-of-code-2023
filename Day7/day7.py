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
    sorted_cards += extract_singles(instructions, sorted_cards)
    sorted_cards += extract_one_pair(instructions, sorted_cards)
    sorted_cards += extract_two_pairs(instructions, sorted_cards)
    sorted_cards += extract_three(instructions, sorted_cards)
    sorted_cards += extract_full_house(instructions, sorted_cards)
    sorted_cards += extract_fours(instructions, sorted_cards)
    sorted_cards += extract_fives(instructions, sorted_cards)
    return count_card_winnings(sorted_cards)

def part2(instructions):
    return 0

def count_card_winnings(sorted_cards):
    winnings = 0
    for i in range(len(sorted_cards)):
        winnings += (sorted_cards[i][-1] * (i+1))
    return winnings

def extract_fives(instructions, sorted_cards):
    fives = []
    for checked_card in instructions:
        if len(checked_card[0]) == 1:
            fives_hand = checked_card[2]
            fives_hand.append(checked_card[1])
            fives.append(fives_hand)
    fives = sorted(fives, key=itemgetter(0,1,2,3,4))
    return fives

def extract_fours(instructions, sorted_cards):
    fours = []
    for checked_card in instructions:
        if(len(checked_card[0])) == 2 and 4 in list(checked_card[0].values()):
            fours_hand = checked_card[2]
            fours_hand.append(checked_card[1])
            fours.append(fours_hand)
    fours = sorted(fours, key=itemgetter(0,1,2,3,4))
    return fours

def extract_full_house(instructions, sorted_cards):
    full_houses = []
    for checked_card in instructions:
        if(len(checked_card[0])) == 2 and 3 in list(checked_card[0].values()):     
            full_house_hand = checked_card[2]
            full_house_hand.append(checked_card[1])
            full_houses.append(full_house_hand)
    full_houses = sorted(full_houses, key=itemgetter(0,1,2,3,4))
    return full_houses

def extract_three(instructions, sorted_cards):
    threes = []
    for checked_card in instructions:
        if(len(checked_card[0])) == 3 and 3 in list(checked_card[0].values()):
            three_hands = checked_card[2]
            three_hands.append(checked_card[1])
            threes.append(three_hands)
    threes = sorted(threes, key=itemgetter(0,1,2,3,4))
    return threes

def extract_two_pairs(instructions, sorted_cards):
    two_pairs = []
    for checked_card in instructions:
        if(len(checked_card[0])) == 3 and 2 in list(checked_card[0].values()):
            two_hands = checked_card[2]
            two_hands.append(checked_card[1])
            two_pairs.append(two_hands)
    two_pairs = sorted(two_pairs, key=itemgetter(0,1,2,3,4))
    return two_pairs

def extract_one_pair(instructions, sorted_cards):
    one_pair = []
    for checked_card in instructions:
        if(len(checked_card[0])) == 4:
            one_pair_hand = checked_card[2]
            one_pair_hand.append(checked_card[1])
            one_pair.append(one_pair_hand)
    one_pair = sorted(one_pair, key=itemgetter(0,1,2,3,4))
    return one_pair

def extract_singles(instructions, sorted_cards):
    singles = []
    for checked_card in instructions:
        if len(checked_card[0]) == 5:
            singles_hand = checked_card[2]
            singles_hand.append(checked_card[1])
            singles.append(singles_hand)
    singles = sorted(singles, key=itemgetter(0,1,2,3,4))
    return singles

if __name__ == "__main__":
    instructions = get_input()
    print(part1(instructions))
    print(part2(instructions))