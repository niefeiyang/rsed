import os
import chromadb
import hashlib
import json
import time
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
from dotenv import load_dotenv

load_dotenv()

openai_ef = OpenAIEmbeddingFunction(
    api_key = os.getenv("API_KEY"),
    model_name="text-embedding-3-large"
)

#print(os.getnev("API_KEY"))
#print("API_KEY")

# 初始化ChromaDB客户端
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="python_code_collection", embedding_function=openai_ef)

# 初始化splitter
splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, chunk_size=1800, chunk_overlap=0
)

def get_python_files(directory):
    """获取指定目录下的所有Python文件"""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
                #print(f"{root}:{file}")
    return python_files

def read_file(file_path):
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def split_and_store_files(directory):
    python_files = get_python_files(directory)
    documents = []
    ids = []

    for file_path in python_files:
        print(file_path)
        absolute_path = os.path.abspath(file_path)  # 获取jidui路径
        print(absolute_path)
        file_content = read_file(file_path)
        hash_content = absolute_path + file_content
        file_hash = hashlib.md5(hash_content.encode()).hexdigest()
        split_docs = splitter.create_documents([file_content])
        split_docs 
        for idx, doc in enumerate(split_docs):
                #print(dir(doc))
            documents.append(doc.page_content)
            ids.append(f"{os.path.basename(absolute_path)}_{idx}_{file_hash}")
            print(f"{os.path.basename(absolute_path)}_{idx}_{file_hash}")

    collection.upsert(documents=documents, ids=ids)

def query_chromadb(query, n_results=3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        #include=["uris","distances"]
        include=["uris","documents","distances"]
    )
    return results

def chromayixia(ask):
    results = query_chromadb(ask)
    print(json.dumps(results, indent=4))

# 示例用法
if __name__ == "__main__":
    directory = "./torch-mlir"  # 替换为你的目录路径
    split_and_store_files(directory)
    
    # 查询示例
    #query = "What is the function to change package name"
    #results = query_chromadb(query)
    #print(results)
    time.sleep(2)
    print("好了，现在文件已经切好，openai已经处理好embedding了")
    time.sleep(3)
    print("让我们试试看！")
    time.sleep(2)
