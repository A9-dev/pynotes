import sys
import win10toast
import argparse

def main():
    parser = argparse.ArgumentParser(description="add a description Henry, I'm no good with words")
    commands_parser = parser.add_subparsers(help='commands')

    parser.add_argument("-q", "--quiet", help="Run command with no output",
    					action="store_true") # specify that the command should be run quietly, i.e. give no console output.

    init_parser = commands_parser.add_parser("init", help="")

    view_parser = commands_parser.add_parser("view", help="")
    view_parser.add_argument("--all", default=False, action="store_true")

    add_note_parser = commands_parser.add_parser("addnote", help="")
    add_note_parser.add_argument("title", help="")
    add_note_parser.add_argument("-m", help="",
    							action="store", type=str)

    print(parser.parse_args())

if __name__ == '__main__':
    main()
