import streamlit as st
import yfinance as yf
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

# --- THE TIME CAPSULE ---
# This saves the data for 1 day ("1d"). It prevents Yahoo from banning us!
@st.cache_data(ttl="1d", show_spinner=False)
def fetch_market_data(watchlist):
    results = []
    for ticker in watchlist:
        try:
            # Notice we removed the "session" disguise completely, as the error requested
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
                    "Stock": ticker,
                    "Exchange": currency,
                    "Live Price": price,
                    "Dividend": safe_div,
                    "Yield %": safe_yield
                })
        except Exception:
            pass # If a single stock fails, skip it quietly instead of breaking the app
            
    return pd.DataFrame(results)

# ==========================================
# PAGE 1: MASTER SCREENER
# ==========================================
if page == "📊 Master Screener (Cash Calculator)":
    st.title("📊 Master Dividend Screener")
    st.write("Enter your cash balance to instantly see what it can buy across top CAD and USD dividend stocks.")
    
    cash = st.number_input("Enter Available Cash ($)", min_value=0.0, value=5000.0, step=500.0)
    
    if st.button("Scan Market"):
        with st.spinner("Checking the Time Capsule for data..."):
            df = fetch_market_data(WATCH_LIST)
            
        if not df.empty:
            # Calculate the math based on the user's cash input
            df['Shares to Buy'] = df['Live Price'].apply(lambda x: math.floor(cash / x))
            df['Expected Annual Income'] = df['Shares to Buy'] * df['Dividend']
            df['Leftover Cash'] = cash - (df['Shares to Buy'] * df['Live Price'])
            
            # Format the numbers to look like real currency
            df['Live Price'] = df['Live Price'].apply(lambda x: f"${x:.2f}")
            df['Dividend'] = df['Dividend'].apply(lambda x: f"${x:.2f}")
            df['Yield %'] = df['Yield %'].apply(lambda x: f"{x:.2f}%")
            df['Expected Annual Income'] = df['Expected Annual Income'].apply(lambda x: f"${x:.2f}")
            df['Leftover Cash'] = df['Leftover Cash'].apply(lambda x: f"${x:.2f}")
            
            st.dataframe(df, use_container_width=True)
            st.success("Data loaded successfully! It is now locked in the daily cache.")
        else:
            st.error("Market data is currently unavailable. Please try again later.")

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
