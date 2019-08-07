import os

def read_file_to_text(path):
    with open(relpath(path), "r") as file:
        data = file.read()
    return data


def relpath(path):
    return os.path.join(os.path.dirname(__file__), path)