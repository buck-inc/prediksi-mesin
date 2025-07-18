import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier

st.set_page_config(page_title="Prediksi Status Mesin", layout="wide")
st.title("🚀 Aplikasi Prediksi Status Mesin")

uploaded_file = st.file_uploader("📤 Upload file Excel (.xlsx)", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("📝 Edit Data")
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    if 'status' in edited_df.columns and 'suhu' in edited_df.columns:
        st.subheader("🔍 Prediksi Berdasarkan Suhu")
        if st.button("🔮 Prediksi Semua"):
            # Logika prediksi sederhana: suhu > 50 = Rusak
            edited_df['status'] = edited_df['suhu'].apply(lambda x: "Rusak" if x > 50 else "Normal")
            st.success("✅ Status berhasil diperbarui berdasarkan suhu (>50 = Rusak)")
            st.dataframe(edited_df, use_container_width=True)

            # Download hasil prediksi
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                edited_df.to_excel(writer, index=False)
            st.download_button("📥 Download Hasil", data=output.getvalue(), file_name="hasil_prediksi.xlsx")

        # Visualisasi Data
        st.subheader("📊 Visualisasi Data Sensor")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Pie Chart Status")
            fig1, ax1 = plt.subplots()
            edited_df['status'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax1)
            ax1.set_ylabel("")
            st.pyplot(fig1)

        with col2:
            st.markdown("#### Line Chart Suhu / Arus / Tegangan")
            numeric_cols = edited_df.select_dtypes(include=['number']).columns
            fig2, ax2 = plt.subplots()
            sns.lineplot(data=edited_df[numeric_cols], ax=ax2)
            ax2.set_xlabel("Index")
            ax2.set_ylabel("Nilai")
            st.pyplot(fig2)

    else:
        st.error("❌ Kolom 'status' dan 'suhu' wajib ada di file Excel kamu.")
else:
    st.info("⬆️ Silakan upload file Excel terlebih dahulu.")
