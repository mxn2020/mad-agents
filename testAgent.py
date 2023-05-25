import logging
import threading
import time
from agents import Agent

class MainAgent(Agent):
    def __init__(self):
        super().__init__("Main Agent")
        self.child_agents = []
        self.scripting_agent = None

    def run(self):
        self.launch
        self.launch_agents()
        
    def launch_agents(self):
        # Create child agents and scripting agent
        child_agent1 = ChildAgent("Child Agent 1", "Task 1")
        child_agent2 = ChildAgent("Child Agent 2", "Task 2")
        child_agent3 = ChildAgent("Child Agent 3", "Task 3")
        scripting_agent = ScriptingAgent("Scripting Agent")

        # Add child agents and scripting agent to the main agent's agent list
        self.child_agents.extend([child_agent1, child_agent2, child_agent3])
        self.scripting_agent = scripting_agent

        # Start child agents and scripting agent
        for agent in self.child_agents + [self.scripting_agent]:
            agent.launch()

        # Join child agent threads
        for agent in self.child_agents:
            agent.join()

        # Stop the scripting agent
        self.scripting_agent.stop()

        # Stop the main agent
        self.stop()


class ChildAgent(Agent):
    def __init__(self, name, task):
        super().__init__(name)
        self.task = task

    def run(self):
        # Implement the child agent's task execution logic here
        # For demonstration purposes, simply print the task and wait for 3 seconds
        print(f"{self.name} executing task: {self.task}")
        time.sleep(3)
        self.complete()


class ScriptingAgent(Agent):
    def run(self):
        # Implement the scripting agent's logging logic here
        while self.is_running:
            for agent in main_agent.child_agents:
                print(f"{agent.name} status: {agent.status}")
            time.sleep(1)


# Usage
main_agent = MainAgent()
main_agent.run()
