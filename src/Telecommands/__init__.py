import os
import importlib
from telecommand_interface import TelecommandInterface
# Get a list of all Python files in the current directory
module_names = [filename[:-3] for filename in os.listdir(os.path.dirname(__file__)) if filename.endswith('.py') and filename != '__init__.py']


# Collect class names
all_telecommands = []

for module_name in module_names:
    module = importlib.import_module(f'.{module_name}', package=__name__)
    for name, obj in module.__dict__.items():
        if isinstance(obj, type) and obj.__module__ == module.__name__:
            all_telecommands.append(obj)

