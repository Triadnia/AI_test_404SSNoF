import google.generativeai as genai
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()
my_api_key = os.getenv("GEMINI_API_KEY") # Рев'юер, по-перше вітаю Вас, по-друге створіть файл .env і покладіть туди свій ключ за зразком із файлу .env.example
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

class Batch(BaseModel):
    results: List[ChatAnalysis]

# промпт для створення жосткої відповіді + пайдентік зверху.
# якщо невдоволеність не буде розуміти будемо щось тут робити
system_prompt = """
Ти - Senior QA Auditor у службі підтримки.
Твоє завдання - проаналізувати кілька діалогів, які розділені тегами <chat id="..."> </chat> і повернути жорстко заданий JSON за схемою Batch.
Ти повинен повернути масив results, де кожен елемент це аналіз одного чату з наданих!
Обов'язково зберігай правильний chat_id для кожного чату!
Правила оцінювання:
1. intent: "проблеми з оплатою", "технічні помилки", "доступ до акаунту", "питання по тарифу", "повернення коштів" або "інше"
2. satisfaction_reasoning: опиши свої думки, проаналізуй слова клієнта на сарказм. Чи була вирішена проблема клієнта по факту?
3. satisfaction: визнач рівень задоволеності клієнта після аналізу:
    "satisfied": клієнт точно задоволений та виражає щиру подяку. Проблема вирішена повністю
    "neutral": клієнт відповідає сухо, не висловлює емоцій, або якщо діалог завершився без явної подяки, але й без претензій
    "unsatisfied": клієнт роздратований, використовує сарказм, АБО коли клієнт формально прощається ввічливо, але фактично його проблема НЕ була вирішена
4. quality_score: Оцінка роботи агента підртримки від 1 до 5 за такою шкалою:
    5: Проблему вирішено повністю, тон ввічливий, швидка і точна відповідь. Клієнт повністю задоволений
    4: Проблему вирішено, але агент відповів максимально сухо
    3: Агент вирішив проблему лише частково, клієнту довелося перепитувати, або рішення вимагало зайвих зусиль користувача.
    2: Агент припустився помилок, проігнорував частину питань, але не був відверто грубим.
    1: Відкрита грубість, повне нерозуміння проблеми, відмова допомогти без причини, шкідливі поради.
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
    batch_size = 5

    # тут був початок створення бранчів. Оскільки API мають свої ліміти, аби зробити більш велику вибірку було вирішено "скомкати" чати для аналізу
    # в нашому випадку це збільшило можливу кількість аналізу з 20 на день до 100 на день. Результати аналізу були незмінними, отже воно не впливає на точність
    for i in range(0, len(chats_data), batch_size):
        batch = chats_data[i:i + batch_size]

        batch_text = ""

        for chat in batch:
            chat_id = chat.get("chat_id", "unknown_id")
            batch_text += f"<chat id='{chat_id}'>\n"

            for msg in chat.get("messages", []):
                if msg.get("role") == "customer":
                    speaker = "Користувач"
                else:
                    speaker = "Агент"
                
                batch_text += f"{speaker}: {msg.get('text', '')}\n"

            batch_text += "</chat>\n\n"

        prompt = f"{system_prompt}\n Діалоги для аналізу: \n {batch_text}"

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
                        "agent_mistakes": item.get("agent_mistakes", [])
                    }
                    results.append(ordered_item)

                print(f"Успішно проаналізовано пачку з {len(batch)} чатів")
                break

            except Exception as e:
                print(f"Збій при аналізі (Спроба {attempt + 1} з {max_retries}): {e}")
                time.sleep(10)
        
        time.sleep(20) # пауза для обходу лімітів у 5 запитів на хвилину
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"Проаналізовано {len(results)} чатів")

if __name__ == "__main__":
    process_chats("input_chats.json", "analyzed_chats.json") # змінити назву, коли доробиться генератоор