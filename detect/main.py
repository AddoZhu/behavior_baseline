import sys
import json
import time
import threading
import multiprocessing
import os
import psutil
import tempfile

from pyflink.common import WatermarkStrategy, Encoder, Types
from pyflink.datastream import StreamExecutionEnvironment, KeyedProcessFunction
from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
from pyflink.datastream.connectors.file_system import FileSource, StreamFormat, FileSink, OutputFileConfig, RollingPolicy
from pyflink.datastream.connectors.kafka import KafkaSource
from pyflink.common.serialization import SimpleStringSchema
sys.path.insert(0, '/behavior_baseline/detect/provenance_graph/')
from provenance_graph.PDM import PDM_pb2
from provenance_graph.associated_event import AssociatedEvent
from provenance_graph.event_type_config import LOG_TYPE
from provenance_graph.basic_node import FileNode, ProcessNode, NetworkNode
from anomaly_path.anomaly_path_mining_on_flink import TagBasedAnomalyPathMiningOnFlink
import uuid
from system_config import topic
import hashlib as md5

def split(line):
    log = json.loads(line)
    event = AssociatedEvent()
    host_uuid = log['host_uuid']
    event_uuid = log['event_uuid']
    event_type = log['event_type']
    event_timestamp = log['event_timestamp']
    
    subject_uuid = log['subject_uuid']
    subject_name = log['subject_name']
    object_uuid = log['object_uuid']
    object_path = log['object_path']

    event.set_host_uuid(uuid.UUID(host_uuid))
    event.set_timestamp(int(event_timestamp))
    event.set_relationship(event_type)
    event.set_event_uuid(uuid.UUID(event_uuid))
    event.set_index(int(log['index']))
    event.set_regular_score(float(log['score']))
    source_node = None  # Default value
    sink_node = None    # Default value
    # if log['index'] < 1700000:
    #     return event
    
    if event_type in LOG_TYPE.PROCESS_OP:
        source_node = ProcessNode(node_uuid=subject_uuid, process_name=subject_name)
        sink_node = ProcessNode(node_uuid=object_uuid, process_name=subject_name)

    elif event_type in LOG_TYPE.FILE_OP:
        if event_type in ('file open', 'file write', 'file modify'):
            source_node = ProcessNode(node_uuid=subject_uuid, process_name=subject_name)
            sink_node = FileNode(node_uuid=object_uuid, file_path=object_path)
        else:
            sink_node = ProcessNode(node_uuid=subject_uuid, process_name=subject_name)
            source_node = FileNode(node_uuid=object_uuid, file_path=object_path)
    elif event_type in LOG_TYPE.NET_OP:
        if '::' in object_path:
            return event
        if event_type in ('network send'):
            source_node = ProcessNode(node_uuid=subject_uuid, process_name=subject_name)
            sink_node = NetworkNode(node_uuid=object_uuid, ip_address=object_path)
        else:
            sink_node = ProcessNode(node_uuid=subject_uuid, process_name=subject_name)
            source_node = NetworkNode(node_uuid=object_uuid, ip_address=object_path)
    else:
        return event
    
    event.set_source_node(source_node)
    event.set_sink_node(sink_node)
    
    return event

def filter_event(event):
    return event.source_node is not None

def main_process():
    # Set a different temporary directory
    temp_dir = tempfile.mkdtemp(dir="/temporary_dir")
    os.environ['JAVA_TOOL_OPTIONS'] = f"-Djava.io.tmpdir={temp_dir}"

    env = StreamExecutionEnvironment.get_execution_environment()
    env.add_jars(
        "file:///behavior_baseline/detect/lib/flink-sql-connector-kafka-1.17.2.jar", 
        "file:///behavior_baseline/detect/lib/kafka-clients-3.5.1.jar",
        "file:///behavior_baseline/detect/lib/flink-connector-base-1.17.2.jar",
        "file:///behavior_baseline/detect/lib/flink-connector-kafka-1.17.2.jar"
    )
    
    env.set_parallelism(8)
    
    kafka_source = KafkaSource.builder() \
    .set_bootstrap_servers("xxxx:9092") \
    .set_group_id("mergeAlert") \
    .set_topics(topic) \
    .set_value_only_deserializer(SimpleStringSchema()) \
    .build()
    ds = env.from_source(kafka_source, WatermarkStrategy.no_watermarks(), "kafka_source")
    event_stream = ds.map(split, output_type=Types.PICKLED_BYTE_ARRAY()).filter(filter_event)
    
    event_stream.key_by(lambda event: event.get_host_uuid()) \
                .process(TagBasedAnomalyPathMiningOnFlink())

    # print(f"Main process PID: {os.getpid()}")

    env.execute('Anomaly Path Mining')

def test_memory_usage(pid, interval=5):
    print(f"Monitoring memory usage for PID: {pid}")
    memory_log = "memory.log"
    total_memory = 0
    count = 0

    try:
        with open(memory_log, 'w') as log_file:
            while True:
                process = psutil.Process(pid)
                mem_info = process.memory_info()
                mem_usage = mem_info.rss / (1024 * 1024)  
                total_memory += mem_usage
                count += 1
                average_memory = total_memory / count
                log_file.write(f"Memory usage: {mem_usage:.2f} MiB, Average memory usage: {average_memory:.2f} MiB\n")
                log_file.flush() 
                # print(f"Memory usage: {mem_usage:.2f} MiB, Average memory usage: {average_memory:.2f} MiB")
                time.sleep(interval)
    except psutil.NoSuchProcess:
        print(f"Process with PID {pid} no longer exists.")
    except KeyboardInterrupt:
        print("Memory monitoring stopped.")

if __name__ == '__main__':

    main_process()