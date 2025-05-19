import json
from typing import Dict

class PreparationLog:
    def __init__(self, host_uuid: str, event_uuid: str, event_type: str, event_timestamp: str, subject_uuid: str, subject_name: str, object_uuid: str, object_path: str, ground_truth: bool = False):
        self.host_uuid = host_uuid
        self.event_uuid = event_uuid
        self.event_type = event_type
        self.event_timestamp = event_timestamp
        self.subject_uuid = subject_uuid
        self.subject_name = subject_name
        self.object_uuid = object_uuid
        self.object_path = object_path
        self.ground_truth = ground_truth

    def to_dict(self) -> Dict[str, str]:
        return {
            'host_uuid': self.host_uuid,
            'event_uuid': self.event_uuid,
            'event_type': self.event_type,
            'event_timestamp': self.event_timestamp,
            'subject_uuid': self.subject_uuid,
            'subject_name': self.subject_name,
            'object_uuid': self.object_uuid,
            'object_path': self.object_path,
            'ground_truth': self.ground_truth
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())