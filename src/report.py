import sqlite3
from pathlib import Path

def main() -> None:
    db_path = Path("data") / "drone_flight.db"
    report_path = Path("data") / "flight_report.txt"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM flight_logs")
    total_rows = cursor.fetchone()[0]  # get one result value

    # Get maximum altitude reached
    cursor.execute("SELECT MAX(altitude_m) FROM flight_logs")
    max_altitude = cursor.fetchone()[0]

    # Get minimum battery percentage
    cursor.execute("SELECT MIN(battery_percent) FROM flight_logs")
    min_battery = cursor.fetchone()[0]

    # Get average motor RPM
    cursor.execute("SELECT AVG(motor_rpm) FROM flight_logs")
    avg_motor_rpm = cursor.fetchone()[0]

    # Get flight duration using the maximum timestamp
    cursor.execute("SELECT MAX(timestamp_seconds) FROM flight_logs")
    flight_duration = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM flight_logs
        WHERE ABS(pitch_deg) > 8 OR ABS(roll_deg) > 8
    """)
    high_tilt_count = cursor.fetchone()[0]

    # Count high-RPM anomaly rows
    cursor.execute("""
        SELECT COUNT(*)
        FROM flight_logs
        WHERE motor_rpm > 4200
    """)
    high_rpm_count = cursor.fetchone()[0]

    # Count low-battery warning rows
    cursor.execute("""
        SELECT COUNT(*)
        FROM flight_logs
        WHERE battery_percent < 85
    """)
    low_battery_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            phase,
            AVG(altitude_m),
            AVG(motor_rpm)
        FROM flight_logs
        GROUP BY phase
        ORDER BY AVG(altitude_m) DESC
    """)
    phase_rows = cursor.fetchall()


    lines = []

    lines.append("DRONE FLIGHT SUMMARY REPORT")
    lines.append("=" * 40)
    lines.append("")

    lines.append("Overall Flight Summary")
    lines.append("-" * 24)
    lines.append(f"Total telemetry rows: {total_rows}")
    lines.append(f"Flight duration: {flight_duration:.2f} seconds")
    lines.append(f"Maximum altitude: {max_altitude:.2f} m")
    lines.append(f"Minimum battery: {min_battery:.2f} %")
    lines.append(f"Average motor RPM: {avg_motor_rpm:.2f}")
    lines.append("")

    lines.append("Anomaly Summary")
    lines.append("-" * 16)
    lines.append(f"High-tilt events: {high_tilt_count}")
    lines.append(f"High-RPM events: {high_rpm_count}")
    lines.append(f"Low-battery warning rows: {low_battery_count}")
    lines.append("")

    lines.append("Phase Summary")
    lines.append("-" * 13)
    for phase, avg_altitude, avg_motor_rpm_phase in phase_rows:
        lines.append(
            f"{phase:<10} | avg altitude = {avg_altitude:>6.2f} m | avg RPM = {avg_motor_rpm_phase:>7.2f}"
        )

    lines.append("")
    lines.append("End of report.")

    report_text = "\n".join(lines)
    print(report_text)
    report_path.write_text(report_text, encoding = "utf-8")
    print(f"\nReport saved to: {report_path}")
    connection.close()

if __name__ == "__main__":
    main()

