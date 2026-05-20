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

# Global Watchlist for the Screener
WATCH_LIST = ["ENB.TO", "TD.TO", "BCE.TO", "T.TO", "KO", "O", "VZ", "JNJ", "MSFT", "AAPL"]

# ==========================================
# PAGE 1: MASTER SCREENER
# ==========================================
if page == "📊 Master Screener (Cash Calculator)":
    st.title("📊 Master Dividend Screener")
    st.write("Enter your cash balance to instantly see what it can buy across top CAD and USD dividend stocks.")
    
    cash = st.number_input("Enter Available Cash ($)", min_value=0.0, value=5000.0, step=500.0)
    
    if st.button("Scan Market"):
        st.info("Gathering live data from Yahoo Finance... please wait.")
        results = []
        
        for ticker in WATCH_LIST:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                
                # Pull live price and dividend data safely
                price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose')
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
            except:
                pass # Skip broken tickers
                
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)
            st.success("Tip: Click on column headers (like Expected Annual Income) to sort the rows!")
        else:
            st.error("Data fetch failed. Try again.")

# --- PLACEHOLDERS FOR OTHER PAGES ---
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
