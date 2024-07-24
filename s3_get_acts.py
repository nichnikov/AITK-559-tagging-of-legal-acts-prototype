import os
import io
import re
import requests
import pandas as pd
from time import sleep

from pdf_parser import text_extract_from_page



files_pathes_df = pd.read_csv(os.path.join("data", "pravoru_documents_uploded_202407111233.txt"), sep="|")
print(files_pathes_df)
print(files_pathes_df.info())

s3_url = "https://s3-documents.prod.dataplatform.aservices.tech/"
# path2 = "/dppdfpravoru264/e5635e72-829d-44f0-b1b7-ae8ef835f045.pdf"

print(files_pathes_df["path_file_in_baquet_s3"])



# for d in files_pathes_df["path_file_in_baquet_s3"].to_list()[:5]:
for d in files_pathes_df.to_dict(orient="records")[:5]:
    pdf_path = s3_url + d["path_file_in_baquet_s3"]
    pdf_path = re.sub("\s+", "", pdf_path)
    print("pdf path:", pdf_path)
    response = requests.get(pdf_path)
       
    try:
        response = requests.get(pdf_path)

        output = io.BytesIO(response.content)

        pages_texts = text_extract_from_page(output, 5)

        doc = ""
        for p_tx in pages_texts:
            doc += p_tx
        print(re.sub("\n|\s+", " ", doc), "\n")    

    except:
        pass
