from typing import List, Optional, Tuple
from uuid import UUID
from datetime import datetime
from provenance_graph.basic_node import NetworkNode

class AnomalyScoreTagCache:
    attenuation_threshold_regular_score = 0.2 # approximately more than three benign events, it will be attenuated
    attenuation_threshold_path_distance = 1
    decay_time_threshold = 1 * 60 * 60 * 1000000000  # 1 hour
    alpha = 3
    alert_threshold = 0.99
    # alert_path_length_threshold = 16

    # current_tag_count = 0
    total_tag_count = 0
    initial_tag_count = 0
    propagation_count = 0
    attenuated_tag_count = 0
    decayed_tag_count = 0
    total_alert_count = 0

    def __init__(self, event_or_path, regular_score: float, visited_node: set = None, last_source_node=None, attenuation_distance=0):
        self.regular_score = regular_score
        self.attenuation_distance = attenuation_distance
        self.alert_mark = False
        self.last_source_node = last_source_node
        if isinstance(event_or_path, list):
            self.anomaly_path = event_or_path
            self.visited_node = set(visited_node)
        else:
            self.anomaly_path = [(event_or_path, regular_score)]
            self.visited_node = set()
            self.visited_node.add(event_or_path.source_node.node_uuid)
            self.tag_initialized_time = event_or_path.timestamp
            self.last_source_node = event_or_path.sink_node

        AnomalyScoreTagCache.initial_tag_count += 1
        AnomalyScoreTagCache.total_tag_count += 1

    def propagate(self, event, edge_regular_score: float) -> 'AnomalyScoreTagCache':

        if self.last_source_node is not None: # avoid last source node is None
            node1 = self.anomaly_path[-1][0].sink_node
            node2 = event.source_node
            if node1.get_node_type() != 'Process' and node1.get_node_name() != node2.get_node_name():
                return None

        new_anomaly_path = []
        for path_event, path_edge_regular_score in self.anomaly_path:
            new_anomaly_path.append((path_event, path_edge_regular_score))
        new_tag = AnomalyScoreTagCache(new_anomaly_path, self.regular_score, self.visited_node, event.sink_node, self.attenuation_distance)
        new_tag.set_regular_score(self.regular_score * edge_regular_score * AnomalyScoreTagCache.alpha)
        new_tag.tag_initialized_time = event.get_timestamp()
        new_tag.visited_node.add(event.source_node.node_uuid)
        new_tag.visited_node.add(event.sink_node.node_uuid)

        if edge_regular_score > 0.1:
            new_tag.attenuation_distance = self.attenuation_distance + 1
        else:
            new_tag.attenuation_distance = 0
        new_tag.anomaly_path.append((event, edge_regular_score))
        AnomalyScoreTagCache.propagation_count += 1
        AnomalyScoreTagCache.total_tag_count += 1
        return new_tag

    def should_replace_tag(self, new_tag: 'AnomalyScoreTagCache') -> bool:

        if new_tag.get_anomaly_score() > self.get_anomaly_score():
            return True
        elif new_tag.get_anomaly_score() == self.get_anomaly_score():
            # avoid "file write" event to continue propagate and replace the tag.
            if self.alert_mark:
                return False
            return True
        return False

    def should_decayed(self, event) -> bool:
        return (event.get_timestamp() - self.tag_initialized_time) >= AnomalyScoreTagCache.decay_time_threshold

    # while regular events occur more than twice, the tag will attenuate
    def should_attenuated(self) -> bool:
        return self.regular_score >= AnomalyScoreTagCache.attenuation_threshold_regular_score
    
    def should_attenuated_path_distance(self) -> bool:
        return self.attenuation_distance >= AnomalyScoreTagCache.attenuation_threshold_path_distance

    def should_trigger_alert(self) -> bool:
        return self.get_anomaly_score() >= AnomalyScoreTagCache.alert_threshold

    def trigger_alert(self) -> 'AnomalyScoreTagCache':
        AnomalyScoreTagCache.total_alert_count += 1
        self.alert_mark = True
        return self

    def get_anomaly_score(self) -> float:
        self.anomaly_score = 1 - self.regular_score
        return self.anomaly_score

    def set_regular_score(self, regular_score: float):
        self.regular_score = regular_score

    def get_regular_score(self) -> float:
        return self.regular_score

    def get_tag_initialized_time(self) -> int:
        return self.tag_initialized_time
    
    def get_alert_mark(self) -> bool:
        return self.alert_mark
    
    def exist_multiple_repeated_entity(self) -> bool:
        entity_dict = {}
        for event, _ in self.anomaly_path:
            node_name = event.source_node.get_node_name()
            if node_name not in entity_dict:
                entity_dict[node_name] = 0
            entity_dict[node_name] += 1
            if entity_dict[node_name] >= 3:
                return True
        node_name = self.anomaly_path[-1][0].sink_node.get_node_name()
        if node_name in entity_dict:
            entity_dict[node_name] += 1
            if entity_dict[node_name] >= 3:
                return True
            
        return False
    
    def avoid_loop(self, event) -> bool:
        if event.sink_node.node_uuid in self.visited_node or  event.sink_node.node_uuid == event.source_node.node_uuid:
            if self.get_tag_cache(event.sink_node) is None and isinstance(event.source, NetworkNode):
                return False
            return True
        return False

    @staticmethod
    def statistics_alert_info():
        print('Total tag count:', AnomalyScoreTagCache.total_tag_count)
        print('Initial tag count:', AnomalyScoreTagCache.initial_tag_count)
        print('Propagation count:', AnomalyScoreTagCache.propagation_count)
        print('Attenuation tag count:', AnomalyScoreTagCache.attenuated_tag_count)
        print('Decayed tag count:', AnomalyScoreTagCache.decayed_tag_count)
        print('Total alert count:', AnomalyScoreTagCache.total_alert_count)
        print()