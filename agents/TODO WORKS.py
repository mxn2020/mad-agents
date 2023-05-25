import time
import uuid
import os
import sys
import json
import threading
import openai
import random

# Function to create a unique slug
def generate_slug():
    return str(uuid.uuid4())

# Function to load prompt template from file
def load_prompt_template(template_file):
    with open(template_file, 'r') as file:
        return file.read()

# Function to replace values within the prompt template
def replace_template_values(template, values):
    for key, value in values.items():
        template = template.replace(f"{{{key}}}", str(value))
    return template

# Function to save the API response to a file
def save_response_to_file(fname, response_text):
    filename = f"V5_{fname}_{generate_slug()}.json"
    with open(filename, 'w') as file:
        file.write(response_text)
    return filename

# Function to extract name and description from JSON in response text
def extract_name_description_from_json(response_text):
    try:
        json_data = json.loads(response_text)
        name = json_data.get('name')
        description = json_data.get('description')
        return name, description
    except json.JSONDecodeError:
        return None, None

def extract_items_from_response(response_text):
    try:
        json_data = json.loads(response_text)
        items = []
        for item in json_data:
            name = item.get('name')
            description = item.get('description')
            examples = item.get('examples')
            tags = item.get('tags')
            keywords = item.get('keywords')
            extracted_item = {
                'name': name,
                'description': description,
                'examples': examples,
                'tags': tags,
                'keywords': keywords
            }
            items.append(extracted_item)
        return items
    except json.JSONDecodeError:
        return []

# Check if the input file path is provided
if len(sys.argv) < 2:
    update_print("Please provide the input JSON file path as a command-line argument.")
    sys.exit(1)

input_file = sys.argv[1]

# Load OpenAI API key from file
with open('openaiAPIkey.json', 'r') as api_key_file:
    api_key_data = json.load(api_key_file)
    openai.api_key = api_key_data['api_key']

# Open the JSON file
with open(input_file, 'r') as file:
    data = json.load(file)

prompt_template_file = "template.prompt"  # Replace with the path to your prompt template file

# Track newly created child items
new_child_items = []
lock = threading.Lock()

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

def generate_agent_name():
    adjectives = ['Sneaky', 'Whiskered', 'Bumbling', 'Zany', 'Quirky', 'Fluffy', 'Charming', 'Wacky', 'Hilarious', 'Crazy', 'Dapper', 'Giggly', 'Cheeky', 'Funky', 'Silly']
    animals = ['Penguin', 'Panda', 'Kangaroo', 'Sloth', 'Giraffe', 'Platypus', 'Hippopotamus', 'Narwhal', 'Ostrich', 'Koala', 'Raccoon', 'Llama', 'Chimpanzee', 'Hedgehog', 'Octopus']
    suffixes = ['007', 'X', 'Mega', 'Mastermind', 'Inferno', 'Phantom', 'Ninja', 'Whisper', 'Rascal', 'Troublemaker', 'Spectacular', 'Snickerdoodle', 'Guru', 'Wizard', 'Champion']

    adjective = random.choice(adjectives)
    animal = random.choice(animals)
    suffix = random.choice(suffixes)

    return f"{adjective} {animal} {suffix}"

# Function to update the print output
def update_print(agent_name, message):
    # Clear the previous print output
    ## sys.stdout.write("\033[F")
    ## sys.stdout.write("\033[K")
    # Print the updated message
    print(f"{agent_name}: {message}")

# Function to process a parent item
def process_parent_item(agent_name, parent_item):
    parent_level_name = parent_item['name'].lower()
    parent_description = parent_item['description']
    parent_id = parent_item['id']
    parent_level_id = parent_item['level_number']

    # Print a log for the parent item
    update_print("Master Agent", f"Created {agent_name} for '{parent_item['name']}'")

    # Load prompt template
    prompt_template = load_prompt_template(prompt_template_file)

    # Replace values within the prompt template
    template_values = {
        'parent_level_name': parent_level_name,
        'parent_description': parent_description
    }
    prompt_text = replace_template_values(prompt_template, template_values)

    # Prepare messages for chat completion
    chat_messages = [{'role': 'system', 'content': 'You are a very sophisticated prompt engineer and web developer. You have a wide understanding everything that humans have discovered'}]
    chat_messages.append({'role': 'user', 'content': prompt_text})

    retry_count = 0
    max_retries = 50
    wait_time = 69

    while retry_count < max_retries:
        try:
            # Update agent status
            update_print(agent_name, "Sending API request")

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=chat_messages,
                max_tokens=3000,
                temperature=0.9,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )

            # Process the response as needed
            # ...

            break  # Exit the loop if API call succeeds
        except Exception as e:
            update_print(agent_name, f"Error occurred: {str(e)}")

            # Increase wait time for next retry
            wait_time += 15
            update_print(agent_name, f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            retry_count += 1

    if retry_count == max_retries:
        update_print(agent_name, "Maximum number of retries reached. Exiting...")

    # Extract items from the API response
    response_messages = response['choices'][0]['message']['content']
    response_items = extract_items_from_response(response_messages)

    # Save API response to a file
    response_file = save_response_to_file(parent_level_name, response_messages)

    # Create child items for the parent
    for i, extracted_item in enumerate(response_items):
        # Generate temporary ID
        temp_id = str(uuid.uuid4())

        name = extracted_item['name']
        description = extracted_item['description']
        examples = extracted_item['examples']
        tags = extracted_item['tags']
        keywords = extracted_item['keywords']
        related_concepts = extracted_item['related_concepts']
        key_thinkers = extracted_item['key_thinkers']
        historical_context = extracted_item['historical_context']
        methodologies = extracted_item['methodologies']
        contemporary_debates = extracted_item['contemporary_debates']
        contemporary_application = extracted_item['contemporary_application']
        case_studies = extracted_item['case_studies']
        relevance = extracted_item['relevance']
        criticisms = extracted_item['criticisms']

        child_item = {
            'id': temp_id,  # Temporary ID
            'name': name if name else f"Child {i+1}",
            'slug': generate_slug(),
            'parentID': parent_id,
            'parent': parent_description,
            'level_number': parent_level_id + 1,
            'level_name': f"sub-{parent_level_name}",
            'description': description if description else f"Description of Child {i+1}",
            'active': False,
            'expanded': False,
            'approved': False,
            'published': False,
            'filename': response_file,
            'generated': bool(name and description),
            'examples': examples,
            'tags': tags,
            'keywords': keywords,
            'related_concepts': related_concepts,
            'key_thinkers': key_thinkers,
            'historical_context': historical_context,
            'methodologies': methodologies,
            'contemporary_debates': contemporary_debates,
            'contemporary_application': contemporary_application,
            'case_studies': case_studies,
            'relevance': relevance,
            'criticisms': criticisms
        }

        # Acquire the lock before updating the shared list
        with lock:
            new_child_items.append(child_item)

        # Print agent status
        with lock:
            update_print(agent_name, "Performing task X")

# Create and start threads for each parent item
threads = []
for i, parent_item in enumerate(data['results']):
    agent_name = generate_agent_name()
    # funny_names.remove(agent_name)  # Remove the chosen name from the list to avoid duplicates
    thread = threading.Thread(target=process_parent_item, args=(agent_name, parent_item))
    thread.start()
    threads.append((agent_name, thread))

# Continuously update agent statuses
while any(thread.is_alive() for _, thread in threads):
    for agent_name, thread in threads:
        if thread.is_alive():
            with lock:
                update_print(agent_name, "Waiting in loop")
    time.sleep(1)

# Wait for all threads to complete
for _, thread in threads:
    thread.join()

# Create a new JSON object with only the newly created items
new_data = {
    'results': new_child_items
}

output_file_name = "Category"

# Generate a unique ID
unique_id = str(uuid.uuid4())

# Append the unique ID to the output file name
output_file = f"{output_file_name}_output_{unique_id}.json"
existing_data = {'results': []}

update_print("", "Finalizing...")

# Append the new data to the existing data
existing_data['results'].extend(new_child_items)

# Write the updated data to the file
with open(output_file, 'w') as file:
    json.dump(existing_data, file, indent=4)

update_print("", f"Processing completed. Check the '{output_file}' file.")
