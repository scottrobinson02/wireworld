import json


def main(filename):

    validfile = False
    while validfile == False:
        if filename[-5:] != ".json":
            return "Config file is not a .json file"

        try:
            with open(filename, "r") as j:
                initial_state = json.load(j)
                validfile = True
        except FileNotFoundError:
            return "File not found"  # Cases where file doesn't exist, and ends with .json

        for row in initial_state:
            for col in row:
                if (col == 0) or (col == 1) or (col == 2) or (col == 3):
                    return initial_state
                else:
                    return "File contains invalid data"

    return initial_state
