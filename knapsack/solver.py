#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])
Item_ratio = namedtuple("Item_Ratio", ['index', 'ratio', 'value', 'weight'])


def dp_solution(item_count, capacity, items):
    table = [[0 for _ in range(item_count+1)] for _ in range(capacity+1)]

    for cap in range(capacity + 1):
        table[cap][0] = 0

    for it in range(item_count + 1):
        table[0][it] = 0

    for cap in range(1, capacity + 1):
        for it in range(1, item_count + 1):
            if items[it-1].weight <= cap:
                table[cap][it] = max(
                    table[cap-items[it-1].weight][it-1] + items[it-1].value, table[cap][it-1])
            else:
                table[cap][it] = table[cap][it-1]
    return table


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []
    items_ratios = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))
        items_ratios.append(Item_ratio(
            i-1, int(parts[0])/int(parts[1]), int(parts[0]), int(parts[1])))

    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    # ----------------------------------------------------------------
    # first lets go with a greedy algorithm based on weight to value ratio
    # weight_to_value_ratio = []
    # for item in items:
    #     weight_to_value_ratio.append((item.value/item.weight, item.index))
    # weight_to_value_ratio.sort(key=lambda tup: tup[0], reverse=True)

    if item_count > 60:
        items_ratios.sort(key=lambda tup: tup[1], reverse=True)

        for item in items_ratios:
            if weight + item.weight <= capacity:
                taken[item.index] = 1
                value += item.value
                weight += item.weight
    else:
        # ----------------------------------------------------------------
        # After greedy (which clearly didn't pass, let's try a DP approach)
        table = dp_solution(item_count, capacity, items)
        # Now we reconstruct the solution based on the table
        curr_cap = capacity
        for it in range(item_count, 0, -1):
            if table[curr_cap][it] != table[curr_cap][it - 1]:
                taken[items[it - 1].index] = 1
                value += items[it-1].value
                curr_cap -= items[it - 1].weight
            else:
                taken[items[it - 1].index] = 0

    # ----------------------------------------------------------------
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
