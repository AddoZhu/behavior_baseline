import numpy as np
import time
import torch
from tqdm import tqdm
import re
import gensim
from gensim.models import Word2Vec
import sys

count = 0
all_words = set()
zero_vector = np.zeros(100)

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
    # words = re.sub(r'/', ' ', text).split()  
    words = text.split(' ', 1)
    
    def file_case():
        return [word for word in words if word]

    def network_case():
        words = text.split()
        return [words[1]] + [words[2]]

    def process_case():
        return [word for word in words if word]
    
    def default_case():
        words = text.split(' ', 1)
        return ['relationship']
        # return [word for word in words if word]

    switch = {
        "File": file_case,
        "Network": network_case,
        "Process": process_case
    }

    return switch.get(words[0], default_case)()


def get_word_vector(words, model):
    vectors = []
    global count

    for i, word in enumerate(words):
        try:
            vector = model.wv[word]
        except KeyError:
            vector = np.zeros(model.vector_size)
            # print(word)
            count = count + 1
        vectors.append(vector)

    vectors_matrix = np.array(vectors)
    return vectors_matrix.flatten()


def encode_triplet(triplet_str, model):

    subject, operator, obj = parse_triplet(triplet_str)
    
    subject = clean_text(subject)
    operator = clean_text(operator)
    obj = clean_text(obj)
    
    event_words = []
    event_words.extend(subject)
    event_words.extend(operator)
    event_words.extend(obj)

    if len(event_words) != 5:
        print(f"Event words length is : {triplet_str}")
        event_words = event_words[:5]
        sys.exit(1)

    event_vector = get_word_vector(event_words, model)
    return event_vector


def batch_encode_events(events, model, batch_size=128, save_path_prefix="encoded_batch"):
    vectors = []

    for i in tqdm(range(0, len(events), batch_size), desc="Encoding events"):
        batch_events = events[i:i + batch_size]
        batch_vectors = [encode_triplet(event, model) for event in batch_events]
        vectors.append(batch_vectors)

    encoded_events = np.vstack(vectors)
    np.save(save_path_prefix, encoded_events)
    print(f"End of encoding events>> the shape of encoded events: {encoded_events.shape}\n") 


if __name__ == '__main__':
    model_path = f'/behavior_baseline/baseline/cadets/model/word2vec.model'
    train_data = '/behavior_baseline/baseline/cadets/data/train_data.csv'
    train_data_path = f'/behavior_baseline/baseline/cadets/data/word2vec/train_data.npy'
    test_data = f'/behavior_baseline/baseline/cadets/data/test_data.csv'
    test_data_path = f'/behavior_baseline/baseline/cadets/data/word2vec/test_data.npy'
    malicious_data = f'/behavior_baseline/baseline/cadets/data/malicious_data.csv'
    malicious_data_path = f'/behavior_baseline/baseline/cadets/data/word2vec/malicious_data.npy'

    batch_size = 1024

    train_events = load_raw_data(train_data)
    test_events = load_raw_data(test_data)
    malicious_events = load_raw_data(malicious_data)

    word2vec = gensim.models.Word2Vec.load(model_path)
    print('End of loading Word2Vec model')

    encode_start_time = time.time()
    batch_encode_events(train_events, word2vec, batch_size, train_data_path)
    training_end_time = time.time()
    batch_encode_events(test_events, word2vec, batch_size, test_data_path)
    encode_end_time = time.time()
    batch_encode_events(malicious_events, word2vec, batch_size, save_path_prefix=malicious_data_path)

    print(f"Time of encoding event data in {encode_end_time - encode_start_time:.2f} seconds")
    print(f'Training events encoding time: {training_end_time - encode_start_time:.2f} seconds')
    print(f'Testing events encoding time: {encode_end_time - training_end_time:.2f} seconds')

