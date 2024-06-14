import os
import chromadb
import hashlib
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

# 初始化ChromaDB客户端&Splitter
chroma_client = chromadb.PersistentClient(path="./ChromaDB")
#chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="python_code_collection", embedding_function=openai_ef)

splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, chunk_size=8000, chunk_overlap=0
)

def get_python_files(directory):
    """获取指定目录下的所有Python文件"""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files

def read_file(file_path):
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def split_and_store_files(directory: str):
    python_files = get_python_files(directory)
    documents = []
    ids = []

    for file_path in python_files:
        print(file_path)
        absolute_path = os.path.abspath(file_path)  # 获取绝对路径
        print(absolute_path)
        file_content = read_file(file_path)
        hash_content = absolute_path + file_content
        file_hash = hashlib.md5(hash_content.encode()).hexdigest()
        split_docs = splitter.create_documents([file_content])
        split_docs
        for idx, doc in enumerate(split_docs):
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
