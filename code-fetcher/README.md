# code-fetcher

Execute the script in the terminal with the following arguments:
- `-t` your github access token (to download the files from GitHub)
- `-f` [optional] amount of files to download per language (defaults to 1000)
- `-u` [optional] url of annotation service (defaults to public url in docker-compose)
- `-o` [optional] file where benchmark output is stored (defaults to `benchmark.csv`)
```
python3 main.py -t <GITHUB_TOKEN> -f 120
```