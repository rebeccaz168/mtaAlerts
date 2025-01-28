# mtaAlerts
Continuously monitors the status of MTA service to see whether a line is delayed or not. Also calculates uptime for each subway line. 

## installation 
1. Clone the repo : 

2. Install the dependencies : 
```pip install requirements.txt```

## Usage 
### Backend 
uvicorn main:app --reload
navigate to : http://127.0.0.1:8000 

### frontend 
npm start 
navigate to : http://localhost:3000

## Requests 
To get the status of a particular subway line : 
curl -X GET "http://127.0.0.1:8000/status/<line_name>"

To get the uptime of a particular subway line : 
curl -X GET "http://127.0.0.1:8000/uptime/<line_name>"
