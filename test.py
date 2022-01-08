import os
import matplotlib.pyplot as plt
import random

input_size = []
basic_time = []
basic_space = []
efficient_time = []
efficient_space = []
j = 0
i = 0
add_j = False
for test_num in range(15):
    if i == j:
        i += 1
    if add_j:  #
        j += 1
        add_j = False
    else:
        add_j = True
    input_size.append(2**(i+2) + 2**(j+2))
    input_file = f'test_input{test_num}.txt'
    with open(input_file, 'w') as input:
        input.write(f'ACTG\n')
        for k in range(i):
            input.write(f'{random.randint(1,9)}\n')
        input.write(f'TACG\n')
        for k in range(j):
            input.write(f'{random.randint(1, 9)}\n')
    os.system(f'python 2908471004_9485343331_9536762353_basic.py {input_file}')
    with open('output.txt', 'r') as output:
        lines = output.readlines()
        basic_time.append(float(lines[3]))
        basic_space.append(float(lines[4]))

    os.system(f'python 2908471004_9485343331_9536762353_efficient.py {input_file}')
    with open('output.txt', 'r') as output:
        lines = output.readlines()
        efficient_time.append(float(lines[3]))
        efficient_space.append(float(lines[4]))

plt.figure(1)
plt.plot(input_size, basic_time, marker='o')
plt.plot(input_size, efficient_time, marker='^')
plt.title('CPU Time vs Problem Size')
plt.xlabel('Problem Size (bytes)')
plt.ylabel('CPU Time (s)')
plt.legend(['Basic', 'Efficient'])
plt.show(block=False)

plt.figure(2)
plt.plot(input_size, basic_space, marker='o')
plt.plot(input_size, efficient_space, marker='^')
plt.title('Memory Usage vs Problem Size')
plt.xlabel('Problem Size (bytes)')
plt.ylabel('Memory Used (KB)')
plt.legend(['Basic', 'Efficient'])
plt.show()

cpu_time_diff = []
for i in range(len(basic_time)):
    if efficient_time[i] != 0 and basic_time[i] != 0:
        cpu_time_diff.append(efficient_time[i] / basic_time[i])
print(f'CPU time diff average: {sum(cpu_time_diff)/len(cpu_time_diff)}')
