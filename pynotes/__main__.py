import sys
import win10toast
import argparse
import json
import pathlib
import os
from colorama import init as c_init
from colorama import Fore, Style
c_init()

json_path = None
data = None

def main():
	global json_path
	global data

	json_path = "\\".join(
		str(pathlib.Path(__file__).absolute()).split("\\")[:-2]) + "\\db.json"
	with open(json_path) as json_file:
		data = json.load(json_file)
	currentDir = str(pathlib.Path().absolute())
	isInitialised = currentDir in [
		x["dir"] for x in data["projects"]]

	parser = argparse.ArgumentParser(
		description="Pynotes is a terminal based app that lets you add notes to specific projects and directories")
	commands_parser = parser.add_subparsers(help='commands', dest="command")

	parser.add_argument(
		"-q", "--quiet", help="Run command with no output", action="store_true")

	init_parser = commands_parser.add_parser(
		"initdir", help="Initialise current directory as a project, letting you automatically filter viewed notes to the ones added to the directory if the command was ran from that directory")
	init_parser.add_argument(
		"-p", "--project", help="", action="store", type=str)

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
	remove_parser.add_argument("-p", "--project", help="",
							 action="store", type=str)
	remove_parser.add_argument("-n", "--note", help="", action="store", type=int)

	args = parser.parse_args()
	if args.command == "initdir":
		if not isInitialised:
			project_dir = currentDir
			project_name = project_dir.split("\\")[-1]
			canInit = True

			if args.project:
				isExisting = False
				for i in range(len(data['projects'])):
					if data['projects'][i]['projectName'] == args.project:
						if data['projects'][i]["dir"]:
							canInit = False
						else:
							isExisting = True
							index = i

				if canInit:
					project_name = args.project
				else:
					print(
						Fore.RED + "Cannot init, {} is already initialised!".format(args.project))
					canInit = False

			if canInit:
				if isExisting:
					data["projects"][index]["dir"] = currentDir

					try:
						with open(json_path, 'w') as json_file:
							json.dump(data, json_file)
					except Exception as e:
						print(Fore.RED + repr(e))

				else:
					addProject(project_name, project_dir)

				if not args.quiet:
					print(Fore.GREEN +
					  "Initialised project {0}!".format(project_name))
				
		else:
			print(
				Fore.RED + "Cannot init directory, {} is already initialised!".format(currentDir))


	elif args.command == "add-project":
		canAdd = True
		for i in data['projects']:
			if(i['projectName'] == args.projectName):
				canAdd = False
		if canAdd:
			addProject(args.projectName)

		if not args.quiet and canAdd:
			print(Fore.GREEN + "Added project {0}".format(args.projectName))
		else:
			print(
				Fore.RED + "Cannot create project, project with the name %s already exists!" % (args.projectName))

	elif args.command == "add-note":
		if not args.project:
			for i in data['projects']:
				if (currentDir == i['dir']):
					try:
						i['notes'].append(args.note)
						with open(json_path, 'w') as json_file:
							json.dump(data, json_file)
						if not args.quiet:
							print(Fore.GREEN + "Successfully added note to %s!" %
								  (i['projectName']))
					except Exception as e:
						print(Fore.RED + repr(e))
		else:
			found = False
			for i in data['projects']:
				if(i['projectName'] == args.project):
					try:
						found = True
						i['notes'].append(args.note)
						with open(json_path, 'w') as json_file:
							json.dump(data, json_file)
						if not args.quiet:
							print(Fore.GREEN + "Successfully added note!")
					except Exception as e:
						print(Fore.RED + repr(e))

			if not found:
				print(Fore.RED + "Project %s not found!" % args.project)

	elif args.command == "view":
		notes = []
		useCurrentDir = False
		found = True
		if(not args.all):
			if(args.project):
				found = False
				projectName = args.project
				for i in data["projects"]:
					if i["projectName"] == args.project:
						notes = i['notes']
						found = True
				if not found:
					print(Fore.RED + "Project %s not found!" % args.project)
			else:
				for i in data['projects']:
					if (currentDir == i['dir']):
						useCurrentDir = True
						projectName = i['projectName']
						notes = i['notes']
				if not useCurrentDir:
					projectName = "Global"
					for i in data["projects"]:
						if i["projectName"] == "Global":
							notes = i["notes"]
			if found:

				print(Style.RESET_ALL + 'Notes from: ' +
					  Fore.GREEN + projectName)
				if not notes:
					print(Fore.RED + "  " + "No notes!")
				i = 1
				for j in notes:
					print(Fore.RED + '  ' + str(i) +
						  ": " + Style.RESET_ALL + j)
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
		removed = False
		if args.note:
			if args.project:
				found = False
				for i in data['projects']:
					if i['projectName'] == args.project:
						found = True
						try:
							i['notes'].pop(args.note-1)
							removed = True
						except Exception as e:
							print(Fore.RED + "Invalid note number!")
						
				if not found and not args.quiet:
					print(Fore.RED + "Project %s not found!"%(args.project))
				# Nice
				# REMOVE args.note FROM args.project
			elif isInitialised:
				pass
				# REMOVE args.note FROM project["dir"] == currentDir
			else:
				pass
				# REMOVE args.note FROM Global
		else:
			if args.project:
				found = False

				for i in range(len(data["projects"])):
					if data["projects"][i]["projectName"] == args.project:
						found = True
						index = i

				if found:
					data["projects"].pop(index)
					removed = True

					if not args.quiet:
						print(Fore.GREEN + "Removed project, %s!"%(args.project))
				else:
					if not args.quiet:
						print(Fore.RED + "Project, %s not found!"%(args.project))

			elif isInitialised:
				index = 0

				for i in range(len(data["projects"])):
					if data["projects"][i]["dir"] == currentDir:
						index = i

				data["projects"].pop(index)
				removed = True

				if not args.quiet:
					print(Fore.GREEN + "Removed project with dir, %s!"%(currentDir))

			else:
				print(Fore.RED + "Please specify a project or note to remove!")

		if removed:
			try:
				with open(json_path, 'w') as json_file:
					json.dump(data, json_file)
			except Exception as e:
				print(Fore.RED + repr(e))


def addProject(project_name, project_dir=""):
	data["projects"].append(
		{"projectName": project_name, "dir": project_dir, "notes": []})
	with open(json_path, 'w') as json_file:
		json.dump(data, json_file)


if __name__ == '__main__':
	main()

	'''
	TODO:
		1. Add notifications.
			- Set reminders either at a specific time or after a certain length of time.
			- Create/Find an icon.
		2. Change searches with isInitialised.
	'''
