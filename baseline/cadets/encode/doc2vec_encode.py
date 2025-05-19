import numpy as np
import time
import torch
from tqdm import tqdm
import re
import gensim
import csv

max_position_size = 10
count = 0

def load_raw_data(file_path): 
    events = []
    with open(file_path, 'r') as file:
        for line in tqdm(file, desc="Loading data"):
            if file_path == '/behavior_baseline/baseline/cadets/data/train_data.csv' or file_path == '/behavior_baseline/baseline/cadets/data/test_data.csv':
                line = line.rsplit(', ', 1)[0]
            events.append(line.strip())
    print(f"End of loading data>> the number of events: {len(events)}\n")
    return events

def parse_triplet(triplet_str):
    subject, operator, obj = triplet_str.split(', ')
    subject = subject.strip()
    operator = operator.strip()
    obj = obj.strip()
    return subject, operator, obj

def clean_text(text):
    words = re.sub(r'/', ' ', text).split()  
    
    def file_case():
        words = text.split(' ', 1)
        return [word for word in words if word]

    def network_case():
        words = text.split()
        return [words[1]] + [words[2]]

    def process_case():
        words = text.split(' ', 1)
        return [word for word in words if word]
    
    def default_case():
        words = text.split(' ', 1)
        return ['relationship']

    switch = {
        "File": file_case,
        "Network": network_case,
        "Process": process_case
    }

    return switch.get(words[0], default_case)()


def get_word_vector(words, model, data_dict):
    sentence = ' '.join(words)
    if sentence in data_dict:
        vector = model.dv[data_dict.get(sentence)]
    else:
        vectors = []
        for word in words:
            if word in model.wv:
                vectors.append(model.wv[word][:100])
            else:
                vectors.append(np.zeros(100))
        vector = np.array(vectors).flatten()

    return vector


def encode_triplet(triplet_str, model, data_dict):
    subject, operator, obj = parse_triplet(triplet_str)
    
    subject = clean_text(subject)
    operator = clean_text(operator)
    obj = clean_text(obj)
    
    event_words = []
    event_words.extend(subject)
    event_words.extend(operator)
    event_words.extend(obj)

    event_vector = get_word_vector(event_words, model, data_dict)
    return event_vector


def batch_encode_events(events, model, data_dict, batch_size=128, save_path_prefix="encoded_batch"):
    vectors = []

    for i in tqdm(range(0, len(events), batch_size), desc="Encoding events"):
        batch_events = events[i:i + batch_size]
        batch_vectors = [encode_triplet(event, model, data_dict) for event in batch_events]
        vectors.append(batch_vectors)

    encoded_events = np.vstack(vectors)
    np.save(save_path_prefix, encoded_events)
    print(f"End of encoding events>> the shape of encoded events: {encoded_events.shape}\n") 

if __name__ == '__main__':
    model_path = f'/behavior_baseline/baseline/cadets/model/doc2vec.model'
    train_data = '/behavior_baseline/baseline/cadets/data/train_data.csv'
    train_data_path = f'/behavior_baseline/baseline/cadets/data/doc2vec/train_data.npy'
    test_data = f'/behavior_baseline/baseline/cadets/data/test_data.csv'
    test_data_path = f'/behavior_baseline/baseline/cadets/data/doc2vec/test_data.npy'
    tag_file = f'/behavior_baseline/baseline/cadets/data/tag_file.csv'
    malicious_data = f'/behavior_baseline/baseline/cadets/data/malicious_data.csv'
    malicious_data_path = f'/behavior_baseline/baseline/cadets/data/doc2vec/malicious_data.npy'

    data_dict = {}

    with open(tag_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            i, event = row[0], row[1].strip()
            data_dict[event] = i

    batch_size = 1024

    train_events = load_raw_data(train_data)
    test_events = load_raw_data(test_data)
    malicious_events = load_raw_data(malicious_data)

    DOC2VEC = gensim.models.Doc2Vec.load(model_path)
    print('End of loading Doc2Vec model')

    encode_start_time = time.time()
    batch_encode_events(train_events, DOC2VEC, data_dict, batch_size, train_data_path)
    training_end_time = time.time()
    batch_encode_events(test_events, DOC2VEC, data_dict, batch_size, test_data_path)
    encode_end_time = time.time()
    batch_encode_events(malicious_events, DOC2VEC, data_dict, batch_size, malicious_data_path)

    print(f"Time of encoding event data in {encode_end_time - encode_start_time:.2f} seconds")
    print(f'Training events encoding time: {training_end_time - encode_start_time:.2f} seconds')
    print(f'Testing events encoding time: {encode_end_time - training_end_time:.2f} seconds')


