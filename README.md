# Repo Search Engine Development Repository

## Quick Start

1. Clone the rsed Repository
```shell
$ git clone https://github.com/niefeiyang/rsed.git
```

2. Create a python virtual environment
```shell
$ python -m venv rsed #Create a virtual environment for repo rsed
```

3. Activate the virtual environment:

On Unix:
```shell
$ cd rsed
$ source bin/activate #Activate the virtual environment
```

On Windows:
```
$ cd rsed
$ Scripts\activate
```

3. Install dependencies
```
$ pip3 install -r requirements.txt #Add all needed requirements.
```

4. Add your own `.env` file and store the OpenAI API key.
```
API_KEY=sk-proj-123456789...
```

5. Run the fastapi framework.
```shell
$ fastapi dev main.py
```

After that, visit `http://127.0.0.1:8000/`.

By pasting the repo url in the field and then submit, all the files in the repo will be downloaded, splitted and stored.

Then, you can ask the question.
