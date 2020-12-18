import random
import numpy as np
class MarkovBuilder:
    def __init__(self, value_list, order):
        self.value_lookup = {}
        self.reverse_value_lookup = value_list
        self.order = order
        value_num = len(value_list)
        for i in range(0,value_num):
            self.value_lookup[value_list[i]] = i
        # 初始化转移矩阵
        self.matrix = np.zeros([value_num for i in range(order+1)], dtype = int)
    
    def add(self, from_value, to_value):
        matrix = self.matrix
        value_map = self.value_lookup

        for i in range(self.order):
            matrix = matrix[value_map[from_value[i]]]
        print("form value is ", from_value)
        print("to value is ", to_value)
        matrix[value_map[to_value]] += 1

    def next_value(self, from_value):
        value_map = self.value_lookup
        value_counts = self.matrix
        for i in range(self.order):
            value_counts = value_counts[value_map[from_value[i]]]
        value_index = self.randomly_choose(value_counts)
        if(value_index < 0):
            raise RuntimeError("Non-existent value selected.")
        else:
            return self.reverse_value_lookup[value_index]
    
    def randomly_choose(self, choice_counts):
        counted_sum = 0
        count_sum = sum(choice_counts)
        if count_sum == 0:
            raise RuntimeError("向任何状态的转移概率都为0")
        selected_count = random.randrange(1, count_sum + 1)
        length = len(choice_counts)
        for index in range(0, length):
            counted_sum += choice_counts[index]
            if(counted_sum >= selected_count):
                return index
        raise RuntimeError("Impossible value selection made. BAD!")

        
        
