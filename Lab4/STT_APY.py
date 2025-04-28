import assemblyai as aai

aai.settings.api_key = "3bc98b278aee480c94f1c77834bf1556"

# audio_file = "./local_file.mp3"
audio_file = r"C:\Users\manue\OneDrive\Documentos\Universidad\NLP lunes\NLP_DIGITAL_PORTFOLIO\Lab4\elevenlabs_tts_output.mp3"

config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)

transcript = aai.Transcriber(config=config).transcribe(audio_file)

if transcript.status == "error":
  raise RuntimeError(f"Transcription failed: {transcript.error}")

print(transcript.text)