import torch
from tqdm import tqdm
import time
import numpy as np
import re
import sys
import tensorflow as tf
from transformers import AutoModel, BertTokenizer, BertModel


count = 0
# loading TinyBERT model
model_dir = '/Models/TinyBERT'
tokenizer = BertTokenizer.from_pretrained(model_dir)
model = BertModel.from_pretrained(model_dir)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)


def load_raw_data(file_path): 
    events = []
    with open(file_path, 'r') as file:
        for line in tqdm(file, desc="Loading data"):
            if file_path == '/behavior_baseline/baseline/cadets/data/train_data.csv' or file_path == '/behavior_baseline/baseline/cadets/data/test_data.csv':
                line = line.rsplit(', ', 1)[0]
            events.append(line.strip())
    print(f"End of loading data>> the number of events: {len(events)}\n")
    return events


def encode_event(event):
    inputs = tokenizer(event, return_tensors='pt').to(device)
    outputs = model(**inputs)
    last_hidden_state = outputs.last_hidden_state
    vector = last_hidden_state.mean(dim=1).squeeze(0).detach().cpu().numpy()
    return vector


def batch_encode_events(events, batch_size=128, save_path_prefix="encoded_batch"):
    vectors = []

    for i in tqdm(range(0, len(events), batch_size), desc="Encoding events"):
        batch_events = events[i:i + batch_size]
        batch_vectors = [encode_event(event) for event in batch_events]
        vectors.append(batch_vectors)

    encoded_events = np.vstack(vectors)
    np.save(save_path_prefix, encoded_events)
    print(f"End of encoding events>> the shape of encoded events: {encoded_events.shape}\n") 


if __name__ == '__main__':
    train_data = '/behavior_baseline/baseline/cadets/data/train_data.csv'
    train_data_path = f'/behavior_baseline/baseline/cadets/data/bert/train_data_tiny.npy'
    test_data = f'/behavior_baseline/baseline/cadets/data/test_data.csv'
    test_data_path = f'/behavior_baseline/baseline/cadets/data/bert/test_data_tiny.npy'
    malicious_data = f'/behavior_baseline/baseline/cadets/data/malicious_data.csv'
    malicious_data_path = f'/behavior_baseline/baseline/cadets/data/bert/malicious_data_tiny.npy'
    
    batch_size = 1024

    train_events = load_raw_data(train_data)
    test_events = load_raw_data(test_data)
    malicious_events = load_raw_data(malicious_data)

    print('End of loading events')

    encode_start_time = time.time()
    batch_encode_events(train_events, batch_size, save_path_prefix=train_data_path)
    training_end_time = time.time()
    batch_encode_events(test_events, batch_size, save_path_prefix=test_data_path)
    encode_end_time = time.time()
    batch_encode_events(malicious_events, batch_size, save_path_prefix=malicious_data_path)

    print(f"Time of encoding event data in {encode_end_time - encode_start_time:.2f} seconds")
    print(f'Training events encoding time: {training_end_time - encode_start_time:.2f} seconds')
    print(f'Testing events encoding time: {encode_end_time - training_end_time:.2f} seconds')

