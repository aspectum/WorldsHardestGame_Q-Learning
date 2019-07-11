## To save after trained offline
from qLearning_offline import QLearning_offline
def save_offline(self):
    with open('offline_learn.txt', 'w') as f:
        for i in self.learn.q_value_table:
            for j in self.learn.q_value_table[i]:
                value = self.learn.q_value_table[i][j].get_val_at_t(0)
                line = str(i) + ', ' + str(j) + ', ' + str(value) + '\n'
                f.write(line)   

## To load to train online (use this values as ininial)
def load_online(self):
    self.learn_offline_initial_conditions = QLearning_offline(self)
    with open('offline_learn.txt', 'r') as f:
        for line in f:
            words = line.split(',')
            x = words[0]
            y = words[1]
            value = words[2]
            self.learn_offline.q_value_table[x][y].val = value