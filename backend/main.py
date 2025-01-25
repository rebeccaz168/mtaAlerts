from fastapi import FastAPI
import requests
# from google.transit import gtfs_realtime_pb2

app = FastAPI()
FEED_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g"


# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to the MTA Alerts API "}

# Status route 
@app.get("/status/{line_name}", tags= ["Status"])
async def getStatus(line_name: str): 
    requests.get(FEED_URL)
    # feed = gtfs_realtime_pb2.FeedMessage()

# # Uptime route 
# @app.get("/uptime/{line_name}", tags=["Uptime"])
#     """
#     Returns the uptime of a subway line 