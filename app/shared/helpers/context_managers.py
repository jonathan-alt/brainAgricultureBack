import requests
import shutil
import functools
import os
import uuid


class TmpFileContextManager():
    def __init__(self, file_url, file_name):
        self.file_path = f'/tmp/{uuid.uuid4()}_{file_name}'
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()
            with open(self.file_path, 'wb') as f:
                r.raw.read = functools.partial(r.raw.read, decode_content=True)
                shutil.copyfileobj(r.raw, f)
          
    def __enter__(self):
        return self.file_path
      
    def __exit__(self, exc_type, exc_value, exc_traceback):
        os.remove(self.file_path)