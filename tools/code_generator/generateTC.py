import json
import os
from jinja2 import Environment, FileSystemLoader
import re

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)


template_file = "TCTemplate.jinja"
json_file = os.path.join(script_dir,"tm_tc.json")
output_directory = os.path.normpath(os.path.join(script_dir, '..', '..', 'src', 'Telecommands'))

os.makedirs(output_directory, exist_ok=True)

# Load the Jinja2 environment and template
env = Environment(loader=FileSystemLoader(script_dir))
template = env.get_template(template_file)

def camel_to_snake(name):
    # Replace uppercase letters with an underscore followed by the lowercase version
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    return name

# Function to render the Jinja2 template and write the file
def generate_telecommand_class(telecommand):
    class_name = camel_to_snake(telecommand['name'])

    # Prepare the data for the template
    template_data = {
        'class_name': class_name,
        'telecommand_name': camel_to_snake(telecommand['name']),
        'operation_id': telecommand['id'],
        'num_inputs': len(telecommand.get('arguments', [])),
        'arguments': telecommand.get('arguments', []),
        'return_type': telecommand.get('return', {}).get('type', None),
        'return_name': telecommand.get('return', {}).get('name', None)
    }

    # Render the template with data
    class_code = template.render(template_data, enumerate=enumerate)

    # Write the generated class code to a Python file
    file_path = os.path.join(output_directory, f"{class_name}.py")
    with open(file_path, 'w') as file:
        file.write(class_code)

    print(f"Generated file: {file_path}")


with open(json_file) as file_handler:
    file_contents = file_handler.read()
parsed_json = json.loads(file_contents)
telecommands = parsed_json['telecommands']
for telecommand in telecommands:
    generate_telecommand_class(telecommand)
