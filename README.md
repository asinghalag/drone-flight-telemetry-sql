🚁 Drone Flight Telemetry Analysis with Python & SQL
Project Overview

I built this project to explore how robotic systems store and analyze telemetry data during operation.

Modern drones generate large volumes of flight logs that engineers analyze to understand performance, detect anomalies, and monitor system health. To better understand this workflow, I designed a small system that:

• simulates a drone flight
• logs telemetry into a relational database
• performs SQL-based analysis on the flight data
• detects abnormal system behavior
• generates reports and monitoring dashboards

The project combines robotics concepts, Python scripting, and SQL analytics into a simplified telemetry pipeline.

✈️ Flight Simulation

The simulator generates a complete drone flight consisting of five phases:

Flight Phase	Description
Takeoff	Initial lift from ground
Climb	Drone gains altitude
Cruise	Stable flight
Descent	Controlled altitude reduction
Landing	Final touchdown

Each second of the simulated flight produces telemetry including:

• altitude
• battery percentage
• motor RPM
• pitch / roll / yaw orientation
• GPS coordinates
• flight phase

These records are stored in a SQLite database for analysis.

🗄 Telemetry Database Design

The telemetry logs are stored in a structured relational table.

Key fields include:

Column	Description
timestamp_seconds	Time since flight start
phase	Current flight phase
altitude_m	Drone altitude
battery_percent	Remaining battery
pitch_deg	Pitch orientation
roll_deg	Roll orientation
yaw_deg	Yaw orientation
motor_rpm	Motor speed
gps_lat / gps_lon	GPS position

The database schema allows telemetry data to be analyzed using standard SQL queries.

📊 SQL-Based Flight Analysis

Once the flight data is generated, SQL queries are used to analyze the system behavior.

Examples of analysis performed:

Maximum altitude reached
SELECT MAX(altitude_m)
FROM flight_logs;
Detect abnormal tilt
SELECT timestamp_seconds, pitch_deg, roll_deg
FROM flight_logs
WHERE ABS(pitch_deg) > 8 OR ABS(roll_deg) > 8;
Average motor RPM by flight phase
SELECT phase, AVG(motor_rpm)
FROM flight_logs
GROUP BY phase;
Time-window flight analysis
SELECT
CAST(timestamp_seconds / 20 AS INTEGER) AS time_bucket,
AVG(altitude_m)
FROM flight_logs
GROUP BY time_bucket;

These queries simulate how engineers analyze telemetry logs to understand drone behavior during flight.

⚠️ Anomaly Detection

To make the analysis more realistic, the simulator injects abnormal events into the flight profile.

Examples include:

• sudden tilt disturbances
• motor RPM spikes
• rapid battery drain near landing

SQL queries then identify and summarize these events.

This mirrors how telemetry monitoring systems flag abnormal conditions during real robotic operations.

🖥 Terminal Telemetry Dashboard

I implemented a simple command-line dashboard that summarizes flight metrics.

Example output:

DRONE FLIGHT TERMINAL DASHBOARD

Total telemetry rows : 140
Flight duration      : 140 seconds
Maximum altitude     : 15.2 m
Minimum battery      : 84.9 %
Average motor RPM    : 3215

High tilt events     : 3
High RPM events      : 1
Low battery warnings : 9

This provides a quick overview of system health and flight behavior.

📄 Automated Flight Report

The project can also generate a flight summary report.

Running:

python src/report.py

produces a structured flight summary including:

• maximum altitude
• battery statistics
• anomaly counts
• phase-based performance metrics

The report is saved to:

data/flight_report.txt
⚡ Database Performance Optimization

To improve query performance, indexes were added on commonly queried columns:

• timestamp
• flight phase
• battery percentage
• motor RPM

Example:

CREATE INDEX idx_flight_logs_timestamp
ON flight_logs(timestamp_seconds);

This helps speed up filtering and aggregation queries.

🗂 Project Structure
src/
  setup_db.py
  generate_data.py
  basic_queries.py
  event_queries.py
  grouped_queries.py
  phase_queries.py
  anomaly_queries.py
  dashboard.py
  report.py
  ascii_plot.py

data/
  drone_flight.db
  flight_report.txt
▶️ How to Run the Project

Create the database:

python src/setup_db.py

Generate simulated flight telemetry:

python src/generate_data.py

Launch the telemetry dashboard:

python src/dashboard.py

Generate the flight report:

python src/report.py
🧠 What I Explored in This Project

Through this project I explored how telemetry systems in robotics log and analyze operational data.

Key takeaways include:

• designing relational schemas for telemetry logs
• using SQL aggregation queries for system analysis
• detecting anomalies through threshold-based queries
• optimizing database performance using indexes
• building Python pipelines that simulate and analyze telemetry data

The project helped me better understand how robotic systems combine software, data pipelines, and analytics to monitor real-world operations.

🚀 Possible Future Improvements

Some directions I would like to explore next:

• ingest real drone flight logs
• visualize telemetry using matplotlib
• build a live telemetry dashboard
• support multiple flights in the same database
• stream telemetry data in real time