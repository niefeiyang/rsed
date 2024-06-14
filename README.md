# Repo Search Engine Development Repository

## Quick Start

```shell
$ git clone https://github.com/niefeiyang/rsed.git
$ cd rsed
$ pip3 install pipreqs # Add all needed requirements.
```

You should add your own `.env` file and store the OpenAI API key.
```
API_KEY=sk-proj-123456789...
```

Then run the fastapi framework.
```shell
$ fastapi dev main.py
```

After that, visit `http://127.0.0.1:8000/`.

By pasting the repo url in the field and then submit, all the files in the repo will be downloaded, splitted and stored.
