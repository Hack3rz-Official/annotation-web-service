# code-fetcher

Note: dot_env only works on INTEL chips. If you are running on a M1 chip, you need to hard code the environment variables.

1. Set languages in `main.py`
2. Add GITHUB_ACCESS_TOKEN (see here: https://docs.github.com/en/enterprise-cloud@latest/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) in `.env` and consider changing MAX_FILES
3. Make sure docker-compose is up
4. Execute `python3 main.py` in this directory