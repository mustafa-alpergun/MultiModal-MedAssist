import streamlit as st
import requests

# Sayfa Ayarları (Sekme adı ve ikonu)
st.set_page_config(page_title="Medical AI Assistant", page_icon="🩺", layout="centered")

# Ana Başlık ve Açıklama
st.title("🩺 Akıllı Tıbbi Asistan")
st.markdown("Bu sistem, hastanın X-Ray görüntüsünü ve geçmiş raporlarını (PDF) analiz ederek doktora yardımcı bir ön değerlendirme sunar.")
st.divider()

# Kullanıcı Giriş Alanları
query = st.text_input("Doktorun Sorusu veya Notu:", placeholder="Örn: Hastanın röntgenini ve geçmişini değerlendirir misiniz?")

col1, col2 = st.columns(2)

with col1:
    image_file = st.file_uploader("Röntgen Görüntüsü Yükle", type=["png", "jpg", "jpeg"])
    if image_file:
        st.image(image_file, caption="Yüklenen Röntgen", use_container_width=True)

with col2:
    pdf_file = st.file_uploader("Geçmiş Raporu Yükle (PDF)", type=["pdf"])
    if pdf_file:
        st.success(f"{pdf_file.name} başarıyla yüklendi.")

st.divider()

# Analiz Butonu ve İşlem
if st.button("🚀 Verileri Analiz Et", use_container_width=True):
    # Dosya Kontrolü
    if not query:
        st.warning("Lütfen asistan için bir soru yazın.")
    elif not image_file or not pdf_file:
        st.warning("Lütfen hem röntgen görüntüsünü hem de geçmiş raporu (PDF) eksiksiz yükleyin.")
    else:
        # Backend'e (FastAPI) İstek Atma
        with st.spinner("Yapay zeka verileri inceliyor, lütfen bekleyin..."):
            try:
                # FastAPI sunucumuzun adresi (Arka planda uvicorn ile çalışan)
                url = "http://127.0.0.1:8000/analyze"
                
                # Dosyaları API'nin istediği formata çeviriyoruz
                files = {
                    "image_file": (image_file.name, image_file.getvalue(), image_file.type),
                    "pdf_file": (pdf_file.name, pdf_file.getvalue(), pdf_file.type)
                }
                data = {"query": query}
                
                # İsteği Gönder
                response = requests.post(url, data=data, files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if "hata" in result:
                        st.error(result["hata"])
                    else:
                        st.success("Analiz Tamamlandı!")
                        
                        # Sonuçları Şık Bir Şekilde Gösterme
                        st.subheader("🤖 Yapay Zeka Değerlendirmesi")
                        st.info(result.get("yapay_zeka_doktor_yorumu", "Yorum bulunamadı."))
                        
                        with st.expander("Görüntü İşleme (Vision) Detayları"):
                            st.json(result.get("radyoloji_analizi", {}))
                            
                        with st.expander("Geçmiş Rapor (RAG) Detayları"):
                            st.text(result.get("pdf_bulgulari_ozeti", "PDF detayı bulunamadı."))
                            
                else:
                    st.error(f"Sunucu Hatası: {response.status_code}")
                    
            except Exception as e:
                st.error(f"Bağlantı Hatası: Sunucunun (FastAPI) çalıştığından emin olun. Detay: {e}")