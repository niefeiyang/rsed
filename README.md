# Repo Search Engine Development Repository

## Modular Development
### Module:rsed/cmdb: Chromadb File Retrieval and Vectorization
|-> rsed/cmdb/main.py

#### Usage Instructions:

```shell
$ pip install chromadb argparse
```

A demo application for RSE vector embedding & querry. The program has two mandatory parameters. First is the git repository address, and second is a brief description of the target file.

**Example:**

```shell
$ python main.py https://github.com/lektor/lektor.git "The file related to package name."
```
