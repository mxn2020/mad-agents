import queue
from agents.agent import Agent


class GlobalDataAgent(Agent):
    def __init__(self, name = "Global Data Agent"):
        super(GlobalDataAgent, self).__init__(name)
        self.data_queue = queue.Queue()
        self.shared_data = {}  # Dictionary to store the shared data
        self.running = False  # Flag to indicate if the agent is running

    def run(self):
        while self.running:
            print("Global Data Agent running...")
            try:
                # Get the next data action from the queue
                data_action = self.data_queue.get(timeout=1)
                
                # Process the data action
                action_type, key, value = data_action
                if action_type == 'add':
                    self.shared_data[key] = value
                elif action_type == 'get':
                    result = self.shared_data.get(key)
                    # Do something with the result, e.g., pass it to a callback function or return it
                    print(f"Value for key '{key}': {result}")
                    return result
                
                # Add more data actions as needed

                # Mark the data action as complete
                self.data_queue.task_done()

            except queue.Empty:
                continue

    def enqueue_data_action(self, data_action):
        self.data_queue.put(data_action)

    def add(self, key, value):
        self.enqueue_data_action(('add', key, value))

    def get(self, key):
        self.enqueue_data_action(('get', key))
