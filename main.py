from model.geminiAdapter import GeminiAdapter
from dotenv import load_dotenv
import os
import argparse

load_dotenv()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", "-i", help="Ruta a la imagen", default=None)
    parser.add_argument("--seccion", "-s", help="Course seccion", default="")
    args = parser.parse_args()

    if (args.image is None):
        raise ValueError("You must provide an image path using --image or -i")

    if (args.seccion is None) or (args.seccion.strip() == ""):
        raise ValueError("You must provide a course section using --seccion or -s")

    client = GeminiAdapter(
        api_key=os.getenv("GEMINI_API_KEY"),
        model=os.getenv("GEMINI_MODEL")
    )

    response = client.generate_from_image(args.image, prompt=os.getenv("GEMINI_IMAGE_PROMPT"))

    print(response)
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")