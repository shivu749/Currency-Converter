import streamlit as st
from PIL import Image
import pandas as pd
import requests
import os

# Load Image
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "Logo.jpeg")

image = Image.open(image_path)

st.image(image, width=500)

st.title("Currency Converter App")
st.markdown("This app interconverts the value of foreign currencies!")

# Sidebar
st.sidebar.header("Input Options")

# Currency List
currency_list = [
    "AUD", "BGN", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "GBP", "HKD", "HRK", "HUF",
    "IDR", "ILS", "INR", "ISK", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PLN",
    "RON", "RUB", "SEK", "SGD", "THB", "TRY", "USD", "ZAR"
]

base_price_unit = st.sidebar.selectbox("Select base currency for conversion", currency_list)
symbols_price_unit = st.sidebar.selectbox("Select target currency to convert to", currency_list)

# API Call
@st.cache_data
def load_data(base_currency, target_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    
    if response.status_code != 200:
        st.error("Error fetching exchange rates. Please try again later.")
        return pd.DataFrame()
    
    data = response.json()
    conversion_rate = data["rates"].get(target_currency, None)
    
    if conversion_rate is None:
        st.error("Invalid currency pair. Please select different currencies.")
        return pd.DataFrame()
    
    df = pd.DataFrame(
        {"Base Currency": [base_currency], "Converted Currency": [target_currency], "Exchange Rate": [conversion_rate]}
    )
    return df

df = load_data(base_price_unit, symbols_price_unit)

st.header("Currency Conversion")
st.write(df)

# About Section
with st.expander("About"):
    st.write("This app uses real-time exchange rates to convert currencies.")



