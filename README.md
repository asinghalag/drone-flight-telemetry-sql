# Drone Flight Telemetry Analysis

### Python + SQL Telemetry Pipeline Simulation

![Python](https://img.shields.io/badge/Python-3.x-blue)
![SQL](https://img.shields.io/badge/Database-SQLite-green)
![Telemetry](https://img.shields.io/badge/Domain-Robotics-orange)
![Status](https://img.shields.io/badge/Project-Complete-success)

---

# Project Overview

In this project I explored how robotic systems store and analyze
telemetry data generated during operation.

Modern drones produce continuous flight logs containing information such
as altitude, battery status, motor performance, and orientation.
Engineers analyze this telemetry to understand system performance and
detect abnormal events.

To better understand this workflow, I built a small telemetry pipeline
that:

• simulates a drone flight\
• logs telemetry into a SQL database\
• performs SQL-based analytics on the flight data\
• detects abnormal system behavior\
• generates automated reports and dashboards

The project combines **Python scripting, relational databases, and
robotics telemetry concepts**.

---

# Simulated Drone Flight

The simulator generates a full drone flight consisting of five phases:

Phase Description

---

Takeoff Initial lift
Climb Gain altitude
Cruise Stable flight
Descent Controlled drop
Landing Final touchdown

Each simulated second generates telemetry including:

• altitude\
• battery percentage\
• motor RPM\
• pitch / roll / yaw orientation\
• GPS position\
• flight phase

Total telemetry rows generated:

    140 rows

---

# Telemetry Database Schema

The telemetry data is stored in a relational SQLite table.

Column Description

---

timestamp_seconds Time since flight start
phase Flight phase
altitude_m Altitude in meters
battery_percent Remaining battery
pitch_deg Pitch orientation
roll_deg Roll orientation
yaw_deg Yaw orientation
motor_rpm Motor speed
gps_lat GPS latitude
gps_lon GPS longitude

---

# SQL Analytics

Several SQL queries analyze the simulated flight data.

### Maximum altitude reached

```sql
SELECT MAX(altitude_m)
FROM flight_logs;
```

### Detect abnormal tilt

```sql
SELECT timestamp_seconds, pitch_deg, roll_deg
FROM flight_logs
WHERE ABS(pitch_deg) > 8 OR ABS(roll_deg) > 8;
```

### Average motor RPM by flight phase

```sql
SELECT phase, AVG(motor_rpm)
FROM flight_logs
GROUP BY phase;
```

### Time-window flight analysis

```sql
SELECT
CAST(timestamp_seconds / 20 AS INTEGER) AS time_bucket,
AVG(altitude_m)
FROM flight_logs
GROUP BY time_bucket;
```

---

# Anomaly Detection

The simulator injects several abnormal events to demonstrate telemetry
monitoring.

Examples include:

• sudden tilt disturbance\
• motor RPM spike\
• accelerated battery drain near landing

SQL queries detect these anomalies and summarize their frequency.

---

# Terminal Dashboard

The project includes a simple terminal telemetry dashboard.

Run:

```bash
python src/dashboard.py
```

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

---

# Automated Flight Report

Generate a structured flight summary:

```bash
python src/report.py
```

Output file:

    data/flight_report.txt

The report summarizes:

• flight duration\
• altitude statistics\
• anomaly counts\
• phase-based performance metrics

---

# Database Optimization

Indexes were added to improve query performance.

```sql
CREATE INDEX idx_flight_logs_timestamp
ON flight_logs(timestamp_seconds);

CREATE INDEX idx_flight_logs_phase
ON flight_logs(phase);

CREATE INDEX idx_flight_logs_battery
ON flight_logs(battery_percent);

CREATE INDEX idx_flight_logs_motor_rpm
ON flight_logs(motor_rpm);
```

---

# 📂 Project Structure

    drone-flight-telemetry-sql

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

    README.md

---

# ▶️ How To Run The Project

### 1️⃣ Create database

```bash
python src/setup_db.py
```

### 2️⃣ Generate simulated telemetry

```bash
python src/generate_data.py
```

### 3️⃣ Launch telemetry dashboard

```bash
python src/dashboard.py
```

### 4️⃣ Generate flight report

```bash
python src/report.py
```

---

# 🧠 What I Learned

Through this project I explored how telemetry pipelines in robotics
systems are designed and analyzed.

Key takeaways include:

• designing relational schemas for telemetry logs\
• writing analytical SQL queries for system monitoring\
• detecting anomalies using threshold queries\
• optimizing databases with indexing\
• building Python scripts that orchestrate data generation and analysis

This project helped me better understand how **robotic systems combine
software, data pipelines, and analytics to monitor real-world
operations**.

---

# 🚀 Future Improvements

Potential next steps include:

• ingest real drone telemetry logs\
• add real-time plotting using matplotlib\
• build a web-based telemetry dashboard\
• support multiple flights in the same database\
• implement streaming telemetry simulation

---

# 📌 Resume Description

Designed and implemented a drone telemetry analysis pipeline using
Python and SQLite. Simulated flight data, stored telemetry in a
relational database, and developed SQL-based analytics for anomaly
detection, phase analysis, and automated reporting.

---

# ⭐ Skills Demonstrated

Python\
SQL / SQLite\
Telemetry simulation\
Data analysis pipelines\
Database indexing\
System monitoring concepts
