from datetime import datetime, timedelta
from services.alert_fetcher import fetch_feed
from services.alert_parser import parse_alerts, get_all_statuses, filter_line_status
import logging 

line_status_cache = {}
logger = logging.getLogger(__name__)
line_uptime_data = {}


def get_line_status(line_name: str):
    """
    returns status for particular subway line
    logs out if train status changes (delayed/recovered)
    """
    try: 
        feed = fetch_feed()
        alerts = parse_alerts(feed)
        print(alerts)
        delayed_trains = get_all_statuses(alerts)
        delayed = filter_line_status(delayed_trains, line_name)
    except Exception as e: 
        raise Exception(f"Failed to fetch or parse data for line {line_name}: {e}")
    
    # Check for status transitions
    prev_status = line_status_cache.get(line_name, False)
    if delayed != prev_status:
        if delayed:
            logger.info(f"Line {line_name} is experiencing delays.")
        else:
            logger.info(f"Line {line_name} is now recovered.")
        line_status_cache[line_name] = delayed
    print(line_status_cache)
    return {"line_name": line_name, "delayed": delayed} 

def calculate_uptime(total_time: timedelta, total_delay: timedelta) -> float:
    """
    Calculates the uptime percentage based on total monitored and delay times.
    """
    total_seconds = total_time.total_seconds()
    delayed_seconds = total_delay.total_seconds()
    return 1 - (delayed_seconds / total_seconds) if total_seconds > 0 else 1.0

def get_uptime(line_name: str):
    """
    tracks and returns the uptime for a particular subway line 
    """
    current_status = get_line_status(line_name.lower())
    currently_delayed = current_status["delayed"]

    # Initialize uptime tracking if not there
    if line_name not in line_uptime_data:
        line_uptime_data[line_name] = {
            "last_checked": datetime.now(),  
            "total_time_monitored": timedelta(0), 
            "total_time_delayed": timedelta(0)
        }
    
    now = datetime.now()
    line_data = line_uptime_data[line_name]
    time_since_last_check = now - line_data["last_checked"]
    line_data["total_time_monitored"] += time_since_last_check
    
    if currently_delayed:
        line_data["total_time_delayed"] += time_since_last_check
    
    line_data["last_checked"] = now 
    
    uptime = calculate_uptime(line_data["total_time_monitored"], line_data["total_time_delayed"])
    print(line_uptime_data)
    return {"uptime": uptime}
    

def monitor_status_task():
    """
    Monitors the status and uptime of specified subway lines.
    """
    lines_to_monitor = ["a", "c", "e", "b", "d", "f", "m", "g", "j", "z", "l", "1", "2", "3", "4", "5", "6", "7", "s"]
    for line in lines_to_monitor:
        get_line_status(line)
        get_uptime(line)

