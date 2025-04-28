from openai import OpenAI

client = OpenAI()
audio_file= open(r"C:\Users\manue\OneDrive\Documentos\Universidad\NLP lunes\NLP_DIGITAL_PORTFOLIO\elevenlabs_tts_output.mp3", "rb")

transcription = client.audio.transcriptions.create(
    model="gpt-4o-transcribe", 
    file=audio_file
)

print(transcription.text)