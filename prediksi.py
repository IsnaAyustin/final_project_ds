import streamlit as st
import pandas as pd
import numpy as np
import joblib
# Atur backend sebelum import pyplot
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import shap
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

def tampilkan_prediksi():
    st.set_page_config(
        page_title="Real Estate Price Prediction",
        page_icon="🏠",
        layout="wide"
    )

    # Custom CSS
    st.markdown("""
    <style>
        .main {
            background-color: #f5f5f5;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px 24px;
        }
        .feature-importance {
            font-size: 0.9em;
            color: #555;
        }
        .input-summary {
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Load model with error handling
    @st.cache_resource
    def load_model():
        try:
            model = joblib.load('real_estate_model.pkl')    
            if not (hasattr(model, 'named_steps') and 'preprocessor' in model.named_steps and 'regressor' in model.named_steps):
                st.error("The loaded model doesn't have the expected structure.")
                return None        
            return model
        except Exception as e:
            st.error(f"Failed to load model: {str(e)}")
            return None

    def predict_price(model, input_data):
        try:
            # Create DataFrame from input
            input_df = pd.DataFrame([input_data])
            
            # Make prediction
            prediction = model.predict(input_df)
            return prediction[0]
        except Exception as e:
            st.error(f"Prediction failed: {str(e)}")
            return None

    # Main function
    def main():
        st.title('🏠 Real Estate Price Prediction')
        st.markdown("Predict property prices using our optimized machine learning model")
        
        # Load model
        model = load_model()
        if model is None:
            st.stop()
        
        # Sidebar for input
        with st.sidebar:
            st.header('⚙️ Property Features')
            
            assessed_value = st.number_input(
                'Assessed Value ($)',
                min_value=0,
                max_value=10000000,
                value=250000,
                step=1000
            )
            
            year = st.slider(
                'Year',
                min_value=2017,
                max_value=2025,
                value=2022
            )
            
            property_type = st.selectbox(
                'Property Type',
                options=['Residential', 'Condo', 'Apartements', 'Commercial', 'Industrial', 'VacantLand', 'Public Utility']
            )
            
            residential_type = st.selectbox(
                'Residential Type',
                options=['Single Family', 'Two Family', 'Condo', 'Three Family', 'Four Family']
            )
            
            if st.button('Predict Price'):
                input_data = {
                    'Assessed Value': assessed_value,
                    'Year': year,
                    'Property Type': property_type,
                    'Residential Type': residential_type
                }
                
                with st.spinner('Calculating prediction...'):
                    prediction = predict_price(model, input_data)
                    if prediction is not None:
                        st.session_state.prediction = prediction
                        st.session_state.input_data = input_data

        # Main content area
        if 'prediction' in st.session_state:
            # Display prediction result
            st.success(f"### Predicted Sale Price: ${st.session_state.prediction:,.2f}")
            
            # Input summary
            with st.expander("📋 Summary", expanded=True):
                st.markdown("""
                <div class="🧾 Penjelasan:
- **Assessed Value** adalah nilai estimasi dari properti berdasarkan penilaian pemerintah atau lembaga pajak. Ini merupakan indikator utama dalam prediksi harga jual.
- **Year** menunjukkan tahun transaksi atau listing. Faktor waktu penting karena harga properti dapat naik atau turun tergantung kondisi pasar.
- **Property Type** adalah jenis properti (residensial, komersial, dll), yang memengaruhi nilai karena tiap tipe punya pasar dan harga rata-rata berbeda.
- **Residential Type** (jika applicable) memberikan rincian tipe hunian. Misalnya, rumah keluarga tunggal cenderung memiliki nilai berbeda dibanding kondominium atau rumah multi-keluarga.

👉 Prediksi harga real estate dihasilkan dengan mempertimbangkan kombinasi semua fitur di atas menggunakan model machine learning berbasis XGBoost. ">
                    <p><strong>Assessed Value:</strong> ${:,.2f}</p>
                    <p><strong>Year:</strong> {}</p>
                    <p><strong>Property Type:</strong> {}</p>
                    <p><strong>Residential Type:</strong> {}</p>
                </div>
                """.format(
                    st.session_state.input_data['Assessed Value'],
                    st.session_state.input_data['Year'],
                    st.session_state.input_data['Property Type'],
                    st.session_state.input_data['Residential Type']
                ), unsafe_allow_html=True)
            
            # Visualization columns
            col1, col2 = st.columns(2)
            
            with col1:
                # Price comparison chart
                st.subheader("Price Comparison")
                fig, ax = plt.subplots(figsize=(8, 4))
                values = [st.session_state.input_data['Assessed Value'], st.session_state.prediction]
                labels = ['Assessed Value', 'Predicted Price']
                bars = ax.bar(labels, values, color=['#3498db', '#2ecc71'])
                
                # Add value labels
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                            f'${height:,.0f}',
                            ha='center', va='bottom')
                
                ax.set_ylabel('Amount ($)')
                st.pyplot(fig)
            
            with col2:
                # Model metrics
                st.subheader("Model Performance")
                st.metric("Mean Absolute Error (MAE)", "$37,799")
                st.metric("Root Mean Squared Error (RMSE)", "$52,889")
                st.metric("Mean Absolute Percentage Error (MAPE)", "16,98%")
                
                st.markdown("""
                <div class="feature-importance">
                <strong>Top Features:</strong>
                <ol>
                    <li>Assessed Value</li>
                    <li>Year</li>
                    <li>Property Type</li>
                </ol>
                </div>
                """, unsafe_allow_html=True)
            
            # SHAP explanation
            st.subheader("Feature Importance Analysis")
            try:
                # Get the preprocessor and model from the pipeline
                preprocessor = model.named_steps['preprocessor']
                xgb_model = model.named_steps['regressor']
                
                # Prepare input data for SHAP
                input_df = pd.DataFrame([st.session_state.input_data])
                input_transformed = preprocessor.transform(input_df)
                
                # Create SHAP explainer
                explainer = shap.Explainer(xgb_model)
                shap_values = explainer(input_transformed)
                
                # Plot SHAP values
                fig = plt.figure(figsize=(10,5))
                shap.plots.waterfall(shap_values[0], show=False)
                st.pyplot(fig)

                
                st.markdown("""
                <div class="feature-importance">
                <strong>How to interpret:</strong>
                <ul>
                    <li>Positive values increase the predicted price</li>
                    <li>Negative values decrease the predicted price</li>
                    <li>Bar length shows the magnitude of effect</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"Could not generate SHAP explanation: {str(e)}")
    main()

        # Model information in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ About the Model")
    st.sidebar.markdown("""
        This XGBoost model was optimized for real estate price prediction with:
        - Hyperparameter tuning
        - Feature engineering
        - Cross-validation
        
        **Best Parameters:**
        - n_estimators: 100
        - max_depth: 5
        - learning_rate: 0.1
        """)
if __name__ == '__main__':
    tampilkan_prediksi()
    