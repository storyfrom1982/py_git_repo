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
    repos = {}
    projects = []
    for subdir in os.listdir(r"depends"):
        dir_path = os.path.join(r"depends/", subdir)
        if os.path.isfile(dir_path):
            continue
        new_tag = {}
        print(dir_path)
        new_tag["dir"] = subdir
        with cd(dir_path):
            with os.popen('git config --get remote.origin.url') as pipe:
                repo = pipe.read()
                new_tag['repo'] = repo
            with os.popen('git symbolic-ref --short -q HEAD') as pipe:
                branch = pipe.read()
                print(branch)
                new_tag['branch'] = branch
            with os.popen('git rev-parse HEAD') as pipe:
                commit_id = pipe.read()
                print(commit_id)
                new_tag['commit'] = commit_id.replace('\n')
        projects.append(new_tag)

    with open(r"depends/repo.json", 'w') as save_f:
        repos['submodules'] = projects
        json.dump(repos, save_f, sort_keys=True, indent=4)
    print(json.dumps(repos, sort_keys=True, indent=4))

    os.system('git add depends/repo.json')
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
