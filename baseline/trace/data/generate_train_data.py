# Description: Generate frequency data for cadets   
import sys
import heapq

from collections import defaultdict
from config import event_csv_list

event_frequency = defaultdict(int)
subject_frequency = defaultdict(int)

def load_data(path):
    file_list = []
    with open(path, 'r') as file:
        for line in file:
            file_list.append(line.strip())
    return file_list

if __name__ == '__main__':
    frequency_path = '/behavior_baseline/baseline/trace/data/frequency_train_data.csv'

    for file in event_csv_list:
        print('Processing:', file)
        if file == '/Datasets/trace/e3_trace_preparation_event_12.csv':
            cnt = 0
            with open(file, 'r') as f:
                for line in f:
                    cnt += 1
                    if cnt >= 177306 and cnt <= 224388:
                        continue
                    event_frequency[line] += 1
                    subject = line.rsplit(', ', 1)[0]
                    subject_frequency[subject] += 1
            break

        if file == '/Datasets/trace/e3_trace_preparation_event_3.csv':
            cnt = 0
            with open(file, 'r') as f:
                for line in f:
                    cnt += 1
                    if cnt >= 178200 and cnt <= 288400:
                        continue
                    event_frequency[line] += 1
                    subject = line.rsplit(', ', 1)[0]
                    subject_frequency[subject] += 1
            break
    
        with open(file, 'r') as f:
            for line in f:
                event_frequency[line] += 1
                subject = line.rsplit(', ', 1)[0]
                subject_frequency[subject] += 1
    print('Event frequency:', len(event_frequency), 'Subject frequency:', len(subject_frequency))

    frequency_list = []
    for key in event_frequency:
        subject = key.rsplit(', ', 1)[0]
        src_num = subject_frequency.get(subject)
        event_num = event_frequency[key]
        score = 0.5 * (event_num / src_num) + 0.5
        frequency_list.append((key, score))
    
    print('Frequency list:', len(frequency_list))
    with open(frequency_path, 'w') as f:
        for item in frequency_list:
            info = item[0].replace('\n', '') +', ' + str(item[1])
            f.write(info + '\n')