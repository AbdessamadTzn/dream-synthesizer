from groq import Groq
from mistralai import Mistral
from dotenv import load_dotenv
from pathlib import Path
import os
import json
import math
from image_generator import generate_from_main_output

load_dotenv()


def read_file(text_file_path):
	with open(text_file_path, "r") as file:
		return file.read()


def softmax(predictions):
	output = {}
	for sentiment, predicted_value in predictions.items():
		output[sentiment] = math.exp(predicted_value*10) / sum([math.exp(value*10) for value in predictions.values()])
	return output


def speach_to_text(audio_path, language="fr"):
	client = Groq(api_key=os.environ["GROQ_API_KEY"])
	with open(audio_path, "rb") as file:

		transcription = client.audio.transcriptions.create(
			file=file, # Required audio file
			model="whisper-large-v3-turbo", # Required model to use for transcription
			prompt="Extrait le text de l'audio de la manière la plus factuelle possible",  # Optional
			response_format="verbose_json",  # Optional
			timestamp_granularities = ["word", "segment"], # Optional (must set response_format to "json" to use and can specify "word", "segment" (default), or both)
			language=language,  # Optional
			temperature=0.0  # Optional
		)

		return transcription.text


def text_analysis(text):

    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

    # Build absolute path to context_analysis.txt
    project_root = Path(__file__).parent.parent.parent
    context_path = project_root / "backend" / "services" / "context_analysis.txt"

    chat_response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "system",
                "content": read_file(text_file_path=str(context_path))
            },
            {
                "role": "user",
                "content": f"Analyse le texte ci-dessous (ta réponse doit être dans le format JSON) : {text}",
            },
        ],
        response_format={"type": "json_object",}
    )
	
    predictions = json.loads(chat_response.choices[0].message.content)
    return softmax(predictions)

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    audio_path = project_root / "data/audio/samples/reve_heureux_01.mp3" 
    print("Extraction de texte")
    text = speach_to_text(audio_path, language="fr")
    print(f"Text extrait : {text}")
    analysis = text_analysis(text)
    print(analysis)
    output_dir = project_root / "data/generated_images"
    result = generate_from_main_output(text, analysis, output_dir)
    print(result)