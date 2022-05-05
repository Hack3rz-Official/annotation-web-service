import os


def load_db_model_to_current_directory(db_model, lang_name):
    if db_model:
        print(f"[SHModel] Newest Model loaded from DB with createdTime {db_model.createdTime}", flush=True)
        with open(lang_name, + "_" + os.environ.get('MODEL_NAME') + ".pt", "wb") as file:
            model_file = db_model.file.read()
            file.write(model_file)
    else:
        print("[SHModel] No model found in DB, creating new model", flush=True)


