from datetime import datetime, timedelta
from services.alert_fetcher import fetch_feed
from services.alert_parser import parse_alerts, get_all_statuses, filter_line_status
import logging 

line_status_cache = {}
logger = logging.getLogger(__name__)
line_uptime_data = {}

# returns boolean True if train is delayed, logs out if a train is delayed or recovered
def get_line_status(line_name: str):
    feed = fetch_feed()
    alerts = parse_alerts(feed)
    delayed_trains = get_all_statuses(alerts)
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

def get_uptime(line_name: str):
    current_status = get_line_status(line_name.lower())
    currently_delayed = current_status["delayed"]
    print("is train currently delayed", currently_delayed)
    # Initialize uptime tracking if not already present
    if line_name not in line_uptime_data:
        line_uptime_data[line_name] = {
            "last_checked": datetime.now(),  # Last time status was checked
            "total_time_monitored": timedelta(0),  # Total monitoring time
            "total_time_delayed": timedelta(0)  # Total delay time
        }
    
    now = datetime.now()
    line_data = line_uptime_data[line_name]
    time_since_last_check = now - line_data["last_checked"]
    line_data["total_time_monitored"] += time_since_last_check
    
    if currently_delayed:
        line_data["total_time_delayed"] += time_since_last_check
    
    line_data["last_checked"] = now 
    
    total_time = line_data["total_time_monitored"].total_seconds()
    total_delay = line_data["total_time_delayed"].total_seconds()
    uptime = 1 - (total_delay / total_time) if total_time > 0 else 1.0
    
    return {"uptime": uptime}
    

def monitor_status_task():
    #  All subway lines to monitor
    lines_to_monitor = ["a", "c", "e", "b", "d", "f", "m", "g", "j", "z", "l", "1", "2", "3", "4", "5", "6", "7", "s"]
    for line in lines_to_monitor:
        get_line_status(line)
        get_uptime(line)

