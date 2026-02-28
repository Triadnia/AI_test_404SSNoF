import google.generativeai as genai
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()
my_api_key = os.getenv("GEMINI_API_KEY_TRS_GEN") # Рев'юер, по-перше вітаю Вас, по-друге створіть файл .env і покладіть туди свій ключ за зразком із файлу .env.example
genai.configure(api_key=my_api_key)

model = genai.GenerativeModel('gemini-3-flash-preview')

# клас від пайдентік аби відповіді були тільки у форматі json
class ChatAnalysis(BaseModel):
    chat_id: str
    intent: str
    satisfaction_reasoning: str
    satisfaction: str
    quality_score: int
    agent_mistakes: List[str]
    passive_aggression: bool # Додано поле для прихованої агресії

class Batch(BaseModel):
    results: List[ChatAnalysis]

# промпт для створення жосткої відповіді + пайдентік зверху.
# якщо невдоволеність не буде розуміти будемо щось тут робити
system_prompt = """
You are a Senior QA Auditor in a customer support team.
Your task is to analyze multiple dialogs enclosed in <chat id="..."> </chat> tags and return a strictly formatted JSON according to the Batch schema.
You must return a `results` array, where each element is the analysis of one of the provided chats!
Be sure to keep the correct `chat_id` for each chat!

Evaluation rules:
1. intent: "payment_issue", "technical_error", "account_access", "tariff_question", "refund_request", or "other".
2. satisfaction_reasoning: describe your thoughts, analyze the client's words for sarcasm. Was the client's problem actually resolved?
3. satisfaction: determine the client's satisfaction level after analysis:
    "satisfied": the client is definitely satisfied and expresses genuine gratitude. The problem is completely resolved.
    "neutral": the client replies dryly, expresses no emotions, or if the dialog ended without clear gratitude but also without complaints.
    "unsatisfied": the client is annoyed, uses sarcasm, OR when the client says goodbye politely on the surface, but their problem was NOT actually resolved.
4. quality_score: Rate the support agent's work from 1 to 5 using the following scale:
    5: The problem is completely resolved, the tone is polite, fast and accurate response. The client is completely satisfied.
    4: The problem is resolved, but the agent replied as dryly as possible.
    3: The agent only partially resolved the problem, the client had to ask again, or the solution required extra effort from the user.
    2: The agent made mistakes, ignored some questions, but was not outright rude.
    1: Outright rudeness, complete misunderstanding of the problem, refusal to help without reason, harmful advice.
5. agent_mistakes: List of agent mistakes (ignored_question, incorrect_info, rude_tone, no_resolution, unnecessary_escalation). If there are no mistakes, return an empty list.
6. passive_aggression: boolean (true/false). Analyze the client's tone. Return true if the client uses sarcasm, passive aggression, or "hidden dissatisfaction" (e.g., politely saying goodbye while the issue remains unresolved or acting annoyed). Otherwise, return false.
"""

# головна функція, вся логіка нижче
def process_chats(input_file: str, output_file: str):
    try:
        with open(input_file, "r", encoding='utf-8') as f:
            raw_data = json.load(f)
            # Дістаємо саме масив чатів, щоб далі працював зріз
            chats_data = raw_data.get("dialogs", raw_data) if isinstance(raw_data, dict) else raw_data
            print(f"Всередині виявлено {len(chats_data)} чатів.")
    except FileNotFoundError:
        return
    except Exception as e:
        print(f"❌ ПОМИЛКА читання JSON: {e}")
        return
    
    results = []
    batch_size = 5

    # тут був початок створення бранчів. Оскільки API мають свої ліміти, аби зробити більш велику вибірку було вирішено "скомкати" чати для аналізу
    # в нашому випадку це збільшило можливу кількість аналізу з 20 на день до 100 на день. Результати аналізу були незмінними, отже воно не впливає на точність
    for i in range(0, len(chats_data), batch_size):
        batch = chats_data[i:i + batch_size]
        batch_text = ""

        print(f"Відправлено на аналіз чати {i + 1} - {i + len(batch)}...")
        for chat in batch:
            chat_id = chat.get("id", "unknown_id")
            batch_text += f"<chat id='{chat_id}'>\n"

            for msg in chat.get("messages", []):
                if msg.get("role") == "client":
                    speaker = "Client"
                else:
                    speaker = "Agent"
                
                batch_text += f"{speaker}: {msg.get('text', '')}\n"

            batch_text += "</chat>\n\n"

        prompt = f"{system_prompt}\n Dialogs for analyse: \n {batch_text}"

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        temperature=0.0,
                        response_mime_type="application/json",
                        response_schema=Batch
                    )
                )

                raw_dict = json.loads(response.text)
                batch_results = raw_dict.get("results", [])
                
                for item in batch_results:
                    ordered_item = {
                        "chat_id": item.get("chat_id", ""),
                        "intent": item.get("intent", ""),
                        "quality_score": item.get("quality_score", 0),
                        "satisfaction_reasoning": item.get("satisfaction_reasoning", ""),
                        "satisfaction": item.get("satisfaction", ""),
                        "agent_mistakes": item.get("agent_mistakes", []),
                        "passive_aggression": item.get("passive_aggression", False) # Записуємо агресію
                    }
                    results.append(ordered_item)

                print(f"Успішно проаналізовано пачку з {len(batch)} чатів")
                break

            except Exception as e:
                print(f"Збій при аналізі (Спроба {attempt + 1} з {max_retries}): {e}")
                time.sleep(10)
        
        time.sleep(5) # пауза для обходу лімітів у 5 запитів на хвилину
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"Проаналізовано {len(results)} чатів")

if __name__ == "__main__":
    process_chats("special_chats.json", "special_anal.json") # змінити назву, коли доробиться генератоор