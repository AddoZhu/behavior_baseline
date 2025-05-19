import numpy as np
import time
import sys
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score 


def load_raw_data(raw_file_path):
    events = []
    with open(raw_file_path, 'r') as f:
        for line in f:
            events.append(line.strip())
    return events


def load_input_data(data_path):
    input_data = np.load(data_path, allow_pickle=True)
    return input_data


def load_values_data(path):
    values = []
    with open(path, 'r') as file:
        for line in file:
            value = line.rsplit(', ', 1)[1]
            values.append(float(value.strip()))
    return np.array(values)

if __name__ == '__main__':
    embedding_model = 'fasttext'
    test_data = f'/behavior_baseline/baseline/cadets/data/test_data.csv'
    test_data_path = f'/behavior_baseline/baseline/cadets/data/{embedding_model}/test_data.npy'
    malicious_data = f'/behavior_baseline/baseline/cadets/data/malicious_data.csv'
    malicious_data_path = f'/behavior_baseline/baseline/cadets/data/{embedding_model}/malicious_data.npy'

    batch_size = 1024

    model_path = f'/behavior_baseline/baseline/cadets/model/{embedding_model}_cnn_model.keras'
    cnn_model = load_model(model_path)
    print("Loaded CNN model")

    test_event = load_raw_data(test_data)
    x_test = load_input_data(test_data_path)
    y_test = load_values_data(test_data)

    start_time = time.time()   
    y_pred_test = cnn_model.predict(x_test)
    end_time = time.time()

    total_time = end_time - start_time      
    print(f"Total execution time: {total_time:.2f} 秒")  

    mse = mean_squared_error(y_test, y_pred_test) 
    mae = mean_absolute_error(y_test, y_pred_test)
    r2 = r2_score(y_test, y_pred_test)

    print(f"MSE: {mse}")
    print(f"MAE: {mae}")
    print(f"R²: {r2}" + '\n')

    count = 0
    difference = 0.2
    for fre, pred in zip(y_test, y_pred_test):
        if abs(fre - pred) < difference:
            count += 1
    print(f'difference < {difference}: {count} / {len(test_event)}')

    malicious_event = load_raw_data(malicious_data)
    x_malicious = load_input_data(malicious_data_path)
    y_pred_malicious = cnn_model.predict(x_malicious)

    count = 0
    difference = 0.2
    for pred in y_pred_malicious:
        if pred < difference:
            count += 1
    print(f'prediction < {difference}: {count} / {len(malicious_event)}')