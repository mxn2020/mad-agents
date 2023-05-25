from agents import Agent, generate_agent_name, PromptAgent
from queue import Queue
from threading import Thread
import logging
import random, time

class PromptManagerAgent(Agent):
    def __init__(self, name="Manager Agent", global_data_agent=None, max_batch_size=5):
        super().__init__(name, global_data_agent)
        self.agent_queue = Queue()
        self.max_batch_size = max_batch_size
        self.in_data = None
        self.out_data = None
        self.agents = []

    def receive_data(self, data):
        self.update_status("Received data.")
        self.in_data = data

    def processDataset(self):
        for item in self.in_data:
            agent_fun_name = generate_agent_name()
            agent_name = f"{agent_fun_name}-{random.randint(0, 100)}"
            agent = PromptAgent(item, agent_name)
            self.agents.append(agent)
            agent_item = (agent, item)
            self.agent_queue.put(agent)


    def process_queue(self):
        num = 0
        running_agents_arr = []
        while not self.agent_queue.empty():
            running_agents = sum(agent.is_running for agent in running_agents_arr)
            pending_agents = self.agent_queue.qsize()
            num += 1
            # print (f"Running agents: {running_agents} / {self.agent_queue.qsize()}")
            prompt_manager_status = f"Running agents: {running_agents} / {self.agent_queue.qsize()}"
            self.update_status(f"Processing {prompt_manager_status} agents...")
            if running_agents < self.max_batch_size:
                agent = self.agent_queue.get()
                running_agents_arr.append(agent)
                # print(f"Is Agent running ???: {agent.is_running}")
                agent.launch()
                # print(f"Starting agent: {agent.name}")

            time.sleep(0.1)
                

    def run(self):
        self.update_status("Queuing...")
        self.processDataset()
        while not self.agent_queue.empty():
            self.update_status("Processing queue...")
            self.process_queue()
            self.update_status("Queue processed.")
        self.stop()




class AgentThread(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.logger = logging.getLogger("AgentThread")
        self.is_running = False

    def run(self):
        # Perform processing logic on self.item
        random_number = random.randint(6, 15)
        # print('-----------------------------------')
        # print(f"Processing item: {self.item}.........waiting {random_number} seconds")
        # print(f"Thread: {self.name}")
        # print('-----------------------------------')
        time.sleep(random_number)
        # self.logger.info(f"Processing item: {self.item}")
        self.stop()

