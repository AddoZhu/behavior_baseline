raw_log_list = [
        '/Datasets/E3-TRACE/ta1-trace-e3-official-1.json',
        '/Datasets/E3-TRACE/ta1-trace-e3-official-1.json.1',
        '/Datasets/E3-TRACE/ta1-trace-e3-official-1.json.2',
        '/Datasets/E3-TRACE/ta1-trace-e3-official-1.json.3',
]

log_list = [
        '/Datasets/trace/e3_trace_preparation_0.json',
        '/Datasets/trace/e3_trace_preparation_1.json',
        '/Datasets/trace/e3_trace_preparation_2.json',
        '/Datasets/trace/e3_trace_preparation_3.json',
]

event_csv_list = [
        '/Datasets/trace/e3_trace_preparation_event_0.csv',
        '/Datasets/trace/e3_trace_preparation_event_1.csv',
        '/Datasets/trace/e3_trace_preparation_event_2.csv',
        # '/Datasets/trace/e3_trace_preparation_event_3.csv',
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

