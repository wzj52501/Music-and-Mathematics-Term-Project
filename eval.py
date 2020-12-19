import numpy as np
from scipy import stats

note_status=['A3', 'A-3', 'A--3', 'A#3', 'A##3', 'B3', 'B-3', 'B--3', 'B#3', 'B##3', 'C3', 'C-3', 'C--3', 'C#3', 'C##3', 'D3', 'D-3', 'D--3', 'D#3', 'D##3', 'E3', 'E-3', 'E--3', 'E#3', 'E##3', 'F3', 'F-3', 'F--3', 'F#3', 'F##3', 'G3', 'G-3', 'G--3', 'G#3', 'G##3', 'A4', 'A-4', 'A--4', 'A#4', 'A##4', 'B4', 'B-4', 'B--4', 'B#4', 'B##4', 'C4', 'C-4', 'C--4', 'C#4', 'C##4', 'D4', 'D-4', 'D--4', 'D#4', 'D##4', 'E4', 'E-4', 'E--4', 'E#4', 'E##4', 'F4', 'F-4', 'F--4', 'F#4', 'F##4', 'G4', 'G-4', 'G--4', 'G#4', 'G##4', 'A5', 'A-5', 'A--5', 'A#5', 'A##5', 'B5', 'B-5', 'B--5', 'B#5', 'B##5', 'C5', 'C-5', 'C--5', 'C#5', 'C##5', 'D5', 'D-5', 'D--5', 'D#5', 'D##5', 'E5', 'E-5', 'E--5', 'E#5', 'E##5', 'F5', 'F-5', 'F--5', 'F#5', 'F##5', 'G5', 'G-5', 'G--5', 'G#5', 'G##5']
interval_status = ["whole", "half", "quarter", "eighth", "16th", "32nd", "64th"]

def srocc(output, target):
    return stats.spearmanr(output, target)[0]

def evaluate(note_gen, interval_gen, note_ori, interval_ori):
    n,m=len(note_gen),len(note_ori)
    x=[note_status.index(note_gen[i])*6+interval_status.index(interval_gen[i]) for i in range(n)]
    y=[note_status.index(note_ori[i])*6+interval_status.index(interval_ori[i]) for i in range(m)]

    score=[srocc(x[i:i+m],y) for i in range(n-m+1)]
    score.sort(reverse=True)

    result=0.0
    k=m
    for i in range(k):
        result+=score[i]
    return result

if __name__ == '__main__':
    note_list1 = ['G4','B-4','A4','B-4', 'G4','D4','A4','F#4', 'D4','G4','E-4','C4','A3', 'D4','B-3', 'G3', 'C4', 'A3', 'D4', 'B-3','A3','G3']
    interval_list1 = ['quarter','eighth','eighth','quarter','eighth','eighth','quarter','eighth','eighth','half', 'quarter','eighth','eighth','quarter','eighth','eighth','eighth','eighth','quarter','quarter','eighth','eighth']
    note_list2 = ['G4','B-4','A4','B-4', 'G4','D4','A4']
    interval_list2 = ['quarter','eighth','eighth','quarter','eighth','eighth','quarter']

    print(evaluate(note_list1,interval_list1,note_list2,interval_list2))
    