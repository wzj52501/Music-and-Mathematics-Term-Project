from music21 import *

music=converter.parse("tinynotation: 3/4 c4 d8 f g16 a g f# c4 d8 f a g e#")

music.show('midi')
mini_stream = stream.Stream(music)
mini_stream.write('midi', fp='output.mid')
mini_stream.write('xml', fp='test.xml')
