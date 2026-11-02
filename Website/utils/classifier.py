"""
classifier.py
=============
Modul klasifikasi kendaraan menggunakan EfficientNet B4.
"""

import numpy as np
import os
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image

# ── Konfigurasi ───────────────────────────────────────────────────────────────
MODEL_PATH = r"D:\@ File Tugas Akhir\Website\asset\b4_fc1_best_model.keras"

IMG_SIZE = (380, 380)

CLASS_NAMES = [
    "Agya / Ayla",
    "Avanza / Xenia",
    "Brio",
    "Fortuner",
    "Innova Reborn",
    "Innova Zenix",
    "Kijang Innova",
    "Pajero Sport",
    "Sigra / Calya",
    "Xpander",
]

# Setiap label → list keyword terpisah untuk OR filtering
# Label yang merupakan 2 model berbeda dipecah jadi 2 keyword
LABEL_TO_KEYWORDS_LIST = {
    "Agya / Ayla"    : ["Agya", "Ayla"],
    "Avanza / Xenia" : ["Avanza", "Xenia"],
    "Brio"           : ["Brio"],
    "Fortuner"       : ["Fortuner"],
    "Innova Reborn"  : ["Innova Reborn"],   
    "Innova Zenix"   : ["Innova Zenix"],
    "Kijang Innova"  : ["Kijang Innova"],  
    "Pajero Sport"   : ["Pajero Sport"],    
    "Sigra / Calya"  : ["Sigra", "Calya"],
    "Xpander"        : ["Xpander"],
}


# ── Load model ────────────────────────────────────────────────────────────────
def load_classifier(model_path: str = MODEL_PATH) -> dict:
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model tidak ditemukan di:\n{model_path}\n"
            "Pastikan MODEL_PATH di classifier.py sudah benar."
        )

    model = load_model(model_path)

    aug_output_layer = None
    for layer in model.layers:
        if layer.name == "efficientnetb4":
            break
        aug_output_layer = layer

    has_aug = (
        aug_output_layer is not None
        and aug_output_layer.name != model.layers[0].name
    )

    aug_model = None
    if has_aug:
        aug_model = tf.keras.Model(
            inputs=model.input,
            outputs=aug_output_layer.output,
        )

    return {
        "model"    : model,
        "aug_model": aug_model,
        "has_aug"  : has_aug,
    }


# ── Prediksi ──────────────────────────────────────────────────────────────────
def predict(pil_image: Image.Image, classifier: dict) -> dict:
    model     = classifier["model"]
    aug_model = classifier["aug_model"]
    has_aug   = classifier["has_aug"]

    img_resized = pil_image.convert("RGB").resize(IMG_SIZE)
    img_array   = keras_image.img_to_array(img_resized)
    img_array   = np.expand_dims(img_array, axis=0)
    img_array   = tf.keras.applications.efficientnet.preprocess_input(img_array)

    if has_aug:
        img_array = aug_model(img_array, training=False)

    predictions = model(img_array, training=False)
    scores      = predictions[0].numpy()

    pred_idx   = int(np.argmax(scores))
    top3_idx   = np.argsort(scores)[::-1][:3]
    top3       = [(CLASS_NAMES[i], float(scores[i]) * 100) for i in top3_idx]
    label      = CLASS_NAMES[pred_idx]
    confidence = float(scores[pred_idx]) * 100

    # ── Validasi ──────────────────────────────────────────────────────────────
    entropy       = -np.sum(scores * np.log(scores + 1e-9))
    max_entropy   = np.log(len(CLASS_NAMES))
    entropy_ratio = entropy / max_entropy
    top2_gap      = confidence - top3[1][1]

    is_valid = (
        confidence    >= 60.0 and
        entropy_ratio <  0.60 and
        top2_gap      >= 20.0
    )

    return {
        "label"        : label,
        "keywords_list": LABEL_TO_KEYWORDS_LIST.get(label, [label]),
        "confidence"   : confidence,
        "top3"         : top3,
        "is_valid"     : is_valid,
        "entropy_ratio": round(entropy_ratio, 3),
        "top2_gap"     : round(top2_gap, 1),
    }