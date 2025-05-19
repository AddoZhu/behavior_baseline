raw_log_list = [
        '/Datasets/E3-THEIA/ta1-theia-e3-official-1r.json',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-1r.json.1',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-1r.json.2',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-1r.json.3',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-1r.json.4',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-1r.json.5',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-1r.json.6',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-1r.json.7',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-1r.json.8',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-1r.json.9',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-3.json',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-5m.json',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-6r.json',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-6r.json.1',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-6r.json.2',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-6r.json.3',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-6r.json.4',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-6r.json.5',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-6r.json.6',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-6r.json.7',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-6r.json.8',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-6r.json.9',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-6r.json.10',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-6r.json.11',
        '/Datasets/E3-THEIA/ta1-theia-e3-official-6r.json.12',
]

log_list = [
        '/Datasets/theia/e3_theia_preparation_0.json',
        '/Datasets/theia/e3_theia_preparation_1.json',
        '/Datasets/theia/e3_theia_preparation_2.json',
        '/Datasets/theia/e3_theia_preparation_3.json',
        '/Datasets/theia/e3_theia_preparation_4.json',
        '/Datasets/theia/e3_theia_preparation_5.json',
        '/Datasets/theia/e3_theia_preparation_6.json',
        '/Datasets/theia/e3_theia_preparation_7.json',
        '/Datasets/theia/e3_theia_preparation_8.json',
        '/Datasets/theia/e3_theia_preparation_9.json',
        '/Datasets/theia/e3_theia_preparation_10.json',
        '/Datasets/theia/e3_theia_preparation_11.json',
        '/Datasets/theia/e3_theia_preparation_12.json',
        '/Datasets/theia/e3_theia_preparation_13.json',
        '/Datasets/theia/e3_theia_preparation_14.json',
        '/Datasets/theia/e3_theia_preparation_15.json',
        '/Datasets/theia/e3_theia_preparation_16.json',
        '/Datasets/theia/e3_theia_preparation_17.json',
        '/Datasets/theia/e3_theia_preparation_18.json',
        '/Datasets/theia/e3_theia_preparation_19.json',
        '/Datasets/theia/e3_theia_preparation_20.json',
        '/Datasets/theia/e3_theia_preparation_21.json',
        '/Datasets/theia/e3_theia_preparation_22.json',
        '/Datasets/theia/e3_theia_preparation_23.json',
        '/Datasets/theia/e3_theia_preparation_24.json',
]

event_csv_list = [
        '/Datasets/theia/e3_theia_preparation_event_0.csv',
        '/Datasets/theia/e3_theia_preparation_event_1.csv',
        '/Datasets/theia/e3_theia_preparation_event_2.csv',
        '/Datasets/theia/e3_theia_preparation_event_3.csv',
        '/Datasets/theia/e3_theia_preparation_event_4.csv',
        '/Datasets/theia/e3_theia_preparation_event_5.csv',
        '/Datasets/theia/e3_theia_preparation_event_6.csv',
        '/Datasets/theia/e3_theia_preparation_event_7.csv',
        '/Datasets/theia/e3_theia_preparation_event_8.csv',
        '/Datasets/theia/e3_theia_preparation_event_9.csv',
        '/Datasets/theia/e3_theia_preparation_event_10.csv',
        '/Datasets/theia/e3_theia_preparation_event_11.csv',
        # '/Datasets/theia/e3_theia_preparation_event_12.csv',
        # '/Datasets/theia/e3_theia_preparation_event_13.csv',
        # '/Datasets/theia/e3_theia_preparation_event_14.csv',
        # '/Datasets/theia/e3_theia_preparation_event_15.csv',
        # '/Datasets/theia/e3_theia_preparation_event_16.csv',
        # '/Datasets/theia/e3_theia_preparation_event_17.csv',
        # '/Datasets/theia/e3_theia_preparation_event_18.csv',
        # '/Datasets/theia/e3_theia_preparation_event_19.csv',
        # '/Datasets/theia/e3_theia_preparation_event_20.csv',
        # '/Datasets/theia/e3_theia_preparation_event_21.csv',
        # '/Datasets/theia/e3_theia_preparation_event_22.csv',
        # '/Datasets/theia/e3_theia_preparation_event_23.csv',
        # '/Datasets/theia/e3_theia_preparation_event_24.csv',

]

event_dict = {
        'EVENT_OPEN': 'file write',
        'EVENT_READ': 'file read',
        'EVENT_WRITE': 'file write',
        'EVENT_MODIFY_FILE_ATTRIBUTES': 'file modify',
        'EVENT_EXECUTE': 'process load',
        'EVENT_FORK': 'process fork',
        'EVENT_CONNECT': 'network send',
        'EVENT_MODIFY_PROCESS': 'process modify',
        'EVENT_RECVFROM': 'network receive',
        'EVENT_SENDTO': 'network send'
}

class LOG_TYPE:
        FILE_OP = ['EVENT_OPEN', 'EVENT_READ', 'EVENT_WRITE', 'EVENT_MODIFY_FILE_ATTRIBUTES', 'EVENT_EXECUTE']
        PROCESS_OP = ['EVENT_FORK', 'EVENT_MODIFY_PROCESS']
        NET_OP = ['EVENT_CONNECT', 'EVENT_SENDTO', 'EVENT_RECVFROM']

class EVENT_TYPE:
        EVENT_OP = ['EVENT_OPEN', 'EVENT_READ', 'EVENT_WRITE', 'EVENT_MODIFY_FILE_ATTRIBUTES', 'EVENT_FORK', 'EVENT_EXECUTE', 'EVENT_CONNECT', 'EVENT_SENDTO', 'EVENT_MODIFY_PROCESS', 'EVENT_RECVFROM']

