import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

def generate_medical_insight(query: str, vision_result: dict, text_context: str):
    print("🧠 LLM (Beyin) verileri birleştiriyor ve düşünüyor...")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "⚠️ HATA: .env dosyasında GOOGLE_API_KEY bulunamadı."
        
    # DİKKAT: OpenAI yerine Gemini 1.5 Flash (hızlı ve ücretsiz) modelini kullanıyoruz
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)
    
    system_template = """
        Sen profesyonel ve son derece dikkatli bir Tıbbi Yapay Zeka Asistanısın. 
        Görevin, doktorun sorusunu, X-Ray görüntü analizini ve hastanın geçmiş PDF raporunu inceleyerek doktora bir ön değerlendirme sunmaktır.

        KESİN KURALLAR (BUNLARA HARFİYEN UYACAKSIN):
        1. TUTARLILIK KONTROLÜ: Önce 'GEÇMİŞ RAPORLAR' olarak verilen metni oku. Eğer bu metin tıbbi bir belge değilse (örneğin bir özgeçmiş/CV, yazılım projesi, alakasız bir makale veya rastgele kelimeler ise), radyoloji analizi ne derse desin KESİNLİKLE teşhis koyma veya bu verileri birleştirmeye çalışma!
        2. UYARI MEKANİZMASI: Eğer 1. maddedeki gibi bir uyumsuzluk (örn: CV yüklenmesi) fark edersen, raporuna tam olarak şu uyarıyı yazarak başla: "⚠️ SİSTEM UYARISI: Yüklenen PDF belgesi bir tıbbi rapor veya hasta geçmişi değildir (İçerik bir özgeçmiş/alakasız metin gibi görünüyor). Radyoloji modelimiz bir bulgu tespit etmiş olsa da, yanlış veri girişi nedeniyle güvenilir bir tıbbi analiz yapılamamaktadır. Lütfen doğru hasta dosyasını yükleyin."
        3. TIBBİ SINIRLAR: Eğer belgeler gerçekten tıbbi ise, sadece belgelerde yazanları özetle. Kendi kendine yeni bir hastalık uydurma.
        4. DİL: Yanıtın her zaman profesyonel ve net olmalıdır.
        
    --- GÖRÜNTÜ İŞLEME (CNN/VISION) SONUCU ---
    {vision_data}
    
    --- GEÇMİŞ RAPORLAR (RAG / PDF CONTEXT) ---
    {context_data}
    """
    
    human_template = "Doktorun Sorusu: {user_query}"
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", human_template)
    ])
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({
            "vision_data": str(vision_result),
            "context_data": text_context,
            "user_query": query
        })
        return response.content
    except Exception as e:
        return f"❌ LLM Yanıt Üretemedi: {str(e)}"