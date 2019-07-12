# To save after trained offline
import time
from qLearning_offline import QLearning_offline
import os


def save_offline(obj, intermediate):
    if intermediate:
        if not os.path.isdir('qtables'):
            os.makedirs('qtables')
        filename = os.path.join('qtables', 'offline_learn_{}.txt'.format(int(time.time())))
    else:
        filename = 'offline_learn.txt'
    with open(filename, 'w') as f:
        for i in obj.learn.q_value_table:
            for j in obj.learn.q_value_table[i]:
                value = obj.learn.q_value_table[i][j].get_val_at_t(0)
                line = str(i) + ',' + str(j) + ',' + str(value) + ',\n'
                f.write(line)


# To load to train online (use this values as ininial)
def load_online(obj):
    obj.learn_offline_initial_conditions = QLearning_offline(obj)
    with open('offline_learn.txt', 'r') as f:
        for line in f:
            words = line.split(',')
            x = int(words[0])
            y = int(words[1])
            value = float(words[2])
            obj.learn_offline.q_value_table[x][y].val = value
            obj.learn.q_value_table[x][y].init_val = value
