# Below serve as example on how this script should look like and not represent the full script
# import related library here

# Load data
data_loc = "./data/fraudTrain.csv"

# load data
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
        "job": row["job"],
        "is_fraud": row["is_fraud"],
    }
    features.append(transformed)

df["json"] = [json.dumps(feature, separators=(",", ":")) for feature in features]

# just take the json column of the dataframe
dfjson = df["json"]

# print out the dataframe to a file
# Note that the timestamp forward slash will be escaped
# to stay true to JSON schema
np.savetxt(r"output/output.txt", dfjson.values, fmt="%s")
