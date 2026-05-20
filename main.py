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

# --- AGGRESSIVE DIAGNOSTIC PIPELINE ---
# We removed the cache here temporarily so it forces a fresh check every time we click the button
def fetch_market_data(watchlist):
    st.info("DEBUG: Knocking on Yahoo's door...")
    try:
        tickers = Ticker(watchlist)
        data = tickers.summary_detail
        st.info("DEBUG: Yahoo answered the door. Checking data...")
    except Exception as e:
        st.error(f"CRITICAL CONNECTION ERROR: {e}")
        return pd.DataFrame()

    results = []
    for ticker in watchlist:
        try:
            if isinstance(data, dict) and ticker in data:
                info = data[ticker]
                
                # If Yahoo specifically blocked or couldn't find this stock, it returns a string message
                if isinstance(info, str):
                    st.warning(f"⚠️ Yahoo Error for {ticker}: {info}")
                    continue
                    
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
            else:
                st.warning(f"⚠️ Missing data for {ticker}")
        except Exception as e:
            st.error(f"❌ Error reading data for {ticker}: {e}")
            
    return pd.DataFrame(results)

# ==========================================
# PAGE 1: MASTER SCREENER
# ==========================================
if page == "📊 Master Screener (Cash Calculator)":
    st.title("📊 Master Dividend Screener")
    st.write("Diagnostic Mode Activated.")
    
    cash = st.number_input("Enter Available Cash ($)", min_value=0.0, value=5000.0, step=500.0)
    
    if st.button("Scan Market"):
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
            st.success("Batch download successful!")
        else:
            st.error("Market data fetch failed. Look at the warnings above to see exactly why.")

# --- PLACEHOLDERS ---
elif page == "🔍 Individual Stock Lookup":
    st.title("🔍 Stock Profile & Live Search")
    st.write("Under construction in Phase 2...")
# ... (rest of placeholders)
