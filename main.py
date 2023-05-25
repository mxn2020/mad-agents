import sys
from agents.backoffice_agent import BackofficeAgent
from agents.global_data_agent import GlobalDataAgent
import threading


class GlobalData:
    def __init__(self):
        self.folder_path = ""
        self.data = {}  # Dictionary to store additional variables
    
    def set_folder_path(self, folder_path):
        self.folder_path = folder_path
    
    def get_folder_path(self):
        return self.folder_path
    
    def save_data(self, key, value):
        self.data[key] = value
    
    def get_data(self, key):
        return self.data.get(key)



def main():
    # Check if the JSON file path is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Please provide the path to the JSON file.")
        print("Usage: python3 main.py <json_file_path>")
        return

    # Create an instance of the GlobalDataAgent
    global_data_agent = GlobalDataAgent("Global Data Agent")

    # Start the GlobalDataAgent thread
    global_data_agent.launch()

    json_file_path = sys.argv[1]

    # Create an instance of your agent and pass the JSON file path
    backoffice_agent_name = "Backoffice Agent"
    backoffice_agent = BackofficeAgent(backoffice_agent_name, global_data_agent)
    backoffice_agent.json_file_path = json_file_path

    # Start the agent as a thread
    backoffice_agent.launch()

    # Wait for the thread to finish
    backoffice_agent.join()
    
    print ("Backoffice Agent finished.")
    
    print ("Closing Global Data")

    # Stop the GlobalDataAgent thread
    global_data_agent.stop()
    
    print ("Joining Global Data")

    # Wait for the GlobalDataAgent thread to finish
    global_data_agent.join()
    
    print ("Global Data closed.")


if __name__ == '__main__':
    main()
