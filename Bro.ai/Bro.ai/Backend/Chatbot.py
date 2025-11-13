import os
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import re
from difflib import get_close_matches

load_dotenv()
GROQ_API_KEY = "[ENTER YOUR API KEY]"

ASSISTANT_NAME = "Bro"
TRAINER_NAME = "Srajan"
FACTS_FILE = "facts.json"
CHAT_FILE = "chat.json"
RULES_FILE = "rules.json"

IMPORTANT_FACT_KEYWORDS = ["meeting", "birthday", "age", "favorite color", "car", "name", "friend"]

def ensure_files():
    if not os.path.exists(FACTS_FILE):
        with open(FACTS_FILE, "w") as f:
            json.dump({}, f)
    if not os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "w") as f:
            json.dump([], f)
    if not os.path.exists(RULES_FILE):
        with open(RULES_FILE, "w") as f:
                json.dump([], f)

def load_facts():
    ensure_files()
    with open(FACTS_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {}

def save_facts(facts):
    with open(FACTS_FILE, "w") as f:
        json.dump(facts, f, indent=2)

def load_chat():
    ensure_files()
    with open(CHAT_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []

def save_chat(chat_history):
    with open(CHAT_FILE, "w") as f:
        json.dump(chat_history[-30:], f, indent=2)

def clear_chat():
    with open(CHAT_FILE, "w") as f:
        json.dump([], f)

def realtime_info():
    now_ist = datetime.utcnow() + timedelta(hours=5, minutes=30)
    return {
        "time": now_ist.strftime("%I:%M %p"),
        "hour": now_ist.hour,
        "minute": now_ist.minute,
        "second": now_ist.second,
        "day": now_ist.strftime("%A"),
        "date": now_ist.strftime("%Y-%m-%d"),
        "month": now_ist.strftime("%B"),
        "year": now_ist.year
    }

def summarize_answer(text, max_words=40):
    words = text.split()
    return " ".join(words[:max_words]) + ("..." if len(words) > max_words else "")

def ask_groq(prompt, history):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    system_prompt = (
        f"You are {ASSISTANT_NAME}, a humanlike assistant created by {TRAINER_NAME}. "
        f"Speak casually and briefly like a human friend. No asterisks (*), no emojis, no roleplay, "
        f"no 'big smile' or stage directions. Don't mention memory or AI. "
        f"Be warm, helpful, and realistic, but natural and simple in tone. "
        f"If you don’t know the answer, say it softly or kindly, never rudely."
        f"talk everyone with energetic dont like dumb and add some feeling while talkig dont talk like robots your are human like assistant."
        f"treat your user as friend and act as suportive guy to him you are good guy who help who needs you"
    )

    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": prompt}]
    payload = {"model": "llama-3.1-8b-instant", "messages": messages, "temperature": 0.7}

    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"].strip()
    except:
        return "Sorry, I couldn't get that."

def extract_facts(text):
    facts = {}
    lower = text.lower().replace("metting", "meeting").replace("tommarwo", "tomorrow")

    if re.search(r"\b(meeting|office).*(at|by|around)?\s*\d{1,2}(:\d{2})?\s*(am|pm)?", lower):
        match = re.search(r"\b(?:meeting|office)[^\d]*(\d{1,2}(:\d{2})?\s*(am|pm)?)", lower)
        if match:
            facts["meeting"] = f"{match.group(1)}"

    if match := re.search(r"\b(i am|i'm|iam|turned|age is)\s+(\d{1,3})\b", lower):
        facts["age"] = {"age": int(match.group(2)), "year": datetime.now().year}
    if match := re.search(r"(?:birthday is|born on)\s+([a-zA-Z0-9 ,]+)", lower):
        facts["birthday"] = match.group(1).strip()
    if match := re.search(r"(?:favorite|favourite) color is\s+([a-zA-Z]+)", lower):
        facts["favorite color"] = match.group(1).strip()
    if match := re.search(r"my name is\s+([a-zA-Z ]+)", lower):
        facts["name"] = match.group(1).strip()
    if match := re.search(r"i have (a |an )?(?P<car>[\w\s]+?) car", lower):
        facts["car"] = match.group("car").strip()
    if match := re.search(r"my friend is\s+([a-zA-Z ]+)", lower):
        facts["friend"] = match.group(1).strip()
    return facts

def fuzzy_fact_match(key, query):
    return key in query or get_close_matches(key, [query], cutoff=0.7)

def handle_remember_statement(user_input):
    remember_text = re.match(r"remember (.+)", user_input.strip(), re.IGNORECASE)
    if remember_text:
        raw = remember_text.group(1).strip()
        key = " ".join(raw.split()[:4]).lower().replace(".", "").replace("!", "").strip()
        key = re.sub(r"[^\w\s]", "", key)[:40]
        facts = load_facts()
        facts[key] = raw
        save_facts(facts)
        return "Alright, got that saved. Thanks for telling me!"
    return None

def extract_rule(user_input):
    match = re.match(r"(when|if) (.+?),? (then )?(.*)", user_input, re.IGNORECASE)
    if match:
        trigger = match.group(2).strip()
        action = match.group(4).strip()
        return {"trigger": trigger, "action": action}
    return None

def load_rules():
    ensure_files()
    with open(RULES_FILE, "r") as f:
        return json.load(f)

def save_rule(rule):
    rules = load_rules()
    rules.append(rule)
    with open(RULES_FILE, "w") as f:
        json.dump(rules, f, indent=2)

def check_and_execute_rule(user_input):
    rules = load_rules()
    for rule in rules:
        if rule["trigger"].lower() in user_input.lower():
            return f"{rule['action']}!"
    return None

def chat_with_Bro_ai(user_input):
    facts = load_facts()
    chat = load_chat()
    query = user_input.strip().lower()

    if query in ["exit", "quit"]:
        print("Bro_ai: Goodbye.")
        return "exit"

    rt = realtime_info()
    if "time" in query and any(p in query for p in ["what", "current", "now", "tell", "much"]):
        return f"The current time is {rt['time']}."
    if "date" in query and any(p in query for p in ["today", "current", "what", "now"]):
        return f"Today's date is {rt['date']}."
    if "day" in query:
        return f"Today is {rt['day']}."
    if "month" in query:
        return f"This month is {rt['month']}."
    if "year" in query:
        return f"The year is {rt['year']}."

    if "what is your name" in query or "who are you" in query:
        return f"My name is {ASSISTANT_NAME}."
    if "what is my name" in query and "name" in facts:
        return f"Your name is {facts['name']}."

    for k in facts:
        if fuzzy_fact_match(k.replace("_", " "), query):
            val = facts[k]
            if isinstance(val, dict) and "age" in val:
                age = val["age"] + (datetime.now().year - val["year"])
                return f"You are {age} years old."
            return f"You told me: {val}."

    greetings = {
        "hi": "Hi there!",
        "hello": "Hello!",
        "hey": "Hey!",
        "how are you": "I'm good, thanks!",
        "kaise ho": "Main theek hoon, aap kaise ho?",
        "whats up": "All good here!"
    }
    if query in greetings:
        return greetings[query]

    general_faq = {
        "are you a robot": "I'm a friendly AI assistant here to help you.",
        "what can you do": "I can answer your questions, help you with tasks, and chat with you!",
        "what is your purpose": "My purpose is to assist and make your life easier."
    }
    cleaned_query = re.sub(r"[^\w\s]", "", query)
    for phrase, resp in general_faq.items():
        if phrase in cleaned_query:
            return resp

    rule = extract_rule(user_input)
    if rule:
        save_rule(rule)
        return f"Okay, noted. When you {rule['trigger']}, I’ll {rule['action']}."

    rule_response = check_and_execute_rule(user_input)
    if rule_response:
        return rule_response

    remember_response = handle_remember_statement(user_input)
    if remember_response:
        return remember_response

    new_facts = extract_facts(user_input)
    if new_facts:
        facts.update(new_facts)
        save_facts(facts)
        prompt = "React warmly to learning these things about the user: " + ", ".join(
            [f"{k} is {v['age']} years old" if isinstance(v, dict) else f"{k} is {v}" for k, v in new_facts.items()])
        chat.append({"role": "user", "content": user_input})
        reply = summarize_answer(ask_groq(prompt, chat))
        chat.append({"role": "assistant", "content": reply})
        save_chat(chat)
        return reply

    chat.append({"role": "user", "content": user_input})
    answer = summarize_answer(ask_groq(user_input, chat))
    chat.append({"role": "assistant", "content": answer})
    save_chat(chat)
    return answer

if __name__ == "__main__":
    print(f"[ {ASSISTANT_NAME} Chatbot CLI Test – type 'exit' to quit ]\n")
    history = load_chat()
    clear_chat()
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print(f"{ASSISTANT_NAME}: Goodbye.")
            break
        response = chat_with_Bro_ai(user_input)
        if response == "exit":
            break
        print(f"{ASSISTANT_NAME}: {response}\n{'-'*50}")
