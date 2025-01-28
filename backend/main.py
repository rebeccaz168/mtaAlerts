from fastapi import FastAPI
from services.status_monitor import get_line_status, get_uptime
from apscheduler.schedulers.background import BackgroundScheduler
from services.status_monitor import monitor_status_task 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
scheduler = BackgroundScheduler()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to the MTA Alerts API "}

# Status route 
@app.get("/status/{line_name}", tags= ["Status"])
async def getStatus(line_name: str): 
   return get_line_status(line_name)

# Uptime route 
@app.get("/uptime/{line_name}", tags=["Uptime"])
async def getUptime(line_name: str): 
    """
    Returns the uptime of a subway line 
    """
    return get_uptime(line_name)

# @app.on_event("startup")
def monitorStatus(): 
    scheduler.add_job(monitor_status_task, 'interval', seconds=30)  # MTA API refreshes every 30 seconds  
    scheduler.start()
    
