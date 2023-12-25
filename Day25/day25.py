import re
import random
import copy

def main():
    instructions = get_input()
    print(part1(instructions))

def get_input():
    f = open("input.txt", "r")
    graph = {}
    for line in f:
        matches = re.findall(r'[A-Za-z]+', line)
        for i in range(1, len(matches)):
            if matches[0] not in graph:
                graph[matches[0]] = []
            graph[matches[0]].append(matches[i])
            if matches[i] not in graph:
                graph[matches[i]] = []
            graph[matches[i]].append(matches[0])
    return graph

def part1(graph):
    while True:
        testing_graph = copy.deepcopy(graph)
        simplified_graph, merged_values = run_random_simulation(testing_graph)
        if valid_result_found(simplified_graph):
            counter = 1
            for key, value in merged_values.items():
                counter *= value
            print(simplified_graph, merged_values)
            return counter

def valid_result_found(simplified_graph):
    for key, value in simplified_graph.items():
        if len(value) != 3:
            return False
    return True

def run_random_simulation(graph):
    merged_values = {}
    # Initialize counter
    for key, value in graph.items():
        merged_values[key] = 1
    while len(graph) > 2:
        # Find random vertex
        random_choice = random.choice(list(graph.items()))
        first_node = random_choice[0]
        second_node = random.choice(list(random_choice[1]))
        # Update value of counter
        merged_values[first_node] += merged_values[second_node]
        merged_values.pop(second_node)
        # Update the graph
        # Add references from the second node to the first one
        for key in graph[second_node]:
            if key != first_node:
                graph[first_node].append(key)
        # Remove reference to the second node from the first node
        while True:
            if second_node not in graph[first_node]:
                break
            if second_node in graph[first_node]:
                graph[first_node].remove(second_node)
        # Replace references to the second node with first node
        for key, value in graph.items():
            if key != first_node:
                while True:
                    if second_node not in value:
                        break
                    else:
                        graph[key].remove(second_node)
                        graph[key].append(first_node)
        # Remove the second node from the graph
        graph.pop(second_node)
    return graph, merged_values

main()