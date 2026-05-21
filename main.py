import streamlit as st
import pandas as pd
import math

st.set_page_config(layout="wide", page_title="Dividend Dashboard")

st.title("📁 Master Offline Dividend Screener")
st.write("Upload your custom Master Database CSV here to run your portfolio calculator.")

uploaded_file = st.file_uploader("Drop your My_Master_Database.csv here", type=["csv"])

if uploaded_file is not None:
    try:
        # Read your custom file
        df = pd.read_csv(uploaded_file)
        
        # Translate your bot's column names into math-friendly numbers
        df['Price'] = df['Live Price'].replace('[\$,]', '', regex=True)
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0)
        
        # Calculate the Annual Payout based on the Yield and Price
        df['Yield Decimal'] = df['Yield %'].replace('[\%,N/A]', '', regex=True)
        df['Yield Decimal'] = pd.to_numeric(df['Yield Decimal'], errors='coerce').fillna(0) / 100
        df['Annual Payout'] = df['Price'] * df['Yield Decimal']
            
        st.success("✅ Custom Database connected successfully!")
        
        # --- THE CASH CALCULATOR ---
        st.write("---")
        st.subheader("📊 Portfolio Calculator")
        cash = st.number_input("Enter Available Cash ($)", min_value=0.0, value=5000.0, step=500.0)
        
        with st.spinner("Calculating..."):
            # The Math
            df['Shares to Buy'] = df['Price'].apply(lambda x: math.floor(cash / float(x)) if float(x) > 0 else 0)
            df['Expected Annual Income'] = df['Shares to Buy'] * df['Annual Payout']
            df['Leftover Cash'] = cash - (df['Shares to Buy'] * df['Price'])
            
            # Format the visual display
            display_df = df.copy()
            columns_to_show = ['Stock', 'Live Price', 'Yield %', 'Next Ex-Div Date', 'Shares to Buy', 'Expected Annual Income', 'Leftover Cash']
            display_df = display_df[[col for col in columns_to_show if col in display_df.columns]]
            
            display_df['Expected Annual Income'] = display_df['Expected Annual Income'].apply(lambda x: f"${float(x):.2f}")
            display_df['Leftover Cash'] = display_df['Leftover Cash'].apply(lambda x: f"${float(x):.2f}")
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
    except Exception as e:
        st.error(f"Could not read the file. Error: {e}")
else:
    st.info("Waiting for you to attach your Master Database file...")
