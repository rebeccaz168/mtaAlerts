from google.transit import gtfs_realtime_pb2
import requests

FEED_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts"

def fetch_feed():
    response = requests.get(FEED_URL)
    if response.status_code == 200:
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        return feed
    else:
        raise Exception(f"Failed to fetch feed: {response.status_code}")