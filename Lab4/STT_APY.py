import requests
import json
import os
import time
from pydub import AudioSegment
import io
import base64

class ElevenLabsSpeechToText:
    def __init__(self, api_key=None):
        """
        Initialize the ElevenLabs Speech-to-Text API client.
        
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
    
    def upload_audio(self, audio_file_path):
        """
        Upload audio file to ElevenLabs for transcription.
        
        Args:
            audio_file_path (str): Path to the audio file to transcribe
            
        Returns:
            str: The audio ID if successful, None otherwise
        """
        try:
            # Check file exists
            if not os.path.exists(audio_file_path):
                raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
            
            # Read audio file
            with open(audio_file_path, "rb") as file:
                file_data = file.read()
            
            # Prepare for upload
            upload_url = f"{self.base_url}/speech-to-text/audio-transcription"
            upload_headers = {
                "xi-api-key": self.api_key,
            }
            
            # Determine the file format based on extension
            file_extension = os.path.splitext(audio_file_path)[1].lower()
            
            # Create files object
            files = {
                "file": (os.path.basename(audio_file_path), file_data, 
                         f"audio/{file_extension[1:]}" if file_extension in ['.mp3', '.wav', '.ogg', '.m4a'] 
                         else "audio/mpeg")
            }
            
            # Upload the file
            response = requests.post(
                upload_url,
                headers=upload_headers,
                files=files
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("audio_id")
            else:
                print(f"Error uploading audio: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error uploading audio: {str(e)}")
            return None
    
    def get_transcription(self, audio_id, language="en", transcription_type="default"):
        """
        Get the transcription of an uploaded audio file.
        
        Args:
            audio_id (str): The ID of the uploaded audio
            language (str): The language code (e.g., "en", "es") 
            transcription_type (str): The type of transcription ("default" or "verbose")
            
        Returns:
            dict: The transcription result
        """
        try:
            # Endpoint for transcription
            transcription_url = f"{self.base_url}/speech-to-text/transcriptions/{audio_id}"
            
            # Parameters for the transcription
            params = {
                "language": language,
                "transcription_type": transcription_type
            }
            
            # Send request
            response = requests.get(
                transcription_url,
                headers=self.headers,
                params=params
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 202:
                # Transcription is still processing
                print("Transcription is still processing. Waiting...")
                time.sleep(2)
                return self.get_transcription(audio_id, language, transcription_type)
            else:
                print(f"Error getting transcription: {response.status_code} - {response.text}")
                return {"error": response.text}
                
        except Exception as e:
            print(f"Error getting transcription: {str(e)}")
            return {"error": str(e)}
    
    def transcribe_audio(self, audio_file_path, language="en", transcription_type="default"):
        """
        Complete process to transcribe an audio file.
        
        Args:
            audio_file_path (str): Path to the audio file to transcribe
            language (str): The language code (e.g., "en", "es")
            transcription_type (str): The type of transcription ("default" or "verbose")
            
        Returns:
            dict: The transcription result
        """
        # Upload the audio file
        audio_id = self.upload_audio(audio_file_path)
        if not audio_id:
            return {"error": "Failed to upload audio file"}
        
        # Wait for a moment to ensure processing has started
        time.sleep(1)
        
        # Get the transcription
        return self.get_transcription(audio_id, language, transcription_type)
    
    def convert_audio_format(self, input_file, output_format="mp3"):
        """
        Convert audio to a format supported by ElevenLabs.
        
        Args:
            input_file (str): Path to the input audio file
            output_format (str): Desired output format (mp3, wav, ogg)
            
        Returns:
            str: Path to the converted file
        """
        try:
            # Load the audio
            audio = AudioSegment.from_file(input_file)
            
            # Create output filename
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}.{output_format}"
            
            # Export in the desired format
            audio.export(output_file, format=output_format)
            
            return output_file
            
        except Exception as e:
            print(f"Error converting audio format: {str(e)}")
            return None


# Example usage
if __name__ == "__main__":
    # Initialize the API client with your ElevenLabs API key
    api_key = "sk_c8be39d0f62a8673b75b988a2432beec3aec896bd5ef0ce5"  # Replace with your actual API key
    stt = ElevenLabsSpeechToText(api_key=api_key)
    
    # Example 1: Convert an audio file to a supported format if needed
    original_audio = "elevenlabs_tts_output.mp3"
    converted_audio = stt.convert_audio_format(original_audio, "mp3")
    
    # Example 2: Transcribe the audio file
    result = stt.transcribe_audio(
        audio_file_path=converted_audio or original_audio,
        language="en",
        transcription_type="default"  # Use "verbose" for more detailed output
    )
    
    # Print the result
    if "error" not in result:
        print("Transcription completed successfully:")
        if "text" in result:
            print(f"Text: {result['text']}")
        else:
            print(result)
    else:
        print(f"Error: {result['error']}")