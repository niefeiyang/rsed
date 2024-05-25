import os
import chromadb
import argparse
import subprocess

parser = argparse.ArgumentParser(description="Demo Module: cmdb.main.py")

parser.add_argument("repo_url", type=str, help="Git Repo Link")
parser.add_argument("description", type=str, help="Your Description")
args = parser.parse_args()

if not args.repo_url:
        parser.error("param1 void")
if not args.description:
        parser.error("param2 void")

try:
    #gitclone
    print("------cloning git repository------")
    subprocess.run(['git', 'clone', args.repo_url])
    print("Repository cloned successfully.")
except Exception as e:
        print("Error:",e)

# 获取克隆的仓库文件夹名
repo_folder_name = args.repo_url.split('/')[-1].replace('.git', '')
# 构建克隆的仓库文件夹路径
repo_folder_path = os.path.join(os.getcwd(), repo_folder_name)

# 初始化 ChromaDB 客户端
chroma_client = chromadb.Client()
collection_name = "my_collection"

def dir_spider(folder_path):
    # 获取文件夹下的所有文件
    files = os.listdir(folder_path)
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            # 读取文件内容
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    document_text = file.read()
            #剔除非文本文件
            except UnicodeDecodeError:
                    print(f"Non-Text-Based file: {file_path}")
                    continue
            # 使用文件名（包含后缀哦）作为文档的 ID
            document_id = file_name
            # 将文档存入 ChromaDB 数据库
            insert_document(document_id, document_text)
        if os.path.isdir(file_path):
            dir_spider(file_path)

def insert_document(document_id, document_text):
    # 获取集合，如果不存在则创建
    collection = chroma_client.get_or_create_collection(name=collection_name)
    # 将文档插入集合
    collection.upsert(documents=[document_text], ids=[document_id])

def insert_documents_from_folder(folder_path):
    dir_spider(folder_path)
    # 返回查询结果
    return query_collection()

def query_collection():
    # 获取集合
    collection = chroma_client.get_or_create_collection(name=collection_name)
    # 查询集合
    results = collection.query(
        query_texts=[args.description],
        n_results=5
    )
    return results

query_results = insert_documents_from_folder(repo_folder_path)

print(query_results["ids"])

