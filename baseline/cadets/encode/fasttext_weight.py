import numpy as np
import time
import torch
from tqdm import tqdm
import re
import gensim
from gensim.models import KeyedVectors
import math

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
    words = re.sub(r'/', ' ', text).split()  
    # words = text.split(' ', 1)
    
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
        return [word for word in words if word]

    switch = {
        "File": file_case,
        "Network": network_case,
        "Process": process_case
    }

    return switch.get(words[0], default_case)()


def get_vector(word, model):
    global count
    try:
        vector = model.wv[word]
    except KeyError:
        vector = np.zeros(model.vector_size)
        print(word)
        count = count + 1
    return vector


def filename_weight(filename, model):
    documents = list(filter(None, filename.split('/')))
    d_len = len(documents)
    vector = np.zeros(model.vector_size)
    sum_weight = 0
    if d_len == 0:
        vector = get_vector(filename, model)
    else:
        for i, document in enumerate(documents):
            d_vec = get_vector(document, model)
            weight = math.log((d_len + 1) / (d_len - i))
            vector = vector + weight * d_vec
            sum_weight += weight
        vector = vector / sum_weight
    return np.array(vector, dtype=np.float32)


def encode_triplet(triplet_str, model):
    subject, operator, obj = parse_triplet(triplet_str)
    
    subject = clean_text(subject)
    operator = clean_text(operator)
    obj = clean_text(obj)

    vectors = []
    vectors.append(get_vector(subject[0], model))
    if subject[0] == 'File':
        vectors.append(filename_weight(subject[1], model))
    else:
        vectors.append(get_vector(subject[1], model))

    vectors.append(get_vector(operator[0], model))

    vectors.append(get_vector(obj[0], model))
    if obj[0] == 'File':
        vectors.append(filename_weight(obj[1], model))
    else:
        vectors.append(get_vector(obj[1], model))

    vectors_matrix = np.array(vectors)
    return vectors_matrix.flatten()


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
    model_path = f'/behavior_baseline/baseline/cadets/model/fasttext_split.model'
    train_data = '/behavior_baseline/baseline/cadets/data/train_data.csv'
    train_data_path = f'/behavior_baseline/baseline/cadets/data/fasttext/train_data_weight.npy'
    test_data = f'/behavior_baseline/baseline/cadets/data/test_data.csv'
    test_data_path = f'/behavior_baseline/baseline/cadets/data/fasttext/test_data_weight.npy'
    malicious_data = f'/behavior_baseline/baseline/cadets/data/malicious_data.csv'
    malicious_data_path = f'/behavior_baseline/baseline/cadets/data/fasttext/malicious_data_weight.npy'

    batch_size = 1024

    train_events = load_raw_data(train_data)
    test_events = load_raw_data(test_data)
    malicious_events = load_raw_data(malicious_data)

    FASTTEXT = gensim.models.FastText.load(model_path)
    print('End of loading FastText model')
    
    encode_start_time = time.time()
    batch_encode_events(train_events, FASTTEXT, batch_size, save_path_prefix=train_data_path)
    training_end_time = time.time()
    batch_encode_events(test_events, FASTTEXT, batch_size, save_path_prefix=test_data_path)
    encode_end_time = time.time()
    batch_encode_events(malicious_events, FASTTEXT, batch_size, save_path_prefix=malicious_data_path)

    print(f"Time of encoding event data in {encode_end_time - encode_start_time:.2f} seconds")
    print(f'Training events encoding time: {training_end_time - encode_start_time:.2f} seconds')
    print(f'Testing events encoding time: {encode_end_time - training_end_time:.2f} seconds')

