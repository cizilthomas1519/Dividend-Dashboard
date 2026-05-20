import streamlit as st

# Force wide-screen layout for a professional look
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

# --- PAGE ROUTING ---
if page == "📊 Master Screener (Cash Calculator)":
    st.title("📊 Master Dividend Screener")
    st.write("This page will scan multiple stocks and calculate exactly what your cash can buy.")
    
elif page == "🔍 Individual Stock Lookup":
    st.title("🔍 Stock Profile & Live Search")
    st.write("This page will let you search any ticker to see live pricing and business details.")
    
elif page == "📅 Dividend History & Payouts":
    st.title("📅 Dividend Payout History")
    st.write("This page will show interactive charts of a company's past dividend payouts.")

elif page == "📆 Upcoming Ex-Dividend Calendar":
    st.title("📆 Upcoming Ex-Dividend Calendar")
    st.write("This page will display a calendar of upcoming dates to capture dividends.")

elif page == "👑 Dividend Aristocrats":
    st.title("👑 Dividend Aristocrats List")
    st.write("This page will track companies with 25+ years of dividend growth.")

elif page == "📁 Portfolio CSV Import":
    st.title("📁 Portfolio Tracker")
    st.write("This page will let you upload a CSV of your holdings to calculate your total income.")

elif page == "📈 DRIP Calculator":
    st.title("📈 DRIP & Compound Growth")
    st.write("This page will calculate how your portfolio snowballs over 10 to 30 years.")
