# Below serve as example on how this script should look like and not represent the full script
# import related libraries

# set starting id and ending id
with open("output/output.txt", "r") as file:
    num_lines = len(file.readlines())

start = 1
end = # customized here

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
            myjson["trans_date_trans_time"], "your date format"
        ).strftime("your date format")
        print("Convert trx date successfull")

        myjson["card_holder"]["dob"] = datetime.strptime(
            dob_datetime, "your date format"
        ).strftime("your date format")
        print("Convert dob date successfull")

    except ValueError as e:
        print(f"Date parsing failed for: {trx_datetime} with error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print(myjson)
    response = requests.post("http://localhost:xx/transaction", json=myjson)
    i += 1
