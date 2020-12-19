from MarkovBuilder import *
from main import *
from itertools import *
import numpy as np

class MusicMatrix:
    def __init__(self, order):
        self.previous_state = [None for i in range(order)]
        self.order = order
        self.current_note_num = 0 # 记录当前输入了几个note
        # 这里应该传入所有需要考虑到的音级，我这里只传入了例子中包含的音级，之后可以改这里就可以更改状态空间
        self.note_list=[]
        for level in range(3,6):
	        for c in range(7):
	        	note=chr(c+ord('A'))
	        	self.note_list.append(note+str(level))
	        	self.note_list.append(note+'-'+str(level))
	        	self.note_list.append(note+'--'+str(level))
	        	self.note_list.append(note+'#'+str(level))
	        	self.note_list.append(note+'##'+str(level))

        #print(len(self.note_list))
        self.interval_list = ["whole", "half", "quarter", "eighth", "16th", "32nd", "64th"]
        # 计算note和interval的笛卡尔积得到和在一起的状态
        self.state_list = list(product(self.note_list, self.interval_list))
        self.state_markov_matrix = MarkovBuilder(self.state_list, order)
    
    # add函数只用于初始化markov transition matrix
    def add(self, to_note, to_interval):
        to_state = (to_note, to_interval)
        if self.current_note_num < self.order:
            self.previous_state[self.current_note_num] = to_state
            self.current_note_num += 1
            return
        self.state_markov_matrix.add(self.previous_state, to_state)
        self.previous_state = self.previous_state[1:] + [to_state]
    
    # from_note 和 form_interval是有order个元素的list，这个用于生成音乐
    def next_state(self, from_note, from_interval):
        return self.state_markov_matrix.next_value(list(zip(from_note, from_interval)))

    def get_matrix(self):
        prob_matrix = self.state_markov_matrix.matrix.astype(float)
        state_num = len(self.state_list)
        self.previous_state_cnt = np.array(self.state_markov_matrix.previous_state, dtype=float)
        self.previous_state_cnt = self.previous_state_cnt/np.sum(self.previous_state_cnt)
        self.enum(state_num, 0, prob_matrix)
        return prob_matrix

    def enum(self, state_num, depth, matrix):
        if depth == self.order:
            # 如果所有转移概率都是0
            if np.sum(matrix) == 0:
                for i in range(state_num):
                    matrix[i] = self.previous_state_cnt[i]
            else:
                s = np.sum(matrix)
                for i in range(state_num):
                    matrix[i] = matrix[i]/s
            return
        else:
            for i in range(state_num):
                self.enum(state_num, depth + 1, matrix[i])
class MusicGenerator:
    # 初始化一个generator,需要提供之前训练好的一个markov转移矩阵，generator的order会自动选择和markov矩阵的order一致
    # 同时需要提供初始的order个note和interval
    def __init__(self, music_matrix, initial_note, initial_interval):
        order = music_matrix.order
        self.music_matrix = music_matrix
        self.previous_note = initial_note
        self.previous_interval = initial_interval
        self.order = order
        self.current_note_num = 0 # 记录当前输入了几个note
    
    def next_state(self):
        # 根据generator当前状态生成下一个状态
        next_state = self.music_matrix.next_state(self.previous_note, self.previous_interval)
        self.previous_note = self.previous_note[1:] + [next_state[0]]
        self.previous_interval = self.previous_interval[1:] + [next_state[1]]
        return next_state

if __name__ == '__main__':
    note_list = ['E4','G4','G4','G4', 'E4','A4','A4','B4','A4', 'A4','G4','C5','C5','C5','A4','C5','A4','G4']
    interval_list = ['eighth','eighth','quarter','eighth','eighth','eighth','eighth','eighth','eighth','eighth','eighth','quarter','eighth', 'eighth','quarter','eighth','eighth','half']

    order = 1
    # 这部分负责训练一个markov matrix
    markov_instance = MusicMatrix(order)
    length = len(interval_list)
    for i in range(length):
        #每次向markov_instance中丢一个note和interval，这些全部用来训练markov chain
        markov_instance.add(note_list[i], interval_list[i])
    
    #获取概率转移矩阵
    print(markov_instance.get_matrix())
    #获取计数矩阵，和转移矩阵有两个区别，一个是计数矩阵没有归一化，一个是全0行在转移矩阵中被设置为了按照之前state出现的次数产生概率
    print(markov_instance.state_markov_matrix.matrix)
    # 这部分负责生成一个新的音乐，先用之前训练好的markov_instance初始化generator,并为其传入初始值
    # 初始值需要传order个note和interval，order是Markov Chain的阶数
    generator = MusicGenerator(markov_instance, note_list[:order], interval_list[:order])
    
    for i in range(0,100):
        #不断调用generator的next_state方法获取下一个音符
        next_state = generator.next_state()
        note_list.append(next_state[0])
        interval_list.append(next_state[1])
    tune = '2/4'
    gen_stream=generate_stream(note_list, interval_list, tune)
    gen_stream.show('midi')
    save_stream(gen_stream,'test/','music8')
    
