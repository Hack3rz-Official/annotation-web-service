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





def do_annotation(language, url, benchmark_filename):

    benchmarks = []

    for root, dirs, filenames in os.walk(language):
        for index, filename in enumerate(filenames):
            with open(language + "/" + filename, "r") as language_file:
                try:
                    print(F"Annotating {language} file {index}/{len(filenames)}: {filename}")
                    code = language_file.read()
                    locs = sum(1 for line in language_file)
                    body = {
                        "language": language.lower(),
                        "code": code
                    }
                    res = requests.post(url, json=body)
                    size = os.path.getsize(language_file.name)
                    time = res.elapsed.total_seconds()
                    error = ""
                    print(f"Size: {convert_size(size)} Done in: {time}s")
                    if res.status_code != 200:
                        error = res.text
                        print("Error during annotation: ", res.text)
                    benchmarks.append({
                        "language": language,
                        "filename": filename,
                        "size": size,
                        "locs": locs,
                        "duration": time,
                        "error": error
                    })
                except Exception as e:
                    print("Error during annotation: ", e)

    return benchmarks
