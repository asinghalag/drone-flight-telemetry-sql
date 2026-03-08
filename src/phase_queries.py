import sqlite3
from pathlib import Path


def print_rows(title: str, rows: list[tuple]) -> None:
    # Print a title for this output section
    print(f"\n{title}")
    print("-" * len(title))

    # Print all returned rows
    for row in rows:
        print(row)

    # Show message if the query returned nothing
    if not rows:
        print("No matching rows found.")


def main() -> None:
    # Build path to the database
    db_path = Path("data") / "drone_flight.db"

    # Connect to the database
    connection = sqlite3.connect(db_path)

    # Create cursor for SQL queries
    cursor = connection.cursor()

    # -------------------------------------------------
    # QUERY 1: Count rows in each phase
    # -------------------------------------------------
    cursor.execute("""
        SELECT phase, COUNT(*)
        FROM flight_logs
        GROUP BY phase
        ORDER BY COUNT(*) DESC
    """)
    phase_counts = cursor.fetchall()

    # -------------------------------------------------
    # QUERY 2: Average altitude and RPM by phase
    # -------------------------------------------------
    cursor.execute("""
        SELECT
            phase,
            AVG(altitude_m) AS avg_altitude,
            AVG(motor_rpm) AS avg_motor_rpm
        FROM flight_logs
        GROUP BY phase
        ORDER BY avg_altitude DESC
    """)
    phase_averages = cursor.fetchall()

    # -------------------------------------------------
    # QUERY 3: Minimum battery by phase
    # -------------------------------------------------
    cursor.execute("""
        SELECT
            phase,
            MIN(battery_percent) AS min_battery
        FROM flight_logs
        GROUP BY phase
        ORDER BY min_battery ASC
    """)
    phase_battery = cursor.fetchall()

    # -------------------------------------------------
    # QUERY 4: Maximum absolute tilt by phase
    # -------------------------------------------------
    cursor.execute("""
        SELECT
            phase,
            MAX(ABS(pitch_deg)) AS max_abs_pitch,
            MAX(ABS(roll_deg)) AS max_abs_roll
        FROM flight_logs
        GROUP BY phase
    """)
    phase_tilt = cursor.fetchall()

    # Print results
    print_rows("Row Count by Flight Phase", phase_counts)
    print_rows("Average Altitude and Motor RPM by Phase", phase_averages)
    print_rows("Minimum Battery by Phase", phase_battery)
    print_rows("Maximum Absolute Tilt by Phase", phase_tilt)

    # Close the database connection
    connection.close()


if __name__ == "__main__":
    main()