import os
import re
import requests
from dotenv import load_dotenv
from pdf_parser import text_extract_from_page

load_dotenv()

LLM_URL = os.getenv('LLM_URL')

pdf_path = os.path.join("data", "test2_ru.pdf")

texts_by_pages = text_extract_from_page(pdf_path, 5)

temp = 0.5

for p_tx in texts_by_pages:
    prompt_key_words = "сократи текст:"
    message = re.sub(r"\t|\n", " ", " ".join([prompt_key_words, p_tx]))
    
    js_data = {
        "temperature": temp,
        "model": "openchat_3.5",
        "messages": [{"role": "user", "content": message}]
    }

    r = requests.post(LLM_URL, json=js_data)
    res_dct = r.json()
    short_text = re.sub("Короткий текст:", "", res_dct["choices"][0]["message"]["content"])

    print("\ntext:", p_tx, "\nshort text:", short_text)
