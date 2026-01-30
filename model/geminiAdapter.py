from google import genai

class GeminiAdapter:
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.connectToClient()
    
    def connectToClient(self):
        try:
            self.client = genai.Client(api_key=self.api_key)
        except Exception as e:
            print(f"Connection error: {e}")

    def generate_text(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Error generating text: {e}")
            return None