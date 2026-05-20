import streamlit as st
import finnhub
import pandas as pd

st.set_page_config(layout="wide", page_title="Dividend Dashboard")

# Your Finnhub API Key
FINNHUB_KEY = "d86mnv1r01qgiu4641kgd86mnv1r01qgiu4641l0"
finnhub_client = finnhub.Client(api_key=FINNHUB_KEY)

WATCH_LIST = ["ENB", "TD", "BCE", "T", "KO", "O", "VZ", "JNJ", "MSFT", "AAPL"]

@st.cache_data(ttl="1d", show_spinner=False)
def get_stock_data(tickers):
    data = []
    for ticker in tickers:
        try:
            # Fetch price
            quote = finnhub_client.quote(ticker)
            # Fetch basic financials (including dividend yield)
            metrics = finnhub_client.company_basic_financials(ticker, 'margin')
            
            price = quote.get('c', 0)
            # Extract dividend yield
            yield_val = metrics.get('metric', {}).get('dividendYieldAnnual', 0)
            
            data.append({"Stock": ticker, "Price": price, "Yield %": yield_val})
        except Exception:
            continue
    return pd.DataFrame(data)

st.title("📊 Master Dividend Screener")
if st.button("Scan Market"):
    with st.spinner("Fetching live data..."):
        df = get_stock_data(WATCH_LIST)
        st.dataframe(df, use_container_width=True)
