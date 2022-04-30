import os
import requests
import math

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def do_annotation(language, url):
    for root, dirs, filenames in os.walk(language):
        for index, filename in enumerate(filenames):
            with open(language + "/" + filename, "r") as language_file:
                try:
                    print(F"Annotating {language} file {index}/{len(filenames)}: {filename}")
                    code = language_file.read()
                    locs = len(language_file.readlines())
                    body = {
                        "language": language.lower(),
                        "code": code
                    }
                    res = requests.post(url, json=body)
                    print(f"Size: {convert_size(os.path.getsize(language_file.name))} LOCs: {locs} Done in: {res.elapsed.total_seconds()}s")
                    if res.status_code != 200:
                        print("Error during annotation: ", res.text)
                except Exception as e:
                    print("Error during annotation: ", e)
