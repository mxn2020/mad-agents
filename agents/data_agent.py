import json
from agents.agent import Agent
import threading
import time


class DataAgent(Agent):
    def __init__(self, name="Data Agent", global_data_agent=None):
        super().__init__(name, global_data_agent)
        self.in_data = None
        self.out_data = None
        self.data_lock = threading.Lock()

    def receive_data(self, data):
        self.in_data = data

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
    
    def getDataResult(self):
        # Check if 'results' key is present and not None
        results = None
        if 'results' in self.in_data and self.in_data['results'] is not None:
            results = self.in_data['results']
        else:
            print("'results' key is missing or set to None.")
        self.out_data = results

    def run(self):
        self.update_status("Running")
        self.getDataResult()
        time.sleep(2)
        self.stop()