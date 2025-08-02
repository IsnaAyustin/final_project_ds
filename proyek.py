import streamlit as st
from PIL import Image
import pandas as pd

def tampilkan_proyek():
    st.set_page_config(
        page_title="Real Estate Analytics",
        page_icon="🏠",
        layout="wide"
    )

    # CSS kustom
    st.markdown("""
    <style>
        .main {
            background-color: #f9f9f9;
        }
        .header {
            color: #2c3e50;
            text-align: center;
            padding: 20px;
        }
        .feature-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .feature-title {
            color: #3498db;
            font-size: 1.2em;
        }
    </style>
    """, unsafe_allow_html=True)

    # Header utama
    st.title("🏠 Real Estate Analytics Platform")
    st.markdown("""
    **Platform komprehensif untuk analisis dan prediksi harga properti**  
    Temukan wawasan dari data real estate dan prediksikan harga properti dengan model machine learning kami.
    """)

    # Gambar header (opsional)
    # header_img = Image.open("assets/header.jpg")
    # st.image(header_img, use_column_width=True)

    # Fitur utama
    st.header("✨ Fitur Utama")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background-color: #f0f8ff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 40px;">📊</div>
            <h4 style="margin-bottom: 5px;">EDA Dashboard</h4>
            <p style="font-size: 14px; color: #555;">Jelajahi distribusi harga, tren tahunan, dan pola properti dengan visualisasi interaktif.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background-color: #fef6e4; padding: 20px; border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 40px;">🔮</div>
            <h4 style="margin-bottom: 5px;">Price Prediction</h4>
            <p style="font-size: 14px; color: #555;">Prediksikan harga properti berdasarkan karakteristik dengan model XGBoost yang akurat.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background-color: #e6fff5; padding: 20px; border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 40px;">📈</div>
            <h4 style="margin-bottom: 5px;">Market Trends</h4>
            <p style="font-size: 14px; color: #555;">Analisis tren pasar real estate dan faktor-faktor yang mempengaruhi harga properti.</p>
        </div>
        """, unsafe_allow_html=True)


    # Tentang dataset
    st.header("📁 Tentang Dataset")
    st.markdown("""
    Dataset real estate ini mencakup:
    - **30,000+** transaksi properti
    - **10+ fitur** termasuk nilai taksiran, tipe properti, lokasi
    - Rentang tahun **2017-2022**

    Fitur utama:
    - `Assessed Value`: Nilai taksiran properti
    - `Sale Amount`: Harga jual aktual (target)
    - `Property Type`: Kategori properti
    - `Residential Type`: Kategori Residential
    - `Year`: Tahun transaksi
    """)

    # Contoh data
    if st.checkbox("Tampilkan contoh data"):
        sample_data = pd.DataFrame({
            "Tahun": [2017, 2018, 2019, 2020, 2021, 2022],
            "Tipe Properti": ["Residential", "Condo", "Apartments",  "Commercial","Vacant Land", "Industrial", "Public Utility"],
            "Nilai Taksiran": [250000, 350000, 500000],
            "Harga Jual": [275000, 325000, 525000]
        })
        st.dataframe(sample_data.style.highlight_max(axis=0))

    # Panduan penggunaan
    st.header("🛠️ Cara Menggunakan")
    st.markdown("""
    1. **Navigasi** ke halaman yang diinginkan melalui menu sidebar
    2. **EDA Dashboard**:
    - Jelajahi visualisasi data interaktif
    - Filter berdasarkan tahun atau tipe properti
    3. **Price Prediction**:
    - Masukkan parameter properti
    - Klik "Predict" untuk melihat hasil
    """)

    # Tim pengembang
    st.markdown("---")
    st.markdown("""
    **Dikembangkan oleh:**  
    Isna Ayustin - Final Project Data Science Bootcamp Dibimbing
    """)