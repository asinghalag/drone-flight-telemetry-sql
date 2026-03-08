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
    # QUERY 1: Average altitude and battery every 20 sec
    cursor.execute("""
                   SELECT
                    CAST(timestamp_seconds / 20 AS INTEGER) AS time_bucket,
                    MIN(timestamp_seconds) AS bucket_start_time,
                    MAX(timestamp_seconds) AS bucket_end_time,
                    AVG(altitude_m) AS avg_altitude,
                    AVG(battery_percent) AS avg_battery
                   FROM flight_logs
                   GROUP BY time_bucket
                   ORDER BY time_bucket
                   """)
    altitude_battery_buckets = cursor.fetchall()

    # QUERY 2: Average motoe RPM every 20 secoinds
    cursor.execute("""
                   SELECT
                   CAST(timestamp_seconds / 20 AS INTEGER) AS time_bucket,
                   AVG(motor_rpm) AS avg_motor_rpm
                   FROM flight_logs
                   GROUP BY time_bucket
                   ORDER BY avg_motor_rpm DESC
                   """)
    rpm_buckets = cursor.fetchall()

    # Query 3: Max tilt in each 20 second bucket
    cursor.execute("""
        SELECT
            CAST(timestamp_seconds / 20 AS INTEGER) AS time_bucket,
            MAX(ABS(pitch_deg)) AS max_abs_pitch,
            MAX(ABS(roll_deg)) AS max_abs_roll
        FROM flight_logs
        GROUP BY time_bucket
        ORDER BY time_bucket
    """)
    tilt_buckets = cursor.fetchall()

    print_rows("Average Altitude and Battery by 20-Second Bucket", altitude_battery_buckets)
    print_rows("Average Motor RPM by 20-Second Bucket (Highest First)", rpm_buckets)
    print_rows("Maximum Absolute Tilt by 20-Second Bucket", tilt_buckets)

    connection.close()

if __name__ == "__main__":
    main()