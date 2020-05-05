import sys
import win10toast
import argparse
import os
import json


def main():

    parser = argparse.ArgumentParser(
        description="Pynotes is a terminal based app that lets you add notes to specific projects and directories")
    commands_parser = parser.add_subparsers(help='commands', dest="command")

    parser.add_argument(
        "-q", "--quiet", help="Run command with no output", action="store_true")

    init_parser = commands_parser.add_parser(
        "initdir", help="Initialise current directory as a project, letting you automatically filter viewed notes to the ones added to the directory if the command was ran from that directory")

    add_project_parser = commands_parser.add_parser(
        "add-project", help="Add a project which you can add notes to and view notes from")
    add_project_parser.add_argument(
        "projectName", help="", action="store", type=str)

    add_note_parser = commands_parser.add_parser(
        "add-note", help="Lets you add a note to a project, a directory, or a global project")
    add_note_parser.add_argument("note", help="", type=str)
    add_note_parser.add_argument(
        "-p", "--project", help="", action="store", type=str)

    view_parser = commands_parser.add_parser(
        "view", help="Lets you view your notes, defaulted to the current dir if ran from an initialised dir, then to the project if specified, and then global")
    view_args = view_parser.add_mutually_exclusive_group()
    view_args.add_argument("-a", "--all", default=False, action="store_true")
    view_args.add_argument("-p", "--project", help="",
                           action="store", type=str)

    args = parser.parse_args()
    if args.command == "initdir":
        pass
        # do stuff
    elif args.command == "add-project":
        pass
        # do stuff
    elif args.command == "add-note":
        pass
        # do stuff
    elif args.command == "view":
        with open("db.json") as json_file:
            data = json.load(json_file)
            notes = data[args.project]["notes"] if (
                args.project) else data["global"]["notes"]

            print("\n".join(notes))


if __name__ == '__main__':
    main()
