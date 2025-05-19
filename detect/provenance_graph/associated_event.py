import json
import uuid
from dataclasses import dataclass, field
from typing import Optional
from provenance_graph import basic_node

class AssociatedEvent:
    def __init__(self, source_node=None, sink_node=None, relationship=None, time_stamp=None, regular_score=None, prediction_score=None, index=None):
        self.source_node_tag = None
        self.sink_node_tag = None
        self.source_node = source_node
        self.sink_node = sink_node
        self.relationship = relationship
        self.event_uuid = None
        self.timestamp = time_stamp
        self.host_uuid = None
        self.generalized_event = None
        self.regular_score = regular_score
        self.prediction_score = None
        self.index = None

    def copy_generalize(self):
        if self.generalized_event is not None:
            return self.generalized_event
        generalized_event = AssociatedEvent(
            self.source_node.copy_node_generalize(),
            self.sink_node.copy_node_generalize(),
            self.relationship,
            self.timestamp,
            self.regular_score,
            self.prediction_score
        )
        self.generalized_event = generalized_event
        return generalized_event

    def get_relationship(self):
        return self.relationship

    def get_event_uuid(self):
        return self.event_uuid

    def get_host_uuid(self):
        return self.host_uuid
    
    def get_timestamp(self):
        return self.timestamp
    
    def get_regular_score(self):
        return self.regular_score
    
    def get_source_uuid(self):
        return self.source_node.node_uuid

    def get_sink_uuid(self):
        return self.sink_node.node_uuid

    def get_index(self):
        return self.index
    
    def set_relationship(self, relationship):
        self.relationship = relationship

    def set_source_node(self, source_node):
        self.source_node = source_node

    def set_sink_node(self, sink_node):
        self.sink_node = sink_node

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def set_host_uuid(self, host_uuid):
        self.host_uuid = host_uuid

    def set_event_uuid(self, event_uuid):
        self.event_uuid = event_uuid
    
    def set_index(self, index):
        self.index = index

    def get_soure_node_name(self):
        return self.source_node.get_node_name()
    
    def get_sink_node_name(self):
        return self.sink_node.get_node_name()

    def set_regular_score(self, regular_score:'float'):
        if regular_score <= 0.1:
            self.regular_score = 0.1
        else:
            self.regular_score = max(0.5, regular_score)

        # self.regular_score = regular_score

    def __str__(self):
        return f"Event: [{self.source_node}] -> {self.relationship} -> [{self.sink_node}], ts:{self.timestamp}"
    
    def preprocess_event(self):
        return f"{self.source_node.get_node_name()}, {self.relationship}, {self.sink_node.get_node_name()}"