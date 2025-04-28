import requests
import os
import json

class WhisperSTT:
    def __init__(self, api_key=None):
        """
        Initialize the Whisper API client for speech-to-text.
        
        Args:
            api_key (str): Your OpenAI API key.
                          If None, uses OPENAI_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.api_url = "https://api.openai.com/v1/audio/transcriptions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def transcribe(self, audio_file_path, language=None, prompt=None):
        """
        Transcribe speech from an audio file using OpenAI's Whisper API.
        
        Args:
            audio_file_path (str): Path to the audio file to transcribe
            language (str, optional): Language code (e.g., "en", "es") 
            prompt (str, optional): Optional text to guide the transcription
            
        Returns:
            dict: The transcription result
        """
        try:
            # Check if file exists
            if not os.path.exists(audio_file_path):
                return {"error": f"File not found: {audio_file_path}"}
            
            # Prepare the form data
            form_data = {
                "model": "whisper-1",
                "response_format": "json"
            }
            
            # Add optional parameters if provided
            if language:
                form_data["language"] = language
            
            if prompt:
                form_data["prompt"] = prompt
            
            # Prepare the file
            with open(audio_file_path, "rb") as f:
                files = {
                    "file": (os.path.basename(audio_file_path), f, "audio/mpeg")
                }
                
                # Make the API request
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    data=form_data,
                    files=files
                )
            
            # Process the response
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"API request failed with status code {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {"error": str(e)}


# Example usage
if __name__ == "__main__":
    # Initialize the API client
    # Option 1: Use environment variable
    # export OPENAI_API_KEY="your-openai-api-key"
    # whisper = WhisperSTT()
    
    # Option 2: Provide API key directly
    whisper = WhisperSTT(api_key="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")
    
    # Transcribe an audio file
    result = whisper.transcribe(
        audio_file_path=r"C:\Users\manue\OneDrive\Documentos\Universidad\NLP lunes\NLP_DIGITAL_PORTFOLIO\Lab4\elevenlabs_tts_output.mp3",
        language="en",  # Optional: specify language
        prompt="This is a conversation about machine learning"  # Optional: context prompt
    )
    
    # Print the result
    if "error" not in result:
        print(f"Transcription: {result['text']}")
    else:
        print(f"Error: {result['error']}")