import google.generativeai as genai
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY_TRS_ANAL")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-3-flash-preview")

BATCH_SIZE = 5
MAX_RETRIES = 3

class Message(BaseModel):
    role: str
    text: str

class Dialog(BaseModel):
    id: int
    messages: List[Message]

class TranslationBatch(BaseModel):
    dialogs: List[Dialog]


system_prompt = """
You are a professional translator.

Translate ONLY the text inside "messages.text" into Ukrainian.
Do NOT modify id.
Do NOT modify role.
Do NOT change JSON structure.
Preserve element order.

Return strictly in TranslationBatch format.
Do not add explanations.
"""

def process_translation(input_file: str, output_file: str):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Input file not found")
        return

    dialogs = data.get("dialogs", [])

    for i in range(0, len(dialogs), BATCH_SIZE):
        batch = dialogs[i:i + BATCH_SIZE]
        batch_payload = {
            "dialogs": [
                {
                    "id": dialog["id"],
                    "messages": dialog["messages"]
                }
                for dialog in batch
            ]
        }

        prompt = (
            system_prompt +
            "\n\nDialogs for translation:\n" +
            json.dumps(batch_payload, ensure_ascii=False)
        )

        for attempt in range(MAX_RETRIES):
            try:
                response = model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        temperature=0.0,
                        response_mime_type="application/json",
                        response_schema=TranslationBatch
                    )
                )

                parsed = json.loads(response.text)
                translated_batch = parsed.get("dialogs", [])
                for translated_dialog in translated_batch:
                    for original_dialog in dialogs:
                        if original_dialog["id"] == translated_dialog["id"]:
                            original_dialog["messages"] = translated_dialog["messages"]
                            break

                print(f"Translated {len(batch)} dialogs")
                break

            except Exception as e:
                print(f"Error (attempt {attempt + 1}): {e}")
                time.sleep(5)

        time.sleep(15) 
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Done. Translated {len(dialogs)} dialogs.")

if __name__ == "__main__":
    process_translation("chats_dataset.json", "chat_dataset_uk.json")