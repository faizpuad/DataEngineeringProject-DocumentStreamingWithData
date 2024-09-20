import numpy as np
from numpy import add
import pandas as pd
import os

# Get the current working directory
current_path = os.getcwd()
print("Current Working Directory:", current_path)

data_loc = "data/Online_Retail.csv"

df = pd.read_csv(data_loc,encoding='ISO-8859-1')
print(df.head())

# add a json column to the dataframe
# splitlines will split the json into multiple rows not a single one
df['json'] = df.to_json(orient='records', lines=True).splitlines()
#print(df)

# just take the json column of the dataframe
dfjson = df['json']
print(dfjson)

# print out the dataframe to a file
# Note that the timestamp forward slash will be escaped to stay true to JSON schema
np.savetxt(r'output/output.txt', dfjson.values, fmt='%s')
