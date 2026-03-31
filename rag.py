import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

def process_pdf_to_faiss(pdf_path: str):
    print(f"📄 PDF işleniyor: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"✂️ Belge {len(chunks)} parçaya bölündü.")
    
    # DİKKAT: OpenAI yerine Google'ın ücretsiz Embedding modelini kullanıyoruz
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    
    print("🧠 Vektör veritabanı (FAISS) oluşturuluyor...")
    vector_db = FAISS.from_documents(chunks, embeddings)
    
    db_path = "data/vector_db"
    vector_db.save_local(db_path)
    print("✅ FAISS veritabanı başarıyla kaydedildi!")
    return True

def get_context_from_db(query: str, db_path: str = "data/vector_db"):
    # Aramayı da Google modeli ile yapıyoruz
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    vector_db = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
    
    results = vector_db.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in results])
    return context