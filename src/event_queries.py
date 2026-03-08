import sqlite3
from pathlib import Path

def print_rows(title: str, rows: list[tuple]) -> None:
    print(f"\n{title}")
    print("-" * len(title))

    for row in rows:
        print(row)
        
    if not rows:
        print("No data found.")

def main() -> None:
    db_path = Path("data") / "drone_flight.db"

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # QUERY 1: Top 5 highest altitude moments

    cursor.execute("""
                   SELECT timestamp_seconds, altitude_m, battery_percent
                   FROM flight_logs
                   ORDER BY altitude_m DESC
                   LIMIT 5
                   """)
    highest_rows = cursor.fetchall()

    # QUERY 2: First low-battery moment
    # Define low battery as below 90%

    cursor.execute("""
                   SELECT timestamp_seconds, battery_percent, altitude_m
                   FROM flight_logs
                   WHERE battery_percent < 90
                   ORDER BY timestamp_seconds ASC
                   LIMIT 1 
                   """)
    first_low_battery = cursor.fetchall()

    # QUERY 3: Dangerous tilt rows
    cursor.execute("""
                   SELECT timestamp_seconds, pitch_deg, roll_deg, altitude_m
                   FROM flight_logs
                   Where ABS(pitch_deg) > 4 OR ABS(roll_deg) > 4
                   ORDER BY timestamp_seconds ASC
                   LIMIT 10
                   """)
    dangerous_tilts = cursor.fetchall()

    # QUERY 4: Last 5 rows of the flight

    cursor.execute("""
                    SELECT timestamp_seconds, altitude_m, battery_percent, motor_rpm
                    FROM flight_logs
                    ORDER BY timestamp_seconds DESC
                    LIMIT 5
                   """)
    last_rows = cursor.fetchall()

    print_rows("Top 5 Highest Altitude Moments", highest_rows)
    print_rows("First Low-Battery Moment (< 90%)", first_low_battery)
    print_rows("Dangerous Tilt Rows (First 10)", dangerous_tilts)
    print_rows("Last 5 Flight Rows", last_rows)

    connection.close()

if __name__ == "__main__":
    main()
