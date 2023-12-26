import re

def main():
    instructions = get_input()
    print(part1(instructions))
    print(part2(instructions))

def get_input():
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        instructions.append(line.strip())
    return instructions

def part1(instructions):
    sum = 0
    for checked_line in instructions:
        sum += calculate_numeric_value(checked_line)
    return sum

def part2(instructions):
    sum = 0
    dictionary = define_dictionary()
    for checked_line in instructions:
        sum += calculate_alpha_numeric_value(checked_line, dictionary)
    return sum

def calculate_numeric_value(checked_line):
    numeric_values = re.findall(r'\d+', checked_line)
    value_as_string = list(''.join(numeric_values))
    converted_value = [value_as_string[0], value_as_string[-1]]
    final_value = ''.join(converted_value)
    return int(final_value)

def calculate_alpha_numeric_value(checked_line, dictionary):
    extracted_numbers = []
    split_line = re.split(r'(\d+)', checked_line)
    for checked_item in split_line:
        if checked_item.isdigit() == True:
            extracted_numbers.append(checked_item)
        else:
            extract_numbers_as_words(checked_item, extracted_numbers, dictionary)
    value_as_string = list(''.join(extracted_numbers))
    converted_value = [value_as_string[0], value_as_string[-1]]
    final_value = ''.join(converted_value)
    return int(final_value)

def extract_numbers_as_words(checked_line, extracted_numbers, dictionary):
    for i in range(len(checked_line)):
        for key, value in dictionary.items():
            if checked_line[i:].startswith(key):
                extracted_numbers.append(value)

def define_dictionary():
    dictionary = {}
    dictionary["one"] = "1"
    dictionary["two"] = "2"
    dictionary["three"] = "3"
    dictionary["four"] = "4"
    dictionary["five"] = "5"
    dictionary["six"] = "6"
    dictionary["seven"] = "7"
    dictionary["eight"] = "8"
    dictionary["nine"] = "9"
    dictionary["zero"] = "0"
    return dictionary

main()