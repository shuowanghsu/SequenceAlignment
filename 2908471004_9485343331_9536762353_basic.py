"""
CSCI 570 Project
Kuan-Ying Wang
Sahil Markanday
Shuo Wang Hsu
"""
import sys
import tracemalloc
import time
import math

def generate_input_strings(input_file):
    string_a, index_a, string_b, index_b = generate_input_indexes(input_file)
    input_a = generate_input_string(string_a, index_a)
    input_b = generate_input_string(string_b, index_b)
    return input_a, input_b

def generate_input_indexes(input_file):
    index_a = list()
    index_b = list()
    with open(input_file) as input:
        string_a = input.readline().strip()  # read first base string A
        line = input.readline()
        while line.strip().isdigit():
            index_a.append(int(line))
            line = input.readline()
        string_b = line.strip()  # read second string B
        line = input.readline()
        while line:
            index_b.append(int(line))
            line = input.readline()
    return string_a, index_a, string_b, index_b


def generate_input_string(base, index):
    for i in range(len(index)):
        pre = base[0: index[i] + 1]
        post = base[index[i] + 1: len(base)]
        result = pre + base
        result = result + post
        base = result
    return base


def basic_alignment(input_a, input_b, a, d):
    # initialization
    m = len(input_a)
    n = len(input_b)

    if m == 0:
        for i in range(n):
            alignment_b = alignment_b + input_b[i]
            alignment_a = alignment_a + '_'
        return alignment_a, alignment_b, (d*len(input_b))   
    elif n == 0:
        for i in range(m):
            alignment_a = alignment_a + input_a[i]
            alignment_b = alignment_b + '_'
        return alignment_a, alignment_b, (d*len(input_a))

    opt = [[0 for i in range(n+1)] for j in range(m+1)]
    char_to_num = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    for i in range(m+1):
        opt[i][0] = i * d
    for j in range(n+1):
        opt[0][j] = j * d

    # compute OPT array
    for j in range(1, n+1):
        for i in range(1, m+1):
            matched = a[char_to_num[input_a[i-1]]][char_to_num[input_b[j-1]]] + opt[i-1][j-1]
            a_not_matched = d + opt[i-1][j]
            b_not_matched = d + opt[i][j-1]
            opt[i][j] = min(matched, a_not_matched, b_not_matched)
    # print(f'Optimal score = {opt[m-1][n-1]}')

    # reconstruct alignments from OPT array
    alignment_a = ''
    alignment_b = ''
    index_a = m
    index_b = n
    while index_a > 0 or index_b > 0:
        if index_a > 0 and index_b > 0 and opt[index_a][index_b] == a[char_to_num[input_a[index_a - 1]]][char_to_num[input_b[index_b - 1]]] + \
                opt[index_a - 1][index_b - 1]:
            alignment_a = input_a[index_a - 1] + alignment_a
            alignment_b = input_b[index_b - 1] + alignment_b
            index_a -= 1
            index_b -= 1
        elif index_a > 0 and opt[index_a][index_b] == d + opt[index_a - 1][index_b]:
            alignment_a = input_a[index_a - 1] + alignment_a
            alignment_b = '_' + alignment_b
            index_a -= 1
        else:  # opt[i][j] == delta + opt[i][j-1]
            alignment_a = '_' + alignment_a
            alignment_b = input_b[index_b - 1] + alignment_b
            index_b -= 1

    # Verify result
    # cost = 0
    # for i in range(len(alignment_a)):
    #     if alignment_a[i] == alignment_b[i]:
    #         pass
    #     elif alignment_a[i] == '_' or alignment_b[i] == '_':
    #         cost += d
    #     else:
    #         cost += a[char_to_num[alignment_a[i]]][char_to_num[alignment_b[i]]]
    # print(f'Expected cost: {opt[m][n]}. Verified cost: {cost}')
    return alignment_a, alignment_b, opt[m][n]


if __name__ == "__main__":
    # Start time and memory tracing
    tracemalloc.start()
    start_time = time.time()
    input_file = 'input.txt'
    output_file = 'output.txt'
    # allow passing in input file
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    inputA, inputB = generate_input_strings(input_file=input_file)

    alpha = [
        [0, 110, 48, 94],
        [110, 0, 118, 48],
        [48, 118, 0, 110],
        [94, 48, 110, 0]
    ]
    delta = 30

    # Run basic algo
    alignment_A, alignment_B, cost = basic_alignment(inputA, inputB, alpha, delta)

    cost = float(cost)

    # End memory and timing trace
    elapsed_time = time.time() - start_time
    current_memory_usage, peak_memory_usage = tracemalloc.get_traced_memory()

    peak_memory_usage = float(peak_memory_usage)

    # Write output
    alignment_A_output = alignment_A[:50] + ' ' + alignment_A[-50:]
    alignment_B_output = alignment_B[:50] + ' ' + alignment_B[-50:]
    with open(output_file, 'w') as output:
        output.write(f'{alignment_A_output}\n{alignment_B_output}\n{cost}\n{elapsed_time}\n{peak_memory_usage}')
        # print(f'{first_50_alignment}\n{last_50_alignment}\n{elapsed_time}\n{peak_memory_usage}')
