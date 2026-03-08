import sqlite3
from pathlib import Path


def main() -> None:
    # Build path to the database file
    db_path = Path("data") / "drone_flight.db"

    # Connect to the SQLite database
    connection = sqlite3.connect(db_path)

    # Create a cursor for running SQL queries
    cursor = connection.cursor()

    # -------------------------
    # OVERALL METRICS
    # -------------------------

    # Count all rows in the flight log table
    cursor.execute("SELECT COUNT(*) FROM flight_logs")
    total_rows = cursor.fetchone()[0]

    # Get total flight duration from the largest timestamp
    cursor.execute("SELECT MAX(timestamp_seconds) FROM flight_logs")
    flight_duration = cursor.fetchone()[0]

    # Get highest altitude reached
    cursor.execute("SELECT MAX(altitude_m) FROM flight_logs")
    max_altitude = cursor.fetchone()[0]

    # Get lowest battery percentage reached
    cursor.execute("SELECT MIN(battery_percent) FROM flight_logs")
    min_battery = cursor.fetchone()[0]

    # Get average motor RPM
    cursor.execute("SELECT AVG(motor_rpm) FROM flight_logs")
    avg_rpm = cursor.fetchone()[0]

    cursor.execute("SELECT MAX(motor_rpm) FROM flight_logs")
    max_rpm = cursor.fetchone()[0]

    # -------------------------
    # ANOMALY COUNTS
    # -------------------------

    # Count rows with large pitch or roll
    cursor.execute("""
        SELECT COUNT(*)
        FROM flight_logs
        WHERE ABS(pitch_deg) > 8 OR ABS(roll_deg) > 8
    """)
    tilt_anomalies = cursor.fetchone()[0]

    # Count rows with unusually high motor RPM
    cursor.execute("""
        SELECT COUNT(*)
        FROM flight_logs
        WHERE motor_rpm > 4200
    """)
    rpm_anomalies = cursor.fetchone()[0]

    # Count rows with low battery
    cursor.execute("""
        SELECT COUNT(*)
        FROM flight_logs
        WHERE battery_percent < 85
    """)
    battery_warnings = cursor.fetchone()[0]

    # -------------------------
    # PHASE BREAKDOWN
    # -------------------------

    # Count rows for each phase
    cursor.execute("""
        SELECT phase, COUNT(*)
        FROM flight_logs
        GROUP BY phase
        ORDER BY COUNT(*) DESC
    """)
    phase_counts = cursor.fetchall()

    # -------------------------
    # PRINT DASHBOARD
    # -------------------------

    print("\n" + "=" * 54)
    print("             DRONE FLIGHT TERMINAL DASHBOARD")
    print("=" * 54)

    print("\n[ OVERALL FLIGHT METRICS ]")
    print(f"Total telemetry rows : {total_rows}")
    print(f"Flight duration      : {flight_duration:.2f} s")
    print(f"Maximum altitude     : {max_altitude:.2f} m")
    print(f"Minimum battery      : {min_battery:.2f} %")
    print(f"Average motor RPM    : {avg_rpm:.2f}")
    print(f"Maximum motor RPM    : {max_rpm}")

    print("\n[ ANOMALY SUMMARY ]")
    print(f"High-tilt events     : {tilt_anomalies}")
    print(f"High-RPM events      : {rpm_anomalies}")
    print(f"Low-battery rows     : {battery_warnings}")

    print("\n[ PHASE BREAKDOWN ]")
    for phase, count in phase_counts:
        print(f"{phase:<10} : {count}")

    if tilt_anomalies > 2 or rpm_anomalies > 0:
        print("\nSystem status        : REVIEW RECOMMENDED")
    else:
        print("\nSystem status        : NORMAL")

    print("\n" + "=" * 54)

    # Close the database connection
    connection.close()


if __name__ == "__main__":
    main()