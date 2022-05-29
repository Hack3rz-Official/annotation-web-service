import argparse
from download import download_files_from_github
from annotate import do_annotation
import csv


def save_benchmark(benchmarks, filename="benchmarks.csv"):
    keys = benchmarks[0].keys()
    a_file = open(filename, "w")
    dict_writer = csv.DictWriter(a_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(benchmarks)
    a_file.close()


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--token', help="Github Access Token", required=True)

    parser.add_argument('-f', '--files', type=int, help="number of files", default=1000)

    parser.add_argument('-u', '--url', help="api url", default="http://localhost:8081/api/v1/highlight")

    parser.add_argument('-o', '--output', help="output file", default="benchmark.csv")

    args = parser.parse_args()

    github_token = args.token
    max_files = args.files
    url = args.url
    filename = args.output

    benchmarks = []

    # supported languages: "java", "python", "kotlin"
    languages = ["java", "python3", "kotlin"]
    for language in languages:
        download_files_from_github(language, github_token, max_files)
        benchmark = do_annotation(language, url, filename)
        benchmarks = [*benchmarks, *benchmark]

    save_benchmark(benchmarks, filename)


if __name__ == "__main__":
    main()
