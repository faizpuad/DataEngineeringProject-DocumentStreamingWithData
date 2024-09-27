import streamlit as st
import pandas as pd
import requests

# Below the fist chart add a input field for the credit card number
cc_num = st.sidebar.text_input("Credit Card No: ")
# st.text(inv_no)  # Use this to print out the content of the input field

# if enter has been used on the input field
if cc_num:

    # Make an API call to the FastAPI endpoint
    url = "http://api-ingest:80/get_transactions"  # Adjust URL if necessary
    response = requests.post(url, json={"cc_num": cc_num})
    
    if response.status_code == 200:
        # Parse the response
        transactions = response.json()["transactions"]
        # Convert to a pandas DataFrame
        df = pd.read_json(transactions)
        
        # Drop duplicates based on 'trans_num' column
        df.drop_duplicates(subset=['trans_num'], inplace=True)

        # Optionally reset the index if needed
        df.reset_index(drop=True, inplace=True)

        # Add the table with a headline
        st.header("Customer Transaction Detail")
        table2 = st.dataframe(data=df)

        if 'merch_location' in df.columns:
            df['latitude'] = df['merch_location'].apply(lambda x: x['lat'] if x else None)
            df['longitude'] = df['merch_location'].apply(lambda x: x['long'] if x else None)

            # Filter only valid lat/long
            df = df.dropna(subset=['latitude', 'longitude'])

            # Prepare DataFrame with 'latitude' and 'longitude' columns
            map_df = df[['latitude', 'longitude']]

            # Display the map using Streamlit
            if not map_df.empty:
                st.header("Merchant Location")
                st.map(map_df)
            else:
                st.write("No valid merch_location data for the given cc_num.")

        else:
            st.write("No merch_location data found for the given cc_num.")

    else:
        st.error(f"Error {response.status_code}: {response.json()['detail']}")