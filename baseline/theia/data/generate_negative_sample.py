import random

def load_raw_data(file_path): 
    events = set()
    values = []
    with open(file_path, 'r') as file:
        for line in file:
            lines = line.split(', ')
            event = lines[0] + ', relationship, ' + lines[2]
            if event not in events:
                events.add(event)
                values.append(float(lines[3].strip()))
    print(f"End of loading data>> the number of events: {len(events)}\n")
    return list(events), values

# Compute difference score between triplet1 and triplet2
# Scope of the score is from 0.01 to 0.1
def compute_difference(triplet1, triplet2):
    max_len = max(len(triplet1), len(triplet2))

    str1 = triplet1.ljust(max_len)
    str2 = triplet2.ljust(max_len)

    diff_count = sum(1 for a, b in zip(str1, str2) if a != b)
    
    diff_score = ((max_len - diff_count) / max_len) * 0.09 + 0.01
    return diff_score

def parse_event(event):
    subject, operator, obj = event.split(', ', 2)
    subject = subject.strip()
    operator = operator.strip()
    obj = obj.strip()
    return subject, operator, obj

def load_entity_data():
    Network = ['Network Connect 111.155.12.122 : 38622', 'Network Connect 111.155.13.122 : 3122', 'Network Connect 111.125.12.122 : 37624']
    Process = ['Process app1', 'Process app2', 'Process app3']
    File = ['File /home/user1/file1', 'File /home/user1/file2', 'File /home/user1/file3']
    return Process, File, Network

def construct_negative_samples(Process, File, Network, events):
    negative_samples = []

    for event in events:
        subject, operator, obj = parse_event(event)
        
        if subject.split(' ')[0] == 'Process': 
            subjects = Process
        elif subject.split(' ')[0] == 'File':
            subjects = File
        else:
            subjects = Network

        if obj.split(' ')[0] == 'Process': 
            objects = Process
        elif obj.split(' ')[0] == 'File':
            objects = File
        else:
            objects = Network

        # Randomly replace subject
        neg_subject = random.choice(subjects)
        neg_value = compute_difference(subject, neg_subject)
        if neg_value == 0.1:
            print(subject, neg_subject)
        negative_samples.append((neg_subject, operator, obj, neg_value))

        # Randomly replace object
        neg_object = random.choice(objects)
        neg_value = compute_difference(obj, neg_object)
        if neg_value == 0.1:
            print(obj, neg_object)
        negative_samples.append((subject, operator, neg_object, neg_value))

    return negative_samples

if __name__ == '__main__':
    raw_file_path = '/behavior_baseline/baseline/theia/data/frequency_train_data.csv'
    train_file_path = '/behavior_baseline/baseline/theia/data/train_data.csv'
    events, values = load_raw_data(raw_file_path)
    
    Process, File, Network = load_entity_data()

    negative_samples = construct_negative_samples(Process, File, Network, events)

    count = 0
    with open(train_file_path, 'w') as file:
        for i, event in enumerate(events):
            file.write(event + ', ' + str(values[i]) + '\n')

            sample1 = negative_samples[2 * i]
            file.write(', '.join(map(str, sample1)) + '\n')
            # file.write(', '.join(map(str, sample1)) + '\n')


            sample2 = negative_samples[2 * i + 1]
            file.write(', '.join(map(str, sample2)) + '\n')
            # file.write(', '.join(map(str, sample2)) + '\n')
            count += 5
    print(count)
