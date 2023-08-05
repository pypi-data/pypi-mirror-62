# -*- coding: utf-8 -*-
""" Smommit: the git small commit system

Usage:
    {0} {1} [-v | --verbose] [(-m <message>)]
    {0} {1} [-v | --verbose] [(<line> [-f | --force])]
    {0} {1} [-v | --verbose]
    {0} {1} [-v | --verbose] [-c | --config]
    {0} {1} [-v | --verbose] [-c | --config]
    {0} -h | --help | --version
Options:
    -m --message  The smommit message (if not present then default editor will be opened)
    -c --config   Specifies the smommit config file
    -f --force    Force/Don't ask for permission
    -v --verbose  Verbose
    -h --help     Shows help
    --version     Show version
    <message>     The smommit message
    <line>        Line number
"""

from docopt import docopt
from smommit import command_handler

__version__ = "0.1.2"

main_exec = "smommit"
commands = {
    # Add a message line to the mini commit text
    "add": command_handler.add,
    # Remove a message line from the mini commit text
    "rm": command_handler.remove,
    # Refresh command to initialise smommit file structure
    "refresh": command_handler.refresh,
    # View all lines of the smommit and config file for the current branch
    "view": command_handler.view,
    # Edit the entire smommit inside the default editor (just acts as an abstraction so that the user doesn't have to go to file)
    "edit": command_handler.edit
}

args_commands = {
    'add': False,
    '--verbose': 0,
    '--message': 0,
    '<message>': None,
    'rm': False,
    '<line>': None,
    '--force': 0,
    'refresh': False,
    'view': False,
    '--config': 0,
    'edit': False,
    '--help': 0,
    '--version': False
}

# Program flow:
# 1. User will use "add" command to add a new line to the commit
# 2. smommit will check if the .smommit dir has been made and checks for a smommit text file for the current branch text file
# 3a. If no .smommit dir exists then will create and also create edit/create .gitignore to add .smommit onto it. Also adds smommit prepare-commit-msg bash
# 3b. If no smommit text file for current branch then creates text file to track messages
# 3c. If smommit text file for current branch exists: then append message to the end
# 4. If "git commit" is called then the prepare-commit-msg bash for smommit is called which adds all the smommits inside the smommit for that branch to the message
#    and deletes the smommit for that branch after commit

def init_docs(_doc: str) -> str:
    """ Initialises the __doc__ field to be parsed into docopts. Just formats
        the __doc__ with the commands from the commands list and adds the
        main executable command to all subcommands.
        - _doc: the string containing the __doc__
        - returns: a formated string with the main executable command and all subcommands
    """
    docs = []
    com_count = 0
    for doc in _doc.split("\n"):
        if "{" in doc or "}" in doc:
            doc = doc.format(main_exec, list(commands.keys())[com_count] if com_count < len(commands.keys()) else None)
            com_count += 1
        docs.append(doc)
        
    docs = "\n".join(docs)
    return docs

def remove_options(args: dict) -> dict:
    """ Strips options part of doc which gets parsed by docopts
        - args: the dictionary of arguments produced by docopts
        - returns: a dictionary with just the useful arguments in it
    """
    new_args = dict()
    for arg in args.keys():
        if arg == "Options:":
            break
        new_args[arg] = args[arg]
    return new_args

def find_difference(dict1: dict, dict2: dict) -> dict:
    """ Finds the items in two dictionaries that are different. Hard to classify this function but here's an
        example. For example if dict1 = {"hello": False, "world": False} and 
        dict2 = {"hello": True, "world": False}, the returned dict would be {"hello": True}
        - dict1: the dictionary to "subtract"
        - dict2: the dictionary to complement
        - returns: the different keys and values between dict1 and dict2
    """
    return {key: dict2[key] for key in dict1.keys() if dict1[key] != dict2[key]}

""" Function called when smommit command is run """
def main():
    arguments = docopt(init_docs(__doc__), version=__version__)
    arguments = remove_options(arguments)
    # print(arguments)
    arguments = find_difference(args_commands, arguments)
    found = False

    if len(arguments.keys()) != 0:
        for arg in arguments.keys():
            if arg in commands.keys():
                # Deletes (sub)command key from dictionary then calls that (sub)command's handler
                # which is stored in the commands dict
                del arguments[arg]
                commands[arg](arguments)
                # found = True
                break
