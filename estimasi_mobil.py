

from pathlib import Path
import pickle
import streamlit as st

st.set_page_config(
    page_title="Estimasi Harga Mobil Bekas",
    layout="centered"
)

st.title("Estimasi Harga Mobil Bekas")

year = st.number_input("Input Tahun Mobil", value=0.0)
mileage = st.number_input("Input Km Mobil", value=0.0)
tax = st.number_input("Input Pajak Mobil", value=0.0)
mpg = st.number_input("Input Konsumsi BBM Mobil", value=0.0)
engineSize = st.number_input("Input Engine Size", value=0.0)

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
            with model_path.open("rb") as file:
                model = pickle.load(file)

            predict = model.predict(
                [[year, mileage, tax, mpg, engineSize]]
            )

            st.write(
                "Estimasi harga mobil bekas dalam Pounds : ",
                predict)
                
            st.write( "Estimasi harga mobil bekas dalam IDR (Juta) : ",predict*19000 
                                                              
            )

        except Exception as exc:
            st.error("Model gagal dimuat atau diprediksi.")
            st.exception(exc)

