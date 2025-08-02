import streamlit as st
st.set_page_config(page_title="Portfolio",
                   layout="wide", page_icon=":rocket:")
st.title("Portofolio Saya")
st.header("Data Science & Analyst")
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih Halaman",
                        ["Tentang Saya",
                         "Proyek",
                         "EDA",
                         "Machine Learning",
                         "Kontak"])

if page == 'Kontak':
    import kontak
    kontak.tampilkan_kontak()
elif page == 'Tentang Saya':
    import tentang
    tentang.tampilkan_tentang()
elif page == 'Proyek':
    import proyek
    proyek.tampilkan_proyek()
elif page == 'EDA':
    import eda
    eda.tampilkan_eda()
elif page == 'Machine Learning':
    import prediksi
    prediksi.tampilkan_prediksi()