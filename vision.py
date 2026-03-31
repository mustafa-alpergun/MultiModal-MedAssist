import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Senin eğittiğin gerçek modelin yolu
MODEL_PATH = "models/pnomoni_model.h5"

print("🧠 CNN Modeli yükleniyor, lütfen bekleyin...")
if os.path.exists(MODEL_PATH):
    try:
        model = load_model(MODEL_PATH)
        print("✅ Model başarıyla yüklendi!")
    except Exception as e:
        model = None
        print(f"⚠️ DİKKAT: Model yüklenirken hata oluştu: {e}")
else:
    model = None
    print("⚠️ DİKKAT: Model dosyası bulunamadı!")

def analyze_xray(image_path: str):
    if model is None:
        return {
            "radyolojik_bulgu": "HATA: Gerçek model (pnomoni_model.h5) yüklenemedi.",
            "yapay_zeka_guven_skoru": "%0",
            "not": "Sistemde model dosyası eksik veya hatalı."
        }

    try:
        # 1. Görüntüyü senin modelinin eğitime girdiği boyuta getiriyoruz.
        # DİKKAT: Eğer resimleri eğitirken 150x150 veya başka bir boyut kullandıysan,
        # buradaki (224, 224) sayılarını KESİNLİKLE ona göre değiştirmelisin!
        img = image.load_img(image_path, target_size=(224, 224))
        
        # 2. Görüntüyü yapay zekanın anlayacağı sayılara (matrislere) çevir
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0 # Pikselleri 0-1 arasına çekme (Normalizasyon)
        
        # 3. GERÇEK TAHMİNİ YAP! (İşte sihir burada gerçekleşiyor)
        prediction = model.predict(img_array)
        score = float(prediction[0][0])
        
        # 4. Sonucu Yorumla
        # Eğer modelin Binary (tek çıktı) ise: genelde 0.5 üstü Zatürre, altı Sağlıklı olur.
        if score > 0.5:
            durum = "Zatürre (Pneumonia) bulgusu tespit edildi."
            guven = f"%{int(score * 100)}"
        else:
            durum = "Akciğerler sağlıklı görünmektedir (Zatürre bulgusuna rastlanmadı)."
            guven = f"%{int((1 - score) * 100)}"
            
        return {
            "radyolojik_bulgu": durum,
            "yapay_zeka_guven_skoru": guven,
            "not": "Bu analiz, yüklenen görüntünün özel CNN modeli ile işlenmesi sonucu elde edilmiştir."
        }
        
    except Exception as e:
        return {
            "radyolojik_bulgu": f"Görüntü işleme hatası: {str(e)}",
            "yapay_zeka_guven_skoru": "%0",
            "not": "Analiz sırasında teknik bir hata oluştu."
        }