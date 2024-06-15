import subprocess
import os

def repo_clone(repo_url: str) -> str:
    try:
        print("=====Cloning Git Repository=====")
        subprocess.run(['git', 'clone', repo_url])
        print("=====Repository Cloned=====")
    except Exception as e:
        print("Clone Error:",e)

    return os.path.join(os.getcwd(), repo_url.split('/')[-1].replace('.git', '')
)
