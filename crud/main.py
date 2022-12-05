# Import libaries from FastApi:
from fastapi import FastAPI
from fastapi import Path, Body

# Import Libraries from Others:
from redis_om import get_redis_connection


# Setting the value of the key for the Redis database:
DB_KEY = "SIMULATION"

# Setting connection with Redis database:
redis = get_redis_connection(

    # Parameters for Redis Connection in localhost:
    host = "localhost",
    port = "6379",
    decode_responses = True,


    # Parameters for Redis Cloud Connection
    #host = "redis-13803.c278.us-east-1-4.ec2.cloud.redislabs.com",
    #port = 13803,
    #password = "aLU9hOCB2iABSjpv33qOL4lxYGLafTNl",
    #decode_responses = True
)


app = FastAPI()


# API for data storage in Redis database: POST request to server using a Body parameter.
@app.post("/simulator/savedata")
def save_data(
    data: dict = Body(...)
):

    return redis.xadd(DB_KEY, data, id='*', maxlen=None)


# API to read all data stored in Redis stream: GET request to server.
@app.get("/simulator/showdata/all")
def show_all_data():

    try:
        return redis.xrange(DB_KEY,min="-",max="+")

    except Exception as e:
        return e


# API to read all data stored in Redis stream: GET request to server.
@app.get("/simulator/showdata/first")
def show_first_data():

    try:
        last_data = redis.xread(streams={DB_KEY:0},count=1,block=3000)
        return last_data[0][1] # Taking only the value of the id and the stored data: ignoring database key.

    except Exception as e:
        return e
    

# API to delete the entire Redis stream data with the key SIMULATION: DELETE request to server.
@app.delete("/simulator/deletedata/all")
def delete_all_data():

    return redis.delete(DB_KEY)


# API to delete data by id from Redis stream: DELETE request to server.
@app.delete("/simulator/deletedata/{id}")
def delete_data_by_id(
    id: str = Path(...)
):

    return redis.xdel(DB_KEY, id)