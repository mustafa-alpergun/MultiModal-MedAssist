import google.generativeai as genai

# API şifreni buraya gir
api_key = "AIzaSyCbMTg5kLPwiy7UDGhkm-AcOueAnq7-oM8"
genai.configure(api_key=api_key)

print("\n--- SENİN API ANAHTARINLA ÇALIŞAN LLM MODELLERİ ---")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)