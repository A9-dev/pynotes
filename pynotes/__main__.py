import sys
import win10toast
import argparse
import json
import pathlib
from colorama import init as c_init
from colorama import Fore, Style
c_init()


def main():
    global json_path
    global isInitialised
    global dirName

    json_path = "\\".join(str(pathlib.Path(__file__).absolute()).split("\\")[:-2]) + "\\db.json"
    with open(json_path) as json_file:
        data = json.load(json_file)

    isInitialised = str(pathlib.Path().absolute()) in [x["dir"] for x in data["projects"]]
    dirName = str(pathlib.Path().absolute()).split("\\")[-1] if isInitialised else None

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
        if not isInitialised:
            project_dir = str(pathlib.Path().absolute())
            project_name = project_dir.split("\\")[-1]

            addProject(project_name, project_dir)

            if not args.quiet:
                print("Initialised project {0}".format(project_name))
        else:
            print("{0} already initialised.".format(dirName))

    elif args.command == "add-project":
        addProject(args.projectName)

        if not args.quiet:
            print("Added project {0}".format(args.projectName))

    elif args.command == "add-note":
        pass
        # do stuff

    elif args.command == "view":
        with open(json_path) as json_file:
            data = json.load(json_file)
        if(not args.all):
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
        else:
            for i in data["projects"]:
                k = 1
                print(Style.RESET_ALL + 'Notes from: %s' %
                      (Fore.GREEN + i["projectName"]))
                if(not i["notes"]):
                    print(Fore.RED + "  "+"No notes!")

                for j in i["notes"]:
                    print(Fore.RED + '  ' + str(k) +
                          ": " + Style.RESET_ALL + str(j))
                    k += 1

    elif args.command == "remove":
        pass
    	#ADD THIS


def addProject(project_name, project_dir=""):
    with open(json_path) as json_file:
        data = json.load(json_file)
    data["projects"].append(
        {"projectName": project_name, "dir": project_dir, "notes": []})
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file)


if __name__ == '__main__':
    main()

    '''
	TODO:
		1. Add the option to link an existing project to a directory. CLAIMED - MORGAN
		2. Add colours to all print messages.
		3. Fix view for initialised directories.
		4. Check if a project exists when trying to add one and if it does, ask to either change name or overwrite. CLAIMED - MORGAN
		5. Write remove function.
		6. Add notifications.
		7. Add notes to projects.
    '''