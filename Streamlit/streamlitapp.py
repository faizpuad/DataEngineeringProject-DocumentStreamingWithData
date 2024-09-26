import streamlit as st
from pandas import DataFrame
import pymongo


# data = pd.read_csv("data.csv")
myclient = pymongo.MongoClient(
    "mongodb://mongo:27017/", username="root", password="example"
)
mydb = myclient["transaction"]
mycol = mydb["creditcard"]


# Below the fist chart add a input field for the credit card number
cc_num = st.sidebar.text_input("Credit Card No: ")
# st.text(inv_no)  # Use this to print out the content of the input field

# if enter has been used on the input field
if cc_num:

    myquery = {"cc_num": cc_num}
    # only includes or excludes
    myquery = {"cc_num": cc_num}
    mydoc = mycol.find(myquery)

    # create dataframe from resulting documents to use drop_duplicates
    df = DataFrame(mydoc)

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


# # Below the fist chart add a input field for the invoice number
# inv_no = st.sidebar.text_input("InvoiceNo:")
# # st.text(inv_no)  # Use this to print out the content of the input field

# # if enter has been used on the input field
# if inv_no:

#     myquery = {"InvoiceNo": inv_no}
#     mydoc = mycol.find(
#         myquery,
#         {"_id": 0, "InvoiceDate": 0, "Country": 0, "CustomerID": 0},
#     )

#     # create the dataframe
#     df = DataFrame(mydoc)

#     # reindex it so that the columns are order lexicographically
#     reindexed = df.reindex(sorted(df.columns), axis=1)

#     # Add the table with a headline
#     st.header("Output by Invoice ID")
#     table2 = st.dataframe(data=reindexed)
