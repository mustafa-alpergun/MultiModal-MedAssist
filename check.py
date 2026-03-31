import google.generativeai as genai

# API şifreni buraya gir
api_key = "google api key"
genai.configure(api_key=api_key)

print("\n--- SENİN API ANAHTARINLA ÇALIŞAN LLM MODELLERİ ---")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
