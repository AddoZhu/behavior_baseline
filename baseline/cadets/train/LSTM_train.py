import numpy as np
import time
import pickle
import threading
from sklearn.neural_network import MLPRegressor
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from datetime import datetime
import random

def load_input_data(data_path):
    return np.load(data_path, allow_pickle=True)


def load_values_data(path):
    values = []
    with open(path, 'r') as file:
        for line in file:
            value = line.rsplit(', ', 1)[1]
            values.append(float(value.strip()))
    return np.array(values)



def train_model(events, values, model_path):
    print(len(events), len(values))

    def set_seed(seed=42):
        random.seed(seed)
        np.random.seed(seed)
        tf.random.set_seed(seed)
    set_seed(42)

    model = keras.Sequential()
    events = np.expand_dims(events, axis=1)
    model.add(tf.keras.layers.Input(shape=(events.shape[1], events.shape[2])))
    model.add(tf.keras.layers.LSTM(100, activation='relu', kernel_regularizer=keras.regularizers.l2(0.0001)))
    # model.add(tf.keras.layers.Dropout(0.5)) 
    model.add(tf.keras.layers.Dense(50, activation='relu', kernel_regularizer=keras.regularizers.l2(0.0001)))
    # model.add(tf.keras.layers.Dropout(0.5)) 
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001), loss='mean_squared_error')
    # model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001), loss=tf.keras.losses.Huber(delta=0.2))

    model.summary()

    start_time = time.time()
    model.fit(
        events, 
        values, 
        epochs=200, 
        batch_size=512, 
        verbose=True, 
        validation_split=0.1, 
        callbacks=[keras.callbacks.EarlyStopping(monitor='val_loss', patience=20, min_delta=0.001, restore_best_weights=True)]
    )
    end_time = time.time()
    training_time = end_time - start_time
    print(f"LSTM model training time: {training_time:.2f} 秒")
    
    model.save(model_path)
    print(f"Model saved to {model_path}")


if __name__ == '__main__':
    embedding_model = 'fasttext'
    train_data_npy = f'/behavior_baseline/baseline/cadets/data/{embedding_model}/train_data.npy'
    lstm_model_path = f'/behavior_baseline/baseline/cadets/model/{embedding_model}_lstm_model.keras'
    values_path =  f'/behavior_baseline/baseline/cadets/data/train_data.csv'
    
    events = load_input_data(train_data_npy)
    print(f"Loaded {len(events)} events, {events.shape}")

    values = load_values_data(values_path)
    print(f"Loaded {len(values)} values")

    train_model(events, values, lstm_model_path)
