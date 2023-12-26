import re

def main():
    seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location = get_input()
    print(part1(seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location))

def get_input():
    seed_to_soil = []
    soil_to_fertilizer = []
    fertilizer_to_water = []
    water_to_light = []
    light_to_temperature = []
    temperature_to_humidity = []
    humidity_to_location = []
    f = open("input.txt", "r")
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

def run_almanac(item, almanac):
    for almanac_line in almanac:
        if item in range(almanac_line[1], almanac_line[1] + almanac_line[2]):
            return almanac_line[0] + (item - almanac_line[1])
    return item

main()