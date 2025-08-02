import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def tampilkan_eda():
    st.set_page_config(
        page_title="EDA - Real Estate",
        page_icon="📊",
        layout="wide"
    )

    # Judul
    st.title("📊 Exploratory Data Analysis")
    st.markdown("""
    Jelajahi distribusi dan pola dalam dataset real estate.
    """)

    # Load data
    @st.cache_data
    def load_data():
        df = pd.read_csv('real_estate_sample_30k.csv')
        
        # Data preprocessing (sesuaikan dengan preprocessing yang Anda lakukan di notebook)
        df['Date Recorded'] = pd.to_datetime(df['Date Recorded'])
        df['Year'] = df['Date Recorded'].dt.year
        
        # Handle missing values
        df['Property Type'] = df['Property Type'].fillna(df[~df['Property Type'].isin(['-1','Unknown'])]['Property Type'].mode()[0])
        df['Residential Type'] = df['Residential Type'].fillna(df[~df['Residential Type'].isin(['-1','Unknown'])]['Residential Type'].mode()[0])
        
        # Convert 'Sale Amount' to numeric
        df['Sale Amount'] = pd.to_numeric(df['Sale Amount'].astype(str).str.replace(',', ''), errors='coerce')
        
        # Drop unnecessary columns
        dropped_columns = ['Serial Number', 'List Year', 'Date Recorded', 'Town', 'Address', 
                          'Non Use Code', 'Assessor Remarks', 'OPM remarks', 'Location']
        df.drop(dropped_columns, axis=1, inplace=True)
        
        # Group property types
        def group_family_only(x):
            if isinstance(x, str) and 'Family' in x:
                return 'Family'
            return x if pd.notna(x) else 'Unknown'
        
        df['Property Type'] = df['Property Type'].apply(group_family_only)
        
        return df

    df = load_data()

    # Show preview
    st.subheader("Preview Data")
    st.dataframe(df.head())

    # Filter sidebar
    st.sidebar.header("Filter Data")
    
    # Pastikan kolom Year ada dan berisi nilai numerik
    if 'Year' in df.columns:
        year_min = int(df['Year'].min())
        year_max = int(df['Year'].max())
        year_range = st.sidebar.slider(
            "Rentang Tahun",
            min_value=year_min,
            max_value=year_max,
            value=(year_min, year_max)
        )
    else:
        st.sidebar.warning("Kolom 'Year' tidak ditemukan dalam data")
        year_range = (0, 0)

    if 'Property Type' in df.columns:
        property_types = st.sidebar.multiselect(
            "Tipe Properti",
            options=df['Property Type'].unique(),
            default=df['Property Type'].unique()
        )
    else:
        st.sidebar.warning("Kolom 'Property Type' tidak ditemukan dalam data")
        property_types = []

    # Filter data
    if 'Year' in df.columns and 'Property Type' in df.columns:
        filtered_df = df[
            (df['Year'].between(year_range[0], year_range[1])) &
            (df['Property Type'].isin(property_types))
        ]
    else:
        filtered_df = df.copy()

    # Tabs untuk berbagai visualisasi
    tab1, tab2, tab3 = st.tabs(["Distribusi Harga", "Tren Tahun", "Analisis Properti"])

    with tab1:
        st.header("Distribusi Harga")
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Sale Amount' in filtered_df.columns:
                st.subheader("Harga Jual")
                fig = px.histogram(
                    filtered_df, 
                    x='Sale Amount',
                    nbins=50,
                    color='Property Type' if 'Property Type' in filtered_df.columns else None,
                    title='Distribusi Harga Jual'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Kolom 'Sale Amount' tidak ditemukan dalam data")
        
        with col2:
            if 'Assessed Value' in filtered_df.columns and 'Sale Amount' in filtered_df.columns:
                st.subheader("Nilai Taksiran vs Harga Jual")
                fig = px.scatter(
                    filtered_df,
                    x='Assessed Value',
                    y='Sale Amount',
                    color='Property Type' if 'Property Type' in filtered_df.columns else None,
                    trendline="ols",
                    title='Korelasi Nilai Taksiran dan Harga Jual'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Kolom 'Assessed Value' atau 'Sale Amount' tidak ditemukan dalam data")

    with tab2:
        st.header("Tren Harga Tahunan")
        
        if 'Year' in filtered_df.columns and 'Sale Amount' in filtered_df.columns:
            # Tren rata-rata harga per tahun
            yearly_data = filtered_df.groupby('Year').agg({
                'Sale Amount': 'mean',
                'Assessed Value': 'mean' if 'Assessed Value' in filtered_df.columns else None
            }).reset_index()
            
            fig = px.line(
                yearly_data,
                x='Year',
                y=['Sale Amount'] + (['Assessed Value'] if 'Assessed Value' in yearly_data.columns else []),
                title='Tren Harga Rata-Rata Tahunan',
                labels={'value': 'Harga ($)', 'variable': 'Metrik'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Boxplot per tahun
            st.subheader("Distribusi Harga per Tahun")
            fig = px.box(
                filtered_df,
                x='Year',
                y='Sale Amount',
                color='Property Type' if 'Property Type' in filtered_df.columns else None,
                title='Distribusi Harga per Tahun'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Kolom 'Year' atau 'Sale Amount' tidak ditemukan dalam data")

    with tab3:
        st.header("Analisis Berdasarkan Tipe Properti")
        
        if 'Property Type' in filtered_df.columns:
            # Perbandingan properti
            st.subheader("Perbandingan Rata-Rata Harga")
            prop_stats = filtered_df.groupby('Property Type').agg({
                'Sale Amount': ['mean', 'median', 'count'] if 'Sale Amount' in filtered_df.columns else None
            }).reset_index()
            
            if not prop_stats.empty:
                prop_stats.columns = ['Property Type', 'Mean Price', 'Median Price', 'Count']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.dataframe(prop_stats.sort_values('Mean Price', ascending=False))
                
                with col2:
                    fig = px.bar(
                        prop_stats,
                        x='Property Type',
                        y='Mean Price',
                        title='Harga Rata-Rata per Tipe Properti'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            # Sales ratio analysis
            if 'Assessed Value' in filtered_df.columns and 'Sale Amount' in filtered_df.columns:
                st.subheader("Analisis Sales Ratio")
                st.markdown("""
                Sales Ratio = Assessed Value / Sale Amount  
                Rasio ~1.0 berarti nilai taksiran mendekati harga jual.
                """)
                filtered_df['Sales Ratio'] = filtered_df['Assessed Value'] / filtered_df['Sale Amount']
                fig = px.box(
                    filtered_df,
                    x='Property Type',
                    y='Sales Ratio',
                    title='Distribusi Sales Ratio per Tipe Properti'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Kolom 'Assessed Value' atau 'Sale Amount' tidak ditemukan untuk analisis Sales Ratio")
        else:
            st.warning("Kolom 'Property Type' tidak ditemukan dalam data")

# Panggil fungsi utama
if __name__ == '__main__':
    tampilkan_eda()