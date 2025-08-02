import streamlit as st

def tampilkan_tentang():
    st.header("👩‍💻 Biodata Profil")
    
    # Menampilkan foto
    st.image("new me.jpg", caption="Isna Ayustin", use_container_width=True)

    # Informasi biodata
    st.markdown("""
    ### 📝 Tentang Saya

    Halo! Nama saya **Isna Ayustin**.  
    Saat ini saya sedang mengikuti **Bootcamp Data Science and Data Analyst di DIBIMBING.ID**,  
    dan sedang mengerjakan project akhir berjudul:

    > 🏠 **Real Estate Prediction with Machine Learning**

    Project ini berfokus pada prediksi harga properti menggunakan model machine learning seperti XGBoost, serta interpretasi hasil prediksi menggunakan SHAP.

    Saya sangat antusias dalam mempelajari data dan berharap bisa berkontribusi dalam dunia teknologi dan analisis bisnis.
    """)
if __name__ == '__main__':
    tampilkan_tentang()
