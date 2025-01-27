from fastapi import FastAPI
from services.status_monitor import get_line_status
from apscheduler.schedulers.background import BackgroundScheduler
from services.status_monitor import monitor_status_task 

app = FastAPI()
scheduler = BackgroundScheduler()

# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to the MTA Alerts API "}

# Status route 
@app.get("/status/{line_name}", tags= ["Status"])
async def getStatus(line_name: str): 
   return get_line_status(line_name)

# # Uptime route 
# @app.get("/uptime/{line_name}", tags=["Uptime"])
#     """
#     Returns the uptime of a subway line 


# @app.on_event("startup")
def monitorStatus(): 
    scheduler.add_job(monitor_status_task, 'interval', seconds=30)  # update every 30 seconds 
    scheduler.start()
    
