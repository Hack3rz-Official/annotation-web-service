import os
import requests
from dotenv import load_dotenv

load_dotenv()

def do_annotation(language):
    for root, dirs, filenames in os.walk(language):
        for filename in filenames:
            with open(language + "/" + filename, "r") as language_file:
                try:
                    print("Annotating... ", filename)
                    code = language_file.read()
                    body = {
                        "lang_name": language.upper(),
                        "code": code
                    }
                    res = requests.post(url=os.environ.get('ANNOTATE_URL'), json=body)
                    if res.status_code != 200:
                        print("Error during annotation: ", res.text)
                except Exception as e:
                    print("Error during annotation: ", e)
