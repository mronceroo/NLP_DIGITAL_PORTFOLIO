import whisper
import pyaudio
import numpy as np

model = whisper.load_model("medium")

CHUNK = 1024
FORMAT = pyaudio.paInt16  
CHANNELS = 1              
RATE = 16000              
RECORD_SECONDS = 5        

p = pyaudio.PyAudio()
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

print("Recording...")
frames = []
for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Record ended")
stream.stop_stream()
stream.close()
p.terminate()

audio_np = np.frombuffer(b''.join(frames), dtype=np.int16)
audio_np = audio_np.astype(np.float32) / 32768.0  # Normalize to [-1.0, 1.0]

result = model.transcribe(audio_np, language="en")
print("\nResult text:", result["text"])

#segments with timestamps
print("\nDetails:")
for segment in result["segments"]:
    print(f"[{segment['start']:.2f}s -> {segment['end']:.2f}s] {segment['text']}")