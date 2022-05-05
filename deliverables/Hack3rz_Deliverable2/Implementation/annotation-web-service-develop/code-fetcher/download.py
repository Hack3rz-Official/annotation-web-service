# importing the requests library
import requests
import json
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    "Authorization": "token " + str(os.environ.get('GITHUB_ACCESS_TOKEN')),
    "Accept": "application/vnd.github.v3+json"
}

def fetch_files(repo_name, language):
    url = "https://api.github.com/search/code?q=repo:" + repo_name
    res = requests.get(url=url, headers=HEADERS)
    files = []
    text = json.loads(res.text)
    if text.get("items"):
        for item in text["items"]:
            file_extensions = {"java": "java", "kotlin": "kt", "python": "py"}
            if item['name'].endswith("." + file_extensions[language]):
                files.append((item['name'], item['url']))
    return files

# first 300 repositories sorted by stars descending
def fetch_repos(language):
    url = "https://api.github.com/search/repositories?q=language:" + language + "&sort=stars&order=desc&per_page=100&page=3"
    res = requests.get(url=url, headers=HEADERS)
    repo_names = []
    text = json.loads(res.text)
    if text.get("items"):
        for item in text["items"]:
            repo_names.append(item['full_name'])
    print("Repos fetched: ", repo_names)
    return repo_names


def get_file_content(url):
    res = requests.get(url=url, headers=HEADERS)
    text = json.loads(res.text)
    if text.get("download_url"):
        res = requests.get(url=text["download_url"], headers=HEADERS)
        return res.text
    print("no download url: ", text)
    return None

def download_files(path, language):
    counter = 0
    for repo_name in fetch_repos(language):
        enough_files = False
        for name, url in fetch_files(repo_name, language):
            if counter == int(os.environ.get('MAX_FILES')):
                print("Stop Download: max files reached")
                enough_files = True
                break

            file_path = os.path.join(path, name)
            content = get_file_content(url)
            if content and not os.path.exists(file_path):
                counter += 1
                with open(file_path, "w") as f:
                    print("Downloading... ", name)
                    f.write(content)
        if enough_files:
            break

def download_files_from_github(language):
    path = language
    # cleanup
    print(f"Cleaning up {language} files...")
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

    download_files(path, language)
