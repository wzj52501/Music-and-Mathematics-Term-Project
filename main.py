from music21 import *


def save_stream(save_stream, path, name):
	save_stream.write('midi', fp=path+name+'.mid')
	save_stream.write('xml', fp=path+name+'.xml')

def save_music(music, path, name):
	mini_stream = stream.Stream(music)
	save_stream(mini_stream, path, name)

def generate_stream(note_list, interval_list, tune):
	gen_stream=stream.Stream()
	ts = meter.TimeSignature(tune)
	gen_stream.insert(0, ts)
	n = len(note_list)
	for i in range(n):
		f = note.Note(note_list[i])
		f.duration = duration.Duration(interval_list[i])
		gen_stream.append(f)

	return gen_stream

if __name__ == '__main__':
# “whole”, “half”, “quarter”, “eighth”, “16th”, “32nd”, “64th”.
	note_list = ['C','D','F','G', 'A','G','F#','C--', 'D','F','A#','G-','E#']
	interval_list = ['quarter','quarter','quarter','quarter','quarter','quarter','quarter','quarter','quarter','quarter','quarter','eighth','eighth']
	tune = '4/4'
	gen_stream=generate_stream(note_list, interval_list, tune)
	save_stream(gen_stream,'test/','test')
