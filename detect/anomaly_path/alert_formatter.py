from typing import List, Tuple

class AlertFormatter:
    def __init__(self, current_time: int, anomaly_score: float, alert_path, attack_nodes):
        self.current_time = current_time
        self.anomaly_score = anomaly_score
        self.alert_path = alert_path
        self.attack_nodes = attack_nodes

    def to_json_string(self) -> str:
        full_alert_json = []
        full_alert_json.append("###############Alert###############\ncurrentTime:" + str(self.current_time) + "\n")
        full_alert_json.append("AnomalyScore: " + str(self.anomaly_score) + "\n")
        full_alert_json.append("AlertPath:\n")
        TP_nodes_detected = set()
        FP_nodes_detected = set()
        for path in self.alert_path:
            source_name = path[0].get_soure_node_name()
            sink_name = path[0].get_sink_node_name()

            if source_name in self.attack_nodes:
                TP_nodes_detected.add(source_name)
            else:
                FP_nodes_detected.add(source_name)

            if sink_name in self.attack_nodes:
                TP_nodes_detected.add(sink_name)
            else:
                FP_nodes_detected.add(sink_name)

            full_alert_json.append(f"{path[0]}: {path[1]}\n")
        
        if len(TP_nodes_detected):
            full_alert_json.append("true positive:\n")
            full_alert_json.append("attack nodes detected: ")
            for node in TP_nodes_detected:
                full_alert_json.append(node + ' ')
            full_alert_json.append('\n')
        else:
            full_alert_json.append("false positive:\n")

        return ''.join(full_alert_json), TP_nodes_detected, FP_nodes_detected