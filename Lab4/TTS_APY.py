from elevenlabs import ElevenLabs
client = ElevenLabs(
    api_key="",
)

audio_generator = client.text_to_speech.convert(
    voice_id="9BWtsMINqrJLrRacOk9x",
    output_format="mp3_44100_128",
    text="The movement you have to do is B2B3",
    model_id="eleven_multilingual_v2",
)

audio_data = b"".join(chunk for chunk in audio_generator)

with open("output_audio.mp3", "wb") as f:
    f.write(audio_data)
