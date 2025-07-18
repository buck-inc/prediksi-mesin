import streamlit as st
import pandas as pd
import io
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Prediksi & Visualisasi", layout="wide")
st.title("📈 Prediksi & Visualisasi Status Mesin")

file = st.file_uploader("Upload File Excel (.xlsx)", type="xlsx")

if file:
    df = pd.read_excel(file)

    st.subheader("📝 Edit Data")
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    if 'status' in edited_df.columns:
        X = edited_df.drop(columns='status')
        y = edited_df['status']

        model = DecisionTreeClassifier()
        model.fit(X, y)
        st.success("✅ Model berhasil dilatih dari data yang sudah diedit!")

        st.subheader("🔍 Prediksi Data Semua Baris")
        if st.button("🔮 Prediksi Semua"):
            pred = model.predict(X)
            edited_df['status'] = pred
            st.dataframe(edited_df, use_container_width=True)

            # Simpan ke file Excel agar bisa di-download
            output = io.BytesIO()
            edited_df.to_excel(output, index=False, engine='openpyxl')
            st.download_button("📥 Download Hasil Prediksi", data=output.getvalue(), file_name="hasil_prediksi.xlsx")

        # --- Visualisasi ---
        st.subheader("📊 Visualisasi Data")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Distribusi Status (Pie Chart)")
            status_count = edited_df['status'].value_counts()
            fig1, ax1 = plt.subplots()
            ax1.pie(status_count, labels=status_count.index, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)

        with col2:
            st.markdown("#### Tren Sensor (Line Chart)")
            fig2, ax2 = plt.subplots()
            sns.lineplot(data=edited_df.drop(columns='status'), ax=ax2)
            ax2.set_xlabel("Index")
            ax2.set_ylabel("Nilai Sensor")
            st.pyplot(fig2)

    else:
        st.error("❌ Kolom 'status' tidak ditemukan dalam data.")
