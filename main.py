from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os

# Kendi yazdığımız Yapay Zeka modüllerini projeye dahil ediyoruz
from vision import analyze_xray
from rag import process_pdf_to_faiss, get_context_from_db
from llm import generate_medical_insight

os.environ["GOOGLE_API_KEY"] = "AIzaSyCbMTg5kLPwiy7UDGhkm-AcOueAnq7-oM8"

# ... kodun geri kalanı aynı şekilde devam edecek ...

app = FastAPI(
    title="Medical Insight Assistant API",
    description="Multi-modal RAG sistemi için Backend",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"mesaj": "Medical RAG API çalışıyor! Sisteme hoş geldin."}

# DİKKAT: Artık sadece metin değil, Dosya (Resim ve PDF) kabul ediyoruz
@app.post("/analyze")
async def analyze_medical_data(
    query: str = Form(..., description="Doktorun hastayla ilgili sorusu"),
    image_file: UploadFile = File(..., description="Hastanın Röntgen (X-Ray) Görüntüsü"),
    pdf_file: UploadFile = File(..., description="Hastanın Geçmiş Tıbbi Raporu (PDF)")
):
    try:
        if image_file.filename == "" or pdf_file.filename == "":
            return {"hata": "Lütfen hem röntgen görüntüsünü hem de geçmiş tıbbi raporu (PDF) eksiksiz yükleyin."}
        
        # 1. ADIM: Gelen dosyaları sunucuya geçici olarak kaydet
        image_path = f"data/uploads/{image_file.filename}"
        pdf_path = f"data/uploads/{pdf_file.filename}"
        
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)
            
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(pdf_file.file, buffer)
            
        # 2. ADIM: Görüntü İşleme (Vision) Boru Hattını Çalıştır
        vision_result = analyze_xray(image_path)
        
        # 3. ADIM: RAG (Metin) Boru Hattını Çalıştır
        process_pdf_to_faiss(pdf_path) # PDF'i FAISS'e kaydet
        context = get_context_from_db(query) # Soruyu sor ve en alakalı paragrafları çek
        
        # 4. ADIM: Beyin (LLM) Boru Hattını Çalıştır ve Birleştir
        final_answer = generate_medical_insight(query, vision_result, context)
        
        # 5. ADIM: Sonucu Frontend'e (veya kullanıcıya) temiz bir JSON olarak dön
        return {
            "islem_durumu": "Başarılı",
            "soru": query,
            "radyoloji_analizi": vision_result,
            "pdf_bulgulari_ozeti": context,
            "yapay_zeka_doktor_yorumu": final_answer
        }
        
    except Exception as e:
        return {"hata": f"Sistem bir hata ile karşılaştı: {str(e)}"}