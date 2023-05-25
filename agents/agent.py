import logging
import threading

class Agent(threading.Thread):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.on_launch()

    def __init__(self, name, global_data_agent=None):
        super().__init__()
        self.name = name
        self.is_running = False
        self.status = "Agent initialized..."
        self.type = "Agent"
        self.previous_status = ""
        self.previous_status_no = 20
        self.completion = 0
        self.task = ""
        self.topic = ""
        self.counter = 0
        self.status_code = "inactive"
        self.logger = logging.getLogger(name)
        self.global_data_agent = global_data_agent
        
        # Task progress tracking
        self.total_tasks = 0
        self.completed_tasks = 0

        # Event notification
        self.event = threading.Event()

        # Pause and resume
        self.pause_event = threading.Event()
        self.pause_event.set()  # Agent is initially not paused

        # Agent dependencies
        self.dependencies = []

    @classmethod
    def on_launch(cls):
        # Function to be called on launch
        print(f"{cls.__name__} launched!")

    def launch(self):
        if not self.is_running:
            self.status = "Agent launched..."
            self.is_running = True
            super().start()

    def stop(self):
        print(f"Stopping {self.name}...")
        self.is_running = False
        self.status = "Agent stopped..."
        self.status_code = "inactive"

    def run(self):
        raise NotImplementedError("Subclasses must implement the run() method.")

    def update_status(self, new_status):
        self.previous_status = self.status
        self.status = new_status
        self.counter = 0
        self.status_code = "active"  # Update status code to "active" when status changes

    def activate(self):
        self.status_code = "active"
        self.status = "Agent activated..."  # Update status when agent is activated

    def complete(self):
        self.status_code = "complete"
        self.status = "Agent completed..."  # Update status when agent is completed

    def update_progress(self, completed_tasks):
        self.completed_tasks = completed_tasks

    def notify_event(self):
        self.event.set()

    def wait_for_event(self):
        self.event.wait(timeout=1)

    def pause(self):
        self.pause_event.clear()
        self.status_code = "paused"  # Update status code to "paused" when agent is paused
        self.status = "Agent paused..."  # Update status when agent is paused

    def resume(self):
        self.pause_event.set()
        self.status_code = "active"  # Update status code to "active" when agent is resumed
        self.status = "Agent resumed..."  # Update status when agent is resumed

    def add_dependency(self, agent):
        if agent not in self.dependencies:
            self.dependencies.append(agent)

    def configure(self, **kwargs):
        # Implement agent configuration logic here
        self.status = "Agent configuration updated..."  # Update status when agent configuration is updated

    def synchronize(self):
        # Implement agent synchronization logic here
        self.status = "Agent synchronized..."  # Update status when agent is synchronized
        self.status_code = "synchronized"  # Update status code to "synchronized" when agent is synchronized

