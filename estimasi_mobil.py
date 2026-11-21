
from pathlib import Path
import pickle
import streamlit as st

st.set_page_config(
    page_title="Estimasi Harga Mobil Bekas",
    layout="centered"
)

st.title("Estimasi Harga Mobil Bekas")

# Input data mobil
year = st.number_input("Input Tahun Mobil", value=0.0)
mileage = st.number_input("Input Km Mobil", value=0.0)
tax = st.number_input("Input Pajak Mobil", value=0.0)
mpg = st.number_input("Input Konsumsi BBM Mobil", value=0.0)
engineSize = st.number_input("Input Engine Size", value=0.0)

# Tombol estimasi harga
if st.button("Estimasi Harga"):

    model_path = (
        Path(__file__).resolve().parent
        / "estimasi_mobil.sav"
    )

    if not model_path.is_file():
        st.error(
            "File estimasi_mobil.sav tidak ditemukan. "
            "Simpan file model di folder yang sama."
        )

    else:
        try:
            # Membuka model prediksi
            with model_path.open("rb") as file:
                model = pickle.load(file)

            # Melakukan prediksi
            predict = model.predict(
                [[year, mileage, tax, mpg, engineSize]]
            )

            # Mengambil hasil prediksi
            harga_pounds = float(predict[0])

            # Konversi Poundsterling ke Rupiah
            kurs_pounds = 19000
            harga_rupiah = harga_pounds * kurs_pounds

            # Format harga Poundsterling
            format_pounds = f"£{harga_pounds:,.2f}"

            # Format harga Rupiah
            format_rupiah = (
                f"Rp {harga_rupiah:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

            # Menampilkan hasil estimasi
            st.subheader("Hasil Estimasi Harga Mobil Bekas")

            st.metric(
                label="Harga dalam Poundsterling (£)",
                value=format_pounds
            )

            st.metric(
                label="Harga dalam Rupiah (Rp)",
                value=format_rupiah
            )

        except Exception as exc:
            st.error("Model gagal dimuat atau diprediksi.")
            st.exception(exc)
