import os, io, re,json, requests
import pandas as pd
from dotenv import load_dotenv
from pdf_parser import text_extract_from_page
from sqlalchemy import create_engine, text, delete, table


load_dotenv()

LLM_URL = os.getenv('LLM_URL')

with open(os.path.join("data", "prompts.json"), "r") as jf:
    prompts_json = json.load(jf)

conn_string = os.environ['SQLALCHEMY_CON']
engine = create_engine(conn_string)

conn = engine.connect() 

files_pathes_df = pd.read_sql_query('SELECT * FROM public.documents LIMIT 10', con=engine)
print("df from BD:", files_pathes_df)


temp = 0.0
    
result = []
for d in files_pathes_df.to_dict(orient="records"):
    pdf_link_resp = requests.get(d["s3_link"])
    link_d = pdf_link_resp.json()
    pdf_path = link_d["Link"]
    
    pdf_path = re.sub("\s+", "", pdf_path)

    response = requests.get(pdf_path)
    
    response = requests.get(pdf_path)

    output = io.BytesIO(response.content)

    pages_texts = text_extract_from_page(output, 30)

    doc = ""
    for p_tx in pages_texts:
        doc += p_tx
    
    doc_text = re.sub("\n|\s+", " ", doc)

    for intent in prompts_json:
        if intent == "claim":
            act_fragment = re.findall(prompts_json[intent]["reg"], doc_text, re.IGNORECASE)
            if act_fragment:
                message = " ".join([prompts_json[intent]["prompt_start"], act_fragment[0], prompts_json[intent]["prompt_finish"]])
                js_data = {
                            "temperature": temp,
                            "model": "openchat_3.5",
                            "messages": [{"role": "user", "content": str(message)}]
                            }

                r = requests.post(LLM_URL, json=js_data)
                res_dct = r.json()
                
                result_text = res_dct["choices"][0]["message"]["content"]
                d["meta_type"] = intent
                d["meta_value"] = re.sub(r"\(|\)", "", result_text)
                result.append(d)
                
            else:
                print("НЕТ ФРАГМЕНТА")

result_df = pd.DataFrame(result)

result_df.to_sql("public.documents_with_meta", con=conn, if_exists='append', index=False)
conn.close()