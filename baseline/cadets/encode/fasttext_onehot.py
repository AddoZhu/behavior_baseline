import numpy as np
import time
import torch
from tqdm import tqdm
import re
import gensim
from gensim.models import KeyedVectors

count = 0
all_words = set()
zero_vector = np.zeros(100)

event_rela = ['file open', 'file read', 'file write', 'file modify', 'process load', 'process modify', 'process fork', 'network connect']
sub_object = ['Process', 'File', 'Network']

def create_onehotdic(event_rela, sub_object):
    event_onehot = {}
    entity_onehot = {}
    for i, event in enumerate(event_rela):
        one_hot = np.zeros(len(event_rela))
        one_hot[i] = 0.5
        custom_one_hot = np.where(one_hot == 0, -0.5, one_hot)
        event_onehot[event] = custom_one_hot
        # event_onehot[event] = one_hot
    
    for i, entity in enumerate(sub_object):
        one_hot = np.zeros(len(sub_object))
        one_hot[i] = 0.5
        custom_one_hot = np.where(one_hot == 0, -0.5, one_hot)
        entity_onehot[entity] = custom_one_hot
        # entity_onehot[entity] = one_hot

    # print(f'event_onehot: {event_onehot}')
    # print(f'entity_onehot: {entity_onehot}')

    return event_onehot, entity_onehot
    

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
    words = text.split()
    
    if words[0] in sub_object:
        if words[0] == 'Network': 
            return words[2]
        else: 
            return words[1]
    else:
        return words


def get_vector(word, model):
    global count
    try:
        vector = model.wv[word]
    except KeyError:
        vector = np.zeros(model.vector_size)
        print(word)
        count = count + 1
    return vector


def encode_triplet(triplet_str, model, event_onehot, entity_onehot):
    subject, operator, obj = parse_triplet(triplet_str)
    
    subject_clean = clean_text(subject)
    operator = operator.strip()
    obj_clean = clean_text(obj)

    vector1 = entity_onehot.get(subject.split()[0]) # 实体one-hot
    vector2 = get_vector(subject_clean, model) # 生成实体名向量

    vector3 = event_onehot.get(operator) # 关系one-hot

    vector4 = entity_onehot.get(obj.split()[0]) # 实体one-hot
    vector5 = get_vector(obj_clean, model) # 生成实体名向量

    con_vector = np.concatenate([vector1, vector2, vector3, vector4, vector5])
    # print(con_vector)

    return con_vector


def batch_encode_events(events, model, batch_size=128, save_path_prefix="encoded_batch"):
    vectors = []
    event_onehot, entity_onehot = create_onehotdic(event_rela, sub_object)

    for i in tqdm(range(0, len(events), batch_size), desc="Encoding events"):
        batch_events = events[i:i + batch_size]
        batch_vectors = [encode_triplet(event, model, event_onehot, entity_onehot) for event in batch_events]
        vectors.append(batch_vectors)

    encoded_events = np.vstack(vectors)
    np.save(save_path_prefix, encoded_events)
    print(f"End of encoding events>> the shape of encoded events: {encoded_events.shape}\n") 


if __name__ == '__main__':
    model_path = f'/behavior_baseline/baseline/cadets/model/fasttext.model'
    train_data = '/behavior_baseline/baseline/cadets/data/train_data.csv'
    train_data_path = f'/behavior_baseline/baseline/cadets/data/fasttext/train_data_onehot.npy'
    test_data = f'/behavior_baseline/baseline/cadets/data/test_data.csv'
    test_data_path = f'/behavior_baseline/baseline/cadets/data/fasttext/test_data_onehot.npy'
    malicious_data = f'/behavior_baseline/baseline/cadets/data/malicious_data.csv'
    malicious_data_path = f'/behavior_baseline/baseline/cadets/data/fasttext/malicious_data_onehot.npy'

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

