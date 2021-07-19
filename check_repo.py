import os
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


if __name__ == "__main__":
    with open('depends/repo.json', 'r') as load_f:
        repo = json.load(load_f)
        submodules = repo['submodules']

    for submodule in submodules:
        submodule_path = os.path.join('depends/', submodule['name'])
        if not os.path.exists(submodule_path):
            os.system('git clone ' + submodule['repo'] + ' ' + submodule_path)

        with cd(submodule_path):
            os.system('git checkout ' + submodule['branch'])
            os.system('git pull')
            os.system('git reset --hard ' + submodule['commit'])
            os.system('git status')


