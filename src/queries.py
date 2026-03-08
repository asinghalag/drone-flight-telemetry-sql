import sqlite3
from pathlib import Path

def main() -> None:
    db_path = Path("data") / "drone_flight.db"

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    #Query 1: MAX altitude reached during the flight
    cursor.execute("SELECT MAX(altitude_m) FROM flight_logs")
    max_altitude = cursor.fetchone()[0]

    #Query 2: Minimum Battery
    cursor.execute("SELECT MIN(battery_percent) FROM flight_logs")
    min_battery = cursor.fetchone()[0]

    #Query 3: Average Motor RPM
    cursor.execute("SELECT AVG(motor_rpm) FROM flight_logs")
    avg_motor_rpm = cursor.fetchone()[0]

    #Query 4: Total Flight Time
    cursor.execute("SELECT MAX(timestamp_seconds) FROM flight_logs")
    flight_duration = cursor.fetchone()[0]

    #Query 5: Dagerous Tilt events
    cursor.execute("""
                   SELECT COUNT(*)
                   FROM flight_logs
                   WHERE ABS(pitch_deg) > 3 OR ABS(roll_deg) > 3
                   """)
    dangerous_tilts = cursor.fetchone()[0]

    print("\n Drone Flight Analysis:")
    print(f"Maximum Altitude: {max_altitude:.2f} m")
    print(f"Minimum Battery: {min_battery:.2f}%")
    print(f"Average Motor RPM: {avg_motor_rpm:.2f}")
    print(f"Flight Duration: {flight_duration:.2f} s")
    print(f"Dangerous Tilt Events: {dangerous_tilts}")

    connection.close()

if __name__ == "__main__":
    main()