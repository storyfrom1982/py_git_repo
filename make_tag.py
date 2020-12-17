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


def make_tag(tag_name, tag_info):

    with open('repo.json', 'r') as load_f:
        repo = json.load(load_f)
        projects = repo['submodules']

    for sub_project in projects:
        if not os.path.exists(sub_project['path']):
            continue
        with cd(sub_project['path']):
            new_tag = {}
            with os.popen('git symbolic-ref --short -q HEAD') as pipe:
                branch = pipe.read()
                print(branch)
                new_tag['branch'] = branch
            with os.popen('git rev-parse HEAD') as pipe:
                commit_id = pipe.read()
                print(commit_id)
                new_tag['commit'] = commit_id
            sub_project['tag'] = new_tag

    with open('repo.json', 'w') as save_f:
        repo['submodules'] = projects
        json.dump(repo, save_f)

    print(repo)
    os.system('git add repo.json')
    os.system('git commit -m ' + '"' + tag_info + '"')
    os.system('git push')
    cmd = 'git tag -a ' + tag_name + ' -m ' + '"' + tag_info + '"'
    print(cmd)
    os.system(cmd)
    os.system('git push ' + 'origin ' + tag_name)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("is not set tag name and tag info")
        exit(0)
    make_tag(sys.argv[1], sys.argv[2])
