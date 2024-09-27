import linecache
import json
import requests
import os
from datetime import datetime

current_path = os.getcwd()
print("Current Working Directory:", current_path)

# set starting id and ending id
with open("output/output.txt", "r") as file:
    num_lines = len(file.readlines())

start = 1
end = num_lines

# Loop over the JSON file
i = start

while i <= end:

    # read a specific line
    line = linecache.getline("output/output.txt", i)

    # write the line to the API
    myjson = json.loads(line)

    # print(myjson)
    try:
        # Fix 1: Remove trailing spaces
        trx_datetime = myjson["trans_date_trans_time"].strip()
        dob_datetime = myjson["card_holder"]["dob"].strip()

        # fix 2: Convert trx date into ISO supported dateformat
        myjson["trans_date_trans_time"] = datetime.strptime(
            myjson["trans_date_trans_time"], "%Y-%m-%d %H:%M:%S"
        ).strftime("%-d/%-m/%Y %H:%M:%S")
        print("Convert trx date successfull")

        myjson["card_holder"]["dob"] = datetime.strptime(
            dob_datetime, "%Y-%m-%d"
        ).strftime("%-d/%-m/%Y")
        print("Convert dob date successfull")

    except ValueError as e:
        print(f"Date parsing failed for: {trx_datetime} with error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print(myjson)
    response = requests.post("http://localhost:80/transaction", json=myjson)
    # print(type(myjson['card_holder']['dob']))
    # Use this for dedbugging
    # print("Status code: ", response.status_code)
    # print("Printing Entire Post Request")
    # print(response.json())
    # break
    # increase i
    i += 1
    break

# Debug

# Get the current working directory
# current_path = os.getcwd()
# print("Current Working Directory:", current_path)

# response = requests.get('http://localhost:80/')
# print("Status Code:", response.status_code)
# print("Response Text:", response.text)
