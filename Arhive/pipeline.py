import os
import io
import re
import requests
import pandas as pd
from dotenv import load_dotenv
from pdf_parser import text_extract_from_page

load_dotenv()

LLM_URL = os.getenv('LLM_URL')

files_pathes_df = pd.read_csv(os.path.join("data", "pravoru_documents_uploded_202407111233.txt"), sep="|")
s3_url = "https://s3-documents.prod.dataplatform.aservices.tech/"


temp = 0.5
for d in files_pathes_df.to_dict(orient="records")[2:5]:
    pdf_path = s3_url + d["path_file_in_baquet_s3"]
    pdf_path = re.sub("\s+", "", pdf_path)

    response = requests.get(pdf_path)
    
    response = requests.get(pdf_path)

    output = io.BytesIO(response.content)

    pages_texts = text_extract_from_page(output, 5)

    doc = ""
    for p_tx in pages_texts:
        doc += p_tx
    
    doc_text = re.sub("\n|\s+", " ", doc)

    prompt_key_words = "сократи текст, напиши слова СОКРАЩЕННЫЙ ТЕКСТ и ответ:"
    message = re.sub(r"\t|\n", " ", " ".join([prompt_key_words, doc_text]))
    
    
    js_data = {
        "temperature": temp,
        "model": "openchat_3.5",
        "messages": [{"role": "user", "content": message}]
    }

    r = requests.post(LLM_URL, json=js_data)
    res_dct = r.json()
    
    short_text = re.sub("Короткий текст:", "", res_dct["choices"][0]["message"]["content"])
    
    print("\nshort text:", short_text)
    