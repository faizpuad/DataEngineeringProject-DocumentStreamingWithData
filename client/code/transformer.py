import numpy as np
import pandas as pd
import json
import os

# Get the current working directory
current_path = os.getcwd()
print("Current Working Directory:", current_path)

# Load data
data_loc = "./data/fraudTrain.csv"

# load only 15 for testing
# df = pd.read_csv(data_loc).head(15)
df = pd.read_csv(data_loc)
print(df.head(2))

# add a json column to the dataframe
# splitlines will split the json into multiple rows not a single one
# Transforming to desired JSON structure
features = []
for _, row in df.iterrows():
    transformed = {
        "trans_num": row["trans_num"],
        "trans_date_trans_time": row["trans_date_trans_time"],
        "cc_num": row["cc_num"],
        "merchant": row["merchant"],
        "category": row["category"],
        "amt": row["amt"],
        "card_holder": {
            "first": row["first"],
            "last": row["last"],
            "gender": row["gender"],
            "dob": row["dob"],
        },
        "job": row["job"],
        "address": {
            "street": row["street"],
            "city": row["city"],
            "state": row["state"],
            "zip": row["zip"],
            "lat": row["lat"],
            "long": row["long"],
        },
        "city_pop": row["city_pop"],
        "merch_location": {
            "lat": row["merch_lat"],
            "long": row["merch_long"],
        },
        "unix_time": row["unix_time"],
        "is_fraud": row["is_fraud"],
    }
    features.append(transformed)

# Convert to JSON string
# df['json'] = [json.dumps(feature, indent=0) for feature in features]

# The default separators are ', ' for items and ': ' for key-value pairs.
# By setting separators=(',', ':'), the output JSON string will have no spaces
# after the commas and colons
df["json"] = [json.dumps(feature, separators=(",", ":")) for feature in features]

# just take the json column of the dataframe
dfjson = df["json"]
# print(dfjson)

# print out the dataframe to a file
# Note that the timestamp forward slash will be escaped
# to stay true to JSON schema
np.savetxt(r"output/output.txt", dfjson.values, fmt="%s")
