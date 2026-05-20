import streamlit as st
import finnhub
import pandas as pd

st.set_page_config(layout="wide", page_title="Dividend Dashboard")

# Your personal Finnhub API Key is already here
FINNHUB_KEY = "d86mnv1r01qgiu4641kgd86mnv1r01qgiu4641l0"
finnhub_client = finnhub.Client(api_key=FINNHUB_KEY)

WATCH_LIST = ["ENB", "TD", "BCE", "T", "KO", "O", "VZ", "JNJ", "MSFT", "AAPL"]

@st.cache_data(ttl="1d", show_spinner=False)
def get_stock_data(tickers):
    data = []
    for ticker in tickers:
        try:
            # Fetch live price
            quote = finnhub_client.quote(ticker)
            price = quote.get('c', 0)
            
            # Fetch company profile (for Currency)
            profile = finnhub_client.company_profile2(symbol=ticker)
            currency = profile.get('currency', 'USD')
            
            # Fetch basic financials ('all' gets us the dividend data)
            financials = finnhub_client.company_basic_financials(ticker, 'all')
            metrics = financials.get('metric', {})
            
            # Extract specific dividend metrics
            annual_div = metrics.get('dividendPerShareAnnual', 0)
            yield_pct = metrics.get('dividendYieldIndicatedAnnual', 0)
            
            # Calculate the monthly average
            monthly_est = (annual_div / 12) if annual_div else 0
            
            data.append({
                "Stock": ticker, 
                "Currency": currency,
                "Price": price, 
                "Annual Div": annual_div,
                "Monthly Est.": monthly_est,
                "Yield %": yield_pct
            })
        except Exception:
            continue
    return pd.DataFrame(data)

st.title("📊 Master Dividend Screener")
if st.button("Scan Market"):
    with st.spinner("Fetching live full-profile data..."):
        df = get_stock_data(WATCH_LIST)
        
        if not df.empty:
            df['Price'] = df['Price'].apply(lambda x: f"${x:.2f}")
            df['Annual Div'] = df['Annual Div'].apply(lambda x: f"${x:.2f}" if x > 0 else "N/A")
            df['Monthly Est.'] = df['Monthly Est.'].apply(lambda x: f"${x:.2f}" if x > 0 else "N/A")
            df['Yield %'] = df['Yield %'].apply(lambda x: f"{x:.2f}%" if x > 0 else "N/A")
            
            st.dataframe(df, use_container_width=True)
        else:
            st.error("No data returned.")
