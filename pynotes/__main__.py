import sys
import win10toast
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="add a description Henry, I'm no good with words")
    commands_parser = parser.add_subparsers(help='commands')

    parser.add_argument("-q", "--quiet", help="Run command with no output", action="store_true")

    init_parser = commands_parser.add_parser("initdir", help="")

    add_project_parser = commands_parser.add_parser("add-project", help="")
    add_project_parser.add_argument("projectName", help="")

    add_note_parser = commands_parser.add_parser("add-note", help="")
    add_note_parser.add_argument("note", help="")
    add_note_parser.add_argument("-p", "--project", help="", action="store", type=str)

    view_parser = commands_parser.add_parser("view", help="")
    view_parser.add_argument("-a", "--all", default=False, action="store_true")
    view_parser.add_argument("-p", "--project", help="", action="store", type=str)

    print(parser.parse_args())

if __name__ == '__main__':
    main()
