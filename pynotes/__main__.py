import sys
import win10toast
import argparse
import json
import pathlib
from colorama import init as c_init
from colorama import Fore, Style
c_init()


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

    remove_parser = commands_parser.add_parser(
    	"remove", help="Lets you remove a project or note.")
    remove_args = remove_parser.add_mutually_exclusive_group()
    remove_args.add_argument("-p", "--project", help="", action="store", type=str)
    remove_args.add_argument("-n", "--note", help="", action="store", type=str)

    args = parser.parse_args()
    if args.command == "initdir":
        project_dir = str(pathlib.Path().absolute())
        project_name = project_dir.split("\\")[-1]

        addProject(project_name, project_dir)

        if not args.quiet:
            print("Initialised project {0}".format(project_name))

    elif args.command == "add-project":
        addProject(args.projectName)

        if not args.quiet:
            print("Added project {0}".format(args.projectName))

    elif args.command == "add-note":
        pass
        # do stuff
    elif args.command == "view":
        with open("db.json") as json_file:
            data = json.load(json_file)
        if(args.project):
            projectName = args.project
            print("doing this one")
            for i in data["projects"]:
                if i["projectName"] == args.project:
                    notes = i['notes']
        else:
            projectName = "Global"
            for i in data["projects"]:
                if i["projectName"] == "Global":
                    notes = i["notes"]
        print('Notes from: %s' % (Fore.GREEN + projectName))
        i = 1
        for j in notes:
            print(Fore.RED + '  ' + str(i) + ": " + Style.RESET_ALL + j)
            i += 1

    elif args.command == "remove":
    	pass
    	#ADD THIS


def addProject(project_name, project_dir=""):
    with open("db.json") as json_file:
        data = json.load(json_file)
    data["projects"].append(
        {"projectName": project_name, "dir": project_dir, "notes": []})
    with open('db.json', 'w') as json_file:
        json.dump(data, json_file)


if __name__ == '__main__':
    main()
