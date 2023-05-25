import logging
import threading
from agents import Agent, DataAgent, PromptManagerAgent, FileAgent, ScriptingAgent, SupplyAgent
import time

class BackofficeAgent(Agent):
    def __init__(self, name="Back Office Agent", global_data_agent=None):
        super().__init__(name, global_data_agent)
        self.type = "Backoffice Agent"
        self.dependencies = [DataAgent, PromptManagerAgent, FileAgent, ScriptingAgent, SupplyAgent]
        self.dependent_agents = []
        self.stop_event = threading.Event()
        self.check_interval = 2  # Check interval in seconds
        self.json_file_path = None

    def stop_dependent_agents(self):
        time.sleep(4)  # Wait for 4 seconds
        for agent in self.dependent_agents:
            agent.stop()

    def check_agents(self):
        # Get the list of running threads
        running_threads = threading.enumerate()
      
        while not self.stop_event.is_set():
            # Print the names of the running threads
            for thread in running_threads:
                # print('')
                # print(' ### RUNNING ### ')
                # print(thread.name)
                name = thread.name
            
            if len(self.dependent_agents) == 1 and isinstance(self.dependent_agents[0], ScriptingAgent):
                print("Stopping Scripting Agent...")
                self.dependent_agents[0].stop()
                self.dependent_agents[0].join()
                break
            time.sleep(self.check_interval)

    def run(self):
        self.logger.info("Backoffice Agent is running.")

        # Create the ScriptingAgent and pass the list of agents to it
        self.scripting_agent = ScriptingAgent(self.dependent_agents + [self], "Scripting Agent")

        # Start the ScriptingAgent
        self.scripting_agent.launch()

        # Perform backoffice tasks
        self.update_status("Performing backoffice tasks...")


        # Open the JSON file with the FileAgent
        file_agent = FileAgent("File Agent")
        self.scripting_agent.add_agent(file_agent)  # Store the dependent agent
        file_agent.file_path = self.json_file_path
        file_agent.launch()
        self.update_status("Waiting for file to load...")
        file_agent.join()  # Wait for the FileAgent's thread to complete
        
        # Retrieve the dataset from the FileAgent
        dataset = file_agent.in_data

        # Prepare the dataset file with the DataAgent
        data_agent = DataAgent("Data Agent JSON Loader")
        self.scripting_agent.add_agent(data_agent)  # Store the dependent agent
        data_agent.receive_data(dataset)
        data_agent.launch()
        self.update_status("Waiting for data to be extracted...")
        data_agent.join()  # Wait for the DataAgent's thread to complete

        # Retrieve the dataset from the DataAgent
        resultdataset = data_agent.out_data

        # Process the dataset file with the PromptManagerAgent
        prompt_manager_agent = PromptManagerAgent("Prompt Manager Agent")
        self.scripting_agent.add_agent(prompt_manager_agent)  # Store the dependent agent
        prompt_manager_agent.receive_data(resultdataset)
        prompt_manager_agent.launch()
        self.update_status("Waiting for data to be processed...")
        # print('prompt_manager_agent', prompt_manager_agent)
        prompt_manager_agent.join()  # Wait for the DataAgent's thread to complete


        # Wait for all dependent agents to complete
        for agent in self.dependent_agents:
            if agent.type != "ScriptingAgent":  # Check if the agent is not the scripting agent
                print(f"ALL Agent {agent.name} has finished...")
                print('ALL agent name', agent)
                agent.join()  # Wait for the dependent agent's thread to complete

        # All tasks completed
        self.complete()
        self.update_status("Backoffice tasks completed.")
        self.logger.info("Backoffice Agent has completed its tasks.")

        time.sleep(2)  # Wait for 2 seconds
        self.scripting_agent.stop()

        print("Stopping Backoffice Agent...")
        
        self.stop()

    def configure(self, **kwargs):
        # Implement backoffice agent configuration logic here
        pass

    def synchronize(self):
        # Implement backoffice agent synchronization logic here
        pass
