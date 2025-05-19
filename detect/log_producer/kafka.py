### FastText+MLP example
import sys
from confluent_kafka import Producer
import json
sys.path.append('/behavior_baseline/detect/log_producer/')
from config import event_dict

json_count = 0
json_sent_count = 0
values = []

def load_raw_data(raw_file_path):
    global values
    with open(raw_file_path, 'r') as f:
        for line in f:
            value = line.rsplit(', ', 1)[-1]
            values.append(value.strip())
    return values

def load_data(path):
    file_list = []
    with open(path, 'r') as file:
        for line in file:
            file_list.append(line.strip())
    return file_list

def send_log(json_file_path, producer, topic):
    global json_count  
    global json_sent_count

    with open(json_file_path, 'r') as json_file:
        for i, jsonline in enumerate(json_file):
            json_count += 1
            log = json.loads(jsonline)
            log['score'] = values[i]
            log['index'] = i
            log['event_type'] = event_dict[log['event_type']]

            # if i <= 1689887:
            #     continue
            producer.produce(topic + "-test", value=json.dumps(log))
            json_sent_count += 1
            
            if json_sent_count % 1000 == 0:
                producer.flush()

            if json_count % 300000 == 0:
                print(f"jsonCount: {json_count} \n jsonSentCount: {json_sent_count}")
                print("continue...\n")

if __name__ == "__main__":
    properties = {
        'bootstrap.servers': 'xxxx:9092'
    }

    producer = Producer(properties)

    print("start sending ...\n")

    count = 2
    predict_data_path = '/behavior_baseline/baseline/cadets/result_file/fasttext_mlp_result_8.csv'
    json_file_path = '/Datasets/cadets/e3_cadets_preparation_8.json'
    print(f"predict_data_path: {predict_data_path} \n json_file_path: {json_file_path}")
    load_raw_data(predict_data_path)
    send_log(json_file_path, producer, f"e3-cadets-{count}")
    print(f"jsonCount: {json_count} \n jsonSentCount: {json_sent_count}")
    print("continue...\n")
    producer.flush()
    json_count = 0
    json_sent_count = 0
    values = []

    print("sending end...")