import os
import tkinter as tk
from tkinter import filedialog
from shutil import copy2

ROOT_DIRECTORY = '.'
BOTS_DESTINATION = 'dome9CloudBots/bots'
ZIP_NAME = 'cloudbots-zipped'
YES = 'y'
NO = 'n'


def main():
    is_add_files = ask_user_if_add_files()
    if is_add_files:
        files_to_add = choose_files_to_add()
        destination = choose_destination()
        add_files(files_to_add, destination)
    function_app_name = get_params_from_user()
    try:
        print(f'Updating function app: {function_app_name}...')
        update_function_app(function_app_name)
    except Exception as e:
        print(f'Error updating function function app: {function_app_name} - {e}')
    print(f'Successfully updated function function app: {function_app_name}')


def update_function_app(function_app_name):
    os.system('func init')
    command = f'func azure functionapp publish {function_app_name}'
    os.system(command)


def get_params_from_user():
    function_app_name = input(f'Enter name of the function app:\n')
    return function_app_name


def ask_user_if_add_files():
    while True:
        add_files_user_choice = input(f'Do you want to add files to the function? ({YES}/{NO}) ')
        if add_files_user_choice != YES and add_files_user_choice != NO:
            print(f'Error! Illegal input. Required: ({YES}/{NO})')
            continue
        if add_files_user_choice == YES:
            return True
        return False


def choose_destination():
    is_chosen = False
    destination = BOTS_DESTINATION
    while not is_chosen:
        is_different_destination = input(f'Default destination is {BOTS_DESTINATION}. '
                                         f'Do you want to choose a different destination? ({YES}/{NO}) ')
        if is_different_destination != NO and is_different_destination != YES:
            print(f'Error! Illegal input. Required: ({YES}/{NO})')
            continue
        if is_different_destination == NO:
            is_chosen = True
        else:
            root = tk.Tk()
            root.withdraw()
            destination = filedialog.askdirectory(initialdir=ROOT_DIRECTORY)
            is_chosen = True
    return destination


def choose_files_to_add():
    root = tk.Tk()
    root.withdraw()
    files = filedialog.askopenfilenames(title='Choose files to add')
    return files


def add_files(files, destination, ):
    for file_path in files:
        try:
            copy2(file_path, destination)
            print(f'Copied file: {file_path} to destination: {os.path.abspath(destination)}')
        except Exception as e:
            print(f'Error! Failed to copy file: {file_path} to {destination} - {e}')


if __name__ == '__main__':
    main()
