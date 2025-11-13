import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import concurrent.futures
import webbrowser

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
SERPER_API_URL = "https://google.serper.dev/search"
MODEL_NAME = "llama-3.1-8b-instant"

def fetch_content(url):
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
            timeout=3
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "noscript", "header", "footer", "svg", "img"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        cleaned = " ".join(text.split())
        return cleaned[:1000] if cleaned else ""
    except Exception:
        return ""

def serper_search(query, num_results=5):
    if not SERPER_API_KEY:
        return {
            "error": "Enter your SERPER_API_KEY in .env file [enter your app URL or API key]",
            "organic": []
        }

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query,
        "num": num_results
    }

    try:
        response = requests.post(
            SERPER_API_URL,
            headers=headers,
            json=payload,
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return {"error": "Invalid SERPER_API_KEY. [enter your app URL or API key]", "organic": []}
        elif e.response.status_code == 429:
            return {"error": "Serper API rate limit exceeded.", "organic": []}
        return {"error": str(e), "organic": []}
    except Exception as e:
        return {"error": str(e), "organic": []}

def get_search_snippets(query, num_results=5, scrape_content=False):
    snippets = []
    search_data = serper_search(query, num_results)
    if "error" in search_data:
        return []
    organic_results = search_data.get("organic", [])
    if not organic_results:
        return []
    for result in organic_results:
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        if snippet:
            snippets.append(f"{title}: {snippet}")
    if scrape_content and len(snippets) < 3:
        urls = [result.get("link") for result in organic_results[:3]]
        if urls:
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                scraped_content = list(executor.map(fetch_content, urls))
            for content in scraped_content:
                if content and len(content) > 100:
                    snippets.append(content)
    return snippets

def filter_subscriber_lines(snippets):
    filtered = []
    for text in snippets:
        lines = text.split(".")
        for line in lines:
            if "subscriber" in line.lower() and len(line.strip()) > 20:
                filtered.append(line.strip())
    return filtered if filtered else snippets

def summarize_with_groq(snippets, question):
    if not GROQ_API_KEY:
        return "GROQ_API_KEY missing. [enter your app URL or API key]"

    if not snippets:
        return "No content available to summarize."

    combined_text = "\n\n".join(snippets[:8])
    if len(combined_text) > 4000:
        combined_text = combined_text[:4000]

    prompt = f"""Answer this question using the web content below:

Question: {question}

Content:
{combined_text}

Provide a clear, factual answer in 2-3 sentences."""

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are Bro.ai, a concise AI assistant Developed By Srajan Shetty. Provide accurate answers and avoid unnecessary information. Speak in a friendly supportive human-like tone."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 200
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=15)
        response.raise_for_status()
        result = response.json()
        if "choices" not in result:
            return f"Groq API error: {result.get('error', 'Unknown error')}"
        answer = result["choices"][0]["message"]["content"].strip()
        return answer
    except requests.exceptions.HTTPError as err:
        error_detail = ""
        status_code = "Unknown"
        if err.response:
            status_code = err.response.status_code
            try:
                error_json = err.response.json()
                error_detail = error_json.get("error", {})
                if isinstance(error_detail, dict):
                    error_detail = error_detail.get("message", str(error_detail))
                else:
                    error_detail = str(error_detail)
            except:
                error_detail = err.response.text[:200]
        if status_code == 401:
            return "Invalid GROQ_API_KEY. [enter your app URL or API key]"
        elif status_code == 429:
            return "Groq API rate limit exceeded."
        else:
            return f"Groq API Error ({status_code}): {error_detail}"
    except requests.exceptions.Timeout:
        return "Groq API timeout."
    except requests.exceptions.ConnectionError:
        return "Cannot connect to Groq API."
    except Exception as e:
        return f"Summarization error: {str(e)}"

def test_api_keys():
    print("\nTesting API Keys...")
    if not SERPER_API_KEY:
        print("SERPER_API_KEY missing. [enter your app URL or API key]")
    else:
        try:
            headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
            response = requests.post(
                SERPER_API_URL,
                headers=headers,
                json={"q": "test", "num": 1},
                timeout=5
            )
            if response.status_code == 200:
                print("Serper API key is valid")
            elif response.status_code == 401:
                print("Invalid Serper API key.")
            else:
                print(f"Serper returned status {response.status_code}")
        except Exception as e:
            print(f"Serper test failed: {e}")

    if not GROQ_API_KEY:
        print("GROQ_API_KEY missing. [enter your app URL or API key]")
    else:
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GROQ_API_KEY}"
            }
            data = {
                "model": MODEL_NAME,
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 10
            }
            response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=10)
            if response.status_code == 200:
                print("Groq API key is valid")
            elif response.status_code == 401:
                print("Invalid Groq API key.")
            else:
                print(f"Groq returned status {response.status_code}")
                print(f"Response: {response.text[:200]}")
        except Exception as e:
            print(f"Groq API test failed: {e}")

    print()

def realtime_answer(query: str, deep_search=False):
    query_lower = query.lower().strip()

    if query_lower in ["hi", "hello", "hey", "hi there", "hello there"]:
        return "Hello! Bro.ai here. Ask me anything!"

    if "search" in query_lower and "on google" in query_lower:
        topic = query_lower.split("search", 1)[1].split("on google")[0].strip()
        if topic:
            url = f"https://www.google.com/search?q={topic.replace(' ', '+')}"
            webbrowser.open(url)
            return f"Opened Google search for '{topic}'."
        else:
            return "Could not extract search topic."

    snippets = get_search_snippets(query, num_results=5, scrape_content=deep_search)

    if not snippets:
        return """Sorry, I couldn't find any results.

Check:
• SERPER_API_KEY in .env
• Serper API quota
• Internet connection

Get a key at: [enter your app URL or API key]"""

    if "subscriber" in query_lower:
        snippets = filter_subscriber_lines(snippets)

    summary = summarize_with_groq(snippets, query)

    return summary

if __name__ == "__main__":
    print("Bro.ai - Real-Time Search Assistant")
    print("Type 'exit' to quit | Type 'test' to check API keys")
    print("Add '--deep' for detailed search\n")

    missing_keys = []
    if not SERPER_API_KEY:
        missing_keys.append("SERPER_API_KEY")
    if not GROQ_API_KEY:
        missing_keys.append("GROQ_API_KEY")

    if missing_keys:
        print("Missing API keys:")
        for key in missing_keys:
            print(f"   • {key}")
        print("\nAdd to .env file:")
        print("   SERPER_API_KEY=[enter your app URL or API key]")
        print("   GROQ_API_KEY=[enter your app URL or API key]\n")

    while True:
        try:
            user_query = input("You: ").strip()

            if user_query.lower() in ["exit", "quit", "q"]:
                print("\nGoodbye!")
                break

            if user_query.lower() == "test":
                test_api_keys()
                continue

            if not user_query:
                continue

            deep_search = False
            if user_query.endswith("--deep"):
                deep_search = True
                user_query = user_query[:-6].strip()

            answer = realtime_answer(user_query, deep_search=deep_search)
            print(f"Bro: {answer}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")
