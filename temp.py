## To save after trained offline
from qLearning_offline import QLearning_offline


def save_offline(obj):
    with open('offline_learn.txt', 'w') as f:
        for i in obj.learn.q_value_table:
            for j in obj.learn.q_value_table[i]:
                value = obj.learn.q_value_table[i][j].get_val_at_t(0)
                line = str(i) + ', ' + str(j) + ', ' + str(value) + '\n'
                f.write(line)   


## To load to train online (use this values as ininial)
def load_online(obj):
    obj.learn_offline_initial_conditions = QLearning_offline(obj)
    with open('offline_learn.txt', 'r') as f:
        for line in f:
            words = line.split(',')
            x = words[0]
            y = words[1]
            value = words[2]
            obj.learn_offline.q_value_table[x][y].val = value