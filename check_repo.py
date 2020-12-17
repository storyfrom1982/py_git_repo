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
    with open('repo.json', 'r') as load_f:
        repo = json.load(load_f)
        projects = repo['submodules']
    for sub_project in projects:
        if os.path.exists(sub_project['path']):
            with cd(sub_project['path']):
                os.system('git reset --hard')
                os.system('git checkout ' + sub_project['tag']['branch'])
                os.system('git pull')
            continue
        cmd = 'git clone ' + sub_project['repo'] + ' ' + sub_project['path']
        print(cmd)
        os.system(cmd)
        with cd(sub_project['path']):
            os.system('git checkout ' + sub_project['tag']['branch'])
            os.system('git pull')
        continue


