import io
import os
import re
import requests
import pandas as pd
import json
from pdf_parser import text_extract_from_page

with open(os.path.join("data", "prompts.json"), "r") as jf:
    prompts_json = json.load(jf)


files_pathes_df = pd.read_csv(os.path.join("data", "pravoru_documents_uploded_202407111233.txt"), sep="|")
s3_url = "https://s3-documents.prod.dataplatform.aservices.tech/"

def promt_create(promts_dic: dict):
    for intent in promts_dic:
        act_fragment = re.findall(prompts_json[intent]["reg"], doc_text, re.IGNORECASE)
        if act_fragment:
            return " ".join([prompts_json[intent]["prompt_start"], act_fragment[0], prompts_json[intent]["prompt_finish"]])
        else:
            return None


temp = 0.5
for d in files_pathes_df.to_dict(orient="records")[:5]:
    pdf_path = s3_url + d["path_file_in_baquet_s3"]
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
        act_fragment = re.findall(prompts_json[intent]["reg"], doc_text, re.IGNORECASE)
        if act_fragment:
            prompt_for_searching = " ".join([prompts_json[intent]["prompt_start"], act_fragment[0], prompts_json[intent]["prompt_finish"]])
        else:
            print(None)