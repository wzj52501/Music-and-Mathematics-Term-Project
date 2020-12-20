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
	note_list = ['E4','G4','G4','G4', 'E4','A4','A4','B4','A4', 'A4','G4','C5','C5','C5','A4','C5','A4','G4']
	interval_list = ['eighth','eighth','quarter','eighth','eighth','eighth','eighth','eighth','eighth','eighth','eighth','quarter','eighth', 'eighth','quarter','eighth','eighth','half']
	tune = '2/4'
	gen_stream=generate_stream(note_list, interval_list, tune)
	gen_stream.show('midi')
	save_stream(gen_stream,'test/','sample6')
