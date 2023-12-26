import re

def main():
    seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location = get_input()
    print(part1(seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location))
    print(part2(seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location))

def get_input():
    seed_to_soil = []
    soil_to_fertilizer = []
    fertilizer_to_water = []
    water_to_light = []
    light_to_temperature = []
    temperature_to_humidity = []
    humidity_to_location = []
    f = open("sample.txt", "r")
    relevant_db = None
    for line in f:
        if line.startswith("seeds"):
            seeds = [int(x) for x in re.findall(r'\d+', line)]
            continue
        if line.startswith("seed-to-soil"):
            relevant_db = seed_to_soil
            continue
        if line.startswith("soil-to-fertilizer"):
            relevant_db = soil_to_fertilizer
            continue
        if line.startswith("fertilizer-to-water"):
            relevant_db = fertilizer_to_water
            continue
        if line.startswith("water-to-light"):
            relevant_db = water_to_light
            continue
        if line.startswith("light-to-temperature"):
            relevant_db = light_to_temperature
            continue
        if line.startswith("temperature-to-humidity"):
            relevant_db = temperature_to_humidity
            continue
        if line.startswith("humidity-to-location"):
            relevant_db = humidity_to_location
            continue
        if len(line) > 1 and relevant_db != None:
            relevant_db.append([int(x) for x in re.findall(r'\d+', line)])

    return seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location

def part1(seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location):
    lowest_db = []
    for seed in seeds:
        soil = run_almanac(seed, seed_to_soil)
        fertilizer = run_almanac(soil, soil_to_fertilizer)
        water = run_almanac(fertilizer, fertilizer_to_water)
        light = run_almanac(water, water_to_light)
        temperature = run_almanac(light, light_to_temperature)
        humidity = run_almanac(temperature, temperature_to_humidity)
        location = run_almanac(humidity, humidity_to_location)
        lowest_db.append(location)
    lowest_db.sort()
    return lowest_db[0]

def part2(seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location):
    ranges_db = set()
    for i in range(0, len(seeds), 2):
        ranges_db.add((seeds[i], seeds[i] + seeds[i + 1] - 1))
    for checked_range in ranges_db:
        ranges_db = run_recursive_almanac(ranges_db, seed_to_soil)
        # ranges_db = run_recursive_almanac(ranges_db, soil_to_fertilizer)
        # ranges_db = run_recursive_almanac(ranges_db, fertilizer_to_water)
        # ranges_db = run_recursive_almanac(ranges_db, water_to_light)
        # ranges_db = run_recursive_almanac(ranges_db, light_to_temperature)
        # ranges_db = run_recursive_almanac(ranges_db, temperature_to_humidity)
        # ranges_db = run_recursive_almanac(ranges_db, humidity_to_location)
    return ranges_db

def run_almanac(item, almanac):
    for almanac_line in almanac:
        if item in range(almanac_line[1], almanac_line[1] + almanac_line[2]):
            return almanac_line[0] + (item - almanac_line[1])
    return item

def run_recursive_almanac(initial_ranges_DB, almanac):
    processed_ranges = set()
    unprocessed_ranges = set()
    buffered_ranges = set()
    for almanac_line in almanac:
        for checked_range in unprocessed_ranges:
            result, failures = run_range_slicing(almanac_line, checked_range)
            if result != None:
                processed_ranges.add(result)
            if failures != None:
                for elem in failures:
                    buffered_ranges.add(elem)
        unprocessed_ranges = buffered_ranges
        buffered_ranges = set()
    for elem in unprocessed_ranges:
        processed_ranges.add(elem)
             
def run_range_slicing(almanac_line, checked_range):
    almanac_range = (almanac_line[1], almanac_line[1] + almanac_line[2] - 1)
    # ALTERNATIVE 1 --- Whole checked range is within the almanac line
    if checked_range[0] >= almanac_range[0] and checked_range[0] <= almanac_range[1] and checked_range[1] >= almanac_range[0] and checked_range[1] <= almanac_range[1]:
        modified_line = run_almanac_on_range(almanac_line, checked_range)
        return modified_line, None
    # ALTERNATIVE 2 --- Whole checked range is left of the almanac line
    elif checked_range[1] < almanac_range[0]:
        return None, checked_range
    # ALTERNATIVE 3 --- Whole checked range is right of the almanac line
    elif checked_range[0] > almanac_range[1]:
        return None, checked_range
    # ALTERNATIVE 4 --- Whole almanac line is within the checked range
    elif almanac_range[0] >= checked_range[0] and almanac_range[0] <= checked_range[1] and almanac_range[1] >= checked_range[0] and almanac_range[1] <= checked_range[1]:
        modified_line = run_almanac_on_range(almanac_line, almanac_range)
        left_side = (checked_range[0], almanac_range[0] - 1)
        right_side = (almanac_range[1] + 1, checked_range[1])
        return modified_line, [left_side, right_side]
    # ALTERNATIVE 5 --- Checked range extends on the right side
    elif checked_range[0] >= almanac_range[0] and checked_range[0] <= almanac_range[1] and checked_range[1] > almanac_range[1]:
        modified_line = run_almanac_on_range(almanac_line, (checked_range[0], almanac_range[1]))
        return modified_line, [(almanac_range[1] + 1, checked_range[1])]
    # ALTERNATIVE 6 --- Checked range extends on the left side
    elif checked_range[0] < almanac_range[0] and checked_range[1] >= almanac_range[0] and checked_range[1] <= checked_range[1]:
        modified_line = run_almanac_on_range(almanac_line, (almanac_range[0], checked_range[1]))
        return modified_line, [(checked_range[0], almanac_line[0] - 1)]
    # ALTERNATIVE 7 --- Error, you should not get here
    else:
        print("Error. You should not be here.")




main()