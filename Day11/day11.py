def get_input():
    f = open("input.txt", "r")
    instructions = []
    for line in f:
        instructions.append(list(line.strip()))
    return instructions

def part1(instructions, expansion_scale):
    expansion_rows = {}
    expansion_columns = {}
    galaxies_db = find_galaxies(instructions)
    expand_by_rows(instructions, expansion_rows)
    expand_by_columns(instructions, expansion_columns)
    expanded_galaxies_db = expand_universe_v2(galaxies_db, expansion_rows, expansion_columns, expansion_scale)
    return calculate_sum_of_shortest_travels(expanded_galaxies_db)

def find_galaxies(expanded_universe):
    galaxies_found = []
    for i in range(len(expanded_universe)):
        for j in range(len(expanded_universe[0])):
            if expanded_universe[i][j] == "#":
                galaxies_found.append((i,j))
    return galaxies_found

def calculate_sum_of_shortest_travels(galaxies_db):
    sum = 0
    for i in range(len(galaxies_db)):
        for j in range(i+1, len(galaxies_db)):
            sum += calculate_manhattan_distance(galaxies_db[i], galaxies_db[j])
    return sum

def calculate_manhattan_distance(galaxy1, galaxy2):
    return abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])

def expand_universe_v2(galaxies_db, expansion_rows, expansion_columns, expansion_scale):
    expanded_galaxies_db = []
    for checked_galaxy in galaxies_db:
        row_expansion = 0
        for i in range(checked_galaxy[0]):
            if expansion_rows[i] == True:
                row_expansion += 1
        column_expansion = 0
        for i in range(checked_galaxy[1]):
            if expansion_columns[i] == True:
                column_expansion += 1
        expanded_galaxies_db.append((checked_galaxy[0] + (row_expansion * (expansion_scale - 1)), checked_galaxy[1] + (column_expansion * (expansion_scale - 1))))
    return expanded_galaxies_db

def expand_by_rows(instructions, expansion_rows):
    for i in range(len(instructions)):
        row_expansion = True
        for j in range(len(instructions[0])):
            if instructions[i][j] == "#":
                row_expansion = False
        expansion_rows[i] = row_expansion

def expand_by_columns(instructions, expansion_columns):
    for i in range(len(instructions[0])):
        column_expansion = True
        for j in range(len(instructions)):
            if instructions[j][i] == "#":
                column_expansion = False
        expansion_columns[i] = column_expansion

if __name__ == "__main__":
    instructions = get_input()
    print(part1(instructions, 2))
    print(part1(instructions, 1000000))