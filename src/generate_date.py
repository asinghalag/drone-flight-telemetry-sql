import sqlite3
from pathlib import Path
import random


def insert_row(
    cursor,
    timestamp: float,
    phase: str,
    altitude: float,
    battery: float,
    pitch: float,
    roll: float,
    yaw: float,
    motor_rpm: int,
    gps_lat: float,
    gps_lon: float
) -> None:
    # Insert one telemetry row into the database
    cursor.execute("""
        INSERT INTO flight_logs (
            timestamp_seconds,
            phase,
            altitude_m,
            battery_percent,
            pitch_deg,
            roll_deg,
            yaw_deg,
            motor_rpm,
            gps_lat,
            gps_lon
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        phase,
        altitude,
        battery,
        pitch,
        roll,
        yaw,
        motor_rpm,
        gps_lat,
        gps_lon
    ))


def main() -> None:
    # Build path to the database file
    db_path = Path("data") / "drone_flight.db"

    # Connect to the database
    connection = sqlite3.connect(db_path)

    # Create cursor for SQL commands
    cursor = connection.cursor()

    # Clear old rows so each run creates one fresh flight
    cursor.execute("DELETE FROM flight_logs")

    # Initial flight values
    timestamp = 0.0
    altitude = 0.0
    battery = 100.0
    yaw = 0.0
    gps_lat = 42.2740
    gps_lon = -71.8060

    # Number of rows per phase
    takeoff_steps = 20
    climb_steps = 30
    cruise_steps = 40
    descent_steps = 30
    landing_steps = 20

    # -------------------------
    # PHASE 1: TAKEOFF
    # -------------------------
    for _ in range(takeoff_steps):
        timestamp += 1.0
        altitude += 0.3
        battery -= 0.15
        pitch = random.uniform(-3, 3)
        roll = random.uniform(-3, 3)
        yaw += random.uniform(-2, 2)
        motor_rpm = random.randint(3200, 3600)
        gps_lat += random.uniform(-0.00001, 0.00001)
        gps_lon += random.uniform(-0.00001, 0.00001)

        insert_row(
            cursor, timestamp, "takeoff", altitude, battery,
            pitch, roll, yaw, motor_rpm, gps_lat, gps_lon
        )

    # -------------------------
    # PHASE 2: CLIMB
    # -------------------------
    for _ in range(climb_steps):
        timestamp += 1.0
        altitude += 0.5
        battery -= 0.18
        pitch = random.uniform(-5, 5)
        roll = random.uniform(-5, 5)
        yaw += random.uniform(-3, 3)
        motor_rpm = random.randint(3400, 3900)
        gps_lat += random.uniform(0.00001, 0.00003)
        gps_lon += random.uniform(0.00001, 0.00003)

        insert_row(
            cursor, timestamp, "climb", altitude, battery,
            pitch, roll, yaw, motor_rpm, gps_lat, gps_lon
        )

    # -------------------------
    # PHASE 3: CRUISE
    # -------------------------
    for _ in range(cruise_steps):
        timestamp += 1.0
        altitude += random.uniform(-0.1, 0.1)
        battery -= 0.12
        pitch = random.uniform(-4, 4)
        roll = random.uniform(-4, 4)
        yaw += random.uniform(-4, 4)
        motor_rpm = random.randint(3000, 3400)
        gps_lat += random.uniform(0.00002, 0.00005)
        gps_lon += random.uniform(0.00002, 0.00005)

        insert_row(
            cursor, timestamp, "cruise", altitude, battery,
            pitch, roll, yaw, motor_rpm, gps_lat, gps_lon
        )

    # -------------------------
    # PHASE 4: DESCENT
    # -------------------------
    for _ in range(descent_steps):
        timestamp += 1.0
        altitude -= 0.4
        battery -= 0.10
        pitch = random.uniform(-4, 4)
        roll = random.uniform(-4, 4)
        yaw += random.uniform(-2, 2)
        motor_rpm = random.randint(2800, 3300)
        gps_lat += random.uniform(0.00001, 0.00003)
        gps_lon += random.uniform(0.00001, 0.00003)

        insert_row(
            cursor, timestamp, "descent", altitude, battery,
            pitch, roll, yaw, motor_rpm, gps_lat, gps_lon
        )

    # -------------------------
    # PHASE 5: LANDING
    # -------------------------
    for _ in range(landing_steps):
        timestamp += 1.0
        altitude -= 0.25
        if altitude < 0:
            altitude = 0.0
        battery -= 0.08
        pitch = random.uniform(-2, 2)
        roll = random.uniform(-2, 2)
        yaw += random.uniform(-1, 1)
        motor_rpm = random.randint(2200, 2800)
        gps_lat += random.uniform(-0.00001, 0.00001)
        gps_lon += random.uniform(-0.00001, 0.00001)

        insert_row(
            cursor, timestamp, "landing", altitude, battery,
            pitch, roll, yaw, motor_rpm, gps_lat, gps_lon
        )

    # Save inserted rows
    connection.commit()

    # Count how many rows were inserted
    cursor.execute("SELECT COUNT(*) FROM flight_logs")
    row_count = cursor.fetchone()[0]

    print("Drone flight simulation complete.")
    print(f"Rows inserted: {row_count}")

    # Close the database connection
    connection.close()


if __name__ == "__main__":
    main()