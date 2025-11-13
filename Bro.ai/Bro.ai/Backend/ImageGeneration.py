import os
import asyncio
import aiohttp
import base64
import re
import json

HUGGINGFACE_API_TOKEN = "[ENTER_YOUR_API_KEY]"
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

output_dir = "[ENTER_OUTPUT_DIRECTORY_PATH]"
os.makedirs(output_dir, exist_ok=True)

def sanitize_filename(text):
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "_", text)
    return text[:50]

def clean_prompt(prompt):
    bad_phrases = [
        "write a letter", "write letter", "letter to", "application to", "make note", "draft email", 
        "write note", "write application", "create content", "compose mail", "write a story",
        "generate a image of", "generate image of", "create image of", "show image of",
        "generate image", "generate a image", "create image", "show image", "generate",
        "and", "to", "my", "friend", "principal", "school", "email", "letter", "note"
    ]
    lowered = prompt.lower()
    for phrase in bad_phrases:
        lowered = re.sub(rf'\b{re.escape(phrase)}\b', '', lowered)
    lowered = re.sub(r'\s+', ' ', lowered)
    return lowered.strip()

async def generate_image(prompt):
    cleaned_prompt = clean_prompt(prompt)
    print(f" Generating image for: {cleaned_prompt}")

    payload = {
        "inputs": cleaned_prompt,
        "options": {"wait_for_model": True}
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, headers=headers, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    image_data = result[0].get("image", None) if isinstance(result, list) else result.get("image", None)

                    if image_data:
                        image_bytes = base64.b64decode(image_data)
                        filename = sanitize_filename(cleaned_prompt) + ".png"
                        output_path = os.path.join(output_dir, filename)
                        with open(output_path, "wb") as f:
                            f.write(image_bytes)
                        print(f"Image saved at: {output_path}")
                    else:
                        print("No image field found in response. Full response:")
                        print(result)
                else:
                    error_text = await response.text()
                    print(f" API Error ({response.status}): {error_text}")
    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    prompt = input("Enter image description: ").strip()
    asyncio.run(generate_image(prompt))
