# Below serve as example on how this script should look like and not represent the full script
# import related library here


# use for /transaction
class CardHolder(BaseModel):
    first: str
    last: str
    gender: str
    dob: str  # Assumes dob is in 'YYYY-MM-DD' format

# use for /transaction
class MerchLocation(BaseModel):
    lat: float
    long: float


# use for /get_transactions
# MongoDB client
myclient = pymongo.MongoClient(
    "input related mongodb port here", username="credential here", password="credential here"
)
mydb = myclient["your collection name"]
mycol = mydb["your document name"]


# use for /get_transactions
# Define a request model (for structured input)
class CreditCardQuery(BaseModel):
    cc_num: str


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/transaction")
async def post_transaction(
    item: CreditTrx,
):  # body expects a JSON with transaction information
    print("Message received")

    try:
        # Validate and parse datetime data (trx and dob)
        # Handle custom date format parsing
        trx_date = datetime.strptime(
            item.trans_date_trans_time, "your date format"
        ).strftime("your date format")
        print("Parsed transaction timestamp: ", trx_date)
        item.trans_date_trans_time = trx_date

        # Parse item back to json
        json_of_item = jsonable_encoder(item)

        # Dump the json out as string
        json_as_string = json.dumps(json_of_item)
        print(json_as_string)

        # Produce the string to Kafka (optional)
        produce_kafka_string(json_as_string)

        return JSONResponse(content=json_of_item, status_code=201)

    except Exception as e:
        print(f"Error: {e}")  # Log the error
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/get_transactions")
async def get_transactions(query: CreditCardQuery):
    myquery = {"cc_num": query.cc_num}
    mydoc = mycol.find(myquery)

    # Convert MongoDB cursor to list and return as JSON
    transactions = dumps(mydoc)
    return {"transactions": transactions}


def produce_kafka_string(json_as_string):
    producer = KafkaProducer(bootstrap_servers="related kafka port", acks=1)
    producer.send("created kafka topic", bytes(json_as_string, "utf-8"))
    producer.flush()
