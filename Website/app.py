import streamlit as st

st.set_page_config(
    page_title="MobilKu Online - Cari Mobil Bekas Impian Anda",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS Global ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Exo+2:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"],
.main .block-container {
    background: #020b18 !important;
    color: #e8f4ff !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0 !important;
    max-width: 100% !important;
}

[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }

/* ── NAVBAR ── */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 60px;
    background: rgba(2, 11, 24, 0.92);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(0, 200, 255, 0.15);
    position: sticky;
    top: 0;
    z-index: 999;
    box-shadow: 0 4px 30px rgba(0, 150, 255, 0.08);
}

.nav-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 1.5rem;
    color: #00d4ff;
    text-decoration: none;
    letter-spacing: 1px;
}

.nav-logo-icon {
    width: 42px;
    height: 42px;
    background: linear-gradient(135deg, #0066ff, #00d4ff);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
}

.nav-logo-text span {
    display: block;
    line-height: 1;
}
.nav-logo-text .main-name { color: #ffffff; font-size: 1.3rem; }
.nav-logo-text .sub-name  { color: #00d4ff; font-size: 0.75rem; font-weight: 500; letter-spacing: 3px; }

.nav-links {
    display: flex;
    align-items: center;
    gap: 36px;
    list-style: none;
}

.nav-links a {
    color: #a0c8e0;
    text-decoration: none;
    font-family: 'Exo 2', sans-serif;
    font-weight: 500;
    font-size: 0.95rem;
    letter-spacing: 0.5px;
    transition: all 0.25s;
    position: relative;
    padding-bottom: 4px;
}

.nav-links a::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 0; height: 2px;
    background: linear-gradient(90deg, #0066ff, #00d4ff);
    transition: width 0.3s ease;
    border-radius: 2px;
}
.nav-links a:hover { color: #00d4ff; }
.nav-links a:hover::after { width: 100%; }

.nav-cta {
    background: linear-gradient(135deg, #0055ff, #00aaff);
    color: white !important;
    padding: 9px 22px;
    border-radius: 25px;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    box-shadow: 0 0 18px rgba(0, 150, 255, 0.35);
    transition: all 0.3s !important;
}
.nav-cta:hover {
    box-shadow: 0 0 28px rgba(0, 212, 255, 0.55) !important;
    transform: translateY(-1px);
}
.nav-cta::after { display: none !important; }

/* ── HERO BANNER ── */
.hero-section {
    position: relative;
    min-height: 520px;
    background:
        radial-gradient(ellipse 80% 60% at 70% 50%, rgba(0,80,200,0.35) 0%, transparent 70%),
        radial-gradient(ellipse 50% 40% at 20% 60%, rgba(0,180,255,0.12) 0%, transparent 60%),
        linear-gradient(135deg, #020b18 0%, #031530 40%, #041a3a 100%);
    overflow: hidden;
    display: flex;
    align-items: center;
    padding: 60px;
}

/* animated grid */
.hero-section::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(0,150,255,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,150,255,0.06) 1px, transparent 1px);
    background-size: 60px 60px;
    animation: gridPulse 6s ease-in-out infinite;
}

@keyframes gridPulse {
    0%,100% { opacity: 0.4; }
    50%      { opacity: 0.8; }
}

/* glowing orb */
.hero-section::after {
    content: '';
    position: absolute;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(0,120,255,0.18) 0%, transparent 70%);
    top: -100px; right: 0;
    border-radius: 50%;
    animation: orbFloat 8s ease-in-out infinite;
    pointer-events: none;
}

@keyframes orbFloat {
    0%,100% { transform: translateY(0) scale(1); }
    50%      { transform: translateY(-30px) scale(1.05); }
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 520px;
    animation: fadeSlideUp 0.8s ease both;
}

@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0, 150, 255, 0.12);
    border: 1px solid rgba(0, 212, 255, 0.3);
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 0.78rem;
    color: #00d4ff;
    font-family: 'Exo 2', sans-serif;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 20px;
    animation: pulse-border 2s ease-in-out infinite;
}

@keyframes pulse-border {
    0%,100% { border-color: rgba(0,212,255,0.3); box-shadow: 0 0 0 0 rgba(0,212,255,0); }
    50%      { border-color: rgba(0,212,255,0.6); box-shadow: 0 0 12px rgba(0,212,255,0.2); }
}

.hero-badge-dot {
    width: 6px; height: 6px;
    background: #00d4ff;
    border-radius: 50%;
    animation: blink 1.5s ease-in-out infinite;
}

@keyframes blink {
    0%,100% { opacity: 1; }
    50%      { opacity: 0.3; }
}

.hero-title {
    font-family: 'Exo 2', sans-serif;
    font-size: 3.6rem;
    font-weight: 900;
    line-height: 1.05;
    margin-bottom: 18px;
    letter-spacing: -1px;
}

.hero-title .line1 { color: #ffffff; display: block; }
.hero-title .line2 {
    display: block;
    background: linear-gradient(90deg, #0088ff, #00d4ff, #7fffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    font-size: 1rem;
    color: #7ab8d4;
    line-height: 1.7;
    margin-bottom: 36px;
    font-weight: 400;
    max-width: 420px;
}

.hero-subtitle strong {
    color: #00d4ff;
    font-weight: 600;
}

.hero-image-area {
    position: absolute;
    right: 0; top: 0; bottom: 0;
    width: 55%;
    z-index: 1;
    overflow: hidden;
}

.hero-image-area img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
    opacity: 0.9;
    animation: fadeSlideRight 1s ease 0.2s both;
}

@keyframes fadeSlideRight {
    from { opacity: 0; transform: translateX(40px); }
    to   { opacity: 0.9; transform: translateX(0); }
}

/* gradient overlay on image */
.hero-image-area::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, #031530 0%, transparent 40%);
    z-index: 2;
}

/* scan lines effect */
.hero-image-area::after {
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 3px,
        rgba(0,150,255,0.03) 3px,
        rgba(0,150,255,0.03) 4px
    );
    z-index: 3;
    pointer-events: none;
}

/* ── SCAN FEATURE BADGE ── */
.scan-badge {
    position: absolute;
    top: 24px; right: 24px;
    background: rgba(0, 20, 60, 0.85);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(0, 212, 255, 0.4);
    border-radius: 16px;
    padding: 16px 22px;
    z-index: 10;
    text-align: center;
    animation: fadeSlideUp 1s ease 0.5s both;
    box-shadow: 0 0 30px rgba(0,150,255,0.2);
}

.scan-badge-icon {
    font-size: 2rem;
    display: block;
    margin-bottom: 6px;
}

.scan-badge-text {
    font-family: 'Exo 2', sans-serif;
    font-weight: 800;
    font-size: 1rem;
    color: #ffffff;
    line-height: 1.2;
    display: block;
}

.scan-badge-sub {
    font-size: 0.7rem;
    color: #00d4ff;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    display: block;
    margin-top: 4px;
}

/* ── CTA BUTTON AREA ── */
.cta-section {
    background: linear-gradient(180deg, #020b18 0%, #031530 50%, #020b18 100%);
    padding: 70px 60px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.cta-section::before {
    content: '';
    position: absolute;
    width: 800px; height: 300px;
    background: radial-gradient(ellipse, rgba(0,100,255,0.12) 0%, transparent 70%);
    left: 50%; top: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
}

.cta-heading {
    font-family: 'Exo 2', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #7ab8d4;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 14px;
}

.cta-title {
    font-family: 'Exo 2', sans-serif;
    font-size: 2.4rem;
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 16px;
    line-height: 1.2;
}

.cta-title span {
    background: linear-gradient(90deg, #0088ff, #00d4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.cta-desc {
    color: #7ab8d4;
    font-size: 1rem;
    margin-bottom: 44px;
    line-height: 1.7;
}

.cta-btn-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
}

.btn-primary {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: linear-gradient(135deg, #0055ff, #00aaff);
    color: #ffffff !important;
    text-decoration: none;
    font-family: 'Exo 2', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    padding: 16px 40px;
    border-radius: 50px;
    box-shadow: 0 0 30px rgba(0, 150, 255, 0.45), 0 8px 24px rgba(0, 80, 200, 0.3);
    transition: all 0.3s ease;
    letter-spacing: 0.5px;
    position: relative;
    overflow: hidden;
    cursor: pointer;
    border: none;
}

.btn-primary::before {
    content: '';
    position: absolute;
    top: -50%; left: -60%;
    width: 60%; height: 200%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
    transform: skewX(-25deg);
    transition: left 0.6s;
}
.btn-primary:hover::before { left: 120%; }
.btn-primary:hover {
    box-shadow: 0 0 50px rgba(0, 200, 255, 0.6), 0 12px 36px rgba(0, 100, 200, 0.4);
    transform: translateY(-3px);
}

.btn-secondary {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: transparent;
    color: #a0c8e0 !important;
    text-decoration: none;
    font-family: 'Exo 2', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    padding: 15px 36px;
    border-radius: 50px;
    border: 1.5px solid rgba(0, 150, 255, 0.4);
    transition: all 0.3s ease;
    cursor: pointer;
}
.btn-secondary:hover {
    border-color: #00d4ff;
    color: #00d4ff !important;
    background: rgba(0, 150, 255, 0.07);
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.15);
}

/* ── STATS ── */
.stats-bar {
    display: flex;
    justify-content: center;
    gap: 60px;
    margin-top: 56px;
    padding-top: 40px;
    border-top: 1px solid rgba(0, 150, 255, 0.12);
    flex-wrap: wrap;
}

.stat-item { text-align: center; }

.stat-number {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #0088ff, #00d4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: block;
    line-height: 1;
    margin-bottom: 6px;
}

.stat-label {
    font-size: 0.82rem;
    color: #5a8aaa;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 500;
}

/* ── FEATURES STRIP ── */
.features-strip {
    background: rgba(0, 40, 100, 0.08);
    border-top: 1px solid rgba(0, 150, 255, 0.1);
    border-bottom: 1px solid rgba(0, 150, 255, 0.1);
    padding: 28px 60px;
    display: flex;
    justify-content: center;
    gap: 56px;
    flex-wrap: wrap;
}

.feature-item {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #8ab8cc;
    font-size: 0.88rem;
    font-family: 'Exo 2', sans-serif;
    font-weight: 500;
}

.feature-icon {
    width: 32px; height: 32px;
    background: rgba(0, 150, 255, 0.1);
    border: 1px solid rgba(0, 150, 255, 0.2);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
}

/* ── FOOTER ── */
.site-footer {
    background: #010810;
    border-top: 1px solid rgba(0, 150, 255, 0.1);
    padding: 32px 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
}

.footer-copy {
    color: #3a5a6e;
    font-size: 0.82rem;
}

.footer-links {
    display: flex;
    gap: 24px;
}

.footer-links a {
    color: #3a5a6e;
    text-decoration: none;
    font-size: 0.82rem;
    transition: color 0.2s;
}
.footer-links a:hover { color: #00d4ff; }

/* ── STREAMLIT ELEMENT CLEANUP ── */
[data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stMarkdownContainer"] { padding: 0 !important; }
div.stMarkdown { padding: 0 !important; }
section.main > div { padding: 0 !important; }
.element-container { margin: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── NAVBAR ──────────────────────────────────────────────────────────────────
st.markdown("""
<nav class="navbar">
  <a href="#" class="nav-logo">
    <div class="nav-logo-text">
      <span class="main-name">MOBILKU</span>
      <span class="sub-name">ONLINE</span>
    </div>
  </a>
  <ul class="nav-links">
    <li><a href="#"> Home</a></li>
    <li><a href="/page_search" target="_self"> Cari Iklan</a></li>
  </ul>
</nav>
""", unsafe_allow_html=True)

# ── HERO BANNER ──────────────────────────────────────────────────────────────
# Encode gambar banner ke base64
import base64
from pathlib import Path

def img_to_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

banner_b64 = img_to_base64(r"D:\@ File Tugas Akhir\Website\asset\Gemini_Generated_Image_85lwq185lwq185lw.png")

st.markdown(f"""
<section class="hero-section">
  <!-- Hero image area -->
  <div class="hero-image-area">
    <img src="data:image/png;base64,{banner_b64}" alt="Cari Mobil Bekas Berdasarkan Foto" />
  </div>

  <!-- Scan badge top-right -->
  <div class="scan-badge">
    <span class="scan-badge-text">SCAN FOTO<br>MOBIL &</span>
    <span class="scan-badge-sub">TEMUKAN!</span>
  </div>

  <!-- Text content -->
  <div class="hero-content">
    <div class="hero-badge">
      <span class="hero-badge-dot"></span>
      Teknologi AI Terbaru
    </div>
    <h1 class="hero-title">
      <span class="line1">CARI MOBIL BEKAS</span>
      <span class="line2">IMPIAN ANDA!</span>
    </h1>
    <p class="hero-subtitle">
      Temukan mobil bekas impian Anda dengan <strong>teknologi pencarian berbasis foto</strong>.
      Cukup upload foto mobil yang Anda inginkan — AI kami akan mengenali dan mencarikannya untuk Anda!
    </p>
  </div>
</section>
""", unsafe_allow_html=True)

# ── FEATURES STRIP ───────────────────────────────────────────────────────────
st.markdown("""
<div class="features-strip">
  <div class="feature-item">
    <span>Pencarian Berbasis AI</span>
  </div>
  <div class="feature-item">
    <span>Identifikasi dari Foto</span>
  </div>
  <div class="feature-item">
    <span>Terverifikasi & Terpercaya</span>
  </div>
  <div class="feature-item">
    <span>Harga Terbaik</span>
  </div>
  <div class="feature-item">
    <span>Transaksi Aman</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── CTA SECTION ──────────────────────────────────────────────────────────────
st.markdown("""
<section class="cta-section">
  <p class="cta-heading"> Mulai Sekarang</p>
  <h2 class="cta-title">Temukan Mobil Impian Anda<br><span>dengan Sekali Scan!</span></h2>
  <p class="cta-desc">
    Tidak perlu bingung mencari nama model atau spesifikasi.<br>
    Upload foto, dan biarkan AI kami bekerja untuk Anda.
  </p>

  <div class="cta-btn-wrapper">
    <a href="/page_search" target="_self" class="btn-primary">
      &nbsp; Mulai Cari Sekarang
    </a>
  </div>

  <!-- Stats Bar -->
  <div class="stats-bar">
    <div class="stat-item">
      <span class="stat-number">50.000+</span>
      <span class="stat-label">Unit Mobil Tersedia</span>
    </div>
    <div class="stat-item">
      <span class="stat-number">120+</span>
      <span class="stat-label">Kota di Indonesia</span>
    </div>
    <div class="stat-item">
      <span class="stat-number">98%</span>
      <span class="stat-label">Akurasi AI Scan</span>
    </div>
    <div class="stat-item">
      <span class="stat-number">200rb+</span>
      <span class="stat-label">Pengguna Puas</span>
    </div>
  </div>
</section>
""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<footer class="site-footer">
  <span class="footer-copy">© 2025 MobilKu Online. Seluruh hak cipta dilindungi.</span>
  <div class="footer-links">
    <a href="#">Kebijakan Privasi</a>
    <a href="#">Syarat & Ketentuan</a>
    <a href="#">Bantuan</a>
    <a href="#">Hubungi Kami</a>
  </div>
</footer>
""", unsafe_allow_html=True)