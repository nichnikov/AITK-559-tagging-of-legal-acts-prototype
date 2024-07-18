import os
import io
import requests
import pandas as pd
from dotenv import load_dotenv
from pdf_parser import text_extract_from_page

load_dotenv()

files_pathes_df = pd.read_csv(os.path.join("data", "pravoru_documents_uploded_202407111233.txt"), sep="|")
print(files_pathes_df)
print(files_pathes_df.info())

s3_url = os.getenv('S3_ENDPOINT_URL')
s3_user = os.getenv('S3_USER')
s3_access_key = os.getenv('S3_ACCESS_KEY')
s3_secret_key = os.getenv('S3_SECRET_KEY')


s3_url = "https://s3-documents.prod.dataplatform.aservices.tech"
path2 = "/dppdfpravoru264/e5635e72-829d-44f0-b1b7-ae8ef835f045.pdf"


pdf_path = "https://s3-documents.prod.dataplatform.aservices.tech/dppdfpravoru264/e5635e72-829d-44f0-b1b7-ae8ef835f045.pdf" 


response = requests.get(pdf_path)

output = io.BytesIO()
output.write(response.content)
pages_texts = text_extract_from_page(output, 5)

for p_tx in pages_texts:
    print(p_tx) 
