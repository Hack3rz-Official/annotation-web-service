# importing the requests library
import requests
import json
import os
import shutil


def make_header(github_token):
    return {
        "Authorization": "token " + github_token,
        "Accept": "application/vnd.github.v3+json"
    }


def fetch_files(repo_name, language, github_token):
    url = "https://api.github.com/search/code?q=repo:" + repo_name
    res = requests.get(url=url, headers=make_header(github_token))
    files = []
    text = json.loads(res.text)
    if text.get("items"):
        for item in text["items"]:
            file_extensions = {"java": "java", "kotlin": "kt", "python3": "py"}
            if item['name'].endswith("." + file_extensions[language]):
                files.append((item['name'], item['url']))
    return files


# first 300 repositories sorted by stars descending
def fetch_repos(language, github_token):
    url = "https://api.github.com/search/repositories?q=language:" + language + "&sort=stars&order=desc&per_page=100&page=3"
    res = requests.get(url=url, headers=make_header(github_token))
    repo_names = []
    text = json.loads(res.text)
    if text.get("items"):
        for item in text["items"]:
            repo_names.append(item['full_name'])
    # print("Repos fetched: ", repo_names)
    return repo_names


def get_file_content(url, github_token):
    header = make_header(github_token)
    res = requests.get(url=url, headers=header)
    text = json.loads(res.text)
    if text.get("download_url"):
        res = requests.get(url=text["download_url"], headers=header)
        return res.text
    print("no download url: ", text)
    return None


def download_files(path, language, github_token, max_files):
    counter = 0
    for repo_name in fetch_repos(language, github_token):
        enough_files = False
        for name, url in fetch_files(repo_name, language, github_token):
            if counter == max_files:
                enough_files = True
                break

            file_path = os.path.join(path, name)
            content = get_file_content(url, github_token)
            if content and not os.path.exists(file_path):
                counter += 1
                with open(file_path, "w") as f:
                    print(f'Downloading {language} file {counter}/{max_files}: {name}')
                    f.write(content)
        if enough_files:
            break


def download_files_from_github(language, github_token, max_files=1000):
    path = language
    # cleanup
    print(f"Cleaning up {language} files...")
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

    download_files(path, language, github_token, max_files)
