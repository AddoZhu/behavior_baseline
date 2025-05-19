from gensim.models import FastText
from gensim.models.word2vec import LineSentence
import gensim
import re
import os
import numpy as np
import sys


def load_raw_data(file_path):
    events = []
    values = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.rsplit(', ', 1)
            events.append(parts[0])
            values.append(parts[1])
    return events, values


def parse_triplet(triplet_str):
    subject, operator, obj = triplet_str.split(', ')
    subject = subject.strip()
    operator = operator.strip()
    obj = obj.strip()
    return subject, operator, obj


def clean_text(text):
    # words = re.sub(r'/', ' ', text).split() 
    words = text.split() 

    def file_case():
        return [word for word in words if word]

    def network_case():
        return [word for word in words if word]

    def process_case():
        return [word for word in words if word]
    
    def default_case():
        return ['relationship']
        # return [word for word in words if word]

    switch = {
        "File": file_case,
        "Network": network_case,
        "Process": process_case
    }

    return switch.get(words[0], default_case)()


def preprocess_data(raw_file_path, word_dataset_path):
    events, values = load_raw_data(raw_file_path)
    
    with open(word_dataset_path, 'w') as file:
        for event in events:
            try:
                subject, operator, obj = parse_triplet(event)
            except ValueError:
                print(f"Error: {event}")
                sys.exit(1)

            subject = clean_text(subject)
            operator = clean_text(operator)
            obj = clean_text(obj)
            
            event_words = []
            event_words.extend(subject)
            event_words.extend(operator)
            event_words.extend(obj)
            event_line = ' '.join(event_words)
            file.write(event_line + '\n')

if __name__ == '__main__':
    raw_file_path = '/behavior_baseline/baseline/cadets/data/frequency_train_data.csv'
    word_dataset_path = '/behavior_baseline/baseline/cadets/data/word_data.txt'
    word_vectors_path = '/behavior_baseline/baseline/cadets/model/word_vectors.kv'

    if os.path.exists(word_dataset_path) == False:
        preprocess_data(raw_file_path, word_dataset_path)
        print('Preprocess data done!')

    print('Start training FastText.')
    model = FastText(
        LineSentence(open(word_dataset_path, 'r', encoding='utf8')),
        vector_size=100,
        window=3,
        min_count=1,
        epochs=10, 
        min_n=3,
        max_n=6,
        workers=8 
    )

    fast_text_model_path = '/behavior_baseline/baseline/cadets/model/fasttext.model'
    model.save(fast_text_model_path)

    print('Saved FastText Model.')
    
    # model.wv.save(word_vectors_path)
    
    # word_vectors = model.wv
    # all_words = set(word_vectors.index_to_key)
    # zero_vector = np.zeros(model.vector_size)


