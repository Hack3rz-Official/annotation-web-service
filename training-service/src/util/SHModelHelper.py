import os
from SHModelUtils import SHModel
from src.models.model import Model

def from_db_model_to_sh_model(db_model, lang_name):
    if db_model:
        print(f"[SHModel] Newest Model loaded from DB with createdTime {db_model.createdTime}", flush=True)
        with open(lang_name, + "_" + os.environ.get('MODEL_NAME') + ".pt", "wb") as file:
            model_file = db_model.file.read()
            file.write(model_file)
    else:
        print("[SHModel] No model found in DB, creating new model", flush=True)

    return SHModel(lang_name, os.environ.get('MODEL_NAME'))


def from_best_sh_model_to_db_model(lang_name, accuracy):
    print("[TRAIN] New Model saved from directory to DB ", flush=True)
    model = Model(language=lang_name, accuracy=accuracy)
    with open(lang_name + "_" + os.environ.get('MODEL_NAME') + ".pt", "rb") as binary_file:
        model.file.put(binary_file)

    return model
