from google import genai
from google.genai import types
import os

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
            # Try common response attributes; fallback to string
            return getattr(response, "text", None) or getattr(response, "output_text", None) or str(response)
        except Exception as e:
            print(f"Error generating text: {e}")
            return None

    def generate_from_image(self, image_path: str, prompt: str = "") -> str:
        if not os.path.isfile(image_path):
            print(f"Image not found: {image_path}")
            return None

        try:
            # 1. Leer los bytes de la imagen
            with open(image_path, "rb") as f:
                img_bytes = f.read()

            # 2. Determinar el MIME type (ej: 'image/jpeg' o 'image/png')
            # Puedes usar imghdr como tenías o algo más simple:
            ext = os.path.splitext(image_path)[1].lower().replace(".", "")
            mime_type = f"image/{ext}" if ext != "jpg" else "image/jpeg"

            # 3. Crear el objeto de contenido CORRECTO (Multimodal)
            # En lugar de Base64 en el texto, usamos objetos de la API
            contents = [
                types.Part.from_bytes(data=img_bytes, mime_type=mime_type),
                prompt
            ]

            response = self.client.models.generate_content(
                model=self.model,
                contents=contents
            )
            
            return response.text

        except Exception as e:
            if "429" in str(e):
                print("Tokens limit exceeded, try again later.")
            else:
                print(f"Error: {e}")
            return None