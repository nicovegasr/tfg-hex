
import base64
import io

import pandas as pd

def process_algorithm_files(files: dict) -> str or list:
    for _, file in files.items():
      is_excel : bool = True
      is_csv : bool = True
      _, content_string = file["file_content"].split(',')
      file_decoded_base_64 = base64.b64decode(content_string)
      try:
          decoded_file = pd.read_csv(io.StringIO(file_decoded_base_64.decode('utf-8')))
      except:
        is_csv = False  
      try:
          decoded_file = pd.read_excel(io.BytesIO(file_decoded_base_64))
      except:
        is_excel = False  
      if (not is_excel) and (not is_csv):
         filename_result = file["filename"]
         raise ValueError(f"File {filename_result}: not supported type.") 
      file["file_content"] = decoded_file.to_json()
    return files


