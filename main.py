import streamlit as st
import yfinance as yf
import pandas as pd
import math
import requests

# Force wide-screen layout
st.set_page_config(layout="wide", page_title="Dividend Dashboard", page_icon="💰")

# --- THE DISGUISE ---
# We create a fake "browser" session to trick Yahoo Finance into thinking we are a human
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
})

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

# ==========================================
# PAGE 1: MASTER SCREENER
# ==========================================
if page == "📊 Master Screener (Cash Calculator)":
    st.title("📊 Master Dividend Screener")
    st.write("Enter your cash balance to instantly see what it can buy across top CAD and USD dividend stocks.")
    
    cash = st.number_input("Enter Available Cash ($)", min_value=0.0, value=5000.0, step=500.0)
    
    if st.button("Scan Market"):
        st.info("Bypassing security and gathering live data... please wait.")
        results = []
        
        for ticker in WATCH_LIST:
            try:
                # We pass the disguised session into yfinance here!
                stock = yf.Ticker(ticker, session=session)
                
                price = stock.fast_info.get('lastPrice')
                info = stock.info
                dividend = info.get('dividendRate', 0.0)
                yield_pct = info.get('dividendYield', 0.0)
                
                if price and price > 0:
                    shares = math.floor(cash / price)
                    cost = shares * price
                    leftover = cash - cost
                    safe_div = dividend if dividend is not None else 0.0
                    annual_income = shares * safe_div
                    safe_yield = (yield_pct * 100) if yield_pct is not None else 0.0
                    currency = "CAD" if ticker.endswith(".TO") else "USD"
                    
                    results.append({
                        "Stock": ticker,
                        "Exchange": currency,
                        "Live Price": f"${price:.2f}",
                        "Yield": f"{safe_yield:.2f}%",
                        "Shares to Buy": shares,
                        "Expected Annual Income": f"${annual_income:.2f}",
                        "Leftover Cash": f"${leftover:.2f}"
                    })
            except Exception as e:
                st.warning(f"Could not load data for {ticker}. Error: {e}")
                
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)
            st.success("Tip: Click on column headers to sort the rows!")
        else:
            st.error("All data fetches failed.")

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
