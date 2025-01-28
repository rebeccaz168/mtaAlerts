import React, { useEffect, useState } from "react";

const linesToMonitor = [
  "a", "c", "e", "b", "d", "f", "m", "g", "j", "z", "l", "1", "2", "3", "4", "5", "6", "7", "s",
];

function App() {
  const [delayedTrains, setDelayedTrains] = useState([]);
  const [runningTrains, setRunningTrains] = useState([]);
  const [history, setHistory] = useState([]);

  // Fetch delayed and running train statuses
  const fetchTrainStatus = async () => {
    try {

      const delayed = [];
      const running = [];

      for (const line of linesToMonitor) {
        const response = await fetch(`http://localhost:8000/status/${line}`);
        const data = await response.json();

        if (data.delayed) {
          delayed.push({ line: data.line_name });
        } else {
          running.push({ line: data.line_name });
        }
      }

      setDelayedTrains(delayed);
      setRunningTrains(running);
    } catch (error) {
      console.error("Error fetching train statuses:", error);
    }
  };

  // Fetch uptime for all monitored lines
  const fetchUptime = async () => {
    try {
      const historyData = [];
      for (const line of linesToMonitor) {
        const response = await fetch(`http://localhost:8000/uptime/${line}`);
        const data = await response.json();
        historyData.push({ line, uptime: (data.uptime * 100).toFixed(2) + "%" });
      }

      setHistory(historyData);
    } catch (error) {
      console.error("Error fetching uptime data:", error);
    }
  };

  useEffect(() => {
    fetchTrainStatus();
    fetchUptime();

    // Refresh data every 30 seconds
    const interval = setInterval(() => {
      fetchTrainStatus();
      fetchUptime();
    }, 30000);

    return () => clearInterval(interval); 
  }, []);

  return (
    <div>
      <h1>MTA Alerts</h1>

      {/* Delayed Trains */}
      <section>
        <h2>Delayed Trains</h2>
        {delayedTrains.length > 0 ? (
          <ul>
            {delayedTrains.map((train, index) => (
              <li key={index}>Line {train.line}</li>
            ))}
          </ul>
        ) : (
          <p>No delayed trains currently.</p>
        )}
      </section>

      {/* Running Trains */}
      <section>
        <h2>Running as Usual</h2>
        {runningTrains.length > 0 ? (
          <ul>
            {runningTrains.map((train, index) => (
              <li key={index}>Line {train.line}</li>
            ))}
          </ul>
        ) : (
          <p>All trains are running as usual!</p>
        )}
      </section>

      {/* Uptime History */}
      <section>
        <h2>Uptime History</h2>
        {history.length > 0 ? (
          <ul>
            {history.map((entry, index) => (
              <li key={index}>
                Line {entry.line} - Uptime: {entry.uptime}
              </li>
            ))}
          </ul>
        ) : (
          <p>No uptime history available yet.</p>
        )}
      </section>
    </div>
  );
}

export default App;

