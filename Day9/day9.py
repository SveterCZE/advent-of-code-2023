def get_input():
    f = open("input.txt", "r")
    instructions = []
    for line in f:
        instructions.append([int(x) for x in line.strip().split()])
    return instructions

def part1(instructions):
    sum = 0
    for checked_instruction in instructions:
        sum += recursive_helper(checked_instruction)[-1]
    return sum

def part2(instructions):
    sum = 0
    for checked_instruction in instructions:
        sum += recursive_helper_backwards(checked_instruction)[0]
    return sum

def recursive_helper(checked_instruction):
    # BASE CASE --- All figures are zero
    if are_figures_zero(checked_instruction) == True:
        return checked_instruction
    
    # RECURSIVE CASE --- Figures are not zero 
    else:
        bottom_line = generate_bottom_line(checked_instruction)
        checked_instruction.append(checked_instruction[-1] + recursive_helper(bottom_line)[-1])
        return checked_instruction

def recursive_helper_backwards(checked_instruction):
    # BASE CASE --- All figures are zero
    if are_figures_zero(checked_instruction) == True:
        return checked_instruction
    
    # RECURSIVE CASE --- Figures are not zero 
    else:
        bottom_line = generate_bottom_line(checked_instruction)
        checked_instruction.insert(0, (checked_instruction[0] - recursive_helper_backwards(bottom_line)[0])) 
        return checked_instruction

def are_figures_zero(checked_instruction):
    for elem in checked_instruction:
        if elem != 0:
            return False
    return True

def generate_bottom_line(checked_instruction):
    bottom_line = []
    for i in range (1, len(checked_instruction)):
        bottom_line.append(checked_instruction[i] - checked_instruction[i-1])
    return bottom_line

if __name__ == "__main__":
    instructions = get_input()
    print(part1(instructions))
    print(part2(instructions))