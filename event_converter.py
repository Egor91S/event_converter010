import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Event Converter", page_icon="✅", layout="centered")


def main():
    date_time = []
    st.header("Event Converter")

    uploaded_file = st.file_uploader("Upload .LOG file", type=".LOG")
    if uploaded_file is not None:
        log_data = uploaded_file.getvalue().decode('utf-8').splitlines()

        text_date = [text[7:17].replace(".", "") for text in log_data if text.startswith("0000")]
        text_time = [text[18:26] for text in log_data if text.startswith("0000")]
        text_easting = [text[31:41] for text in log_data if text.startswith("0000")]
        text_northing = [text[42:53] for text in log_data if text.startswith("0000")]

        for i in range(len(text_date)):
            date_time.append(f"{text_date[i]}/{text_time[i]}")

        data = {"Waypoint name": date_time, "Easting": text_easting, "Northing": text_northing}
        df = pd.DataFrame(data)
        st.write(df)

        csv = convert_df(df)
        st.download_button("Download CSV", data=csv, file_name="convert_output.csv", mime="text/csv")


@st.cache_data
def read_data(path_local):
    with open(path_local, "r") as file:
        log_data = file.readlines()
        return log_data


@st.cache_data
def convert_df(df):
    return df.to_csv(header=False, index=False).encode('utf-8')


if __name__ == "__main__":
    main()
