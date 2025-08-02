import streamlit as st

def tampilkan_kontak():
    st.title("📬 Kontak Saya")
    st.markdown("Silakan hubungi saya melalui platform berikut:")

    # Gunakan 3 kolom untuk kontak
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <a href="https://www.linkedin.com/in/isnayustina" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="40"/>
                <div style="margin-top: 8px;">LinkedIn</div>
            </a>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <a href="https://github.com/IsnaAyustin" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="40"/>
                <div style="margin-top: 8px;">GitHub</div>
            </a>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="text-align: center;">
            <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" width="40"/>
            <div style="margin-top: 8px;">isnaayustin@gmail.com</div>
        </div>
        """, unsafe_allow_html=True)
