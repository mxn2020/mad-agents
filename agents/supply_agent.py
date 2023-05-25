import json
from agents.agent import Agent
import threading
import time


class SupplyAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.in_data = None
        self.out_data = None
        self.data_lock = threading.Lock()

    def receive_data(self, data):
        self.in_data = data

    def receive_data_array(self, data_array):
        self.in_data = data_array

    def extract_objects_by_field(self, field_name, field_value):
        extracted_objects = []
        if isinstance(self.in_data, list):
            for item in self.in_data:
                if field_name in item and item[field_name] == field_value:
                    extracted_objects.append(item)
        elif isinstance(self.in_data, dict):
            if field_name in self.in_data and self.in_data[field_name] == field_value:
                extracted_objects.append(self.in_data)
        return extracted_objects

    def merge_data_array(self):
        if isinstance(self.out_data, list):
            merged_data = {}
            for item in self.out_data:
                if isinstance(item, dict):
                    merged_data.update(item)
            return merged_data
        else:
            return {}

    def append_data(self, new_data):
        with self.data_lock:
            self.out_data.append(new_data)
            
    def additional_tool(self):
        # Implement additional useful tools for data manipulation here
        pass

    def run(self):
        self.update_status("Queueying...")
        self.update_status("Running")
        time.sleep(6)
        self.stop()