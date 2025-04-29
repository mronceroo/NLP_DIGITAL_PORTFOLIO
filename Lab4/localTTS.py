from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import torch
from datasets import load_dataset
import sounddevice as sd
import os

# Cache configuration
CACHE_DIR = "tts_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# Load models
def load_models():
    processor = SpeechT5Processor.from_pretrained(
        "microsoft/speecht5_tts",
        cache_dir=os.path.join(CACHE_DIR, "models")
    )
    model = SpeechT5ForTextToSpeech.from_pretrained(
        "microsoft/speecht5_tts",
        cache_dir=os.path.join(CACHE_DIR, "models")
    )
    vocoder = SpeechT5HifiGan.from_pretrained(
        "microsoft/speecht5_hifigan",
        cache_dir=os.path.join(CACHE_DIR, "models")
    )
    return processor, model, vocoder

# Load embeddings
def load_embeddings():
    try:
        dataset = load_dataset(os.path.join(CACHE_DIR, "embeddings"))
    except:
        dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        dataset.save_to_disk(os.path.join(CACHE_DIR, "embeddings"))
    return dataset

# Execution
processor, model, vocoder = load_models()
dataset = load_embeddings()

# Device configuration
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
vocoder = vocoder.to(device)

# Text
text = "b two b three"
inputs = processor(text=text, return_tensors="pt").to(device)

# Obtain embeddings (index 7306 = femenine voice)
speaker_embeddings = torch.tensor(dataset[7306]["xvector"]).unsqueeze(0).to(device)

# Generate and reproduce audio
with torch.no_grad():
    audio = model.generate_speech(
        inputs["input_ids"],
        speaker_embeddings=speaker_embeddings,
        vocoder=vocoder
    )

# Reproduce directly
sd.play(audio.cpu().numpy(), samplerate=16000)
sd.wait()
print("Audio reproduction ended")