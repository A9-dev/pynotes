import sys
import win10toast
import argparse
import os


def main():
	parser = argparse.ArgumentParser(
		description="Pynotes is a terminal based app that lets you add notes to specific projects and directories")
	commands_parser = parser.add_subparsers(help='commands', dest="command")

	parser.add_argument("-q", "--quiet", help="Run command with no output", action="store_true")

	init_parser = commands_parser.add_parser("initdir",
		help="Initialise current directory as a project, letting you automatically filter viewed notes to the onesadded to the directory if the command was ran from that directory")

	add_project_parser = commands_parser.add_parser("add-project",
		help="Add a project which you can add notes to and view notes from")
	add_project_parser.add_argument("projectName", help="", action="store", type=str)

	add_note_parser = commands_parser.add_parser("add-note",
		help="Lets you add a note to a project, a directory, or a global project")
	note_args = add_note_parser.add_mutually_exclusive_group()
	note_args.add_argument("-p", "--project", help="", action="store", type=str)
	note_args.add_argument("-g", "--global", help="", action="store_true")
	add_note_parser.add_argument("note", help="", type=str)

	view_parser = commands_parser.add_parser("view",
		help="Lets you view your notes, defaulted to the current dir if ran from an initialised dir, then to the project if specified, and then global")
	view_args = view_parser.add_mutually_exclusive_group()
	view_args.add_argument("-a", "--all", default=False, action="store_true")
	view_args.add_argument("-p", "--project", help="", action="store", type=str)

	args = parser.parse_args()

	if args.command == "initdir":
		pass
		# do stuff
	elif args.command == "add-project":
		pass
		#do stuff
	elif args.command == "add-note":
		pass
		#do stuff
	elif args.command == "view":
		pass
		#do stuff


if __name__ == '__main__':
	main()
