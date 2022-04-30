import argparse
from download import download_files_from_github
from annotate import do_annotation

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--token', help="Github Access Token", required=True)

    parser.add_argument('-f', '--files', type=int, help="number of files", default=1000)

    parser.add_argument('-u', '--url', help="api url", default="http://localhost:3000/highlight")

    args = parser.parse_args()

    github_token = args.token
    max_files = args.files
    url = args.url

    # supported languages: "java", "python", "kotlin"
    languages = ["java", "python3", "kotlin"]
    for language in languages:
        download_files_from_github(language, github_token, max_files)
        do_annotation(language, url)


if __name__ == "__main__":
    main()
