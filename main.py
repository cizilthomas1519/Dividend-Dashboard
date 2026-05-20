import streamlit as st
from yahooquery import Ticker
import pandas as pd
import math

# Force wide-screen layout
st.set_page_config(layout="wide", page_title="Dividend Dashboard", page_icon="💰")

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

WATCH_LIST = ["ENB.TO", "TD.TO", "BCE.TO", "T.TO", "KO", "O", "VZ", "JNJ", "MSFT", "AAPL"]

# --- THE BULK PIPELINE ---
@st.cache_data(ttl="1d", show_spinner=False)
def fetch_market_data(watchlist):
    # This grabs EVERY stock in one single lightning-fast request
    tickers = Ticker(watchlist)
    data = tickers.summary_detail
    
    results = []
    for ticker in watchlist:
        try:
            # Check if the data came back successfully for this specific stock
            if isinstance(data, dict) and ticker in data and isinstance(data[ticker], dict):
                info = data[ticker]
                price = info.get('previousClose', 0.0)
                dividend = info.get('dividendRate', 0.0)
                yield_pct = info.get('dividendYield', 0.0)
                
                if price and price > 0:
                    currency = "CAD" if ticker.endswith(".TO") else "USD"
                    safe_div = dividend if dividend is not None else 0.0
                    safe_yield = (yield_pct * 100) if yield_pct is not None else 0.0
                    
                    results.append({
                        "Stock": ticker,
                        "Exchange": currency,
                        "Live Price": price,
                        "Dividend": safe_div,
                        "Yield %": safe_yield
                    })
        except Exception:
            pass # Skip broken tickers quietly
            
    return pd.DataFrame(results)

# ==========================================
# PAGE 1: MASTER SCREENER
# ==========================================
if page == "📊 Master Screener (Cash Calculator)":
    st.title("📊 Master Dividend Screener")
    st.write("Enter your cash balance to instantly see what it can buy across top CAD and USD dividend stocks.")
    
    cash = st.number_input("Enter Available Cash ($)", min_value=0.0, value=5000.0, step=500.0)
    
    if st.button("Scan Market"):
        with st.spinner("Batch processing market data..."):
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
            st.success("Batch download successful! Data is locked in the cache.")
        else:
            st.error("Market data fetch failed. Please try again later.")

# --- PLACEHOLDERS ---
elif page == "🔍 Individual Stock Lookup":
    st.title("🔍 Stock Profile & Live Search")
    st.write("Under construction in Phase 2...")
elif page == "📅 Dividend History & Payouts":
    st.title("📅 Dividend Payout History")
    st.write("Under construction in Phase 2...")
elif page == "📆 Upcoming Ex-Dividend Calendar":
    st.title("📆 Upcoming Ex-Dividend Calendar")
    st.write("Under construction in Phase 3...")
elif page == "👑 Dividend Aristocrats":
    st.title("👑 Dividend Aristocrats List")
    st.write("Under construction in Phase 3...")
elif page == "📁 Portfolio CSV Import":
    st.title("📁 Portfolio Tracker")
    st.write("Under construction in Phase 4...")
elif page == "📈 DRIP Calculator":
    st.title("📈 DRIP & Compound Growth")
    st.write("Under construction in Phase 4...")
