import os
import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from tqdm import tqdm
import time
import re
import random
import numpy as np
import sys


def load_raw_data(file_path): 
    events = []
    values = []
    with open(file_path, 'r') as file:
        for line in tqdm(file, desc="Loading data"):
            event, value = line.rsplit(',', 1)
            events.append(event.strip())
            values.append(float(value.strip()))
    print(f"End of loading data>> the number of events: {len(events)}\n")
    return events, values


def parse_triplet(triplet_str):
    subject, operator, obj = triplet_str.split(', ', 2)
    subject = subject.strip()
    operator = operator.strip()
    obj = obj.strip()
    return subject, operator, obj


def clean_text(text):
    words = text.split() 
    # words = re.sub(r'/', ' ', text).split()  

    def file_case():
        return [word for word in words if word]

    def network_case():
        # ip = words[2].split('.')
        # return words[:2] + ip[:] + words[3:5]
        return [word for word in words if word]

    def process_case():
        return [word for word in words if word]
    
    def default_case():
        # return ['relationship']
        return [word for word in words if word]

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

    if os.path.exists(word_dataset_path) == False:
        preprocess_data(raw_file_path, word_dataset_path)

    documents = []
    with open(word_dataset_path, 'r') as file:
        for line in file:
            documents.append(line.strip())

    tagged_data = [TaggedDocument(words=doc.split(), tags=[str(i)]) for i, doc in enumerate(documents)]
    tag_file_path = '/behavior_baseline/baseline/cadets/data/tag_file.csv'
    with open(tag_file_path, 'w') as f:
        for i, doc in enumerate(documents):
            f.write(f'{i}, {doc}\n')
    print('Finish loading tagged_data.')

    model = Doc2Vec(
        vector_size=500, 
        min_count=1
        )
    model.build_vocab(tagged_data)
    print('Start training Doc2Vec model.')
    start_time = time.time()
    model.train(
        tagged_data,
        total_examples=model.corpus_count,
        epochs=10
    )
    end_time = time.time()
    training_time = end_time - start_time
    print(f"Doc2vec model training time: {training_time:.2f} 秒")

    doc2vec_model_path = '/behavior_baseline/baseline/cadets/model/doc2vec.model'
    os.makedirs(os.path.dirname(doc2vec_model_path), exist_ok=True)

    # save model
    model.save(doc2vec_model_path)

