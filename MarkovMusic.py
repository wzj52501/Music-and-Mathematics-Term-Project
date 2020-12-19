from MarkovBuilder import *
from main import *
from eval import *

class MusicMatrix:
    def __init__(self, order):
        self.previous_note = [None for i in range(order)]
        self.previous_interval = [None for i in range(order)]
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

        print(self.note_list)
        self.interval_list = ["whole", "half", "quarter", "eighth", "16th", "32nd", "64th"]
        self.note_markov_matrix = MarkovBuilder(self.note_list, order)
        self.interval_markov_matrix = MarkovBuilder(self.interval_list, order)
    
    # add函数只用于初始化markov transition matrix
    def add(self, to_note, to_interval):
        if self.current_note_num < self.order:
            self.previous_note[self.current_note_num] = to_note
            self.previous_interval[self.current_note_num] = to_interval
            self.current_note_num += 1
            return
        self.note_markov_matrix.add(self.previous_note, to_note)
        self.interval_markov_matrix.add(self.previous_interval, to_interval)
        self.previous_note = self.previous_note[1:] + [to_note]
        self.previous_interval = self.previous_interval[1:] + [to_interval]
    
    # from_note 和 form_interval是有order个元素的list，这个用于生成音乐
    def next_state(self, from_note, from_interval):
        return [self.note_markov_matrix.next_value(from_note), self.interval_markov_matrix.next_value(from_interval)]

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
    note_list = ['G4','B-4','A4','B-4', 'G4','D4','A4','F#4', 'D4','G4','E-4','C4','A3', 'D4','B-3', 'G3', 'C4', 'A3', 'D4', 'B-3','A3','G3']
    interval_list = ['quarter','eighth','eighth','quarter','eighth','eighth','quarter','eighth','eighth','half', 'quarter','eighth','eighth','quarter','eighth','eighth','eighth','eighth','quarter','quarter','eighth','eighth']
    tune = '4/4'

    order = 1
    # 这部分负责训练一个markov matrix
    markov_instance = MusicMatrix(order)
    length = len(interval_list)
    for i in range(length):
        #每次向markov_instance中丢一个note和interval，这些全部用来训练markov chain
        markov_instance.add(note_list[i], interval_list[i])
    
    #这里是打印生成的markov转移矩阵，note和interval是独立的两个矩阵，不过之后也可以修改
    print('note_list:', markov_instance.note_list)
    print('note_matrix:\n', markov_instance.note_markov_matrix.matrix[2])
    print('interval_list:', markov_instance.interval_list)
    print('interval_matrix:\n' , markov_instance.interval_markov_matrix.matrix)
    # 这部分负责生成一个新的音乐，先用之前训练好的markov_instance初始化generator,并为其传入初始值
    # 初始值需要传order个note和interval，order是Markov Chain的阶数
    generator = MusicGenerator(markov_instance, note_list[:order], interval_list[:order])
    
    best=0.0

    for loop in range(1024):
	    note_gen=[]
	    interval_gen=[]
	    for i in range(0,100):
	        #不断调用generator的next_state方法获取下一个音符
	        next_state = generator.next_state()
	        note_gen.append(next_state[0])
	        interval_gen.append(next_state[1])

	    ret=evaluate(note_gen,interval_gen,note_list,interval_list)
	    print(loop, ret)
	    if(ret > best):
	    	best=ret
	    	gen_stream=generate_stream(note_gen, interval_gen, tune)
    		#gen_stream.show('midi')
    		save_stream(gen_stream,'test/','score='+str(ret))


    ori_stream=generate_stream(note_list, interval_list, tune)
    save_stream(ori_stream,'test/','orimusic8')
    
