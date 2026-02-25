import google.generativeai as genai
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()
my_api_key = os.getenv("GEMINI_API_KEY") # Рев'юер, по-перше вітаю Вас, по-друге створіть файл .env і покладіть туди свій ключ за зразком із файлу .env.example
model = genai.GenerativeModel('gemini-2.5-flash')

# клас від пайдентік аби відповіді були тільки у форматі json
class ChatAnalysis(BaseModel):
    intent: str
    satisfaction_reasoning: str
    satisfaction: str
    quality_score: int
    agent_mistakes: List[str]

# промпт для створення жосткої відповіді + пайдентік зверху.
# якщо невдоволеність не буде розуміти будемо щось тут робити
system_prompt = """
Ти - Senior QA Auditor у службі підтримки.
Твоє завдання - проаналізувати діалог і повернути жорстко заданий JSON за схемою.
Правила оцінювання:
1. intent: "проблеми з оплатою", "технічні помилки", "доступ до акаунту", "питання по тарифу", "повернення коштів" або "інше"
2. satisfaction_reasoning: опиши свої думки, проаналізуй слова клієнта на сарказм. Чи була вирішена проблема клієнта по факту?
3. satisfaction: "satisfied" , "neutral" , "unsatisfied". Якщо клієнт дякує, але проблема не вирішена або звучить сарказм - статус ПОВИНЕН БУТИ 'unsatisfied"
4. quality_score: Оцінка роботи агента підртримки від 1 до 5, де 1 - повністю незадоволений, 5 - повністю задоволений
5. agent_mistakes: Список помилок агента (ignored_question, incorrect_info, rude_tone, no_resolution, unnecessary_escalation). Якщо помилок немає - повертай порожній список
"""

# головна функція, вся логіка нижче
def process_chats(input_file: str, output_file: str):
    try:
        with open(input_file, "r", encoding='utf-8') as f:
            chats_data = json.load(f)
    except FileNotFoundError:
        return
    
    results = []

    for chat in chats_data:
        chat_id = chat.get("id", "unknown_id")
        messages = chat.get("messages", [])

        chat_text = ""
        for msg in messages:
            if msg.get("role") == "customer":
                speaker = "Користувач"
            else:
                speaker = "Агент"
            
            text = msg.get("text", "")
            chat_text += f"{speaker}: {text}\n"

        prompt = f"{system_prompt}\n Діалог для аналізу: \n {chat_text}"

        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig( # на жаль в Gemini може часто не працювати параметр seed
                    # тому за детермінованість буде відповідати температура
                    temperature=0.0,
                    response_mime_type="application/json", # потрібен формат JSON
                    response_schema=ChatAnalysis # це шаблон для відповіді
                )
            )

            raw_dict = json.loads(response.text)
            # сортуємо json аби він був гарний та структурований
            analysis_dict = {
                "chat_id": chat_id,
                "intent": raw_dict.get("intent"),
                "quality_score": raw_dict.get("quality_score"),
                "satisfaction_reasoning": raw_dict.get("satisfaction_reasoning"),
                "satisfaction": raw_dict.get("satisfaction"),
                "agent_mistakes": raw_dict.get("agent_mistakes", [])
            }

            results.append(analysis_dict)

        except Exception as e:
            # якщо світло зникне
            print(f"Помилка при аналізі чату {chat_id}: {e}")

        time.sleep(5) #Геміні дає 15 запитів у хвилину, тому потрібно зробити обмеження
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"Проаналізовано {len(results)} чатів")

if __name__ == "__main__":
    process_chats("input_chats.json", "analyzed_chats.json") # змінити назву, коли доробиться генератоор
