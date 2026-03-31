# 🩺 Multi-Modal RAG-Based Intelligent Medical Assistant (MedAssist AI)

An end-to-end artificial intelligence project combining image processing (Computer Vision) and Large Language Models (LLM) in a single architecture. This system goes beyond consuming readily available APIs, integrating a specially trained deep learning model (CNN) into a modern RAG (Retrieval-Augmented Generation) pipeline.

## 🚀 How Does the System Work?

1. **Image Processing (Vision):** The patient's X-ray is analyzed by the specially trained CNN model, and a radiological finding (e.g., risk of pneumonia) is mathematically calculated.
2. **Information Retrieval (RAG):** The patient's past medical reports (PDF) are processed using a FAISS vector database, and relevant texts are extracted. 
3. **Learning and Intelligent Interpretation (LLM):** Scores from the image and patient history from the PDF are combined using LangChain and Gemini infrastructure to provide the doctor with a supporting preliminary assessment.

## 💡 Featured Feature: Hallucination Control & Security

To prevent "hallucinations" (fabrications), the biggest problem with AI systems, rigorous Prompt Engineering has been applied to the system. The system doesn't just combine incoming data, it establishes logic: For example, even if the X-ray model detects a high probability of "Pneumonia," if the user accidentally uploads a resume (CV) instead of a medical report, the LLM will instantly detect this discrepancy. Instead of blindly making a diagnosis, it stops the process and warns the user with a *"System Alert: The uploaded document is not a medical report, there is a data discrepancy."*

## 🛠️ Technology Stack
* **Backend:** FastAPI
* **Frontend:** Streamlit
* **Machine Learning:** Python, TensorFlow, Keras (CNN Model)
* **NLP & LLM:** LangChain, FAISS, Prompt Engineering, Google Gemini 1.5 Flash

## 💻 Setup and Run

To test the project on your own computer, you can follow these steps:

**1. Clone the repository:**
git clone [https://github.com/mustafa-alpergun/MultiModal-MedAssist.git](https://github.com/mustafa-alpergun/MultiModal-MedAssist.git)
cd MultiModal-MedAssist

2. Install the necessary libraries:
pip install -r requirements.txt

3. Set the environment variables:
Create a .env file in the project's main directory and add your Google API key:
GOOGLE_API_KEY=your_api_key_here

4. Start the FastAPI Server:
uvicorn main:app --reload

5. Start the Streamlit Interface (in a new terminal):
streamlit run frontend.py
TÜRKÇE (Turkish)
🩺 Multi-Modal RAG Tabanlı Akıllı Tıbbi Asistan (MedAssist AI)
Görüntü işleme (Computer Vision) ve Büyük Dil Modellerini (LLM) tek bir mimaride birleştiren uçtan uca (end-to-end) yapay zeka projesi. Bu sistem, hazır API'ler tüketmenin ötesine geçerek, özel eğitilmiş bir derin öğrenme modelini (CNN) modern bir RAG (Retrieval-Augmented Generation) boru hattına entegre etmektedir.

🚀 Sistem Nasıl Çalışıyor?
Görüntü İşleme (Vision): Hastanın X-Ray röntgeni, özel olarak eğitilmiş CNN modeli tarafından analiz edilir ve radyolojik bir bulgu (örn: Pnömoni/Zatürre riski) matematiksel olarak hesaplanır.

Bilgi Getirimi (RAG): Hastanın geçmiş tıbbi raporları (PDF), FAISS vektör veritabanı kullanılarak işlenir ve ilgili metinler çıkarılır.

Akıllı Yorumlama (LLM): Görüntüden gelen skorlar ve PDF'ten gelen hasta geçmişi, LangChain ve Gemini altyapısı ile harmanlanarak doktora destekleyici bir ön değerlendirme sunulur.

💡 Öne Çıkan Özellik: Halüsinasyon Kontrolü & Güvenlik
Yapay zeka sistemlerinin en büyük sorunu olan "halüsinasyon" (uydurma) durumunu engellemek için sisteme sıkı bir Prompt Engineering uygulandı. Sistem sadece gelen veriyi birleştirmez, mantık kurar: Örneğin; röntgen modeli yüksek oranda "Zatürre" tespit etse bile, kullanıcı yanlışlıkla tıbbi rapor yerine bir özgeçmiş (CV) yüklerse, LLM bu tutarsızlığı anında yakalar. Körü körüne teşhis koymak yerine süreci durdurup, "Sistem Uyarısı: Yüklenen belge tıbbi bir rapor değildir, veri uyumsuzluğu var" diyerek kullanıcıyı uyarır.

🛠️ Teknoloji Yığını
Backend: FastAPI

Frontend: Streamlit

Makine Öğrenmesi: Python, TensorFlow, Keras (CNN Modeli)

NLP & LLM: LangChain, FAISS, Prompt Engineering, Google Gemini 1.5 Flash

💻 Kurulum ve Çalıştırma
Projeyi kendi bilgisayarınızda test etmek için aşağıdaki adımları izleyebilirsiniz:

1. Depoyu klonlayın:
git clone [https://github.com/mustafa-alpergun/MultiModal-MedAssist.git](https://github.com/mustafa-alpergun/MultiModal-MedAssist.git)
cd MultiModal-MedAssist

2. Gerekli kütüphaneleri yükleyin:
pip install -r requirements.txt

3. Çevresel değişkenleri ayarlayın:
Proje ana dizininde bir .env dosyası oluşturun ve Google API anahtarınızı ekleyin:
GOOGLE_API_KEY=sizin_api_anahtariniz_buraya

4. FastAPI Sunucusunu Başlatın:
uvicorn main:app --reload

5. Streamlit Arayüzünü Başlatın (Yeni bir terminalde):
streamlit run frontend.py
