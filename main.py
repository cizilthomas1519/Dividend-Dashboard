import streamlit as st
import finnhub
import pandas as pd

st.set_page_config(layout="wide", page_title="Dividend Dashboard")

FINNHUB_KEY = "d86mnv1r01qgiu4641kgd86mnv1r01qgiu4641l0"
finnhub_client = finnhub.Client(api_key=FINNHUB_KEY)

@st.cache_data(ttl="1d", show_spinner=False)
def get_stock_data(tickers):
    data = []
    for ticker in tickers:
        try:
            quote = finnhub_client.quote(ticker)
            price = quote.get('c', 0)
            
            profile = finnhub_client.company_profile2(symbol=ticker)
            currency = profile.get('currency', 'USD')
            
            financials = finnhub_client.company_basic_financials(ticker, 'all')
            metrics = financials.get('metric', {})
            
            annual_div = metrics.get('dividendPerShareAnnual', 0)
            yield_pct = metrics.get('dividendYieldIndicatedAnnual', 0)
            
            data.append({
                "Stock": ticker, 
                "Currency": currency,
                "Price": price, 
                "Annual Payout": annual_div,
                "Frequency": "N/A (Free API Limit)", 
                "Yield %": yield_pct
            })
        except Exception:
            continue
    return pd.DataFrame(data)

st.title("📊 Master Dividend Screener")

# A dynamic input box instead of a hardcoded list
st.write("Enter the stock symbols you want to scan, separated by commas.")
user_tickers = st.text_input("Watchlist:", "ENB, TD, BCE, T, KO, O, VZ, JNJ, MSFT, AAPL")

if st.button("Scan Market"):
    # Clean up the user's input list
    clean_list = [t.strip().upper() for t in user_tickers.split(",") if t.strip()]
    
    with st.spinner("Fetching live data..."):
        df = get_stock_data(clean_list)
        
        if not df.empty:
            df['Price'] = df['Price'].apply(lambda x: f"${x:.2f}")
            df['Annual Payout'] = df['Annual Payout'].apply(lambda x: f"${x:.2f}" if x > 0 else "N/A")
            df['Yield %'] = df['Yield %'].apply(lambda x: f"{x:.2f}%" if x > 0 else "N/A")
            
            # hide_index=True completely removes the 0, 1, 2, 3 column!
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.error("No data returned. Check your ticker symbols.")
