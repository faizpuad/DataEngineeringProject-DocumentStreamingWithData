import linecache
import json
import requests
import os
from datetime import datetime

#set starting id and ending id
with open('output/output.txt', 'r') as file:
    num_lines = len(file.readlines())

start = 1
end = num_lines

# Loop over the JSON file
i=start

while i <= end:     
    
    # read a specific line
    line = linecache.getline('output/output.txt', i)
    # print('line')
    # print(line)
    # write the line to the API
    myjson = json.loads(line)
    
    # print('')
    # print('myjson')
    print(myjson)
    try:
        # Fix 1: Remove trailing spaces
        invoice_date_str = myjson['InvoiceDate'].strip()

        try:
            # Fix 2: Try to convert string to datetime object with the first format
            date = datetime.strptime(invoice_date_str, "%d/%m/%y %H:%M")
        except ValueError:
            # If the first format fails, try the second format
            date = datetime.strptime(invoice_date_str, "%m/%d/%y %H:%M")

        # Fix 3: Format the datetime object as a string in the desired format (without padding)
        formatted_date = date.strftime("%-d/%-m/%Y %H:%M")

        # Fix 4: Manually remove leading zeros (especially in %H)
        formatted_date = formatted_date.replace('/0', '/').replace(' 0', ' ')

        # Fix 5: Update the JSON data with the new date format
        myjson['InvoiceDate'] = formatted_date
        print(myjson['InvoiceDate'])  # Output: e.g., '12/1/2010 8:26'

    except ValueError as e:
        print(f"Date parsing failed for: {invoice_date_str} with error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    response = requests.post('http://localhost:80/invoiceitem', json=myjson)

    # Use this for dedbugging
    # print("Status code: ", response.status_code)
    # print("Printing Entire Post Request")
    # print(response.json())
    # break
    # increase i
    i+=1

###Debug 

# # Get the current working directory
# current_path = os.getcwd()
# print("Current Working Directory:", current_path)

# response = requests.get('http://localhost:80/')
# print("Status Code:", response.status_code)
# print("Response Text:", response.text)