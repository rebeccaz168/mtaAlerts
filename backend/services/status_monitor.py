from services.alert_fetcher import fetch_feed
from services.alert_parser import parse_alerts, get_all_statuses, filter_line_status
import logging 

line_status_cache = {}
logger = logging.getLogger(__name__)

def get_line_status(line_name: str):
    feed = fetch_feed()
    alerts = parse_alerts(feed)
    delayed_trains = get_all_statuses(alerts)
    print("DELAYED", delayed_trains)
    delayed = filter_line_status(delayed_trains, line_name)
    
    # Check for status transitions
    prev_status = line_status_cache.get(line_name, False)
    if delayed != prev_status:
        if delayed:
            logger.info(f"Line {line_name} is experiencing delays.")
        else:
            logger.info(f"Line {line_name} is now recovered.")
        line_status_cache[line_name] = delayed

    return {"line_name": line_name, "delayed": delayed}

# def get_uptime(line_name: str):
#     # Simplified for now (implement time tracking as needed)
#     total_time = 100  # Placeholder
#     total_time_delayed = 20  # Placeholder
#     uptime = 1 - (total_time_delayed / total_time)
#     return {"line_name": line_name, "uptime": uptime}

def monitor_status_task():
    #  All subway lines to monitor
    lines_to_monitor = ["a", "c", "e", "b", "d", "f", "m", "g", "j", "z", "l", "1", "2", "3", "4", "5", "6", "7", "s"]
    for line in lines_to_monitor:
        get_line_status(line)