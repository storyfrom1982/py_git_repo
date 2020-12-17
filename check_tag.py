import os
import sys
import json


class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def check_tag(tag_name):

    os.system('git checkout ' + tag_name)

    with open('repo.json', 'r') as load_f:
        repo = json.load(load_f)
        projects = repo['submodules']

    for sub_project in projects:
        if not os.path.exists(sub_project['path']):
            continue
        with cd(sub_project['path']):
            tag = sub_project['tag']
            os.system('git checkout ' + tag['branch'])
            os.system('git reset --hard ' + tag['commit'])
            os.system('git status')


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("is not set tag name")
        exit(0)
    check_tag(sys.argv[1])
