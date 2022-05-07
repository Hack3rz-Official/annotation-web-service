import os


def get_model_path(lang_name):
    """Gets the path of a model based on its programming language

    Args:
        String which is "python3", "java" or "kotlin"
    
    Returns:
        Path of requested model
    """
    return F"{lang_name}_{os.environ.get('MODEL_NAME')}.pt"

def load_db_model_to_current_directory(db_model, lang_name):
    if db_model:
        print(f"[SHModel] Newest Model loaded from DB with createdTime {db_model.createdTime}", flush=True)
        with open(get_model_path(lang_name), "wb") as file:
            model_file = db_model.file.read()
            file.write(model_file)
    else:
        print("[SHModel] No model found in DB, creating new model", flush=True)


