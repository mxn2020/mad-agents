# utils.py

import json
import random

def generate_agent_name():
    adjectives = ['Sneaky', 'Whiskered', 'Bumbling', 'Zany', 'Quirky', 'Fluffy', 'Charming', 'Wacky', 'Hilarious', 'Crazy', 'Dapper', 'Giggly', 'Cheeky', 'Funky', 'Silly']
    animals = ['Penguin', 'Panda', 'Kangaroo', 'Sloth', 'Giraffe', 'Platypus', 'Hippopotamus', 'Narwhal', 'Ostrich', 'Koala', 'Raccoon', 'Llama', 'Chimpanzee', 'Hedgehog', 'Octopus']
    suffixes = ['007', 'X', 'Mega', 'Mastermind', 'Inferno', 'Phantom', 'Ninja', 'Whisper', 'Rascal', 'Troublemaker', 'Spectacular', 'Snickerdoodle', 'Guru', 'Wizard', 'Champion']

    adjective = random.choice(adjectives)
    animal = random.choice(animals)
    suffix = random.choice(suffixes)

    return f"{adjective} {animal} {suffix}"


# List of funny agent names
funny_names = [
    "Captain Chuckles",
    "Doctor Giggles",
    "Agent Jester",
    "Sir Laughs-a-Lot",
    "Madame Funnybone",
    "Baron Witty",
    "The Comical Commander",
    "Duchess Giggleworth"
]


def get_prompt_details(prompt):
    return 0
    
def load_json_file(file_path):
    """
    Load and parse data from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Parsed JSON data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON data.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_json_file(data, file_path):
    """
    Save data to a JSON file.

    Args:
        data (dict): Data to be saved.
        file_path (str): Path to the output JSON file.
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def update_screen(agent_statuses):
    """
    Update the screen with agent statuses.

    Args:
        agent_statuses (dict): Dictionary containing agent names as keys and their statuses as values.
    """
    # Implement your logic to update the screen with agent statuses
    pass

def generate_unique_filename(prefix, extension):
    """
    Generate a unique filename based on the prefix and extension.

    Args:
        prefix (str): Prefix for the filename.
        extension (str): File extension.

    Returns:
        str: Unique filename.
    """
    # Implement your logic to generate a unique filename based on the prefix and extension
    pass

def load_template(template_file):
    with open(template_file, 'r') as file:
        return file.read()