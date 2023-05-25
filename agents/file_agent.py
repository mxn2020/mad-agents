import json
from agents.agent import Agent
import threading
import time


class FileAgent(Agent):
    def __init__(self, name="File Agent", global_data_agent=None):
        super().__init__(name, global_data_agent)
        self.in_data = None
        self.out_data = None
        self.data_lock = threading.Lock()
        self.file_path = None

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

    def open_file(self, file_path):
        if file_path:
            print("Opening file...", file_path)
            try:
                with open(file_path, 'r') as file:
                    try:
                        self.in_data = json.load(file)
                        self.update_status("File opened successfully.")
                    except json.JSONDecodeError as e:
                        self.update_status("Failed to open file. JSON decoding error.")
                        self.logger.error(f"JSON decoding error: {str(e)}")
                    except Exception as e:
                        self.update_status("Failed to open file.")
                        self.logger.error(f"Error opening file: {str(e)}")
            except IOError as e:
                self.update_status("Failed to open file. IOError occurred.")
                self.logger.error(f"IOError occurred while opening file: {str(e)}")
        else:
            self.update_status("No file path provided.")


    def additional_tool(self):
        # Implement additional useful tools for data manipulation here
        pass

    def run(self):
        self.update_status(("Opening file...", self.file_path))
        self.open_file(self.file_path)
        self.stop()
