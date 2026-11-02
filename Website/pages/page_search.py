import streamlit as st
from PIL import Image
import random
import sys, os

import base64

def _img_to_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

LOGO_PATH = r"D:\@ File Tugas Akhir\Website\asset\Gemini_Generated_Image_280usb280usb280u.png"
try:
    LOGO_B64 = _img_to_base64(LOGO_PATH)
    LOGO_TAG = f'<img src="data:image/png;base64,{LOGO_B64}" style="width:42px;height:42px;object-fit:cover;border-radius:10px;box-shadow:0 0 20px rgba(0,212,255,0.4);">'
except Exception:
    # fallback emoji jika file tidak ditemukan
    LOGO_TAG = '<div class="nav-logo-icon">🚗</div>'
# Hardcode path utils secara absolut
_UTILS_DIR = r"D:\@ File Tugas Akhir\Website\utils"
if _UTILS_DIR not in sys.path:
    sys.path.insert(0, _UTILS_DIR)

_CLASSIFIER_AVAILABLE = False
_CLASSIFIER_IMPORT_ERROR = None
try:
    from classifier import load_classifier, predict as clf_predict
    _CLASSIFIER_AVAILABLE = True
except Exception as e:
    _CLASSIFIER_IMPORT_ERROR = str(e)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MobilKu Online - Cari Iklan",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Exo+2:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"],
.main .block-container {
    background: #0a1929 !important;
    color: #a0c8e0 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0 !important;
    max-width: 100% !important;
}

[data-testid="stHeader"]  { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

.navbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 18px 60px;
    background:rgba(10, 25, 41, 0.85);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(0, 200, 255, 0.15);
    position: fixed; top: 0; left: 0; right: 0; z-index: 999;
    box-shadow: 0 4px 30px rgba(255,255,255);
}
[data-testid="stAppViewContainer"] > section[data-testid="stMain"] {
    padding-top: 72px !important;
}
.nav-logo {
    display: flex; align-items: center; gap: 10px;
    font-family: 'Rajdhani', sans-serif; font-weight: 700;
    font-size: 1.5rem; color: #00d4ff; text-decoration: none; letter-spacing: 1px;
}
.nav-logo-icon {
    width: 42px; height: 42px;
    background: linear-gradient(135deg, #0066ff, #00d4ff);
    border-radius: 10px; display: flex; align-items: center;
    justify-content: center; font-size: 1.3rem;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
}
.nav-logo-text span { display: block; line-height: 1; }
.nav-logo-text .main-name { color: #ffffff; font-size: 1.3rem; }
.nav-logo-text .sub-name  { color: #00d4ff; font-size: 0.75rem; font-weight: 500; letter-spacing: 3px; }
.nav-links { display: flex; align-items: center; gap: 36px; list-style: none; }
.nav-links a {
    color: #a0c8e0; text-decoration: none;
    font-family: 'Exo 2', sans-serif; font-weight: 500;
    font-size: 0.95rem; letter-spacing: 0.5px; transition: all 0.25s;
    position: relative; padding-bottom: 4px;
}
.nav-links a::after {
    content: ''; position: absolute; bottom: 0; left: 0;
    width: 0; height: 2px;
    background: linear-gradient(90deg, #0066ff, #00d4ff);
    transition: width 0.3s ease; border-radius: 2px;
}
.nav-links a:hover { color: #00d4ff; }
.nav-links a:hover::after, .nav-links a.active::after { width: 100%; }
.nav-links a.active { color: #00d4ff; }

.filter-panel-header {
    font-family: 'Exo 2', sans-serif; font-size: 0.72rem;
    font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px;
    color: #00d4ff; margin-bottom: 1rem;
}
.page-title {
    font-family: 'Exo 2', sans-serif; font-size: 1.6rem;
    font-weight: 800; color: #ffffff; margin-bottom: 4px; letter-spacing: -0.5px;
}
.page-title span {
    background: linear-gradient(90deg, #0088ff, #00d4ff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.page-subtitle { font-size: 0.85rem; color: #5a8aaa; margin-bottom: 1.2rem; }

.photo-tag {
    display: inline-flex; align-items: center; gap: 0.5rem;
    background: rgba(0, 150, 255, 0.1); border: 1px solid rgba(0, 212, 255, 0.25);
    border-radius: 8px; padding: 0.4rem 0.8rem; font-size: 0.8rem;
    color: #00d4ff; font-weight: 600; margin-bottom: 0.75rem;
    font-family: 'Exo 2', sans-serif;
}

.car-card {
    background: rgba(0, 150, 255, 0.04); border: 1px solid rgba(0, 150, 255, 0.12);
    border-radius: 14px; padding: 1.1rem 1.25rem;
    display: flex; flex-direction: column; gap: 0.6rem;
    transition: all 0.25s; position: relative; overflow: hidden; margin-bottom: 0.5rem;
}
.car-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #0066ff, #00d4ff, transparent);
    opacity: 0; transition: opacity 0.25s;
}
.car-card:hover {
    border-color: rgba(0, 200, 255, 0.3); background: rgba(0, 150, 255, 0.07);
    transform: translateY(-2px); box-shadow: 0 8px 32px rgba(0, 100, 255, 0.15);
}
.car-card:hover::before { opacity: 1; }
.card-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 0.75rem; }
.car-title { font-family: 'Exo 2', sans-serif; font-size: 1rem; font-weight: 700; color: #e8f4ff; line-height: 1.2; }
.car-badge {
    font-size: 0.68rem; font-weight: 700; padding: 0.25rem 0.6rem; border-radius: 6px;
    background: rgba(0, 150, 255, 0.12); color: #00d4ff;
    border: 1px solid rgba(0, 212, 255, 0.25); white-space: nowrap;
    text-transform: uppercase; letter-spacing: 0.5px; flex-shrink: 0;
}
.card-meta { display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; }
.meta-item { font-size: 0.77rem; color: #4a7a94; display: flex; align-items: center; gap: 0.3rem; }
.meta-sep { color: #1a3a4e; }
.card-footer { display: flex; align-items: center; justify-content: space-between; margin-top: 0.3rem; }
.car-price {
    font-family: 'Rajdhani', sans-serif; font-size: 1.2rem; font-weight: 700;
    background: linear-gradient(135deg, #0088ff, #00d4ff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; letter-spacing: -0.5px;
}
.view-btn {
    padding: 0.45rem 1rem; background: transparent;
    border: 1.5px solid rgba(0, 150, 255, 0.35); border-radius: 8px;
    color: #00d4ff; font-family: 'Exo 2', sans-serif; font-size: 0.78rem;
    font-weight: 700; cursor: pointer; text-decoration: none;
    transition: all 0.2s; display: inline-flex; align-items: center; gap: 0.3rem;
}
.view-btn:hover {
    background: rgba(0, 150, 255, 0.1); border-color: #00d4ff;
    box-shadow: 0 0 12px rgba(0, 212, 255, 0.2);
}
.results-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 0.75rem; padding-bottom: 0.6rem;
    border-bottom: 1px solid rgba(0, 150, 255, 0.1);
}
.results-count { font-family: 'Exo 2', sans-serif; font-size: 0.82rem; color: #4a7a94; font-weight: 500; }
.results-count strong { color: #00d4ff; }

/* Modal */
.modal-box {
    background: rgba(255, 255, 255, 0.95); border: 1.5px solid rgba(0, 150, 255, 0.25);
    border-radius: 16px; padding: 1.5rem; margin-top: 1rem;
    box-shadow: 0 16px 50px rgba(0, 80, 200, 0.2);
}
.modal-title { font-family: 'Exo 2', sans-serif; font-size: 1.1rem; font-weight: 800; color: #e8f4ff; margin-bottom: 0.3rem; }
.modal-sub   { font-size: 0.82rem; color: #4a7a94; margin-bottom: 1rem; line-height: 1.5; }
.detected-box {
    background: rgba(0, 150, 255, 0.08); border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 10px; padding: 0.8rem 1rem; margin-top: 0.8rem;
}
.detected-label { font-size: 0.7rem; color: #00d4ff; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.3rem; font-family: 'Exo 2', sans-serif; }
.detected-value { font-family: 'Exo 2', sans-serif; font-size: 1.1rem; font-weight: 800; color: #e8f4ff; }
.top3-row { display: flex; flex-direction: column; gap: 0.3rem; margin-top: 0.5rem; }
.top3-item { display: flex; align-items: center; gap: 0.6rem; }
.top3-bar-bg { flex: 1; height: 6px; background: rgba(0,150,255,0.12); border-radius: 3px; overflow: hidden; }
.top3-bar    { height: 100%; background: linear-gradient(90deg, #0066ff, #00d4ff); border-radius: 3px; }
.top3-name   { font-size: 0.78rem; color: #7ab8d4; min-width: 130px; font-family: 'Exo 2', sans-serif; font-weight: 600; }
.top3-pct    { font-size: 0.78rem; color: #00d4ff; min-width: 45px; text-align: right; font-family: 'Rajdhani', sans-serif; font-weight: 700; }

.empty-state { text-align: center; padding: 4rem 2rem; color: #1a3a4e; }
.empty-icon  { font-size: 3rem; margin-bottom: 1rem; }
.empty-text  { font-size: 0.95rem; color: #2a5a6e; }

[data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stMarkdownContainer"] { padding: 0 !important; }
div.stMarkdown { padding: 0 !important; }
section.main > div { padding: 0 !important; }
.element-container { margin: 0 !important; }

div[data-testid="stExpander"] {
    background: rgba(0, 150, 255, 0.04) !important;
    border: 1px solid rgba(0, 150, 255, 0.1) !important;
    border-radius: 10px !important; margin-bottom: 0.5rem !important;
}
div[data-testid="stExpander"] summary {
    color: #a0c8e0 !important; font-family: 'Exo 2', sans-serif !important;
    font-weight: 600 !important; font-size: 0.85rem !important;
}
div[data-testid="stExpander"] summary:hover { color: #00d4ff !important; }
div[data-testid="stExpander"] svg { fill: #4a7a94 !important; }

div[data-testid="stNumberInput"] input {
    background: rgba(0, 150, 255, 0.05) !important; border: 1px solid rgba(0, 150, 255, 0.15) !important;
    border-radius: 8px !important; color: #e8f4ff !important; font-size: 0.85rem !important;
}
div[data-testid="stTextInput"] input {
    background: rgba(0, 150, 255, 0.04) !important; border: 1.5px solid rgba(0, 150, 255, 0.15) !important;
    border-radius: 10px !important; color: #e8f4ff !important; font-size: 0.95rem !important; padding: 0.75rem 1rem !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #00d4ff !important; box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1) !important;
    background: rgba(0, 150, 255, 0.07) !important;
}
div[data-testid="stTextInput"] input::placeholder { color: #2a4a5e !important; }
div[data-testid="stCheckbox"] label { color: #7ab8d4 !important; font-size: 0.85rem !important; }
div[data-testid="stSelectbox"] > div > div {
    background: rgba(0, 150, 255, 0.05) !important; border: 1px solid rgba(0, 150, 255, 0.15) !important;
    border-radius: 8px !important; color: #e8f4ff !important; font-size: 0.85rem !important;
}
div[data-testid="stButton"] button {
    background: rgba(0, 150, 255, 0.1) !important; border: 1.5px solid rgba(0, 150, 255, 0.3) !important;
    color: #00d4ff !important; font-family: 'Exo 2', sans-serif !important;
    font-weight: 700 !important; border-radius: 10px !important; transition: all 0.2s !important;
}
div[data-testid="stButton"] button:hover {
    background: rgba(0, 150, 255, 0.18) !important; border-color: #00d4ff !important;
    box-shadow: 0 0 16px rgba(0, 212, 255, 0.2) !important; transform: translateY(-1px) !important;
}
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, #0055ff, #00aaff) !important;
    border: none !important; color: white !important;
    box-shadow: 0 4px 20px rgba(0, 150, 255, 0.35) !important;
}
div[data-testid="stFileUploader"] {
    background: rgba(0, 150, 255, 0.03) !important;
    border: 2px dashed rgba(0, 150, 255, 0.2) !important; border-radius: 12px !important;
}
label[data-testid="stWidgetLabel"] p {
    color: #4a7a94 !important; font-size: 0.75rem !important; font-weight: 600 !important;
    text-transform: uppercase !important; letter-spacing: 0.8px !important; font-family: 'Exo 2', sans-serif !important;
}
hr { border-color: rgba(0, 150, 255, 0.08) !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    "show_photo_modal": False,
    "photo_label"          : None,   # label terprediksi (nama kelas) untuk ditampilkan
    "photo_keyword_display": None,   # teks display di search bar (misal "Agya / Ayla")
    "photo_keywords_list"  : None,   # list keyword untuk OR filter (misal ["Agya","Ayla"])
    "clf_result"           : None,   # dict hasil predict() lengkap
    "classifier"           : None,   # model yang sudah di-load
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Load model (sekali per session) ──────────────────────────────────────────
if _CLASSIFIER_AVAILABLE and st.session_state.classifier is None:
    try:
        st.session_state.classifier = load_classifier()
    except Exception as e:
        st.session_state.classifier = None
        st.session_state["_model_error"] = str(e)

# Tampilkan error model jika ada (di luar spinner agar tidak hilang saat rerun)
if not _CLASSIFIER_AVAILABLE and _CLASSIFIER_IMPORT_ERROR:
    st.warning(f"Gagal import classifier.py: {_CLASSIFIER_IMPORT_ERROR}")
elif _CLASSIFIER_AVAILABLE and st.session_state.get("_model_error"):
    st.warning(f"Gagal load model: {st.session_state['_model_error']}")

# ── Sample data ───────────────────────────────────────────────────────────────
SAMPLE_CARS = [
    {"id":1,  "title":"Toyota Avanza 1.3 G MT",      "year":2021, "provinsi":"DKI Jakarta",        "kota":"Jakarta Selatan",   "harga":185000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":2,  "title":"Honda Brio RS CVT",            "year":2022, "provinsi":"Jawa Barat",          "kota":"Bandung",           "harga":215000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":3,  "title":"Suzuki Ertiga GX MT",          "year":2020, "provinsi":"DKI Jakarta",        "kota":"Jakarta Timur",     "harga":175000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":4,  "title":"Daihatsu Xenia 1.3 R MT",     "year":2019, "provinsi":"Banten",              "kota":"Tangerang",         "harga":148000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":5,  "title":"Mitsubishi Xpander Cross AT",  "year":2023, "provinsi":"Jawa Timur",          "kota":"Surabaya",          "harga":298000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":6,  "title":"Toyota Rush S AT",             "year":2021, "provinsi":"DKI Jakarta",        "kota":"Jakarta Barat",     "harga":258000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":7,  "title":"Honda HR-V 1.5 E CVT",        "year":2020, "provinsi":"Jawa Barat",          "kota":"Depok",             "harga":235000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":8,  "title":"Daihatsu Terios R AT",         "year":2022, "provinsi":"Kalimantan Selatan",  "kota":"Banjarmasin",       "harga":218000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":9,  "title":"Suzuki Baleno Hatchback AT",   "year":2019, "provinsi":"Banten",              "kota":"Tangerang Selatan", "harga":168000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":10, "title":"Toyota Innova 2.0 G AT",       "year":2021, "provinsi":"Jawa Tengah",         "kota":"Semarang",          "harga":320000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":11, "title":"Honda Jazz RS CVT",            "year":2020, "provinsi":"DKI Jakarta",        "kota":"Jakarta Pusat",     "harga":198000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":12, "title":"Toyota Calya 1.2 G MT",        "year":2023, "provinsi":"Jawa Barat",          "kota":"Bogor",             "harga":142000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":13, "title":"Daihatsu Sigra R MT",          "year":2022, "provinsi":"Jawa Barat",          "kota":"Bandung",           "harga":125000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":14, "title":"Toyota Agya 1.2 G AT",         "year":2021, "provinsi":"DKI Jakarta",        "kota":"Jakarta Selatan",   "harga":138000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":15, "title":"Daihatsu Ayla X MT",           "year":2020, "provinsi":"Banten",              "kota":"Tangerang",         "harga":110000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":16, "title":"Toyota Innova Zenix Q TSS AT", "year":2023, "provinsi":"DKI Jakarta",        "kota":"Jakarta Pusat",     "harga":498000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":17, "title":"Toyota Kijang Innova 2.0 V",   "year":2018, "provinsi":"Jawa Tengah",         "kota":"Solo",              "harga":268000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":18, "title":"Mitsubishi Pajero Sport Exceed","year":2020,"provinsi":"Jawa Timur",          "kota":"Surabaya",          "harga":430000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":19, "title":"Toyota Fortuner 2.4 VRZ AT",   "year":2022, "provinsi":"DKI Jakarta",        "kota":"Jakarta Selatan",   "harga":565000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":20, "title":"Daihatsu Xenia R AT",              "year":2023, "provinsi":"Jawa Barat",          "kota":"Bogor",             "harga":195000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},

    # Agya / Ayla
    {"id":21, "title":"Toyota Agya 1.0 E MT",              "year":2019, "provinsi":"Jawa Tengah",         "kota":"Semarang",          "harga":98000000,  "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":22, "title":"Toyota Agya GR Sport AT",           "year":2023, "provinsi":"DKI Jakarta",         "kota":"Jakarta Timur",     "harga":178000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":23, "title":"Toyota Agya 1.2 TRD AT",            "year":2020, "provinsi":"Jawa Barat",          "kota":"Bekasi",            "harga":142000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":24, "title":"Daihatsu Ayla 1.0 D MT",            "year":2018, "provinsi":"Banten",              "kota":"Tangerang Selatan", "harga":82000000,  "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":25, "title":"Daihatsu Ayla 1.2 R Deluxe AT",     "year":2022, "provinsi":"Jawa Timur",          "kota":"Malang",            "harga":148000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":26, "title":"Daihatsu Ayla X MT",                "year":2021, "provinsi":"Jawa Tengah",         "kota":"Yogyakarta",        "harga":112000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},

    # Avanza / Xenia
    {"id":27, "title":"Toyota Avanza 1.5 G AT",            "year":2022, "provinsi":"DKI Jakarta",         "kota":"Jakarta Utara",     "harga":218000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":28, "title":"Toyota Avanza Veloz 1.5 AT",        "year":2020, "provinsi":"Jawa Barat",          "kota":"Bandung",           "harga":198000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":29, "title":"Toyota Avanza 1.3 E MT",            "year":2018, "provinsi":"Jawa Tengah",         "kota":"Solo",              "harga":155000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":30, "title":"Daihatsu Xenia 1.5 R MT",           "year":2021, "provinsi":"Banten",              "kota":"Serang",            "harga":168000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":31, "title":"Daihatsu Xenia 1.3 X MT",           "year":2019, "provinsi":"Jawa Timur",          "kota":"Sidoarjo",          "harga":142000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":32, "title":"Daihatsu Xenia 1.5 R Deluxe AT",    "year":2023, "provinsi":"Kalimantan Selatan",  "kota":"Banjarbaru",        "harga":208000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},

    # Brio
    {"id":33, "title":"Honda Brio Satya E MT",             "year":2019, "provinsi":"Jawa Barat",          "kota":"Depok",             "harga":148000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":34, "title":"Honda Brio RS Urbanite CVT",        "year":2023, "provinsi":"DKI Jakarta",         "kota":"Jakarta Selatan",   "harga":238000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":35, "title":"Honda Brio Satya S MT",             "year":2020, "provinsi":"Jawa Tengah",         "kota":"Magelang",          "harga":132000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":36, "title":"Honda Brio RS MT",                  "year":2021, "provinsi":"Banten",              "kota":"Cilegon",           "harga":188000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},

    # Fortuner
    {"id":37, "title":"Toyota Fortuner 2.4 G AT",          "year":2020, "provinsi":"DKI Jakarta",         "kota":"Jakarta Barat",     "harga":478000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":38, "title":"Toyota Fortuner 2.7 SRZ AT",        "year":2019, "provinsi":"Jawa Timur",          "kota":"Surabaya",          "harga":428000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":39, "title":"Toyota Fortuner GR Sport 4x4 AT",   "year":2023, "provinsi":"Jawa Barat",          "kota":"Bandung",           "harga":698000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":40, "title":"Toyota Fortuner 2.4 TRD AT",        "year":2021, "provinsi":"Jawa Tengah",         "kota":"Semarang",          "harga":518000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},

    # Innova Reborn
    {"id":41, "title":"Toyota Innova Reborn 2.0 G AT",     "year":2019, "provinsi":"DKI Jakarta",         "kota":"Jakarta Pusat",     "harga":298000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":42, "title":"Toyota Innova Reborn 2.4 V Diesel", "year":2021, "provinsi":"Jawa Timur",          "kota":"Malang",            "harga":415000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":43, "title":"Toyota Innova Reborn 2.0 Q AT",     "year":2022, "provinsi":"Jawa Barat",          "kota":"Bogor",             "harga":368000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},

    # Innova Zenix
    {"id":44, "title":"Toyota Innova Zenix 2.0 G AT",      "year":2023, "provinsi":"DKI Jakarta",         "kota":"Jakarta Selatan",   "harga":458000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":45, "title":"Toyota Innova Zenix Hybrid Q AT",   "year":2023, "provinsi":"Jawa Barat",          "kota":"Bandung",           "harga":598000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":46, "title":"Toyota Innova Zenix 2.0 V AT",      "year":2024, "provinsi":"Jawa Tengah",         "kota":"Solo",              "harga":498000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},

    # Kijang Innova
    {"id":47, "title":"Toyota Kijang Innova 2.0 G MT",     "year":2016, "provinsi":"Jawa Tengah",         "kota":"Magelang",          "harga":218000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":48, "title":"Toyota Kijang Innova 2.5 G Diesel", "year":2015, "provinsi":"Jawa Timur",          "kota":"Gresik",            "harga":235000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":49, "title":"Toyota Kijang Innova 2.0 V AT",     "year":2017, "provinsi":"DKI Jakarta",         "kota":"Jakarta Timur",     "harga":258000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},

    # Pajero Sport
    {"id":50, "title":"Mitsubishi Pajero Sport Dakar AT",  "year":2019, "provinsi":"DKI Jakarta",         "kota":"Jakarta Selatan",   "harga":468000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":51, "title":"Mitsubishi Pajero Sport GLX MT",    "year":2018, "provinsi":"Jawa Barat",          "kota":"Bekasi",            "harga":368000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":52, "title":"Mitsubishi Pajero Sport Rockford AT","year":2022,"provinsi":"Jawa Timur",          "kota":"Surabaya",          "harga":698000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":53, "title":"Mitsubishi Pajero Sport Dakar 4x4", "year":2021, "provinsi":"Jawa Tengah",         "kota":"Semarang",          "harga":548000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},

    # Sigra / Calya
    {"id":54, "title":"Daihatsu Sigra 1.2 R MT",           "year":2020, "provinsi":"Jawa Barat",          "kota":"Cimahi",            "harga":118000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":55, "title":"Daihatsu Sigra 1.2 R Deluxe AT",    "year":2022, "provinsi":"DKI Jakarta",         "kota":"Jakarta Utara",     "harga":142000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":56, "title":"Daihatsu Sigra 1.0 D MT",           "year":2018, "provinsi":"Banten",              "kota":"Tangerang",         "harga":95000000,  "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":57, "title":"Toyota Calya 1.2 E MT",             "year":2019, "provinsi":"Jawa Tengah",         "kota":"Yogyakarta",        "harga":108000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":58, "title":"Toyota Calya 1.2 G AT",             "year":2021, "provinsi":"Jawa Timur",          "kota":"Malang",            "harga":135000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":59, "title":"Toyota Calya 1.2 G MT",             "year":2020, "provinsi":"Kalimantan Selatan",  "kota":"Banjarmasin",       "harga":112000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},

    # Xpander
    {"id":60, "title":"Mitsubishi Xpander 1.5 GLS MT",     "year":2019, "provinsi":"DKI Jakarta",         "kota":"Jakarta Barat",     "harga":218000000, "transmisi":"Manual",    "link":"https://www.olx.co.id"},
    {"id":61, "title":"Mitsubishi Xpander Ultimate AT",    "year":2022, "provinsi":"Jawa Barat",          "kota":"Bandung",           "harga":298000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":62, "title":"Mitsubishi Xpander Cross AT",       "year":2021, "provinsi":"Jawa Tengah",         "kota":"Solo",              "harga":278000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":63, "title":"Mitsubishi Xpander 1.5 Exceed AT",  "year":2020, "provinsi":"Jawa Timur",          "kota":"Sidoarjo",          "harga":248000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
    {"id":64, "title":"Mitsubishi Xpander Cross Rockford", "year":2023, "provinsi":"DKI Jakarta",         "kota":"Jakarta Selatan",   "harga":358000000, "transmisi":"Automatic", "link":"https://www.olx.co.id"},
]

LOKASI = {
    "Semua Provinsi": {},
    "DKI Jakarta":   {"Semua Kota":[], "Jakarta Selatan":[], "Jakarta Timur":[], "Jakarta Barat":[], "Jakarta Utara":[], "Jakarta Pusat":[]},
    "Jawa Barat":    {"Semua Kota":[], "Bandung":[], "Depok":[], "Bogor":[], "Bekasi":[], "Cimahi":[]},
    "Banten":        {"Semua Kota":[], "Tangerang":[], "Tangerang Selatan":[], "Cilegon":[], "Serang":[]},
    "Jawa Timur":    {"Semua Kota":[], "Surabaya":[], "Malang":[], "Sidoarjo":[], "Gresik":[]},
    "Jawa Tengah":   {"Semua Kota":[], "Semarang":[], "Solo":[], "Yogyakarta":[], "Magelang":[]},
    "Kalimantan Selatan": {"Semua Kota":[], "Banjarmasin":[], "Banjarbaru":[], "Martapura":[]},
}

# ── NAVBAR ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<nav class="navbar">
  <a href="/" target="_self" class="nav-logo">
    {LOGO_TAG}
    <div class="nav-logo-text">
      <span class="main-name">MOBILKU</span>
      <span class="sub-name">ONLINE</span>
    </div>
  </a>
  <ul class="nav-links">
    <li><a href="/" target="_self">Home</a></li>
    <li><a href="/page_search" target="_self" class="active">Cari Iklan</a></li>
  </ul>
</nav>
""", unsafe_allow_html=True)

# ── LAYOUT ────────────────────────────────────────────────────────────────────
col_filter, col_main = st.columns([1, 3], gap="small")

# ════════════════════════════════════════════════════════
# LEFT — Filter Panel
# ════════════════════════════════════════════════════════
with col_filter:
    st.markdown("<div style='padding:1.4rem 0.8rem 0;'>", unsafe_allow_html=True)

    if st.button("Cari dari Foto", use_container_width=True, type="primary"):
        st.session_state.show_photo_modal = True
        st.rerun()

    st.markdown("<hr style='margin:1rem 0;'>", unsafe_allow_html=True)
    st.markdown("<p class='filter-panel-header'>Filter Pencarian</p>", unsafe_allow_html=True)

    with st.expander("Tahun", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            tahun_min = st.number_input("Min", min_value=1990, max_value=2026, value=2015, step=1, key="tahun_min", label_visibility="collapsed")
            st.caption("Min tahun")
        with c2:
            tahun_max = st.number_input("Max", min_value=1990, max_value=2026, value=2025, step=1, key="tahun_max", label_visibility="collapsed")
            st.caption("Max tahun")

    with st.expander("Harga (Rp) dalam Juta", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            harga_min = st.number_input("Min", min_value=0, max_value=5000, value=0, step=10, key="harga_min", label_visibility="collapsed")
            st.caption("Min (juta Rp)")
        with c2:
            harga_max = st.number_input("Max", min_value=0, max_value=5000, value=500, step=10, key="harga_max", label_visibility="collapsed")
            st.caption("Max (juta Rp)")

    with st.expander("Transmisi", expanded=True):
        cb_auto   = st.checkbox("Automatic", key="cb_auto")
        cb_manual = st.checkbox("Manual",    key="cb_manual")

    with st.expander("Lokasi", expanded=True):
        provinsi_list = list(LOKASI.keys())
        sel_provinsi  = st.selectbox("Provinsi", provinsi_list, key="sel_provinsi", label_visibility="collapsed")
        st.caption("Pilih Provinsi")

        kota_list = ["Semua Kota"]
        if sel_provinsi != "Semua Provinsi" and LOKASI[sel_provinsi]:
            kota_list = list(LOKASI[sel_provinsi].keys())

        sel_kota = st.selectbox(
            "Kota/Kabupaten", kota_list, key="sel_kota",
            label_visibility="collapsed",
            disabled=(sel_provinsi == "Semua Provinsi"),
        )
        st.caption("Pilih Kota / Kabupaten")

    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# RIGHT — Search & Results
# ════════════════════════════════════════════════════════
with col_main:
    st.markdown("<div style='padding:1.4rem 1.2rem 0;'>", unsafe_allow_html=True)

    st.markdown("""
    <p class="page-title">Cari <span>Iklan Mobil</span></p>
    <p class="page-subtitle">Temukan mobil bekas impian Anda dari ribuan iklan terpercaya</p>
    """, unsafe_allow_html=True)

    # Photo tag: tampil jika ada hasil klasifikasi
    if st.session_state.photo_label:
        col_tag, col_x = st.columns([10, 1])
        with col_tag:
            conf_text = ""
            if st.session_state.clf_result:
                conf_text = f" &nbsp;·&nbsp; {st.session_state.clf_result['confidence']:.1f}% confidence"
            st.markdown(f"""
            <div class="photo-tag">
              Deteksi AI: <strong>{st.session_state.photo_label}</strong>{conf_text}
            </div>""", unsafe_allow_html=True)
        with col_x:
            if st.button("✕", key="clear_photo", help="Hapus filter foto"):
                st.session_state.photo_label           = None
                st.session_state.photo_keyword_display = None
                st.session_state.photo_keywords_list   = None
                st.session_state.clf_result            = None
                st.rerun()

    # Search bar
    # Jika dari foto: filter pakai photo_keywords_list (OR match antar keyword)
    # Jika manual: filter pakai teks yang diketik
    default_search = st.session_state.get("photo_keyword_display", "") or ""
    search_q = st.text_input(
        "search",
        value=default_search,
        placeholder="Cari model kendaraan... (contoh: Toyota Avanza, Honda Brio)",
        key="search_query_input",
        label_visibility="collapsed",
    )

    # Filter logic
    photo_kw_list = st.session_state.get("photo_keywords_list", None)

    transmisi_filter = []
    if cb_auto:   transmisi_filter.append("Automatic")
    if cb_manual: transmisi_filter.append("Manual")

    def _matches_keyword(title):
        t = title.lower()
        if photo_kw_list:
            # Hasil deteksi foto: OR match, tiap keyword dicek sendiri-sendiri
            # misal ["Agya", "Ayla"] akan menampilkan mobil yang judulnya mengandung
            # kata "Agya" ATAU "Ayla"
            return any(kw.lower() in t for kw in photo_kw_list)
        # Manual search: satu string
        kw = search_q.strip().lower()
        return (not kw) or (kw in t)

    results = []
    for car in SAMPLE_CARS:
        if not _matches_keyword(car["title"]):
            continue
        if not (tahun_min <= car["year"] <= tahun_max):
            continue
        harga_juta = car["harga"] / 1_000_000
        if not (harga_min <= harga_juta <= harga_max):
            continue
        if transmisi_filter and car["transmisi"] not in transmisi_filter:
            continue
        if sel_provinsi != "Semua Provinsi" and car["provinsi"] != sel_provinsi:
            continue
        if sel_kota not in ("Semua Kota", "Semua Provinsi") and car["kota"] != sel_kota:
            continue
        results.append(car)

    st.markdown(f"""
    <div class="results-header">
      <span class="results-count">
        Ditemukan <strong>{len(results)}</strong> kendaraan
      </span>
    </div>""", unsafe_allow_html=True)

    if results:
        cols_per_row = 2
        for i in range(0, len(results), cols_per_row):
            row_cols = st.columns(cols_per_row, gap="small")
            for j, col in enumerate(row_cols):
                idx = i + j
                if idx >= len(results):
                    break
                car = results[idx]
                harga_fmt = f"Rp {car['harga']:,.0f}".replace(",", ".")
                with col:
                    st.markdown(f"""
                    <div class="car-card">
                      <div class="card-header">
                        <span class="car-title">{car['title']}</span>
                        <span class="car-badge">{car['transmisi']}</span>
                      </div>
                      <div class="card-meta">
                        <span class="meta-item">{car['year']}</span>
                        <span class="meta-sep">·</span>
                        <span class="meta-item">{car['kota']}, {car['provinsi']}</span>
                      </div>
                      <div class="card-footer">
                        <span class="car-price">{harga_fmt}</span>
                        <a href="{car['link']}" target="_blank" class="view-btn">Lihat Iklan ↗</a>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon"></div>
          <div class="empty-text">
            Tidak ada kendaraan yang sesuai filter.<br>
            Coba ubah kata kunci atau sesuaikan filter.
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# PHOTO UPLOAD MODAL
# ════════════════════════════════════════════════════════
@st.dialog("Cari Kendaraan dari Foto", width="large")
def photo_modal():
    st.markdown('<p style="font-size:0.85rem;color:#5a8aaa;">Upload foto — AI akan mengenali model kendaraan otomatis.</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload foto", type=["jpg","jpeg","png","webp"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        img = Image.open(uploaded_file).convert("RGB")
        img_col, info_col = st.columns([1,1], gap="medium")

        with img_col:
            use_real_model = _CLASSIFIER_AVAILABLE and st.session_state.classifier is not None
            if use_real_model:
                with st.spinner("Menganalisis..."):
                    clf_result = clf_predict(img, st.session_state.classifier)
            else:
                # fallback simulasi
                all_classes = [
                    ("Agya / Ayla",    ["Agya","Ayla"]),
                    ("Avanza / Xenia", ["Avanza","Xenia"]),
                    ("Brio",           ["Brio"]),
                    ("Fortuner",       ["Fortuner"]),
                    ("Innova Reborn",  ["Innova Reborn"]),
                    ("Innova Zenix",   ["Innova Zenix"]),
                    ("Kijang Innova",  ["Kijang Innova"]),
                    ("Pajero Sport",   ["Pajero Sport"]),
                    ("Sigra / Calya",  ["Sigra","Calya"]),
                    ("Xpander",        ["Xpander"]),
                ]
                picked = random.sample(all_classes, 3)
                scores = sorted([random.uniform(5,30) for _ in range(3)], reverse=True)
                scores[0] = random.uniform(60, 95)
                lbl, kw_list = picked[0]
                clf_result = {
                    "label"        : lbl,
                    "keywords_list": kw_list,
                    "confidence"   : scores[0],
                    "top3"         : [(picked[i][0], scores[i]) for i in range(3)],
                    "is_valid"     : True, 
                }

            st.image(img, caption="Foto yang diupload", use_container_width=True)
            if not use_real_model:
                st.caption("⚠️ Mode simulasi — model tidak tersedia")

        with info_col:
            # ── Cek validasi ──────────────────────────────────────────────
            if not clf_result.get("is_valid", True):
                st.markdown("""
                <div style="background:rgba(255,50,50,0.08);border:1px solid rgba(255,80,80,0.3);
                            border-radius:12px;padding:1.2rem;margin-top:0.5rem;text-align:center;">
                  <p style="font-size:1.8rem;margin-bottom:0.5rem;">🚫</p>
                  <p style="font-family:'Exo 2',sans-serif;font-weight:800;color:#ff6b6b;
                            font-size:0.95rem;margin-bottom:0.4rem;">
                    Gambar Tidak Dikenali
                  </p>
                  <p style="font-size:0.8rem;color:#7a4a4a;line-height:1.5;">
                    Foto yang Anda upload sepertinya bukan kendaraan atau Model Kendaraan yang didukung.<br>
                    Pastikan foto menampilkan mobil dengan jelas.
                  </p>
                </div>
                """, unsafe_allow_html=True)

                # Tampilkan top-3 sebagai info tambahan (greyed out)
                top3_html = '<div class="top3-row" style="opacity:0.4;">'
                for name, pct in clf_result["top3"]:
                    top3_html += f"""
                    <div class="top3-item">
                      <span class="top3-name">{name}</span>
                      <div class="top3-bar-bg">
                        <div class="top3-bar" style="width:{max(2,int(pct))}%;background:rgba(255,100,100,0.5);"></div>
                      </div>
                      <span class="top3-pct">{pct:.1f}%</span>
                    </div>"""
                top3_html += "</div>"
                st.markdown(f"""
                <div style="background:rgba(0,150,255,0.03);border:1px solid rgba(0,150,255,0.08);
                            border-radius:12px;padding:1rem;margin-top:0.8rem;">
                  <p style="font-size:0.7rem;color:#4a5a6a;font-weight:700;text-transform:uppercase;
                            letter-spacing:1px;font-family:'Exo 2',sans-serif;margin-bottom:0.6rem;">
                    Prediksi Terdekat (tidak cukup yakin)
                  </p>{top3_html}
                </div>""", unsafe_allow_html=True)

                st.markdown("<div style='margin-top:1rem;'>", unsafe_allow_html=True)
                if st.button("🔄 Upload Foto Lain", type="primary", use_container_width=True):
                    st.rerun()  # rerun dialog → file uploader reset
                st.markdown("</div>", unsafe_allow_html=True)

            else:
                # ── Hasil valid ───────────────────────────────────────────
                st.markdown(f"""
                <div class="detected-box">
                  <p class="detected-label">Hasil Deteksi AI</p>
                  <p class="detected-value">{clf_result['label']}</p>
                  <p style="font-size:0.78rem;color:#4a7a94;margin-top:0.3rem;">
                    Confidence: {clf_result['confidence']:.1f}%
                  </p>
                </div>""", unsafe_allow_html=True)

                top3_html = '<div class="top3-row">'
                for name, pct in clf_result["top3"]:
                    top3_html += f"""
                    <div class="top3-item">
                      <span class="top3-name">{name}</span>
                      <div class="top3-bar-bg">
                        <div class="top3-bar" style="width:{max(2,int(pct))}%"></div>
                      </div>
                      <span class="top3-pct">{pct:.1f}%</span>
                    </div>"""
                top3_html += "</div>"
                st.markdown(f"""
                <div style="background:rgba(0,150,255,0.04);border:1px solid rgba(0,150,255,0.12);
                            border-radius:12px;padding:1rem;margin-top:0.8rem;">
                  <p style="font-size:0.7rem;color:#00d4ff;font-weight:700;text-transform:uppercase;
                            letter-spacing:1px;font-family:'Exo 2',sans-serif;margin-bottom:0.6rem;">
                    Top-3 Prediksi
                  </p>{top3_html}
                </div>""", unsafe_allow_html=True)

                if st.button(f"🔍 Cari '{clf_result['label']}'", type="primary", use_container_width=True):
                    st.session_state.photo_label           = clf_result["label"]
                    st.session_state.photo_keyword_display = clf_result["label"]
                    st.session_state.photo_keywords_list   = clf_result["keywords_list"]
                    st.session_state.clf_result            = dict(clf_result)
                    st.session_state.show_photo_modal      = False
                    st.rerun()

if st.session_state.show_photo_modal:
    photo_modal()