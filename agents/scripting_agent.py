import threading
import time
from agents import Agent
import os

class ScriptingAgent(Agent):
    def __init__(self, agents, name="Prompt Manager Agent", global_data_agent=None):
        super().__init__(name, global_data_agent)
        self.agents = agents
        self.is_running = False


    def run(self):
        self.is_running = True
        while self.is_running:
            self.clear_screen()
            self.display_status(self.agents)
            time.sleep(1)  # Update the status every 1 second

    def stop(self):
        self.is_running = False

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen

    def display_status(self, agents, indentation=0):
        keyword_colors = {
            'error': '\033[91m',     # Red color for 'error' keyword
            'warning': '\033[93m',   # Yellow color for 'warning' keyword
            'success': '\033[92m',    # Green color for 'success' keyword
            'retrying': '\033[93m',   # Yellow color for 'retrying' keyword
            'complete': '\033[92m',   # Green color for 'complete' keyword
            'inactive': '\033[90m',   # Gray color for 'inactive' keyword
        }
        
        print("Agent Name\t\tStatus\t\tStatus Code\t\tCompletion")
        print("-----------------------------------------------------------")
        
        for agent in agents:
            status_color = self.get_status_color(agent)
            completion_color = self.get_completion_color(agent)
            
            # Check if any keyword is present in the status
            keyword_color = ''
            for keyword, color in keyword_colors.items():
                # print ('')
                # print ('agent.status_code ######## ----> ', agent.status_code)
                if keyword.lower() in agent.status_code.lower():
                    keyword_color = color
                    break
            
            print(f"{' ' * indentation}{agent.name}\t\t{status_color}{agent.status}{keyword_color}\033[0m\t\t{agent.status_code}\t\t{completion_color}{agent.completion}%\033[0m")
            
            if hasattr(agent, 'agents'):
                self.display_status(agent.agents, indentation + 4)
        
        print()

    def get_status_color(self, agent):
        if agent.status_code == "inactive":
            return "\033[90m"  # Gray color for inactive agents
        elif agent.counter <= 15:
            return "\033[94m"  # Blue color for recent updates
        elif agent.status_code == "complete":
            return "\033[92m"  # Green color for completed agents
        elif agent.status_code == "error":
            return "\033[91m"  # Red color for agents with errors
        elif agent.status_code == "retrying":
            return "\033[93m"  # Orange color for agents retrying
        else:
            return ""

    def get_completion_color(self, agent):
        if agent.completion < 100:
            return "\033[33m"  # Yellow color for incomplete agents
        else:
            return "\033[32m"  # Green color for agents with completion 100%

    def add_agent(self, agent):
        self.agents.append(agent)
