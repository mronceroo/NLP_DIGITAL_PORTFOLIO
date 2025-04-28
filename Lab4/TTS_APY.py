import requests
import json
import os
import time
from pydub import AudioSegment
from pydub.playback import play
import io

class ElevenLabsTextToSpeech:
    def __init__(self, api_key=None):
        """
        Initialize the ElevenLabs Text-to-Speech API client.
        
        Args:
            api_key (str): Your ElevenLabs API key.
                          If None, uses ELEVENLABS_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ElevenLabs API key is required")
        
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def list_voices(self):
        """
        List all available voices from ElevenLabs.
        
        Returns:
            list: Available voices
        """
        try:
            response = requests.get(
                f"{self.base_url}/voices",
                headers=self.headers
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("voices", [])
            else:
                print(f"Error listing voices: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"Error listing voices: {str(e)}")
            return []
    
    def get_default_voice_settings(self):
        """
        Get default voice settings from ElevenLabs.
        
        Returns:
            dict: Default voice settings
        """
        try:
            response = requests.get(
                f"{self.base_url}/voices/settings/default",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting default voice settings: {response.status_code} - {response.text}")
                return {}
                
        except Exception as e:
            print(f"Error getting default voice settings: {str(e)}")
            return {}
    
    def synthesize_speech(self, text, voice_id="21m00Tcm4TlvDq8ikWAM", 
                         output_file=None, stability=0.5, similarity_boost=0.75, 
                         style=0.0, use_speaker_boost=True, model_id="eleven_multilingual_v2"):
        """
        Convert text to speech using ElevenLabs API.
        
        Args:
            text (str): The text to convert to speech
            voice_id (str): The voice ID to use
            output_file (str): Path to save the audio file (optional)
            stability (float): Voice stability (0.0 to 1.0)
            similarity_boost (float): Voice similarity boost (0.0 to 1.0)
            style (float): Speaking style control (0.0 to 1.0)
            use_speaker_boost (bool): Whether to use speaker boost
            model_id (str): The TTS model to use
            
        Returns:
            bytes or str: Audio data as bytes if output_file is None,
                         otherwise the path to the saved file
        """
        try:
            # Prepare the request payload
            payload = {
                "text": text,
                "model_id": model_id,
                "voice_settings": {
                    "stability": stability,
                    "similarity_boost": similarity_boost,
                    "style": style,
                    "use_speaker_boost": use_speaker_boost
                }
            }
            
            # Make the API request
            response = requests.post(
                f"{self.base_url}/text-to-speech/{voice_id}",
                headers=self.headers,
                json=payload,
                stream=True
            )
            
            if response.status_code == 200:
                # Get audio content
                audio_content = response.content
                
                # Save to file if output_file is specified
                if output_file:
                    with open(output_file, "wb") as out:
                        out.write(audio_content)
                    print(f"Audio content written to file: {output_file}")
                    return output_file
                
                return audio_content
            else:
                print(f"Error synthesizing speech: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error synthesizing speech: {str(e)}")
            return None
    
    def synthesize_speech_with_streaming(self, text, voice_id="21m00Tcm4TlvDq8ikWAM", 
                                       output_file=None, stability=0.5, similarity_boost=0.75, 
                                       style=0.0, use_speaker_boost=True, model_id="eleven_multilingual_v2",
                                       chunk_callback=None):
        """
        Convert text to speech using ElevenLabs API with streaming for real-time audio output.
        
        Args:
            text (str): The text to convert to speech
            voice_id (str): The voice ID to use
            output_file (str): Path to save the audio file (optional)
            stability (float): Voice stability (0.0 to 1.0)
            similarity_boost (float): Voice similarity boost (0.0 to 1.0)
            style (float): Speaking style control (0.0 to 1.0)
            use_speaker_boost (bool): Whether to use speaker boost
            model_id (str): The TTS model to use
            chunk_callback (callable): Optional callback function to receive audio chunks
            
        Returns:
            bytes or str: Complete audio data as bytes if output_file is None,
                         otherwise the path to the saved file
        """
        try:
            # Prepare the request payload
            payload = {
                "text": text,
                "model_id": model_id,
                "voice_settings": {
                    "stability": stability,
                    "similarity_boost": similarity_boost,
                    "style": style,
                    "use_speaker_boost": use_speaker_boost
                }
            }
            
            # Set headers for streaming
            streaming_headers = self.headers.copy()
            streaming_headers["Accept"] = "audio/mpeg"
            
            # Make the API request with streaming
            response = requests.post(
                f"{self.base_url}/text-to-speech/{voice_id}/stream",
                headers=streaming_headers,
                json=payload,
                stream=True
            )
            
            if response.status_code == 200:
                # Buffer for all audio data
                all_audio_data = io.BytesIO()
                
                # Process the streaming response
                for chunk in response.iter_content(chunk_size=4096):
                    if chunk:
                        # Append to overall buffer
                        all_audio_data.write(chunk)
                        
                        # Call callback if provided
                        if chunk_callback and callable(chunk_callback):
                            chunk_callback(chunk)
                
                # Get complete audio content
                all_audio_data.seek(0)
                audio_content = all_audio_data.read()
                
                # Save to file if output_file is specified
                if output_file:
                    with open(output_file, "wb") as out:
                        out.write(audio_content)
                    print(f"Audio content written to file: {output_file}")
                    return output_file
                
                return audio_content
            else:
                print(f"Error synthesizing speech: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error synthesizing speech: {str(e)}")
            return None
    
    def play_audio(self, audio_data=None, audio_file=None):
        """
        Play the synthesized audio.
        
        Args:
            audio_data (bytes): Audio data as bytes
            audio_file (str): Path to audio file
        """
        try:
            if audio_data:
                # Load audio from bytes
                audio = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
            elif audio_file:
                # Load audio from file
                audio = AudioSegment.from_file(audio_file)
            else:
                raise ValueError("Either audio_data or audio_file must be provided")
            
            # Play the audio
            play(audio)
            
        except Exception as e:
            print(f"Error playing audio: {str(e)}")
    
    def get_voice_by_name(self, voice_name):
        """
        Find a voice by name (partial match) from the available voices.
        
        Args:
            voice_name (str): Name of the voice to find
            
        Returns:
            dict: Voice information including ID if found, None otherwise
        """
        try:
            voices = self.list_voices()
            
            # Search for voice by name (case-insensitive partial match)
            voice_name_lower = voice_name.lower()
            for voice in voices:
                if voice_name_lower in voice.get("name", "").lower():
                    return voice
            
            return None
            
        except Exception as e:
            print(f"Error finding voice: {str(e)}")
            return None


# Example usage
if __name__ == "__main__":
    # Initialize the API client with your ElevenLabs API key
    api_key = "sk_c8be39d0f62a8673b75b988a2432beec3aec896bd5ef0ce5"  # Replace with your actual API key
    tts = ElevenLabsTextToSpeech(api_key=api_key)
    
    # Example 1: List available voices
    voices = tts.list_voices()
    print(f"Found {len(voices)} voices:")
    for i, voice in enumerate(voices[:5]):  # Print first 5 voices
        print(f"{i+1}. {voice['name']} (ID: {voice['voice_id']})")
    
    # Example 2: Find a voice by name
    voice = tts.get_voice_by_name("Rachel")
    voice_id = voice["voice_id"] if voice else "21m00Tcm4TlvDq8ikWAM"  # Default voice if not found
    
    # Example 3: Convert text to speech and save to file
    text = "The movement you have to do is b two b three"
    output_file = "elevenlabs_tts_output.mp3"
    
    tts.synthesize_speech(
        text=text,
        voice_id=voice_id,
        output_file=output_file,
        stability=0.7,
        similarity_boost=0.7
    )
    