import streamlit as st
import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import os
import datetime
import plotly.express as px
import html
import base64

st.set_page_config(page_title="Sistem Rekomendasi Inovasi", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "beranda"

data = pd.read_csv("fixr.csv", encoding='utf-8', low_memory=True)
data = data.dropna(subset=["judul", "sinopsis", "label"])
data = data.reset_index(drop=True)

data["gabungan"] = (data["judul"].fillna('') * 3 + " " + data["sinopsis"].fillna('')).str.strip()

vectorizer = joblib.load("tfidf_vectorizer.pkl")
model = joblib.load("model_kategori.pkl") 
tfidf_matrix = vectorizer.transform(data["gabungan"])

def rekomendasi(teks, top_n=None):
    input_vec = vectorizer.transform([teks])
    cosine_sim = cosine_similarity(input_vec, tfidf_matrix).flatten()
    hasil = data.copy()
    hasil["similarity"] = cosine_sim
    hasil = hasil.sort_values(by="similarity", ascending=False)
    return hasil if top_n is None else hasil.head(top_n)

def show_footer():
    st.markdown("""
        <style>
            .footer {
                margin-top: 3rem;
                padding-top: 1rem;
                border-top: 1px solid #ddd;
                font-size: 14px;
                text-align: center;
                color: gray;
            }
        </style>
        <div class="footer">
            © 2025 RISDA - Sistem Rekomendasi Inovasi Daerah | Built with ❤️ using Streamlit
        </div>
    """, unsafe_allow_html=True)

def get_base64_from_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_pemda = get_base64_from_image("animasi-gedung-pemerintah-0.png")
img_industri = get_base64_from_image("industri.jpg")
img_masyarakat = get_base64_from_image("masyarakat.jpg")

def halaman_beranda():
    st.markdown("""
        <style>
            .hero {
                text-align: center;
                padding: 50px 20px;
                background: linear-gradient(to right, #dbeafe, #f0f9ff);
                border-radius: 20px;
                margin-bottom: 30px;
            }
            .hero h1 {
                font-size: 44px;
                font-weight: 700;
                color: #1f2937;
            }
            .hero p {
                font-size: 18px;
                color: #333;
                margin-bottom: 25px;
            }
            .section-title {
                font-size: 28px;
                font-weight: 600;
                margin-top: 40px;
                margin-bottom: 15px;
                color: #1f2937;
            }
        </style>

        <div class="hero">
            <h1>Discover The Right Research for Local Problems</h1>
            <p>Let's explore local research that matches your region's challenges. Support collaboration between researchers and government for better solutions.</p>
        </div>
    """, unsafe_allow_html=True)

    # === Highlight Inovasi Terbaru (Grid 3 Kolom x 2 Baris) ===
    st.markdown("""
        <style>
            /* Judul dan Subjudul */
            .highlight-title-container {
                margin-bottom: 24px;
            }
            .highlight-title {
                font-size: 26px;
                font-weight: 600;
                color: #1f2937;
                border-bottom: 3px solid #1f77b4;
                padding-bottom: 6px;
                margin: 0;
                letter-spacing: 0.5px;
            }
            .highlight-subtitle {
                font-size: 14px;
                color: #666;
                margin-top: 4px;
            }

            /* Grid dan Kartu */
            .highlight-grid {
                display: grid;
                grid-template-columns: repeat(3, 2fr);
                gap: 2rem;
            }
            .highlight-card {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                padding: 16px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                transition: 0.2s ease;
            }
            .highlight-card:hover {
                transform: scale(1.01);
                border-color: #1f77b4;
            }
            .highlight-card h4 {
                font-size: 16px;
                margin: 0 0 8px 0;
                color: #111827;
            }
            .highlight-card p {
                font-size: 13px;
                color: #555;
                margin: 2px 0;
            }

            /* Responsif untuk layar kecil */
            @media screen and (max-width: 768px) {
                .highlight-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>

        <!-- Judul dan Subjudul -->
        <div class="highlight-title-container">
            <div class="highlight-title">Highlight Inovasi Terbaru</div>
            <div class="highlight-subtitle">Rekomendasi dan publikasi unggulan terbaru yang perlu kamu lihat.</div>
        </div>

        <!-- Grid Kartu Mulai -->
        <div class="highlight-grid">
    """, unsafe_allow_html=True)

    # Ambil 6 data terbaru
    latest = data.sort_values("tahun", ascending=False).head(5)

    # Render setiap kartu
    for _, row in latest.iterrows():
        st.markdown(f"""
            <div class="highlight-card">
                <h4>{row['judul']}</h4>
                <p><b>{row['tahun']}</b> — {row['nama']}</p>
                <p>{row['afiliasi']}</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


    # === Testimoni Pengguna ===
    st.markdown("""
        <style>
            .section-title {
                font-size: 26px;
                font-weight: 700;
                color: #1f2937;
                border-left: 6px solid #1f77b4;
                padding-left: 12px;
                margin-top: 40px;
                margin-bottom: 20px;
            }

            .testimonial-container {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 1.2rem;
                margin-bottom: 30px;
            }

            .testimonial-card {
                background-color: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 10px;
                padding: 20px 24px;
                box-shadow: 0 1px 4px rgba(0,0,0,0.04);
                position: relative;
            }

            .testimonial-card::before {
                content: "“";
                font-size: 60px;
                color: #1f77b4;
                position: absolute;
                top: -10px;
                left: 15px;
                line-height: 1;
                font-family: serif;
            }

            .testimonial-card p {
                font-size: 15px;
                color: #374151;
                margin-bottom: 12px;
                margin-left: 20px;
                line-height: 1.6;
            }

            .testimonial-author {
                font-size: 14px;
                font-style: italic;
                color: #6b7280;
                margin-left: 20px;
            }

            @media screen and (max-width: 768px) {
                .testimonial-container {
                    grid-template-columns: 1fr;
                }
            }
        </style>

        <div class="section-title">Pendapat Pengguna RISDA</div>

        <div class="testimonial-container">
            <div class="testimonial-card">
                <p>RISDA sangat mempermudah kami dalam menemukan referensi riset yang sesuai dengan isu lokal di wilayah kami.</p>
                <div class="testimonial-author">— Dinas Lingkungan Hidup Provinsi Jawa Tengah</div>
            </div>
            <div class="testimonial-card">
                <p>Data dan rekomendasi yang disajikan RISDA sangat membantu dalam proses perencanaan kebijakan berbasis bukti.</p>
                <div class="testimonial-author">— Bappeda Kota Makassar</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <style>
            .section-title {{
                font-size: 28px;
                font-weight: 800;
                color: #1f2937;
                margin-top: 50px;
                margin-bottom: 30px;
                text-align: center;
            }}

            .roles-container {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 1.5rem;
                margin-bottom: 40px;
            }}

            .role-box {{
                border-radius: 16px;
                padding: 16px 18px;
                background-color: #ffffff;
                box-shadow: 0 4px 10px rgba(0,0,0,0.04);
                transition: 0.3s ease;
                border: 1px solid #e5e7eb;
            }}

            .role-box:hover {{
                transform: translateY(-4px);
                box-shadow: 0 6px 16px rgba(0,0,0,0.08);
            }}

            .role-image-wrapper {{
                background-color: #000;
                width: 100%;
                height: 130px;
                border-radius: 12px;
                overflow: hidden;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 16px;
            }}

            .role-image {{
                width: 100%;
                height: 100%;
                object-fit: cover;
            }}

            .role-box h3 {{
                font-size: 18px;
                font-weight: 700;
                margin-bottom: 10px;
                color: #1f2937;
            }}

            .role-box ul {{
                padding-left: 1.2rem;
                margin: 0;
            }}

            .role-box li {{
                font-size: 14px;
                margin-bottom: 8px;
                color: #374151;
            }}

            @media screen and (max-width: 768px) {{
                .roles-container {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>

        <div class="section-title">Peran Pengguna dalam RISDA</div>

        <div class="roles-container">
            <div class="role-box">
                <div class="role-image-wrapper">
                    <img src="data:image/png;base64,{img_pemda}" class="role-image" alt="Pemerintah">
                </div>
                <h3>Pemerintah Daerah</h3>
                <ul>
                    <li>Ajukan permasalahan strategis</li>
                    <li>Dapatkan klasifikasi otomatis</li>
                    <li>Telusuri rekomendasi inovasi</li>
                    <li>Kelola dokumentasi kebijakan</li>
                </ul>
            </div>
            <div class="role-box">
                <div class="role-image-wrapper">
                    <img src="data:image/jpeg;base64,{img_industri}" class="role-image" alt="Industri">
                </div>
                <h3>Perusahaan / Industri</h3>
                <ul>
                    <li>Telusuri riset yang siap diadopsi</li>
                    <li>Identifikasi peluang teknologi</li>
                    <li>Jalin kerja sama dengan peneliti</li>
                </ul>
            </div>
            <div class="role-box">
                <div class="role-image-wrapper">
                    <img src="data:image/jpeg;base64,{img_masyarakat}" class="role-image" alt="Publik">
                </div>
                <h3>Masyarakat Umum</h3>
                <ul>
                    <li>Akses solusi atas masalah publik</li>
                    <li>Ikuti perkembangan riset lokal</li>
                    <li>Gunakan fitur pencarian inovasi</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # === CTA Buttons ===
    st.markdown("""
        <style>
            .cta-section {
                margin-top: 50px;
                padding: 30px;
                background: linear-gradient(to right, #dbeafe, #f0f9ff);
                border-radius: 20px;
                text-align: center;
            }
            .cta-section h2 {
                font-size: 26px;
                font-weight: 700;
                color: #1f2937;
                margin-bottom: 10px;
            }
            .cta-section p {
                font-size: 16px;
                color: #555;
                margin-bottom: 30px;
            }
            .cta-button-container {
                display: flex;
                justify-content: center;
                gap: 2rem;
                flex-wrap: wrap;
            }
            .cta-button {
                background-color: #1f77b4;
                color: white;
                padding: 14px 26px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                text-decoration: none;
                transition: 0.2s ease;
                border: none;
                cursor: pointer;
            }
            .cta-button.secondary {
                background-color: #10b981;
            }
            .cta-button:hover {
                background-color: #155a8a;
            }
            .cta-button.secondary:hover {
                background-color: #0d946b;
            }

            @media screen and (max-width: 768px) {
                .cta-button-container {
                    flex-direction: column;
                    gap: 1rem;
                }
            }
        </style>

        <div class="cta-section">
            <h2>Siap Mengeksplorasi Solusi Inovatif?</h2>
            <p>Pilih jalur Anda: telusuri inovasi daerah yang tersedia atau inputkan permasalahan baru untuk direkomendasikan.</p>
            <div class="cta-button-container">
                <form action="">
                    <button class="cta-button" type="submit" name="jelajahi">🔍 Jelajahi Inovasi</button>
                </form>
                <form action="">
                    <button class="cta-button secondary" type="submit" name="input">➕ Input Permasalahan</button>
                </form>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Deteksi klik tombol lewat query param palsu
    query_params = st.query_params
    if "jelajahi" in query_params:
        st.session_state.page = "research"
        st.rerun()
    elif "input" in query_params:
        st.session_state.page = "rekomendasi"
        st.rerun()

    show_footer()

def render_label_badges(label_list):
    color_map = {
        'Air Bersih & Sanitasi': '#a2d5f2',
        'Banjir': '#f8d7da',
        'Energi': '#fce38a',
        'Industri': '#cce5ff',
        'Infrastruktur': '#e2f0cb',
        'Kebakaran': '#ffcccc',
        'Kemacetan': '#f6c6ea',
        'Kemiskinan & Sosial': '#ffd3b6',
        'Kesehatan': '#d1ecf1',
        'Keselamatan': '#fff3cd',
        'Ketahanan Pangan': '#c3f584',
        'Limbah': '#ffddcc',
        'Lingkungan': '#b8f2e6',
        'Otomasi & Kontrol': '#f0e68c',
        'Pencemaran Air': '#add8e6',
        'Pendidikan': '#e2e3e5',
        'Perkotaan / Permukiman': '#b5ead7',
        'Perubahan Iklim': '#f4cccc',
        'Polusi Udara': '#ffe4e1',
        'Sampah': '#e0bbe4',
        'Transportasi': '#dadada',
        'Transportasi Laut / Maritim': '#d0f0c0',
        'Umum': '#dddddd'
    }

    badge_html = ""
    for label in label_list:
        warna = color_map.get(label.strip(), "#e2e3e5")
        badge_html += f"""
        <span style="
            background-color: {warna};
            color: #111;
            padding: 6px 12px;
            margin: 4px 6px 4px 0;
            border-radius: 14px;
            font-size: 13px;
            display: inline-block;
            white-space: nowrap;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        ">{label}</span>"""
    return f'<div style="margin-top: 8px; display: flex; flex-wrap: wrap;">{badge_html}</div>'


def label_with_emoji(label):
    emoji_map = {
        "Air Bersih & Sanitasi": "🚿",
        "Banjir": "🌊",
        "Energi": "⚡",
        "Industri": "🏭",
        "Infrastruktur": "🛣️",
        "Kebakaran": "🔥",
        "Kemacetan": "🚗",
        "Kemiskinan & Sosial": "🤝",
        "Kesehatan": "🩺",
        "Keselamatan": "🛡️",
        "Ketahanan Pangan": "🌾",
        "Limbah": "🧴",
        "Lingkungan": "🌱",
        "Otomasi & Kontrol": "🤖",
        "Pencemaran Air": "🚱",
        "Pendidikan": "📚",
        "Perkotaan / Permukiman": "🏘️",
        "Perubahan Iklim": "🌡️",
        "Polusi Udara": "🌫️",
        "Sampah": "🗑️",
        "Transportasi": "🚌",
        "Transportasi Laut / Maritim": "🚢",
        "Umum": "📌"
    }
    return f"{emoji_map.get(label, '')} {label}"

#Fungsi Inovasi
def halaman_research():
    col1, col2 = st.columns([6, 1])
    with col2:
        st.markdown("""
        <a href="https://sistem-sinergi-brin.streamlit.app/" target="_blank">
            <button style="
                background-color: #2563eb;
                color: white;
                border: none;
                padding: 8px 14px;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 600;
                font-size: 14px;
                margin-top: 10px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            ">
                🔗 SDM BRIN
            </button>
        </a>
        """, unsafe_allow_html=True)
        
    st.markdown("""
        <style>
            .judul-utama {
                font-size: 48px;
                font-weight: 900 !important;
                color: #1e293b;
                margin-bottom: 12px;
                line-height: 1.2;
            }
            .deskripsi-sub {
                font-size: 18px;
                color: #4b5563;
                margin-bottom: 30px;
            }
            .hero-section {
                background-color: #f9fafb;
                padding: 2rem 1rem;
                border-radius: 16px;
                margin-bottom: 2rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.03);
            }
        </style>

        <div class="hero-section">
            <div style="text-align: center;">
                <div class="judul-utama">RISDA Innovation & Research</div>
                <div class="deskripsi-sub">
                    Real-world solutions from diverse contributors for a better future.<br>
                    Explore a wide range of innovative works created by individuals from various backgrounds — academics, professionals, practitioners, and the broader community.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if "view_option" not in st.session_state:
        st.session_state.view_option = "Card View"

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Card View", key="btn_card_view", use_container_width=True):
            st.session_state.view_option = "Card View"
    with col2:
        if st.button("List View", key="btn_list_view", use_container_width=True):
            st.session_state.view_option = "List View"

    st.markdown(f"""
        <div style='text-align:center;margin:-10px 0 20px;font-weight:600;color:#1e40af;'>
            Saat ini menampilkan: {st.session_state.view_option}
        </div>
    """, unsafe_allow_html=True)

    view_option = st.session_state.view_option

    # Ambil semua label unik (handle format string list)
    all_labels = set()
    for lbl in data["label"]:
        try:
            labels = eval(lbl) if isinstance(lbl, str) else lbl
            all_labels.update(labels)
        except:
            continue

    # Filter Label & Urutan Tahun
    col1, col2 = st.columns([3, 2])
    with col1:
        selected_labels = st.multiselect("🔍 Filter berdasarkan Label", sorted(all_labels))
    with col2:
        sort_order = st.selectbox("Urutkan Tahun", ["Terbaru", "Terlama"])

    search = st.text_input("Cari berdasarkan judul, label, atau sinopsis")


    filtered = data.copy()

    if search:
        # === 1. Cosine similarity
        hasil_rekom = rekomendasi(search)

        # === 2. Cek sinopsis mengandung minimal satu kata dari input
        keywords = search.lower().split()  # pisahkan kata-kata
        sinopsis_match = data[data["sinopsis"].str.lower().apply(lambda text: any(k in text for k in keywords))]

        # === 3. Gabungkan hasil tanpa duplikat
        filtered = pd.concat([hasil_rekom, sinopsis_match]).drop_duplicates(subset=["judul", "sinopsis"])

    # Tetap filter label
    if selected_labels:
        def match_labels(label_raw):
            try:
                label_list = eval(label_raw) if isinstance(label_raw, str) else label_raw
                return any(lbl in label_list for lbl in selected_labels)
            except:
                return False
        filtered = filtered[filtered["label"].apply(match_labels)]

    # Urutkan berdasarkan tahun
    filtered = filtered.sort_values("tahun", ascending=(sort_order == "Terlama"))

    # # Urutkan tahun
    # filtered = filtered.sort_values("tahun", ascending=(sort_order == "Terlama"))

    # Paginasi
    per_page = 15
    total_data = len(filtered)
    total_pages = (total_data - 1) // per_page + 1

    if "page_research" not in st.session_state:
        st.session_state.page_research = 1

    page = st.session_state.page_research
    start = (page - 1) * per_page
    end = min(start + per_page, total_data)

    if view_option == "Card View":
        num_cols = 3
        rows = [filtered.iloc[i:i+num_cols] for i in range(start, end, num_cols)]

        for row_chunk in rows:
            cols = st.columns(num_cols)
            for idx, (_, row) in enumerate(row_chunk.iterrows()):
                with cols[idx]:
                    try:
                        label_list = eval(row["label"]) if isinstance(row["label"], str) else row["label"]
                    except:
                        label_list = [row["label"]]

                    # Handle label dan sinopsis aman
                    label_badges = ", ".join([label_with_emoji(lbl) for lbl in label_list])
                    sinopsis_text = html.escape(row.get('sinopsis', '-'))
                    judul = html.escape(row.get('judul', ''))
                    afiliasi = html.escape(row.get('afiliasi', ''))
                    daerah = html.escape(row.get('daerah', ''))

                    # Format nama peneliti
                    nama_peneliti = html.escape(row.get("nama", ""))
                    peneliti_list = [p.strip() for p in nama_peneliti.split(";") if p.strip()]
                    peneliti_display = "; ".join(peneliti_list[:2]) + (", dkk." if len(peneliti_list) > 2 else "")

                    # Kondisi link
                    html_link_section = ""
                    if pd.notna(row.get("link")) and str(row["link"]).startswith("http"):
                        html_link_section = f"""
                            <div style="margin-top: 8px;">
                                <a href="{row['link']}" target="_blank" style="
                                    font-size: 13px;
                                    color: #2563eb;
                                    text-decoration: none;
                                ">🔗 Link Penelitian</a>
                            </div>
                        """

                    # Render kartu
                    # Escape sinopsis text
                    sinopsis_text = html.escape(row.get('sinopsis', '-'))

                    # Kartu HTML
                    card_html = f"""
                    <div style="
                        background-color: #fdfdfd;
                        padding: 20px;
                        border-radius: 12px;
                        box-shadow: 0 1px 6px rgba(0,0,0,0.08);
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                        min-height: 480px;
                        margin-bottom: 16px;
                    ">
                        <div>
                            <h4 style="margin-bottom: 0.2rem;">{row['judul']}</h4>
                            <div style="font-size: 13px; color: #555;">
                                <b>{row['tahun']}</b> &bull; {label_badges}
                            </div>
                            <p style="font-size: 14px; margin-top: 0.8rem;">
                                <b>Peneliti:</b> {peneliti_display}<br>
                                <b>Afiliasi:</b> {row['afiliasi']}<br>
                                <b>Daerah:</b> {row['daerah']}
                            </p>
                            <div style="
                                margin-top: 14px;
                                font-size: 13px;
                                color: #374151;
                            ">
                                <b>📝 Sinopsis:</b>
                                <div style="
                                    max-height: 100px;
                                    overflow-y: auto;
                                    padding: 10px;
                                    background-color: #ffffff;
                                    border: 1px solid #e5e7eb;
                                    border-radius: 8px;
                                    margin-top: 6px;
                                ">
                                    {sinopsis_text}
                                </div>
                            </div>
                        </div>
                    </div>
                    """

                    # Tampilkan kartu
                    st.markdown(card_html, unsafe_allow_html=True)

                    # Tampilkan tombol link jika ada
                    if pd.notna(row.get("link")) and str(row["link"]).startswith("http"):
                        st.markdown(f"""
                            <div style="margin-top: -12px; margin-bottom: 12px;">
                                <a href="{row['link']}" target="_blank" style="
                                    font-size: 13px;
                                    color: #2563eb;
                                    text-decoration: none;
                                ">🔗 Link Penelitian</a>
                            </div>
                        """, unsafe_allow_html=True)

    else:
        for _, row in filtered.iloc[start:end].iterrows():
            try:
                label_list = eval(row["label"]) if isinstance(row["label"], str) else row["label"]
            except:
                label_list = [row["label"]]

            # Bagian Header: Tahun + Label
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center;
                        background-color: #f1f5f9; padding: 10px 16px; border-radius: 10px 10px 0 0;
                        border: 1px solid #e5e7eb; border-bottom: none;">
                <div style="font-weight: 600; font-size: 15px;"> {row['tahun']}</div>
                <div>{render_label_badges(label_list)}</div>
            </div>
            """, unsafe_allow_html=True)

            # Judul + Info Peneliti
            st.markdown(f"""
            <div style="border: 1px solid #e5e7eb; border-top: none; border-radius: 0 0 10px 10px;
                        background-color: #ffffff; padding: 16px 20px; margin-bottom: 20px;">
                <h4 style="margin-top: 0; margin-bottom: 8px; color: #1f2937;">{row['judul']}</h4>
                <div style="font-size: 14px; color: #374151;">
                    <b>👤 Nama:</b> {row['nama']}<br>
                    <b>📧 Email:</b> {row['email']}<br>
                    <b>🏢 Afiliasi:</b> {row['afiliasi']}<br>
                    <b>📍 Daerah:</b> {row['daerah']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Sinopsis
            with st.expander("📝 Sinopsis"):
                st.markdown(f"""
                <div style="background-color: #f9fafb; border: 1px solid #e2e8f0;
                            border-radius: 8px; padding: 12px; font-size: 14px;
                            color: #374151; max-height: 150px; overflow-y: auto;">
                    <b>Sinopsis:</b><br>{row.get('sinopsis', '-')}
                </div>

                """, unsafe_allow_html=True)

            # Tombol Link jika ada
            if pd.notna(row['link']) and row['link'].startswith("http"):
                st.markdown(f"""
                <a href="{row['link']}" target="_blank" style="
                    display: inline-block;
                    margin-top: 10px;
                    background-color: #1d4ed8;
                    color: white;
                    padding: 6px 14px;
                    font-size: 13px;
                    border-radius: 8px;
                    text-decoration: none;">
                    🔗 Kunjungi Penelitian
                </a>
                """, unsafe_allow_html=True)

            # Garis pemisah
            st.markdown("<hr style='margin: 24px 0;'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if page > 1:
            if st.button("Sebelumnya"):
                st.session_state.page_research -= 1
                st.rerun()   
    
    with col2:
        st.markdown(f"<div style='text-align:center; padding-top:6px;'>📄 Halaman {page} dari {total_pages}</div>", unsafe_allow_html=True)
    with col3:
        if page < total_pages:
            if st.button("Selanjutnya"):
                st.session_state.page_research += 1
                st.rerun()

    # Tombol Kembali
    if st.button("🔙 Beranda", use_container_width=True):
        st.session_state.page = "beranda"
        st.rerun()

    show_footer()

# Lokasi file CSV
USER_DB_PATH = "users.csv"
# Fungsi untuk load data user
def load_users():
    if os.path.exists(USER_DB_PATH):
        return pd.read_csv(USER_DB_PATH)
    else:
        return pd.DataFrame(columns=["username", "password", "name", "email", "phone", "institution"])

# Fungsi untuk menyimpan user baru
def save_user(username, password, name, email, phone, institution):
    users = load_users()
    if username in users["username"].values:
        return False  # Username sudah ada

    new_user = pd.DataFrame([{
        "username": username,
        "password": password,
        "name": name,
        "email": email,
        "phone": phone,
        "institution": institution
    }])
    updated_users = pd.concat([users, new_user], ignore_index=True)
    updated_users.to_csv(USER_DB_PATH, index=False)
    return True

# === Halaman input pemerintah ===
def halaman_pemerintah():
    if not st.session_state.get("is_logged_in", False):
        st.markdown("""
            <style>
                .login-header {
                    text-align: center;
                    margin-top: 20px;
                    margin-bottom: 10px;
                }
                .login-header h2 {
                    font-size: 28px;
                    font-weight: bold;
                    color: #1f2937;
                    margin-bottom: 5px;
                }
                .login-header p {
                    font-size: 15px;
                    color: #666;
                    margin: 0;
                }
                .form-section {
                    padding: 20px;
                    background-color: #f8fafc;
                    border-radius: 12px;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
                    margin-top: 20px;
                }
            </style>
        """, unsafe_allow_html=True)


        if "menu" not in st.session_state:
            st.session_state.menu = "Log in"

        menu = st.session_state.menu

        if menu == "Log in":
            st.markdown("""
                <style>
                    .auth-hero {
                        text-align: center;
                        padding: 40px 20px;
                        background: linear-gradient(to right, #e0f2fe, #f0f9ff);
                        border-radius: 18px;
                        margin-top: 30px;
                        margin-bottom: 25px;
                    }
                    .auth-hero h2 {
                        font-size: 32px;
                        font-weight: 800;
                        color: #1e3a8a;
                        margin-bottom: 10px;
                    }
                    .auth-hero p {
                        font-size: 16px;
                        color: #374151;
                        margin: 0;
                    }
                </style>

                <div class="auth-hero">
                    <h2>Masuk ke RISDA</h2>
                    <p>Masukkan username dan password Anda untuk mengakses fitur pemerintah daerah.</p>
                </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                masuk_clicked = st.button("Masuk", use_container_width=True)
            with col2:
                daftar_clicked = st.button("Daftar", use_container_width=True)


            if masuk_clicked:
                st.session_state.menu = "Log in"
            elif daftar_clicked:
                st.session_state.menu = "Sign in"
                
            with st.form("login_form"):
                with st.container():
                    st.markdown('<div class="form-section">', unsafe_allow_html=True)
                    username = st.text_input("👤 Username")
                    password = st.text_input("🔒 Password", type="password")
                    st.markdown('</div>', unsafe_allow_html=True)
                    submitted = st.form_submit_button("Masuk")

            if submitted:
                users = load_users()
                user = users[(users["username"] == username) & (users["password"] == password)]
                if not user.empty:
                    st.session_state.is_logged_in = True
                    st.session_state.current_user = username
                    st.success(f"✅ Berhasil masuk sebagai **{username}**!")
                    users = load_users()
                    user_info = users[users["username"] == username].iloc[0]
                    st.session_state.nama_instansi = user_info["institution"]
                    st.rerun()
                else:
                    st.error("❌ Username atau password salah.")

        elif menu == "Sign in":
            st.markdown("""
                <style>
                    .auth-hero {
                        text-align: center;
                        padding: 40px 20px;
                        background: linear-gradient(to right, #ede9fe, #f5f3ff);
                        border-radius: 18px;
                        margin-top: 30px;
                        margin-bottom: 25px;
                    }
                    .auth-hero h2 {
                        font-size: 32px;
                        font-weight: 800;
                        color: #6b21a8;
                        margin-bottom: 10px;
                    }
                    .auth-hero p {
                        font-size: 16px;
                        color: #4b5563;
                        margin: 0;
                    }
                </style>

                <div class="auth-hero">
                    <h2>Daftar Akun Pemerintah</h2>
                    <p>Silakan isi data lengkap untuk mendaftarkan akun instansi Anda.</p>
                </div>
            """, unsafe_allow_html=True)


            with st.form("register_form"):
                with st.container():
                    st.markdown("#### 👤 Informasi Pribadi")
                    st.markdown('<div class="form-section">', unsafe_allow_html=True)
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("Nama Lengkap", placeholder="Contoh: Budi Santoso")
                        email = st.text_input("Email", placeholder="Contoh: budi@email.com")
                    with col2:
                        phone = st.text_input("Nomor HP", placeholder="08123456789")
                        institution = st.text_input("Instansi", placeholder="Contoh: Dinas Pendidikan")
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.markdown("#### 🔐 Informasi Login")
                    st.markdown('<div class="form-section">', unsafe_allow_html=True)
                    col3, col4 = st.columns(2)
                    with col3:
                        new_username = st.text_input("Username", placeholder="Buat username unik")
                    with col4:
                        new_password = st.text_input("Password", type="password", placeholder="Buat password aman")
                    st.markdown('</div>', unsafe_allow_html=True)

                    submitted = st.form_submit_button("🟢 Daftar Sekarang")

            if submitted:
                if all([name, email, phone, institution, new_username, new_password]):
                    if save_user(new_username, new_password, name, email, phone, institution):
                        st.success("✅ Berhasil daftar! Silakan login.")
                    else:
                        st.error("❌ Username sudah digunakan. Silakan pilih yang lain.")
                else:
                    st.warning("⚠️ Semua kolom wajib diisi.")
            
            if st.button("Masuk", use_container_width=True):
                st.session_state.menu = "Log in"
                st.rerun()


        return  

    # === Setelah login: tampilkan sapaan dan tombol logout ===
    col_logout, col_spacer, col_sapaan = st.columns([1, 6, 5])
    with col_logout:
        if st.button("🔓 Logout"):
            st.session_state.is_logged_in = False
            st.success("Berhasil logout.")
            st.rerun()

    with col_sapaan:
        st.markdown(f"""
            <div style='text-align: right; margin-top: 8px;'>
                <h5 style='margin: 0;'>👋 Selamat datang, <strong>{st.session_state.nama_instansi}</strong></h5>
            </div>
        """, unsafe_allow_html=True)

    # === INISIALISASI SESSION STATE ===
    for key in ["saved_rekomendasi", "clicked_save", "show_saved", "rekomendasi"]:
        if key not in st.session_state:
            st.session_state[key] = [] if key == "saved_rekomendasi" else False

    # === Judul utama & deskripsi
    st.markdown(f"""
        <style>
            .judul-utama {{
                font-size: 42px;
                font-weight: 800;
                color: #1f2937;
                margin-bottom: 0.4rem;
            }}
            .deskripsi-sub {{
                font-size: 18px;
                color: #4b5563;
                margin-bottom: 2rem;
            }}
            .welcome-box {{
                background-color: #f1f5f9;
                border-radius: 12px;
                padding: 20px;
                margin-top: 20px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.03);
            }}
        </style>

        <div class="welcome-box">
            <div style="text-align: center;">
                <div class="judul-utama">Permasalahan Daerah dan Inovasi Solutif</div>
                <div class="deskripsi-sub">
                    Temukan beragam permasalahan dari berbagai daerah dan inovasi yang dapat menjadi solusinya — dibagikan oleh masyarakat, peneliti, dan instansi daerah.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # === LOAD DATA PERMASALAHAN & REKOMENDASI TERSIMPAN ===
    if os.path.exists("permasalahan.csv"):
        df_problems = pd.read_csv("permasalahan.csv")
        if st.session_state["current_user"] != "admin":
            if "username" in df_problems.columns:
                df_problems = df_problems[df_problems["username"] == st.session_state["current_user"]]
            else:
                df_problems = df_problems[df_problems["Instansi"] == st.session_state.nama_instansi]
    else:
        df_problems = pd.DataFrame(columns=["Waktu", "Nama", "Instansi", "Judul", "Deskripsi", "username"])

    # ✅ Tambahkan ini:
    df_rekom = pd.DataFrame(st.session_state.get("saved_rekomendasi", []))

    # === DASHBOARD RINGKASAN ===
    col1, col2, col3 = st.columns(3)
    col1.metric("📌 Total Permasalahan", len(df_problems))
    col2.metric("🧠 Klasifikasi Unik", df_rekom["label"].nunique() if not df_rekom.empty else 0)
    col3.metric("🔍 Total Rekomendasi", len(df_rekom))

    # === CHART ===
    if not df_rekom.empty:
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            try:
                label_flat = df_rekom["label"].dropna().apply(lambda x: eval(x) if isinstance(x, str) else x)
                label_counts = pd.Series([lbl for sublist in label_flat for lbl in sublist]).value_counts().reset_index()
                label_counts.columns = ["Klasifikasi", "Jumlah"]
                fig = px.bar(label_counts, x="Klasifikasi", y="Jumlah", color="Klasifikasi", height=350)
                st.plotly_chart(fig, use_container_width=True)
            except:
                st.info("Belum ada data klasifikasi yang valid untuk ditampilkan.")

        with col_chart2:
            if "tahun" in df_rekom.columns:
                df_year = df_rekom.groupby("tahun").size().reset_index(name="Jumlah")
                fig2 = px.line(df_year, x="tahun", y="Jumlah", markers=True, height=350)
                st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    judul = st.text_input("Judul Masalah")
    deskripsi = st.text_area("Deskripsi Permasalahan")
    hasil = pd.DataFrame()  

    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

    with col1:
        if st.button("🔍 Tampilkan Hasil Rekomendasi"):
            if not judul and not deskripsi:
                st.warning("⚠️ Silakan masukkan minimal judul atau deskripsi.")
            else:
                input_text = f"{judul}. {deskripsi}" if judul and deskripsi else judul or deskripsi
                st.session_state.tampilkan_rekom = True

    with col2:
        if st.button("💾 Simpan Hasil"):
            st.session_state.clicked_save = True

    with col3:
        if st.button("📑 Rekomendasi Tersimpan"):
            st.session_state.show_saved = True

    with col4:
        if st.button("🏛️ Permasalahan Daerah"):
            st.session_state.show_permasalahan = True

    st.markdown("---")

    if st.session_state.get("clicked_save", False):
        st.session_state.clicked_save = False  # reset tombol

        hasil_df = st.session_state.get("rekomendasi")  # ambil hasil yang sebelumnya
        if isinstance(hasil_df, pd.DataFrame):
            st.session_state.saved_rekomendasi.extend(hasil_df.to_dict("records"))
            hasil = hasil_df
            st.success("✅ Semua hasil rekomendasi telah disimpan.")
        else:
            hasil = pd.DataFrame()
            st.warning("Belum ada hasil rekomendasi yang ditampilkan.")
    else:
        rekom = st.session_state.get("rekomendasi", pd.DataFrame())
        hasil = rekom if isinstance(rekom, pd.DataFrame) else pd.DataFrame()

    if st.session_state.get("show_saved", False):
        st.markdown("""
        <div style="text-align: center; margin-top: 30px; margin-bottom: 20px;">
            <h4 style="font-size: 24px; font-weight: 600;">Daftar Rekomendasi Tersimpan</h4>
        </div>
        """, unsafe_allow_html=True)

        col_left, col_center, col_right = st.columns([1, 6, 1])
        with col_center:
            if not st.session_state.saved_rekomendasi:
                st.info("Belum ada data yang disimpan.")
            else:
                df_saved = pd.DataFrame(st.session_state.saved_rekomendasi)
                st.dataframe(df_saved, use_container_width=True)

                csv = df_saved.to_csv(index=False).encode("utf-8")
                st.download_button("⬇️ Unduh CSV", data=csv, file_name="rekomendasi_tersimpan.csv", mime="text/csv")

                if st.button("❌ Tutup Rekomendasi Tersimpan"):
                    st.session_state.show_saved = False
                    st.rerun()

    if st.session_state.get("show_permasalahan", False):
        st.markdown("""
        <div style="text-align: center; margin-top: 30px; margin-bottom: 20px;">
            <h4 style="font-size: 24px; font-weight: 600;">Daftar Permasalahan Daerah</h4>
        </div>
        """, unsafe_allow_html=True)

        col_left, col_center, col_right = st.columns([1, 6, 1])
        with col_center:
            if os.path.exists("permasalahan.csv"):
                df = pd.read_csv("permasalahan.csv")
                if "username" in df.columns:
                    df = df[df["username"] == st.session_state["current_user"]]
                else:
                    df = df[df["Instansi"] == st.session_state["nama_instansi"]]

                if df.empty:
                    st.info("Belum ada permasalahan yang pernah diajukan.")
                else:
                    st.dataframe(df[["Waktu", "Nama", "Instansi", "Judul", "Deskripsi"]])
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇️ Download CSV", data=csv, file_name="permasalahan_saya.csv", mime="text/csv")

                    if st.button("❌ Tutup"):
                        st.session_state.show_permasalahan = False
                        st.rerun()
            else:
                st.info("Belum ada data permasalahan yang tersimpan.")


    if st.session_state.get("tampilkan_rekom", False):
        input_text = f"{judul}. {deskripsi}" if judul and deskripsi else judul or deskripsi
        # label = model.predict([input_text])[0]

        # st.success(f"🔖 Prediksi Kategori: **{label}**")
        st.markdown("---")
        st.subheader("🔎 Rekomendasi Inovasi")

        hasil = rekomendasi(input_text, top_n=50)  # ambil lebih banyak dulu
        hasil = hasil.drop_duplicates(subset=["judul", "sinopsis", "link"]).head(20).reset_index(drop=True)
        st.session_state.rekomendasi = hasil

        # Simpan histori
        waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user = st.session_state["current_user"]
        nama_instansi = st.session_state.get("nama_instansi", "")

        users = load_users()
        user_info = users[users["username"] == user].iloc[0]
        nama_lengkap = user_info["name"]

        data_baru = {
            "Waktu": waktu,
            "Nama": nama_lengkap,
            "Instansi": nama_instansi,
            "Judul": judul,
            "Deskripsi": deskripsi
        }

        columns = ["Waktu", "Nama", "Instansi", "Judul", "Deskripsi"]
        if os.path.exists("permasalahan.csv"):
            df_lama = pd.read_csv("permasalahan.csv")
        else:
            df_lama = pd.DataFrame(columns=columns)

        df_baru = pd.concat([df_lama, pd.DataFrame([data_baru])], ignore_index=True)
        df_baru.to_csv("permasalahan.csv", index=False)

        st.success("✅ Permasalahan berhasil disimpan!")

        # Reset setelah ditampilkan
        st.session_state.tampilkan_rekom = False
 
    # Ambil hasil rekomendasi dari session_state jika tersedia
    rekom = st.session_state.get("rekomendasi", pd.DataFrame())
    hasil = rekom if isinstance(rekom, pd.DataFrame) else pd.DataFrame()


    # === TAMPILKAN INOVASI ACAK JIKA BELUM ADA HASIL ===
    if hasil.empty and not st.session_state.get("show_saved", False) and not st.session_state.get("show_permasalahan", False):

        random_samples = data.sample(n=6).reset_index(drop=True)

        st.markdown("""
            <style>
                .grid-container {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 1.2rem;
                    margin-bottom: 2rem;
                }
                .inovasi-card {
                    background-color: #f9fafb;
                    border: 1px solid #e5e7eb;
                    border-radius: 16px;
                    padding: 18px 20px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.03);
                    transition: 0.2s ease;
                }
                .inovasi-card:hover {
                    border-color: #1f77b4;
                    transform: scale(1.01);
                }
                .inovasi-card h4 {
                    margin-top: 0;
                    font-size: 16px;
                    color: #1f2937;
                }
                .inovasi-card p {
                    font-size: 13px;
                    margin: 4px 0;
                    color: #374151;
                }
                .inovasi-card .sinopsis {
                    font-size: 12px;
                    color: #6b7280;
                    margin-top: 8px;
                }
                @media screen and (max-width: 768px) {
                    .grid-container {
                        grid-template-columns: 1fr;
                    }
                }
            </style>

            <div class="grid-container">
        """, unsafe_allow_html=True)

        for _, row in random_samples.iterrows():
            st.markdown(f"""
                <div class="inovasi-card">
                    <h4>{row['judul']}</h4>
                    <p><b>{row['tahun']}</b> — {row['nama']}</p>
                    <p>{row['afiliasi']}</p>
                    <p><i>{row['daerah']}</i></p>
                    <p class="sinopsis">{row.get('sinopsis', '-')[:150]}...</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Navigasi Halaman
    if "page_research" not in st.session_state:
        st.session_state.page_research = 1

    page = st.session_state.page_research
    per_page = 5
    total_pages = (len(hasil) - 1) // per_page + 1
    start = (page - 1) * per_page
    end = start + per_page

    for _, row in hasil.iloc[start:end].iterrows():
        # Ubah label ke list
        try:
            label_list = eval(row["label"]) if isinstance(row["label"], str) else row["label"]
        except:
            label_list = [row["label"]]

        # Header (Tahun + Label)
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center;
                    background-color: #f1f5f9; padding: 10px 16px; border-radius: 10px 10px 0 0;
                    border: 1px solid #e5e7eb; border-bottom: none;">
            <div style="font-weight: 600; font-size: 15px;">{row['tahun']}</div>
            <div>{render_label_badges(label_list)}</div>
        </div>
        """, unsafe_allow_html=True)

        # Judul dan detail peneliti
        st.markdown(f"""
        <div style="border: 1px solid #e5e7eb; border-top: none; border-radius: 0 0 10px 10px;
                    background-color: #ffffff; padding: 16px 20px; margin-bottom: 20px;">
            <h4 style="margin-top: 0; margin-bottom: 8px; color: #1f2937;">{row['judul']}</h4>
            <div style="font-size: 14px; color: #374151;">
                <b>👤 Nama:</b> {row['nama']}<br>
                <b>📧 Email:</b> {row['email']}<br>
                <b>🏢 Afiliasi:</b> {row['afiliasi']}<br>
                <b>📍 Daerah:</b> {row['daerah']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Sinopsis & Ringkasan
        with st.expander("📝 Sinopsis"):
            st.markdown(f"""
            <div style="background-color: #f9fafb; border: 1px solid #e2e8f0;
                        border-radius: 8px; padding: 12px; font-size: 14px;
                        color: #374151; max-height: 150px; overflow-y: auto;">
                <b>Sinopsis:</b><br>{row.get('sinopsis', '-')}
            </div>
            """, unsafe_allow_html=True)

        # Link penelitian
        if pd.notna(row['link']) and row['link'].startswith("http"):
            st.markdown(f"""
            <a href="{row['link']}" target="_blank" style="
                display: inline-block;
                margin-top: 10px;
                background-color: #1d4ed8;
                color: white;
                padding: 6px 14px;
                font-size: 13px;
                border-radius: 8px;
                text-decoration: none;">
                🔗 Kunjungi Penelitian
            </a>
            """, unsafe_allow_html=True)

        # Garis pemisah
        st.markdown("<hr style='margin: 24px 0;'>", unsafe_allow_html=True)


    # Navigasi halaman
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if page > 1:
            if st.button("Sebelumnya"):
                st.session_state.page_research -= 1
                st.rerun()
    with col2:
        st.markdown(f"<div style='text-align:center; padding-top:6px;'>📄 Halaman {page} dari {total_pages}</div>", unsafe_allow_html=True)
    with col3:
        if page < total_pages:
            if st.button("Selanjutnya"):
                st.session_state.page_research += 1
                st.rerun()

    # Tombol kembali ke beranda
    if st.button("Beranda", use_container_width=True):
        st.session_state.page = "beranda"
        st.rerun()

    # # Tombol tambahan SETELAH tombol kembali ke beranda
    # if st.button("📨 Hubungi Peneliti"):
    #     st.info("🚧 Fitur kontak peneliti belum aktif.")  # Placeholder, bisa dikaitkan dengan email atau form kontak
    show_footer()

def login_admin():
    st.title("🔐 Login Admin")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":  # bisa kamu ganti
            st.session_state.admin_logged_in = True
            st.success("Login berhasil!")
            st.session_state.page = "research"
            st.rerun()
        else:
            st.error("Username atau password salah.")

def tambah_inovasi():
    st.markdown("""
        <style>
            .judul-container {
                background: linear-gradient(to right, #e0f2fe, #f0f9ff);
                border-radius: 12px;
                padding: 30px 24px 24px;
                margin: 30px auto 20px;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                max-width: 800px;
            }
            .judul-utama {
                font-size: 38px;
                font-weight: 800;
                color: #0f172a;
                margin-bottom: 10px;
                font-family: 'Segoe UI', sans-serif;
            }
            .deskripsi-sub {
                font-size: 17px;
                color: #475569;
                line-height: 1.6;
                max-width: 700px;
                margin: 0 auto;
            }
            .admin-login-box {
                max-width: 420px;
                margin: 0 auto;
                padding: 30px;
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 16px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.06);
                font-family: 'Segoe UI', sans-serif;
                margin-top: 30px;
            }
            .forgot-password {
                text-align: right;
                font-size: 13px;
                margin-top: -8px;
                margin-bottom: 20px;
            }
            .forgot-password a {
                color: #3b82f6;
                text-decoration: none;
            }
            .forgot-password a:hover {
                text-decoration: underline;
            }
        </style>

        <div class="judul-container">
            <div class="judul-utama">Tambah Inovasi Baru</div>
            <div class="deskripsi-sub">
                Halaman ini hanya dapat diakses oleh <b>Admin</b> untuk menambahkan data inovasi ke sistem,
                baik melalui <i>form manual</i> maupun <i>upload file CSV</i>.<br>
                Pastikan data yang dimasukkan telah sesuai dengan format yang berlaku.
            </div>
        </div>
    """, unsafe_allow_html=True)


    if "logged_in_admin" not in st.session_state:
        st.session_state.logged_in_admin = False

    if not st.session_state.logged_in_admin:
        with st.form("login_form"):
            username = st.text_input("👤 Username", key="admin_username")
            password = st.text_input("🔒 Password", type="password", key="admin_password")

            st.markdown("""
                <div style="text-align: right; font-size: 13px; margin-top: -8px; margin-bottom: 20px;">
                    <a href="mailto:support@risda.id?subject=Lupa%20Password%20Admin" style="color:#3b82f6; text-decoration: none;">
                        Lupa password?
                    </a>
                </div>
            """, unsafe_allow_html=True)

            submit = st.form_submit_button("Masuk")

        if submit:
            if username == "admin" and password == "admin123":
                st.success("✅ Login berhasil!")
                st.session_state.logged_in_admin = True
                st.rerun()
            else:
                st.error("❌ Username atau password salah.")

        return

    # === PILIH METODE INPUT ===
    # Inisialisasi pilihan input
    if "metode_input" not in st.session_state:
        st.session_state.metode_input = "Form Manual"

    # Gaya CSS toggle tab
    st.markdown("""
        <style>
            .tab-container {
                display: flex;
                justify-content: center;
                gap: 12px;
                margin-top: 1.5rem;
                margin-bottom: 1.5rem;
            }
            .tab-button {
                flex: 1;
                padding: 10px 20px;
                text-align: center;
                border-radius: 8px;
                font-weight: 600;
                border: 1px solid #cbd5e1;
                background-color: #f1f5f9;
                color: #334155;
                cursor: pointer;
                transition: 0.2s ease;
            }
            .tab-button:hover {
                background-color: #e2e8f0;
            }
            .tab-button.selected {
                background-color: #2563eb;
                color: white;
                border-color: #2563eb;
            }
        </style>
    """, unsafe_allow_html=True)

    # Form invisible buat handle klik
    with st.form("toggle_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            form_manual = st.form_submit_button("📝 Form Manual")
        with col2:
            form_csv = st.form_submit_button("📁 Upload CSV")

    # Deteksi klik
    if form_manual:
        st.session_state.metode_input = "Form Manual"
    elif form_csv:
        st.session_state.metode_input = "Upload CSV"

    # Tampilkan toggle visual (yang rapi)
    selected_manual = "selected" if st.session_state.metode_input == "Form Manual" else ""
    selected_csv = "selected" if st.session_state.metode_input == "Upload CSV" else ""

    st.markdown(f"""
    <div class="tab-container">
        <div class="tab-button {selected_manual}">📝 Form Manual</div>
        <div class="tab-button {selected_csv}">📁 Upload CSV</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.metode_input == "Form Manual":
        with st.form("form_manual"):
            st.subheader("📝 Input Data Inovasi Manual")

            col1, col2 = st.columns(2)
            with col1:
                judul = st.text_input("Judul Inovasi")
                sinopsis = st.text_area("Sinopsis")
                nama = st.text_input("Nama Peneliti")
                email = st.text_input("Email")

            with col2:
                afiliasi = st.text_input("Afiliasi")
                daerah = st.text_input("Daerah")
                tahun = st.number_input("Tahun", min_value=2000, max_value=2100, step=1, value=2025)

            link = st.text_input("Link (opsional)")

            submit_manual = st.form_submit_button("💾 Simpan Inovasi")

        if submit_manual:
            input_text = f"{judul}. {sinopsis}" if judul and sinopsis else judul or sinopsis
            label = model.predict([input_text])[0]
            st.success(f"🔖 Prediksi Klasifikasi: **{label}**")

            new_data = {
                "judul": judul, "sinopsis": sinopsis,
                "nama": nama, "email": email, "afiliasi": afiliasi,
                "daerah": daerah, "tahun": tahun, "label": str([label]), "link": link
            }

            df = pd.DataFrame([new_data])
            if os.path.exists("fixr.csv"):
                df.to_csv("fixr.csv", mode="a", index=False, header=False)
            else:
                df.to_csv("fixr.csv", index=False)
            st.success("✅ Inovasi berhasil ditambahkan!")
            st.balloons()

    elif st.session_state.metode_input == "Upload CSV":
        st.subheader("📁 Upload File CSV")
        st.markdown("Pastikan file CSV memiliki kolom: `judul`, `sinopsis`, `ringkasan`, `nama`, `email`, `afiliasi`, `daerah`, `tahun`, `link`")

        uploaded_file = st.file_uploader("Pilih file CSV", type=["csv"])

        if uploaded_file:
            try:
                df_upload = pd.read_csv(uploaded_file)
                required_cols = ["judul", "sinopsis", "ringkasan", "nama", "email", "afiliasi", "daerah", "tahun", "link"]

                if not all(col in df_upload.columns for col in required_cols):
                    st.error(f"❌ Kolom CSV harus mencakup: {', '.join(required_cols)}")
                else:
                    df_upload["label"] = df_upload.apply(
                        lambda row: str([model.predict([f"{row['judul']}. {row['sinopsis']}"])[0]]),
                        axis=1)

                    if os.path.exists("fixr.csv"):
                        df_upload.to_csv("fixr.csv", mode="a", index=False, header=False)
                    else:
                        df_upload.to_csv("fixr.csv", index=False)

                    st.success("✅ Data dari CSV berhasil ditambahkan ke sistem!")
                    st.dataframe(df_upload)

            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses file: {e}")

    # === Riwayat Input Inovasi (Edit, Hapus, Pulihkan, Unduh) ===
    st.markdown("---")
    st.markdown("""
    <h3 style='text-align: center; color: #4A90E2; margin-bottom: 0.3rem;'>Data Inovasi</h3>
    <hr style='border: 1px solid #ccc; margin-top: 0.3rem;' />
    """, unsafe_allow_html=True)



    fixr_path = "fixr.csv"
    trash_path = "fixr_trash.csv"

    # --- STATE & TOGGLE ---
    if "show_all_data" not in st.session_state:
        st.session_state.show_all_data = False

    def toggle_data_view():
        st.session_state.show_all_data = not st.session_state.show_all_data

    # --- TOMBOL TOGGLE ---
    label = "📂 Tampilkan Semua Data" if not st.session_state.show_all_data else "❌ Tutup Data"
    st.button(label, on_click=toggle_data_view)

    # --- TAMPILKAN DATA + UNDUH ---
    if st.session_state.show_all_data and os.path.exists(fixr_path):
        df_all = pd.read_csv(fixr_path)
        st.dataframe(df_all, use_container_width=True)

    if os.path.exists(fixr_path):
        df_inovasi = pd.read_csv(fixr_path)

        # Unduh seluruh data
        st.download_button("⬇️ Unduh Semua Data Inovasi", data=df_inovasi.to_csv(index=False).encode("utf-8"),
                        file_name="data_inovasi.csv", mime="text/csv")

        st.markdown("""
        <h4 style='color: #333333; margin-bottom: 0.2rem;'>Edit Data Inovasi</h4>
        <hr style='border: 0.5px solid #cccccc; margin-top: 0.2rem; margin-bottom: 0.8rem;' />
        """, unsafe_allow_html=True)

        selected_index = st.selectbox("Pilih baris untuk diedit atau dihapus:", df_inovasi.index)
        selected_data = df_inovasi.loc[selected_index]

        with st.form("form_edit_inovasi"):
            col1, col2 = st.columns(2)
            with col1:
                judul = st.text_input("Judul", value=selected_data["judul"])
                sinopsis = st.text_area("Sinopsis", value=selected_data["sinopsis"])
                nama = st.text_input("Nama Peneliti", value=selected_data["nama"])
                email = st.text_input("Email", value=selected_data["email"])
            with col2:
                afiliasi = st.text_input("Afiliasi", value=selected_data["afiliasi"])
                daerah = st.text_input("Daerah", value=selected_data["daerah"])
                tahun = st.number_input("Tahun", min_value=2000, max_value=2100, value=int(selected_data["tahun"]))
                link = st.text_input("Link", value=selected_data["link"])

            submit_edit = st.form_submit_button("💾 Simpan Perubahan")
            delete_row = st.form_submit_button("🗑️ Hapus Data Ini")

        if submit_edit:
            input_text = f"{judul}. {sinopsis}"
            label_baru = model.predict([input_text])[0]
            df_inovasi.loc[selected_index] = {
                "judul": judul,
                "sinopsis": sinopsis,
                "nama": nama,
                "email": email,
                "afiliasi": afiliasi,
                "daerah": daerah,
                "tahun": tahun,
                "label": str([label_baru]),
                "link": link
            }
            df_inovasi.to_csv(fixr_path, index=False)
            st.success("✅ Data berhasil diperbarui!")
            st.rerun()

        if delete_row:
            deleted_row = df_inovasi.loc[[selected_index]]
            if os.path.exists(trash_path):
                df_trash = pd.read_csv(trash_path)
                df_trash = pd.concat([df_trash, deleted_row], ignore_index=True)
            else:
                df_trash = deleted_row
            df_trash.to_csv(trash_path, index=False)

            df_inovasi = df_inovasi.drop(index=selected_index).reset_index(drop=True)
            df_inovasi.to_csv(fixr_path, index=False)
            st.success("🗑️ Data berhasil dihapus dan disimpan di tempat sampah.")
            st.rerun()
    else:
        st.info("Belum ada data inovasi yang tersimpan.")

    # Pulihkan Data
    st.markdown("""
    <h4 style='color: #333333; margin-bottom: 0.2rem;'>♻️ Pulihkan Data</h4>
    <hr style='border: 0.5px solid #cccccc; margin-top: 0.2rem; margin-bottom: 0.8rem;' />
    """, unsafe_allow_html=True)
    if os.path.exists(trash_path):
        df_trash = pd.read_csv(trash_path)
        if not df_trash.empty:
            idx_to_restore = st.selectbox("Pilih baris yang ingin dipulihkan:", df_trash.index, key="restore_select")
            st.write(df_trash.loc[idx_to_restore])

            if st.button("♻️ Pulihkan Data", key="restore_button"):
                df_restore = df_trash.loc[[idx_to_restore]]
                df_trash = df_trash.drop(index=idx_to_restore).reset_index(drop=True)

                df_existing = pd.read_csv(fixr_path) if os.path.exists(fixr_path) else pd.DataFrame()
                df_combined = pd.concat([df_existing, df_restore], ignore_index=True)
                df_combined.to_csv(fixr_path, index=False)
                df_trash.to_csv(trash_path, index=False)
                st.success("✅ Data berhasil dipulihkan ke database inovasi.")
                st.rerun()
        else:
            st.info("Tempat sampah kosong.")
    else:
        st.info("Belum ada data yang dihapus.")

    # Tombol Kembali
    if st.button("🔙 Daftar Inovasi"):
        st.session_state.page = "research"
        st.rerun()

    st.markdown("---")
    st.markdown("""

    <p style='text-align: center; color: #475569; margin-top: 0.2rem; font-size: 15px;'>
        Lihat daftar permintaan kerja sama yang dikirim oleh pengguna umum.
    </p>
    """, unsafe_allow_html=True)

    if "show_data_kerjasama" not in st.session_state:
        st.session_state.show_data_kerjasama = False

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        toggle = st.button(
            "📄 Lihat Permintaan" if not st.session_state.show_data_kerjasama else "❌ Tutup Tabel Permintaan",
            use_container_width=True
        )

    if toggle:
        st.session_state.show_data_kerjasama = not st.session_state.show_data_kerjasama

    if st.session_state.show_data_kerjasama:
        st.markdown("<br>", unsafe_allow_html=True)

        file_path = "form_kerjasama.csv"
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            if df.empty:
                st.info("Belum ada permintaan kerja sama.")
            else:
                st.markdown("""
                <div style='background-color: #f8fafc; padding: 1rem; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);'>
                """, unsafe_allow_html=True)

                st.dataframe(df, use_container_width=True)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("⬇️ Unduh Data Kerja Sama", data=csv,
                                   file_name="permintaan_kerjasama.csv", mime="text/csv",
                                   use_container_width=True)

                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Belum ada file permintaan kerja sama.")

def tampilkan_bantuan():
    with st.expander("❓ Bantuan"):
        st.markdown("""
        Jika Anda mengalami kendala dalam penggunaan sistem, silakan hubungi tim admin kami:

        📧 Email: [risda.support@gmail.com](mailto:risda.support@gmail.com)  
        🕐 Jam operasional: Senin–Jumat, 08.00–16.00 WIB
        """)

def tampilkan_form_kerjasama():
    # Inisialisasi session state
    if "show_form_kerjasama" not in st.session_state:
        st.session_state.show_form_kerjasama = False

    if "trigger_rerun" not in st.session_state:
        st.session_state.trigger_rerun = False

    # Tombol toggle
    label = "Ajukan Kerja Sama dengan Peneliti" if not st.session_state.show_form_kerjasama else "❌ Tutup Form Kerja Sama"
    toggle_clicked = st.button(label)

    if toggle_clicked:
        st.session_state.show_form_kerjasama = not st.session_state.show_form_kerjasama
        st.session_state.trigger_rerun = True  # tandai untuk rerun di luar callback

    # Form hanya ditampilkan jika status True
    if st.session_state.show_form_kerjasama:
        st.markdown("#### Silakan lengkapi data berikut:")
        with st.form("form_kerjasama"):
            nama = st.text_input("Nama Lengkap")
            instansi = st.text_input("Asal Instansi / Industri")
            keperluan = st.text_area("Keperluan Kerja Sama")
            kontak = st.text_input("Kontak yang Bisa Dihubungi (HP/Email)")

            kirim = st.form_submit_button("📩 Kirim")

            if kirim:
                # Simpan ke CSV
                data_kerjasama = {
                    "nama": nama,
                    "instansi": instansi,
                    "keperluan": keperluan,
                    "kontak": kontak,
                    "tanggal": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                df_kerjasama = pd.DataFrame([data_kerjasama])
                file_path = "form_kerjasama.csv"

                if os.path.exists(file_path):
                    existing = pd.read_csv(file_path)
                    df_kerjasama = pd.concat([existing, df_kerjasama], ignore_index=True)

                df_kerjasama.to_csv(file_path, index=False)
                st.success("Terima kasih! Admin akan menghubungi Anda maksimal dalam H+2 hari kerja.")

                st.session_state.show_form_kerjasama = False
                st.session_state.trigger_rerun = True  # rerun agar form hilang langsung


# === Navigasi antar halaman ===
if st.session_state.page == "beranda":
    halaman_beranda()
elif st.session_state.page == "research":
    halaman_research()
elif st.session_state.page == "rekomendasi":
    halaman_pemerintah()
elif st.session_state.page == "login":
    login_admin()
elif st.session_state.page == "tambah_inovasi":
    tambah_inovasi()

# === Sidebar navigasi ===
with st.sidebar:
    st.markdown("## Navigasi")
    if st.button("Beranda", use_container_width=True, key="main_beranda_btn"):
        st.session_state.page = "beranda"
        st.rerun()

    if st.button("Daftar Inovasi", use_container_width=True):
        st.session_state.page = "research"
        st.rerun()
    if st.button("Rekomendasi", use_container_width=True):
        st.session_state.page = "rekomendasi"
        st.rerun()

    st.markdown("## Pencarian Istilah Asing")
    istilah_asing = st.text_input("Masukkan istilah asing")
    if istilah_asing:
        url = f"https://www.google.com/search?q=apa+itu+{istilah_asing.replace(' ', '+')}"
        st.markdown(f"[🔗 Cari di Google]({url})", unsafe_allow_html=True)

    # === Tombol Tambah Data Inovasi (dengan login check langsung)
    if st.button("➕ Tambah Data Inovasi", use_container_width=True):
        st.session_state.page = "tambah_inovasi"
        st.rerun()

    if st.session_state.get("logged_in_admin"):
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in_admin = False
            st.success("Berhasil logout")
            st.rerun()

    tampilkan_bantuan()
    tampilkan_form_kerjasama()

    st.markdown("---")
    st.caption("Sistem Rekomendasi Inovasi Daerah (RISDA) © 2025")

# === RERUN AMAN ===
if st.session_state.get("trigger_rerun", False):
    st.session_state.trigger_rerun = False
    st.rerun()
