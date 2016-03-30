import sys
import shutil
import os
import json

from classes.main_display import MainDisplay
from the_parser import parser

def do_stuff():
    config = get_config()
    for file in os.listdir():
        if os.path.isfile(file):
            create_and_move(config, file)
    print("Finished Organizing")

def get_config():
    with open(os.path.dirname(os.path.realpath(__file__))+'/config.json') as config:
        valid_config = json.load(config)
        return valid_config

def print_matching_extensions(config, extension):
    for folder in config:
        if extension in config[folder]:
            print('Found {0} in {1}'.format(extension, folder))

def create_and_move(config, file):
    extension = os.path.splitext(file)[1]
    for folder in config:
        if extension in config[folder]:
            if not os.path.exists('/'+folder):
                os.makedirs(folder, exist_ok=True)
            shutil.move(file, './'+folder)

if __name__ == '__main__':
    args = parser.parse_args()

    if args.choice == 'config':
        config = MainDisplay()
        config.run()

    do_stuff()
