import streamlit as st
import yfinance as yf
import pandas as pd
import math

st.set_page_config(layout="wide", page_title="Dividend Dashboard", page_icon="💰")

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

WATCH_LIST = ["ENB.TO", "TD.TO", "BCE.TO", "T.TO", "KO", "O", "VZ", "JNJ", "MSFT", "AAPL"]

@st.cache_data(ttl="1d", show_spinner=False)
def fetch_market_data(watchlist):
    results = []
    for ticker in watchlist:
        try:
            stock = yf.Ticker(ticker)
            price = stock.fast_info.get('lastPrice')
            info = stock.info
            dividend = info.get('dividendRate', 0.0)
            yield_pct = info.get('dividendYield', 0.0)
            
            if price and price > 0:
                safe_div = dividend if dividend is not None else 0.0
                safe_yield = (yield_pct * 100) if yield_pct is not None else 0.0
                currency = "CAD" if ticker.endswith(".TO") else "USD"
                
                results.append({
                    "Stock": ticker, "Exchange": currency, "Live Price": price,
                    "Dividend": safe_div, "Yield %": safe_yield
                })
        except Exception:
            pass 
    return pd.DataFrame(results)

if page == "📊 Master Screener (Cash Calculator)":
    st.title("📊 Master Dividend Screener")
    st.write("Enter your cash balance to instantly see what it can buy across top CAD and USD dividend stocks.")
    
    cash = st.number_input("Enter Available Cash ($)", min_value=0.0, value=5000.0, step=500.0)
    
    if st.button("Scan Market"):
        with st.spinner("Scanning the market..."):
            df = fetch_market_data(WATCH_LIST)
            
        if not df.empty:
            df['Shares to Buy'] = df['Live Price'].apply(lambda x: math.floor(cash / x))
            df['Expected Annual Income'] = df['Shares to Buy'] * df['Dividend']
            df['Leftover Cash'] = cash - (df['Shares to Buy'] * df['Live Price'])
            
            df['Live Price'] = df['Live Price'].apply(lambda x: f"${x:.2f}")
            df['Dividend'] = df['Dividend'].apply(lambda x: f"${x:.2f}")
            df['Yield %'] = df['Yield %'].apply(lambda x: f"{x:.2f}%")
            df['Expected Annual Income'] = df['Expected Annual Income'].apply(lambda x: f"${x:.2f}")
            df['Leftover Cash'] = df['Leftover Cash'].apply(lambda x: f"${x:.2f}")
            
            st.dataframe(df, use_container_width=True)
            st.success("Scan complete! Data locked in cache.")
        else:
            st.error("Fetch failed. The server blocked the request.")

# --- PLACEHOLDERS ---
elif page == "🔍 Individual Stock Lookup":
    st.title("🔍 Stock Profile & Live Search")
    st.write("Under construction in Phase 2...")
elif page == "📅 Dividend History & Payouts":
    st.title("📅 Dividend Payout History")
    st.write("Under construction...")
