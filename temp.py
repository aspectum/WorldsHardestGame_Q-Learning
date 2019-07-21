# To save after trained offline
import time
from qLearning import QLearning
import os
from shutil import copyfile


def save_offline(obj, intermediate):
    if intermediate:
        if not os.path.isdir('qtables'):
            os.makedirs('qtables')
        filename = os.path.join('qtables', 'offline_learn_{}.txt'.format(int(time.time())))
    else:
        filename = 'offline_learn.txt'
    with open(filename, 'w') as f:
        f.write(str(obj.player_vel) + '\n')
        for i in obj.learn.q_value_table:
            for j in obj.learn.q_value_table[i]:
                value = obj.learn.q_value_table[i][j].get_val_at_t(0)
                line = str(i) + ',' + str(j) + ',' + str(value) + ',\n'
                f.write(line)
    # copyfile('offline_learn.txt', 'resultado/offline_learn.txt')


# To load to train online (use this values as ininial)
def load_online(obj):
    obj.learn_offline_initial_conditions = QLearning(obj, online=False)
    with open('offline_learn.txt', 'r') as f:
        f.readline()
        for line in f:
            words = line.split(',')
            x = int(words[0])
            y = int(words[1])
            value = float(words[2])
            obj.learn_offline_initial_conditions.q_value_table[x][y].val = value
            obj.learn.q_value_table[x][y].init_val = value


def save_online(obj):
    filename = 'resultado/online_learn.txt'
    with open(filename, 'w') as f:
        f.write(str(obj.player_vel) + '\n')
        for i in obj.learn.q_value_table:
            for j in obj.learn.q_value_table[i]:
                f.write(str(i) + ',' + str(j) + ',')
                if len(obj.learn.q_value_table[i][j].t) > 0:
                    for k in range(len(obj.learn.q_value_table[i][j].t)):
                        t = obj.learn.q_value_table[i][j].t[k]
                        v = obj.learn.q_value_table[i][j].val[k]
                        f.write(str(t) + ',' + str(v) + ',')
                f.write('\n')
