from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
from kafka import KafkaProducer
import json

class CardHolder(BaseModel):
    first: str
    last: str
    gender: str
    dob: str  # Assumes dob is in 'YYYY-MM-DD' format

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip: int
    lat: float
    long: float

class MerchLocation(BaseModel):
    lat: float
    long: float

class CreditTrx(BaseModel):
    trans_num: str
    trans_date_trans_time: str  # Assumes format is 'YYYY-MM-DD HH:MM:SS'
    cc_num: int
    merchant: str
    category: str
    amt: float
    card_holder: CardHolder
    job: str
    address: Address
    city_pop: int
    merch_location: MerchLocation
    unix_time: int
    is_fraud: int

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/transaction")
async def post_transaction(item: CreditTrx):  # body expects a JSON with transaction information
    print("Message received")

    try:
        # Validate and parse datetime data (trx and dob)
        # Handle custom date format parsing
        trx_date = datetime.strptime(item.trans_date_trans_time, '%d/%m/%Y %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
        print('Parsed transaction timestamp: ', trx_date)
        item.trans_date_trans_time = trx_date

        dob_date = datetime.strptime(item.card_holder.dob, '%d/%m/%Y').strftime("%Y-%m-%d")
        print('Parsed date of birth: ', dob_date)
        item.card_holder.dob = dob_date

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

def produce_kafka_string(json_as_string):
    producer = KafkaProducer(bootstrap_servers='kafka:9092', acks=1)
    producer.send('ingestion-topic', bytes(json_as_string, 'utf-8'))
    producer.flush()