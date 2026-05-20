import streamlit as st
import requests
import pandas as pd
import math

# Force wide-screen layout
st.set_page_config(layout="wide", page_title="Dividend Dashboard", page_icon="💰")

# Your Alpha Vantage API Key
API_KEY = "O5WB1YJNUAVYFBCC"

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to:", [
    "📊 Master Screener (Cash Calculator)", 
    "🔍 Individual Stock Lookup", 
    "📅 Dividend History & Payouts",
    "📆 Upcoming Ex-Dividend Calendar",
    "👑 Dividend Aristocrats",
    "📁 Portfolio CSV Import",
    "📈 DRIP Calculator"
])

# Note: Alpha Vantage uses 'ENB' instead of 'ENB.TO'
WATCH_LIST = ["ENB", "TD", "BCE", "T", "KO", "O", "VZ", "JNJ", "MSFT", "AAPL"]

@st.cache_data(ttl="1d", show_spinner=False)
def fetch_alpha_vantage_data(watchlist):
    results = []
    for ticker in watchlist:
        try:
            # Using the GLOBAL_QUOTE endpoint
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}"
            response = requests.get(url).json()
            
            if "Global Quote" in response and response["Global Quote"]:
                data = response["Global Quote"]
                price = float(data.get("05. price", 0))
                
                # Alpha Vantage basic tier doesn't always provide dividend yield. 
                # For this setup, we'll use a placeholder or add logic later.
                results.append({
                    "Stock": ticker,
                    "Live Price": price,
                    "Yield %": "N/A" # Placeholder
                })
        except Exception:
            continue
    return pd.DataFrame(results)

# ==========================================
# PAGE 1: MASTER SCREENER
# ==========================================
if page == "📊 Master Screener (Cash Calculator)":
    st.title("📊 Master Dividend Screener")
    st.write("Fetching data via Alpha Vantage API.")
    
    cash = st.number_input("Enter Available Cash ($)", min_value=0.0, value=5000.0, step=500.0)
    
    if st.button("Scan Market"):
        with st.spinner("Connecting to API..."):
            df = fetch_alpha_vantage_data(WATCH_LIST)
            
        if not df.empty:
            df['Shares to Buy'] = df['Live Price'].apply(lambda x: math.floor(cash / x) if x > 0 else 0)
            st.dataframe(df, use_container_width=True)
            st.success("API Data Loaded!")
        else:
            st.error("Could not fetch data. The API key might have hit a limit.")
