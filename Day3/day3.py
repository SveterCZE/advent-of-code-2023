def main():
    instructions = get_input()
    print(part1(instructions, False))
    print(part1(instructions, True))

def get_input():
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        instructions.append(list(line.strip()))
    return instructions

def part1(instructions, gear_search):
    disconnted_values = []
    connected_values = []
    temp_value_builder = ""
    value_connected = False

    gear_db = {}
    connected_to_gear = False
    gear_identification = None

    for row in range(len(instructions)):
        for column in range(len(instructions[0])):
            if instructions[row][column].isnumeric() == True:
                temp_value_builder += instructions[row][column]
                if is_connected(instructions, row, column) == True:
                    value_connected = True
                
                checked_gear_conn = is_connected_to_gear(instructions, row, column)
                if checked_gear_conn != False and connected_to_gear == False:
                    connected_to_gear = True
                    gear_identification = checked_gear_conn
                    if gear_identification not in gear_db:
                        gear_db[gear_identification] = []

            else:
                if value_connected == False and len(temp_value_builder) > 0:
                    disconnted_values.append(int(temp_value_builder))
                elif len(temp_value_builder) > 0:
                    connected_values.append(int(temp_value_builder))
                    if connected_to_gear == True:
                        gear_db[gear_identification].append(int(temp_value_builder)) 

                temp_value_builder = ""
                value_connected = False
                connected_to_gear = False
                gear_identification = None
        # Catch a case when the number ends of the line
        if value_connected == False and len(temp_value_builder) > 0:
            disconnted_values.append(int(temp_value_builder))
        elif len(temp_value_builder) > 0:
            connected_values.append(int(temp_value_builder))
            if connected_to_gear == True:
                gear_db[gear_identification].append(int(temp_value_builder)) 
        temp_value_builder = ""
        value_connected = False
        connected_to_gear = False
        gear_identification = None
    if gear_search == False:
        sum = 0
        for elem in connected_values:
            sum += elem
        return sum
    else:
        sum = 0
        for key, value in gear_db.items():
            if len(value) == 2:
                sum += (value[0] * value[1])
        return sum

def is_connected(instructions, row, column):
    for x in range (-1, 2):
        for y in range (-1, 2):
            try:
                if instructions[row+x][column+y] != "." and instructions[row+x][column+y].isnumeric() == False:
                    return True
            except:
                pass
    return False

def is_connected_to_gear(instructions, row, column):
    for x in range (-1, 2):
        for y in range (-1, 2):
            try:
                if instructions[row+x][column+y] == "*":
                    return (row+x, column+y)
            except:
                pass
    return False

main()
