#below is sample script for create a main.py for streamlit
#import related library for use case

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
            "card_holder_last"
        ]
    ]
    return cust_info


def display_trx_info(df):
    trx_info = df[
        [
            "trans_num",
            "trans_date_trans_time"
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
    url = "http://api-ingest:xx/get_transactions"  # Adjust URL and port if necessary
    # url = "http://localhost:xx/get_transactions"  # Adjust URL if necessary
    response = requests.post(url, json={"cc_num": cc_num})

    if response.status_code == 200:
        # Parse the response
        transactions = response.json()["transactions"]
        df = pd.read_json(transactions)

        # Customer Info Section
        st.markdown(
            "<div style='background-color: #f0f8ff; padding: 2px; border-radius: 7px;'><h3 style='color: #004d00; margin: 0;'>Customer Info <span style='font-size: 16px;'>👤</span></h3></div>",
            unsafe_allow_html=True,
        )
        st.dataframe(display_cust_info(df))

    else:
        st.error(
            f"Error {response.status_code}: {response.json()['detail']}"
        )
