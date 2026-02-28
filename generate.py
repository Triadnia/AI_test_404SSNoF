import json
import random
import re
from ollama import chat

MODEL = "llama3:8b"
SEED = 2
NUM_DIALOGS = 100
OUTPUT_FILE = "chats_dataset.json"

random.seed(SEED)

SCENARIOS = [
    "payment issues",
    "technical errors",
    "account access",
    "questions about pricing plan",
    "refund request",
    "other"]

CASE_TYPES = [
    "successful",
    "problematic",
    "conflict"]

SATISFACTION = ["satisfied",
                "neutral", 
                "unsatisfied"]

PASSIVE_AGR = ["True", "False"]

AGENT_MIST = ["ignored_question",
               "incorrect_info", 
               "rude_tone", 
               "no_resolution",
               "unnecessary_escalation"]


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text


def validate_messages(messages):
    if not isinstance(messages, list):
        return False

    if len(messages) < 3 or len(messages) > 12:
        return False

    for msg in messages:
        if not isinstance(msg, dict):
            return False
        if "role" not in msg or "text" not in msg:
            return False
        if msg["role"] not in ["client", "agent"]:
            return False
        if not msg["text"] or not msg["text"].strip():
            return False

    return True


def generate_dialog(dialog_id):
    scenario = random.choice(SCENARIOS)
    case_type = random.choice(CASE_TYPES)
    turns_count = random.randint(3, 12)
    passive_arg = random.choice(PASSIVE_AGR)
    num_mistakes = random.randint(0, 4)
    agend_mistake = random.sample(AGENT_MIST, num_mistakes)
    prompt = f"""
    Generate a dialogue in English between a client and a customer support agent.

    Scenario: {scenario}
    Case type: {case_type}
    Client passive aggression: {passive_arg}
    Agent mistake: {agend_mistake}

    Requirements:
    - Between 3 and 12 messages.
    - Response format: JSON array.
    - Each element:
        {{
          "role": "client" or "agent",
          "text": "message text"
        }}
    - English language only.
    - No explanations.
    """

    response = chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={
            "seed": SEED + dialog_id,
            "temperature": 0.8
        }
    )

    try:
        messages = json.loads(response["message"]["content"])

        for msg in messages:
            msg["text"] = clean_text(msg["text"])

        if not validate_messages(messages):
            return generate_dialog(dialog_id + 1000)

    except:
        return generate_dialog(dialog_id + 2000)

    return {
        "id": dialog_id,
        "scenario": scenario,
        "case_type": case_type,
        "agent_mistake": agend_mistake,
        "passive_agression": passive_arg,

        "messages": messages
    }


def main():
    dialogs = []
    summary = {case: 0 for case in CASE_TYPES}

    for i in range(1, NUM_DIALOGS + 1):
        dialog = generate_dialog(i)
        if validate_messages(dialog["messages"]):
            dialogs.append(dialog)
            '''print(f"Dialog {i}")'''
            summary[dialog["case_type"]] += 1

    dataset = {
        "metadata": {
            "seed": SEED,
            "total_dialogs": len(dialogs)
        },
        "dialogs": dialogs,
        "summary": summary
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)

    print(f"Dataset saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()