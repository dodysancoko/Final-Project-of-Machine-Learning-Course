import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load('svm_stroke_model.pkl')

# Judul aplikasi
st.title("Aplikasi Prediksi Stroke")
st.write("Masukkan data pasien untuk memprediksi kemungkinan terkena stroke.")

# Form input
with st.form("form_stroke"):
    name = st.text_input("Nama Pasien")
    gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    age = st.number_input("Usia", min_value=0, max_value=120)
    hypertension = st.selectbox("Hipertensi", ["Tidak", "Iya"])
    heart_disease = st.selectbox("Penyakit Jantung", ["Tidak", "Iya"])
    ever_married = st.selectbox("Pernah Menikah", ["Tidak", "Iya"])
    work_type = st.selectbox("Jenis Pekerjaan", ["Pegawai Swasta", "Wiraswasta", "PNS", "Anak-anak", "Belum Pernah Bekerja"])
    residence_type = st.selectbox("Tinggal di", ["Perkotaan", "Pedesaan"])
    avg_glucose_level = st.number_input("Rata-rata Kadar Glukosa")
    bmi = st.number_input("BMI")
    smoking_status = st.selectbox("Status Merokok", ["Bekas Perokok", "Tidak Pernah Merokok", "Masih Merokok", "Tidak Diketahui"])

    # Tombol prediksi besar dan di tengah dengan st.form_submit_button, pakai style css
    submitted = st.form_submit_button("Prediksi", help="Klik untuk memprediksi")

# Saat tombol ditekan
if submitted:
    if not name.strip():
        st.warning("Mohon isi nama pasien terlebih dahulu.")
    else:
        # Encode input sesuai dengan pelatihan model
        gender = 1 if gender == "Laki-laki" else (2 if gender == "Lainnya" else 0)
        hypertension = 1 if hypertension == "Iya" else 0
        heart_disease = 1 if heart_disease == "Iya" else 0
        ever_married = 1 if ever_married == "Iya" else 0
        residence_type = 1 if residence_type == "Perkotaan" else 0

        work_type_dict = {
            "Pegawai Swasta": 0,
            "Wiraswasta": 1,
            "PNS": 2,
            "Anak-anak": 3,
            "Belum Pernah Bekerja": 4
        }
        smoking_status_dict = {
            "Bekas Perokok": 0,
            "Tidak Pernah Merokok": 1,
            "Masih Merokok": 2,
            "Tidak Diketahui": 3
        }

        work_type = work_type_dict[work_type]
        smoking_status = smoking_status_dict[smoking_status]

        # Susun data input
        input_data = np.array([[gender, age, hypertension, heart_disease, ever_married,
                                work_type, residence_type, avg_glucose_level, bmi, smoking_status]])

        # Prediksi
        prediction = model.predict(input_data)

        # Tampilkan hasil pakai nama pasien
        if prediction[0] == 1:
            st.error(f"⚠️ {name} **berisiko** terkena stroke. Silahkan kunjungi dokter segera.")
        else:
            st.success(f"✅ Selamat, {name} **tidak berisiko** terkena stroke.")

# CSS custom supaya tombol submit lebih besar dan di tengah
st.markdown("""
    <style>
        div.stButton > button:first-child {
            display: block;
            margin: 20px auto;
            padding: 12px 48px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True)
