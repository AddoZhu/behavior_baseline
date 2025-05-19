from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class BasicNode:
    def get_properties(self) -> Dict:
        return {}
    
    def copy_node_generalize(self):
        return BasicNode()

@dataclass
class FileNode(BasicNode):
    node_uuid: Optional[str] = None
    file_path: str = ""

    def get_properties(self) -> Dict:
        props = super().get_properties()
        props.update({"uuid": self.node_uuid})
        props.update({"file_path": self.file_path})
        return props
    
    def copy_node_generalize(self):
        return self.__class__(self.node_uuid, self.file_path)
    
    def __str__(self):
        return f"File {self.node_uuid} {self.file_path}"
    
    def get_node_name(self):
        return self.file_path
    
    def get_node_type(self):
        return "File"

@dataclass
class ProcessNode(BasicNode):
    node_uuid: Optional[str] = None
    process_name: str = ""

    def get_properties(self) -> Dict:
        props = super().get_properties()
        props.update({"uuid": self.node_uuid})
        props.update({"process_name": self.process_name})
        return props
    
    def copy_node_generalize(self):
        return self.__class__(self.node_uuid, self.process_name)
    
    def __str__(self):
        return f"Process {self.node_uuid} {self.process_name}"
    
    def get_node_name(self):
        return self.process_name
    
    def get_node_type(self):
        return "Process"

@dataclass
class NetworkNode(BasicNode):
    node_uuid: Optional[str] = None
    ip_address: str = ""

    def get_properties(self) -> Dict:
        props = super().get_properties()
        props.update({"uuid": self.node_uuid})
        props.update({"ip_address": self.ip_address})
        return props
    
    def copy_node_generalize(self):
        return self.__class__(self.node_uuid, self.ip_address)
    
    def __str__(self):
        return f"Network Connect {self.node_uuid} {self.ip_address}"
    
    def get_node_name(self):
        return self.ip_address.split(" : ")[0]
    
    def get_node_type(self):
        return "Network"