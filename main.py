import streamlit as st
import requests
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

# --- THE RAW DATA PIPELINE ---
@st.cache_data(ttl="1d", show_spinner=False)
def fetch_market_data(watchlist):
    results = []
    try:
        # We bypass all tools and hit Yahoo's raw data feed directly
        symbols = ",".join(watchlist)
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbols}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if "quoteResponse" in data and "result" in data["quoteResponse"]:
            for stock in data["quoteResponse"]["result"]:
                ticker = stock.get("symbol")
                price = stock.get("regularMarketPrice", 0.0)
                
                # Grab the dividends (Yahoo sometimes uses different names for these fields)
                dividend = stock.get("dividendRate", stock.get("trailingAnnualDividendRate", 0.0))
                yield_pct = stock.get("dividendYield", stock.get("trailingAnnualDividendYield", 0.0))
                currency = stock.get("currency", "USD")
                
                if price and price > 0:
                    results.append({
                        "Stock": ticker,
                        "Exchange": currency,
                        "Live Price": price,
                        "Dividend": dividend,
                        "Yield %": yield_pct * 100
                    })
    except Exception as e:
        st.error(f"Pipeline Error: {e}")
        
    return pd.DataFrame(results)

# ==========================================
# PAGE 1: MASTER SCREENER
# ==========================================
if page == "📊 Master Screener (Cash Calculator)":
    st.title("📊 Master Dividend Screener")
    st.write("Enter your cash balance to instantly see what it can buy across top CAD and USD dividend stocks.")
    
    cash = st.number_input("Enter Available Cash ($)", min_value=0.0, value=5000.0, step=500.0)
    
    if st.button("Scan Market"):
        with st.spinner("Connecting to raw data feed..."):
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
            st.success("Direct feed connection successful! Data is locked in the cache.")
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
