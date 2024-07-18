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



for pdf_p in files_pathes_df["path_file_in_baquet_s3"].to_list()[:20]:
    pdf_path = s3_url + pdf_p
    pdf_path = re.sub("\s+", "", pdf_path)
    print("pdf path:", pdf_path)
    response = requests.get(pdf_path)
    print("GET:", response)
    
    
    # print(response.content)
    # response.close()
    # del response
    '''    
    try:
        response = requests.get(pdf_path)
        print(response.content)
        output = io.BytesIO(response.content)
        # output.write(response.content)
        pages_texts = text_extract_from_page(output, 5)
        # output.close()
        # del output
        
        for p_tx in pages_texts:
            print(p_tx)
    except:
        pass
    '''




# pdf_path = "https://s3-documents.prod.dataplatform.aservices.tech/dppdfpravoru30/3553a013-7787-49b5-ab50-d13c600dc08a.pdf"
pdf_path = "https://s3-documents.prod.dataplatform.aservices.tech/dppdfpravoru36/112b08ba-2244-4f0c-ba50-f67d4019b729.pdf"
output = io.BytesIO()
response = requests.get(pdf_path)
output.write(response.content)
pages_texts = text_extract_from_page(output, 5)

for p_tx in pages_texts:
    print(p_tx)
output.close()

# pdf_path = "https://s3-documents.prod.dataplatform.aservices.tech/dppdfpravoru264/e5635e72-829d-44f0-b1b7-ae8ef835f045.pdf" 


