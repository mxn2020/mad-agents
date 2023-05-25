from agents import Agent, ai_response
import random, time

class PromptAgent(Agent):
    def __init__(self, item, name="Prompt Agent", global_data_agent=None):
        super().__init__(name, global_data_agent)
        self.prompt_template = None
        self.item = item
        self.task_id = None
        self.status = "Initialized"
        self.manager = None  # Reference to the PromptManagerAgent

    def load_prompt_template(self, template):
        self.update_status("Loading prompt template...")
        self.prompt_template = template

    def generate_prompt(self):
        self.update_status("Generating prompt...")
        name = self.item.get("name", "")
        description = self.item.get("description", "")
        # prompt = self.prompt_template.replace("<name>", name).replace("<description>", description)
        # return prompt

    def set_manager(self, manager):
        self.manager = manager

    def assign_task_id(self, task_id):
        self.task_id = task_id

    def get_task_id(self):
        return self.task_id

    def process_prompt(self, prompt):
        self.update_status("Processing prompt...")
        # response = ai_response(prompt)

    def run(self):
        self.update_status("Running")
        random_number = random.randint(8, 12 )
        time.sleep(random_number)
        try:
            prompt = self.generate_prompt()
            prompt_result = self.process_prompt(prompt)
            
            if prompt_result is not None:
                self.update_status("Completed")
                # self.is_running = False
                self.stop()
                return prompt_result
            else:
                self.update_status("Failed to Complete")
                # self.is_running = False
                self.stop()
                return None
                
        except Exception as e:
            self.update_status("Error: {}".format(str(e)))
            self.logger.error("Error in prompt {}: {}".format(self.name, str(e)))
