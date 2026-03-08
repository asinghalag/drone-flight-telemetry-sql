import sqlite3
from pathlib import Path


def print_rows(title: str, rows: list[tuple]) -> None:
    # Print a title for the section
    print(f"\n{title}")
    print("-" * len(title))

    # Print each row returned by SQL
    for row in rows:
        print(row)

    # Show a message if no rows were found
    if not rows:
        print("No matching rows found.")


def main() -> None:
    # Build the path to the database file
    db_path = Path("data") / "drone_flight.db"

    # Connect to the database
    connection = sqlite3.connect(db_path)

    # Create a cursor for SQL commands
    cursor = connection.cursor()

    # -------------------------------------------------
    # QUERY 1: High-tilt anomalies
    # We define anomaly as abs(pitch) > 8 or abs(roll) > 8
    # -------------------------------------------------
    cursor.execute("""
        SELECT timestamp_seconds, phase, pitch_deg, roll_deg
        FROM flight_logs
        WHERE ABS(pitch_deg) > 8 OR ABS(roll_deg) > 8
        ORDER BY timestamp_seconds
    """)
    high_tilt_rows = cursor.fetchall()

    # -------------------------------------------------
    # QUERY 2: High RPM anomalies
    # We define anomaly as motor RPM > 4200
    # -------------------------------------------------
    cursor.execute("""
        SELECT timestamp_seconds, phase, motor_rpm, altitude_m
        FROM flight_logs
        WHERE motor_rpm > 4200
        ORDER BY timestamp_seconds
    """)
    high_rpm_rows = cursor.fetchall()

    # -------------------------------------------------
    # QUERY 3: Low battery warning rows
    # We define warning as battery < 85%
    # -------------------------------------------------
    cursor.execute("""
        SELECT timestamp_seconds, phase, battery_percent, altitude_m
        FROM flight_logs
        WHERE battery_percent < 85
        ORDER BY timestamp_seconds
        LIMIT 15
    """)
    low_battery_rows = cursor.fetchall()

    # -------------------------------------------------
    # QUERY 4: Count anomalies by phase
    # This combines tilt and RPM anomaly logic
    # -------------------------------------------------
    cursor.execute("""
        SELECT phase, COUNT(*)
        FROM flight_logs
        WHERE ABS(pitch_deg) > 8
           OR ABS(roll_deg) > 8
           OR motor_rpm > 4200
           OR battery_percent < 85
        GROUP BY phase
        ORDER BY COUNT(*) DESC
    """)
    anomaly_counts = cursor.fetchall()

    # Print all result sections
    print_rows("High-Tilt Anomalies", high_tilt_rows)
    print_rows("High-RPM Anomalies", high_rpm_rows)
    print_rows("Low-Battery Warning Rows (First 15)", low_battery_rows)
    print_rows("Anomaly Count by Phase", anomaly_counts)

    # Close the database connection
    connection.close()


if __name__ == "__main__":
    main()