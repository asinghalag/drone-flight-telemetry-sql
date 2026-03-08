import sqlite3
from pathlib import Path
import random

def main() -> None:
    data_folder = Path("data")
    data_folder.mkdir(exist_ok=True)

    db_path = data_folder / "drone_flight.db"

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM flight_logs")

    # Start values for the flight
    timestamp = 0.0
    altitude = 0.0
    battery = 100.0
    yaw = 0.0
    gps_lat = 42.2740
    gps_lon = -71.8060

    # Total number of time steps per phase
    takeoff_steps = 20
    climb_steps = 30
    cruise_steps = 40
    descent_steps = 30
    landing_steps = 20

    for _ in range(takeoff_steps):
        timestamp +=1.0
        altitude +=0.3
        battery -=0.15
        pitch = random.uniform(-3,3)
        roll = random.uniform(-3,3)
        yaw += random.uniform(-2,2)
        motor_rpm = random.randint(3200,3600)
        gps_lat += random.uniform(-0.00001,0.00001)
        gps_lon += random.uniform(-0.00001,0.00001)

# Phase 1: Takeoff
        cursor.execute("""
            INSERT INTO flight_logs (
                timestamp_seconds,
                altitude_m,
                battery_percent,
                pitch_deg,
                roll_deg,
                yaw_deg,
                motor_rpm,
                gps_lat,
                gps_lon
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            altitude,
            battery,
            pitch,
            roll,
            yaw,
            motor_rpm,
            gps_lat,
            gps_lon
        ))
#Phase 2: Climb
    for _ in range(climb_steps):
        timestamp += 1.0
        altitude += 0.5                       # climb faster than takeoff
        battery -= 0.18
        pitch = random.uniform(-5, 5)
        roll = random.uniform(-5, 5)
        yaw += random.uniform(-3, 3)
        motor_rpm = random.randint(3400, 3900)
        gps_lat += random.uniform(0.00001, 0.00003)   # forward movement
        gps_lon += random.uniform(0.00001, 0.00003)

        cursor.execute("""
            INSERT INTO flight_logs (
                timestamp_seconds,
                altitude_m,
                battery_percent,
                pitch_deg,
                roll_deg,
                yaw_deg,
                motor_rpm,
                gps_lat,
                gps_lon
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            altitude,
            battery,
            pitch,
            roll,
            yaw,
            motor_rpm,
            gps_lat,
            gps_lon
        ))

#Phase 3: Cruise
    for _ in range(cruise_steps):
        timestamp += 1.0
        altitude += random.uniform(-0.1, 0.1)  # maintain altitude with small variations
        battery -= 0.12
        pitch = random.uniform(-4, 4)
        roll = random.uniform(-4, 4)
        yaw += random.uniform(-4, 4)
        motor_rpm = random.randint(3000, 3400)
        gps_lat += random.uniform(0.00002, 0.00005)
        gps_lon += random.uniform(0.00002, 0.00005)

        cursor.execute("""
            INSERT INTO flight_logs (
                timestamp_seconds,
                altitude_m,
                battery_percent,
                pitch_deg,
                roll_deg,
                yaw_deg,
                motor_rpm,
                gps_lat,
                gps_lon
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            altitude,
            battery,
            pitch,
            roll,
            yaw,
            motor_rpm,
            gps_lat,
            gps_lon
        ))
#Phase 4: Descent
    for _ in range(descent_steps):
        timestamp += 1.0
        altitude -= 0.4                        # altitude decreases
        battery -= 0.10
        pitch = random.uniform(-4, 4)
        roll = random.uniform(-4, 4)
        yaw += random.uniform(-2, 2)
        motor_rpm = random.randint(2800, 3300)
        gps_lat += random.uniform(0.00001, 0.00003)
        gps_lon += random.uniform(0.00001, 0.00003)

        cursor.execute("""
            INSERT INTO flight_logs (
                timestamp_seconds,
                altitude_m,
                battery_percent,
                pitch_deg,
                roll_deg,
                yaw_deg,
                motor_rpm,
                gps_lat,
                gps_lon
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            altitude,
            battery,
            pitch,
            roll,
            yaw,
            motor_rpm,
            gps_lat,
            gps_lon
        ))
#Phase 5: Landing
    for _ in range(landing_steps):
        timestamp += 1.0
        altitude -= 0.25                       # slow final landing
        if altitude < 0:
            altitude = 0.0                     # altitude should never go below ground
        battery -= 0.08
        pitch = random.uniform(-2, 2)
        roll = random.uniform(-2, 2)
        yaw += random.uniform(-1, 1)
        motor_rpm = random.randint(2200, 2800)
        gps_lat += random.uniform(-0.00001, 0.00001)
        gps_lon += random.uniform(-0.00001, 0.00001)

        cursor.execute("""
            INSERT INTO flight_logs (
                timestamp_seconds,
                altitude_m,
                battery_percent,
                pitch_deg,
                roll_deg,
                yaw_deg,
                motor_rpm,
                gps_lat,
                gps_lon
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            altitude,
            battery,
            pitch,
            roll,
            yaw,
            motor_rpm,
            gps_lat,
            gps_lon
        ))

    connection.commit()

    cursor.execute("SELECT COUNT(*) FROM flight_logs")
    row_count = cursor.fetchone()[0]

    cursor.execute("""
                   SELECT * FROM flight_logs
                   ORDER BY timestamp_seconds
                   LIMIT 5
                   """)
    first_rows = cursor.fetchall()

    print("\nDrone flightsimulation saved.")
    print(f"Rows inserted: {row_count}")
    print("\nFirst 5 rows:")
    print("----------------------")
    for row in first_rows:
        print(row)
    connection.close()

if __name__ == "__main__":
    main()