import streamlit as st
import pandas as pd
import requests

# Set page config
st.set_page_config(page_title="Transaction Dashboard", page_icon="💳")


# Prepare required functions
def display_cust_info(df):
    cust_info = df[
        [
            "trans_num",
            "cc_num",
            "unix_time",
            "card_holder_first",
            "card_holder_last",
            "card_holder_gender",
            "card_holder_dob",
            "address_street",
            "address_city",
            "address_state",
            "address_zip",
            "address_lat",
            "address_long",
        ]
    ]
    return cust_info


def display_trx_info(df):
    trx_info = df[
        [
            "trans_num",
            "trans_date_trans_time",
            "unix_time",
            "category",
            "amt",
            "is_fraud",
        ]
    ]
    return trx_info


def display_merch_info(df):
    merch_info = df[
        [
            "trans_num",
            "merchant",
            "unix_time",
            "merch_location_lat",
            "merch_location_long",
        ]
    ]
    return merch_info


def flatten_nested_data(df):
    # Flatten 'card_holder' column
    df_card_holder = pd.json_normalize(df["card_holder"])
    df_card_holder.columns = [
        f"card_holder_{col}" for col in df_card_holder.columns
    ]

    # Flatten 'address' column
    df_address = pd.json_normalize(df["address"])
    df_address.columns = [
        f"address_{col}" for col in df_address.columns
    ]

    # Flatten 'merch_location' column
    df_merch_location = pd.json_normalize(df["merch_location"])
    df_merch_location.columns = [
        f"merch_location_{col}" for col in df_merch_location.columns
    ]

    # Combine the flattened columns with the original DataFrame
    df_flattened = pd.concat(
        [
            df.drop(
                ["card_holder", "address", "merch_location"], axis=1
            ),
            df_card_holder,
            df_address,
            df_merch_location,
        ],
        axis=1,
    )
    return df_flattened


# Sidebar for input
st.sidebar.header("Input Section")
cc_num = st.sidebar.text_input("Credit Card No: ")

# If credit card number is entered
if cc_num:
    # Make an API call to the FastAPI endpoint
    # url = "http://api-ingest:80/get_transactions"  # Adjust URL if necessary
    url = "http://localhost:80/get_transactions"  # Adjust URL if necessary
    response = requests.post(url, json={"cc_num": cc_num})

    if response.status_code == 200:
        # Parse the response
        transactions = response.json()["transactions"]
        df = pd.read_json(transactions)

        # Drop duplicates based on 'trans_num' column
        df.drop_duplicates(subset=["trans_num"], inplace=True)
        df = flatten_nested_data(df)
        df.reset_index(drop=True, inplace=True)

        # Customer Info Section
        st.markdown(
            "<div style='background-color: #f0f8ff; padding: 2px; border-radius: 7px;'><h3 style='color: #004d00; margin: 0;'>Customer Info <span style='font-size: 16px;'>👤</span></h3></div>",
            unsafe_allow_html=True,
        )
        st.dataframe(display_cust_info(df))

        # Transaction Detail Info Section
        st.markdown(
            "<div style='background-color: #f0f8ff; padding: 2px; border-radius: 7px;'><h3 style='color: #004d00; margin: 0;'>Transaction Detail Info <span style='font-size: 16px;'>📊</span></h3></div>",
            unsafe_allow_html=True,
        )
        st.dataframe(display_trx_info(df))

        # Merchant Info Section
        st.markdown(
            "<div style='background-color: #f0f8ff; padding: 2px; border-radius: 7px;'><h3 style='color: #004d00; margin: 0;'>Merchant Info <span style='font-size: 16px;'>🏪</span></h3></div>",
            unsafe_allow_html=True,
        )
        st.dataframe(display_merch_info(df))

        # Merchant Location Mapping
        if "merch_location_lat" in df.columns:
            df = df.dropna(
                subset=["merch_location_lat", "merch_location_long"]
            )
            df = df.rename(
                columns={
                    "merch_location_lat": "latitude",
                    "merch_location_long": "longitude",
                }
            )
            map_df = df[["latitude", "longitude"]]

            if not map_df.empty:
                st.markdown(
                    "<div style='background-color: #f0f8ff; padding: 2px; border-radius: 7px;'><h3 style='color: #004d00; margin: 0;'>Merchant Location Mapping <span style='font-size: 16px;'>🗺️</span></h3></div>",
                    unsafe_allow_html=True,
                )
                st.map(map_df[["latitude", "longitude"]])
            else:
                st.write(
                    "No valid merchant location data for the given credit card number."
                )
        else:
            st.write(
                "No merchant location data found for the given credit card number."
            )
    else:
        st.error(
            f"Error {response.status_code}: {response.json()['detail']}"
        )

# Footer Section
st.markdown(
    "<footer style='text-align: center; padding: 2px; background-color: #f0f8ff;'><p style='color: #004d00;'>© 2024 Transaction Dashboard | Developed with ❤️</p></footer>",
    unsafe_allow_html=True,
)
