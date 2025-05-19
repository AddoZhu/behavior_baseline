import json
import os
import sys
sys.path.insert(0, '/Baseline_Frequency/baseline')
from preparation_log import PreparationLog
from config import raw_log_list, LOG_TYPE, EVENT_TYPE, event_dict
network_cache = {}
parent_uuid_cache = {}
parent_name_cache = {}
socket_count = 0

def load_data(path):
    ground_truth = []
    with open(path, 'r') as file:
        for line in file:
            ground_truth.append(line.strip())
    return ground_truth

def convert_json_to_standard_format(log):
    global socket_count
    host_uuid = log['datum']['com.bbn.tc.schema.avro.cdm18.Event']['hostId']
    
    event_uuid = log['datum']['com.bbn.tc.schema.avro.cdm18.Event']['uuid']
    event_type = log['datum']['com.bbn.tc.schema.avro.cdm18.Event']['type']
    event_timestamp = log['datum']['com.bbn.tc.schema.avro.cdm18.Event']['timestampNanos']
    
    subject_uuid = log['datum']['com.bbn.tc.schema.avro.cdm18.Event']['subject']['com.bbn.tc.schema.avro.cdm18.UUID']
    subject_name = log['datum']['com.bbn.tc.schema.avro.cdm18.Event']['properties']['map']['exec']
    try:
        object_uuid = log['datum']['com.bbn.tc.schema.avro.cdm18.Event']['predicateObject']['com.bbn.tc.schema.avro.cdm18.UUID']
    except TypeError:
        return None, None

    objectPath = ''

    standard_format = ''
    if event_type in LOG_TYPE.FILE_OP:
        try:
            objectPath = log['datum']['com.bbn.tc.schema.avro.cdm18.Event']['predicateObjectPath']['string']
        except TypeError:
            return None, None
        
        if event_type in ('EVENT_OPEN', 'EVENT_WRITE', 'EVENT_MODIFY_FILE_ATTRIBUTES'):
            standard_format = 'Process ' + subject_name + ', ' + event_dict.get(event_type) + ', ' + 'File ' + objectPath
        else:
            standard_format = 'File ' + objectPath + ', ' + event_dict.get(event_type) + ', ' + 'Process ' + subject_name
        
    elif event_type in LOG_TYPE.NET_OP:
        objectPath = network_cache.get(object_uuid)
        if objectPath is None: 
            socket_count = socket_count + 1
            return None, None

        if event_type in ('EVENT_CONNECT', 'EVENT_SENDTO'):
            standard_format = 'Process ' + subject_name + ', ' + event_dict.get(event_type) + ', ' + 'Network Connect ' + objectPath
        else:
            standard_format = 'Network Connect ' + objectPath + ', ' + event_dict.get(event_type) + ', ' + 'Process ' + subject_name
    elif event_type in LOG_TYPE.PROCESS_OP:
        if event_type == 'EVENT_MODIFY_PROCESS':
            object_uuid = parent_uuid_cache.get(subject_uuid)
            objectPath = parent_name_cache.get(subject_uuid)
        else:
            parent_uuid_cache[object_uuid] = subject_uuid
            parent_name_cache[object_uuid] = subject_name
            objectPath = subject_name
        try:
            standard_format = 'Process ' + subject_name + ', ' + event_dict.get(event_type) + ', ' + 'Process ' + objectPath
        except TypeError:
            return None, None
    else:
        print(log)
        sys.exit(1)
    
    preparation_log = PreparationLog(host_uuid, event_uuid, event_type, event_timestamp, subject_uuid, subject_name, object_uuid, objectPath, False)
    
    return standard_format, preparation_log.to_json()

if __name__ == '__main__':

    for index, file_path in enumerate(raw_log_list):
        print('Now processing file is ', file_path)
        if os.path.isfile(file_path): 
            preparation_events = []
            preparation_logs = []
            with open(file_path, 'r') as f:
                for line in f:
                    data = json.loads(line)
                    if 'com.bbn.tc.schema.avro.cdm18.Event' in data['datum']:
                            event_type = data['datum']['com.bbn.tc.schema.avro.cdm18.Event']['type']
                            if event_type in EVENT_TYPE.EVENT_OP:
                                standard_data, preparation_log = convert_json_to_standard_format(data)
                                if standard_data is None: continue
                                preparation_events.append(standard_data)
                                preparation_logs.append(preparation_log)
                    elif 'com.bbn.tc.schema.avro.cdm18.NetFlowObject' in data['datum'] :
                        key = data['datum']['com.bbn.tc.schema.avro.cdm18.NetFlowObject']['uuid']
                        ip = data['datum']['com.bbn.tc.schema.avro.cdm18.NetFlowObject']['remoteAddress']
                        port = data['datum']['com.bbn.tc.schema.avro.cdm18.NetFlowObject']['remotePort']
                        network_cache[key] = ip + ' : ' + str(port)
        
            preparation_event_path = f'/Datasets/cadets/e3_cadets_preparation_event_{index}.csv'
            preparation_log_path = f'/Datasets/cadets/e3_cadets_preparation_{index}.json'
            with open(preparation_event_path, 'w') as f:
                for event in preparation_events:
                    f.write(event + '\n')

            with open(preparation_log_path, 'w') as f:
                for log in preparation_logs:
                    f.write(log + '\n')



