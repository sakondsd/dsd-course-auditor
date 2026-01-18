import os
import shutil
import time
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings 
from langchain_core.documents import Document 

PERSIST_DIRECTORY = "db_storage"
RULE_SEPARATOR = "--------------------"

def rebuild_knowledge_base(folder_path="knowledge_base"):
    if os.path.exists(PERSIST_DIRECTORY):
        try:
            shutil.rmtree(PERSIST_DIRECTORY)
            time.sleep(1)
        except: pass 

    documents = []
    if not os.path.exists(folder_path): os.makedirs(folder_path)
    
    files = os.listdir(folder_path)
    if not files: return "⚠️ ไม่พบไฟล์ใน knowledge_base"

    for f_name in files:
        f_path = os.path.join(folder_path, f_name)
        if f_name.endswith(".txt"):
            try:
                with open(f_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    rules = content.split(RULE_SEPARATOR)
                    for r in rules:
                        if r.strip():
                            documents.append(Document(page_content=r.strip(), metadata={"source": f_name}))
            except: pass 

    if not documents: return "❌ ไม่พบกฎที่อ่านได้"

    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_db = FAISS.from_documents(documents, embeddings)
        vector_db.save_local(PERSIST_DIRECTORY)
        return f"✅ จดจำกฎสำเร็จ: {len(documents)} ข้อ"
    except Exception as e:
        return f"Error: {str(e)}"

def search_rules(query):
    if not os.path.exists(PERSIST_DIRECTORY): return ""
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_db = FAISS.load_local(PERSIST_DIRECTORY, embeddings, allow_dangerous_deserialization=True)
        results = vector_db.similarity_search(query, k=10)
        if not results: return ""
        return "\n\n--------------------\n\n".join([doc.page_content for doc in results])
    except Exception as e:
        return ""