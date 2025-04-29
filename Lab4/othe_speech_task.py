import whisper
from transformers import pipeline

model_whisper = whisper.load_model("medium") 

result = model_whisper.transcribe(r"C:\Users\manue\OneDrive\Documentos\Universidad\NLP lunes\NLP_DIGITAL_PORTFOLIO\elevenlabs_tts_output.mp3", task="transcribe", language="en")
texto_en = result["text"]

traductor = pipeline("translation_en_to_es", model="Helsinki-NLP/opus-mt-en-es")
texto_es = traductor(texto_en)[0]["translation_text"]

print("English text:", texto_en)
print("Spanish Text:", texto_es)