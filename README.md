# 🚗 Klasifikasi Model Mobil di Indonesia Menggunakan Convolutional Neural Network (CNN)

Proyek ini merupakan implementasi **Deep Learning berbasis Convolutional Neural Network (CNN)** untuk mengklasifikasikan model mobil populer di Indonesia berdasarkan citra eksterior kendaraan. Sistem dikembangkan menggunakan arsitektur EfficientNet dengan pendekatan Transfer Learning dan Fine-Tuning untuk mengenali karakteristik visual kendaraan.

Hasil klasifikasi kemudian diintegrasikan ke dalam aplikasi berbasis web menggunakan Streamlit sebagai pendukung sistem rekomendasi mobil bekas, sehingga pengguna dapat menemukan iklan kendaraan berdasarkan gambar mobil yang diunggah.

## 📌 Project Overview

Pasar mobil bekas di Indonesia memiliki beragam merek dan model kendaraan dengan karakteristik visual yang terkadang sulit dibedakan. Proyek ini bertujuan mengembangkan sistem klasifikasi otomatis yang dapat mengenali model kendaraan berdasarkan citra visual dan menghubungkan hasil prediksi dengan informasi iklan mobil bekas.

**Tujuan utama:**
- Mengembangkan model klasifikasi citra kendaraan menggunakan CNN.
- Membandingkan performa arsitektur EfficientNet-B1 dan EfficientNet-B4.
- Menerapkan Transfer Learning, Feature Extraction, dan Fine-Tuning.
- Menganalisis interpretabilitas model menggunakan Grad-CAM.
- Mengintegrasikan model ke dalam aplikasi web untuk mendukung pencarian dan rekomendasi mobil bekas.

## 🚘 Classification Classes

Model dikembangkan untuk mengenali 10 kelas model mobil populer di Indonesia, meliputi:

| Merek | Model |
|---|---|
| Toyota | Avanza, Agya_Ayla, Fortuner, Innova, Innova Reborn, Innova Zenix, Sigra_Calya |
| Daihatsu | Xenia |
| Honda | Brio |
| Mitsubishi | Pajero Sport, Xpander |

## ⚙️ Methodology

Tahapan pengembangan model meliputi:

1. **Data Collection** – Mengumpulkan citra kendaraan dari berbagai sumber.
2. **Data Preprocessing** – Melakukan pembersihan, penyesuaian ukuran, dan persiapan dataset.
3. **Data Augmentation** – Meningkatkan variasi citra untuk membantu model mempelajari karakteristik kendaraan.
4. **Feature Extraction** – Memanfaatkan model EfficientNet pra-latih untuk mengekstraksi fitur visual.
5. **Fine-Tuning** – Menyesuaikan bobot model pra-latih agar lebih sesuai dengan karakteristik dataset kendaraan.
6. **Model Evaluation** – Mengevaluasi performa menggunakan Accuracy, Precision, Recall, F1-Score, Confusion Matrix, dan Loss.
7. **Model Interpretability** – Menggunakan Grad-CAM untuk memahami area citra yang menjadi perhatian model.
8. **Web Deployment** – Mengintegrasikan model ke dalam aplikasi berbasis Streamlit.

## 🧠 Model Architecture

Eksperimen dilakukan dengan membandingkan dua arsitektur CNN berbasis EfficientNet:

- **EfficientNet-B1**
- **EfficientNet-B4**

Kedua model menggunakan pendekatan Transfer Learning dengan bobot pra-latih, kemudian dilanjutkan melalui Feature Extraction dan Fine-Tuning untuk memperoleh performa klasifikasi yang optimal.

## 📊 Model Evaluation Results

Berdasarkan pengujian menggunakan 1.000 citra testing independen, EfficientNet-B4 menghasilkan performa terbaik.

| Evaluation Metrics | EfficientNet-B1 | EfficientNet-B4 |
|---|---:|---:|
| Test Accuracy | 94.20% | **99.10%** |
| Macro Precision | 0.94 | **0.99** |
| Macro Recall | 0.94 | **0.99** |
| Macro F1-Score | 0.94 | **0.99** |
| Misclassified Images | 58 | **10** |

<details>
<summary><b>Model Performance Summary</b></summary>

EfficientNet-B4 menghasilkan akurasi pengujian sebesar **99.10%**, dengan hanya 10 kesalahan klasifikasi dari 1.000 citra pengujian. Hasil tersebut menunjukkan kemampuan klasifikasi dan generalisasi yang lebih baik dibandingkan EfficientNet-B1.

</details>

## 🔍 Model Interpretability with Grad-CAM

Grad-CAM (Gradient-weighted Class Activation Mapping) digunakan untuk menganalisis area visual yang menjadi fokus perhatian model ketika melakukan klasifikasi.

Analisis dilakukan pada:
- **Correct Prediction:** Mengevaluasi fokus perhatian model pada citra kendaraan yang berhasil diklasifikasikan.
- **Misclassification:** Menganalisis penyebab kesalahan prediksi, terutama akibat kemiripan karakteristik visual, variasi sudut pandang, dan jarak pengambilan gambar.

## 🌐 Web Application

Model EfficientNet-B4 diintegrasikan menggunakan Streamlit untuk membangun aplikasi klasifikasi dan rekomendasi mobil bekas.

Fitur utama aplikasi:
- Upload gambar kendaraan.
- Prediksi model mobil secara otomatis.
- Menampilkan confidence score hasil klasifikasi.
- Menampilkan rekomendasi iklan mobil bekas berdasarkan hasil prediksi.
- Validasi prediksi untuk membantu menangani citra di luar distribusi dataset.

## 🛠️ Technologies & Tools

- **Programming Language:** Python
- **Deep Learning:** TensorFlow / Keras
- **Computer Vision:** OpenCV
- **Data Processing:** NumPy, Pandas
- **Data Visualization:** Matplotlib, Seaborn
- **Model Interpretation:** Grad-CAM
- **Web Framework:** Streamlit
- **Development Environment:** Jupyter Notebook, Visual Studio Code
- **Version Control:** Git & GitHub


## 🚀 Installation & Usage

1. Clone repository:

```bash
git clone https://github.com/USERNAME/Tugas-Akhir-Klasifikasi-Model-Mobil-Menggunakan-CNN.git
```

2. Masuk ke direktori proyek:

```bash
cd Tugas-Akhir-Klasifikasi-Model-Mobil-Menggunakan-CNN
```

3. Buat virtual environment:

```bash
python -m venv .venv
```

4. Aktifkan virtual environment:

```bash
# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Jalankan aplikasi Streamlit (sesuaikan path dengan lokasi file aplikasi):

```bash
streamlit run app.py
```

## 🎯 Future Improvements

Beberapa pengembangan yang dapat dilakukan selanjutnya:
- Menambahkan lebih banyak kelas model dan generasi kendaraan.
- Memperluas dataset dengan variasi kondisi citra yang lebih beragam.
- Mengintegrasikan vehicle detection sebelum proses klasifikasi.
- Mengembangkan metode Out-of-Distribution Detection (OOD).
- Mengoptimalkan model untuk kebutuhan deployment yang lebih efisien.

## 👨‍💻 Author

**Reza Irwansyah Aryanto**

Alumni Sains Data – Universitas Teknologi Yogyakarta.

- GitHub: [@rezabdl](https://github.com/rezabdl)
- LinkedIn: [Reza Irwansyah Aryanto](https://www.linkedin.com/in/reza-irwansyah-aryanto-0b1483274/)

---

*Developed as part of a Final Project in Data Science, focusing on Computer Vision and Deep Learning for vehicle image classification.*
