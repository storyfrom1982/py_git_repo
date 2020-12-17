import os
import json
import sys


class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


if __name__ == "__main__":
    with open('repo.json', 'r') as load_f:
        repo = json.load(load_f)
        projects = repo['submodules']
    for sub_project in projects:
        if not os.path.exists(sub_project['path']):
            continue
        with cd(sub_project['path']):
            os.system('echo "' + sys.argv[1] + '" >> README.md')
            os.system('git add README.md')
            os.system('git commit -m "' + sys.argv[1] + '"')
            os.system('git push')


