import sys
import win10toast
import argparse

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-q", help="Add a new project", action="store_true") # specify that the command should be run quietly, i.e. give no console output.
    

if __name__ == '__main__':
    main()
