from google.protobuf.json_format import MessageToDict

DELAY_KEYWORDS = ["delayed", "delays"]
delayed_trains = []

def parse_alerts(feed):
    feed_dict = MessageToDict(feed)
    alerts = [
        entity for entity in feed_dict.get("entity", []) if "alert" in entity
    ]
    return alerts

def get_all_statuses(alerts): 
    for alert in alerts:
        header_texts = alert["alert"].get("headerText", {}).get("translation", [])
        description_texts = alert["alert"].get("descriptionText", {}).get("translation", [])

        # Combine all text fields to search for delay keywords
        texts_to_check = [t["text"] for t in header_texts + description_texts]
    
        # filter for the delayed entities 
        if any(keyword in text.lower() for text in texts_to_check for keyword in DELAY_KEYWORDS):
            # Check for specific train lines 
            informed_entities = alert["alert"].get("informedEntity", [])
            route_ids = [entity.get("routeId") for entity in informed_entities if "routeId" in entity]
            for id in route_ids: 
                if id.lower() not in delayed_trains: 
                    delayed_trains.append(id.lower())
   
    return delayed_trains
    
def filter_line_status(delayed_trains, line_name):
    return line_name in delayed_trains
