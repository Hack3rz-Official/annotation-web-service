from download import download_files_from_github
from annotate import do_annotation

# supported languages: "java", "python", "kotlin"
languages = ["java", "python", "kotlin"]
for language in languages:
    download_files_from_github(language)
    do_annotation(language)

