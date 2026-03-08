import sqlite3
from pathlib import Path

def main() -> None:
    data_folder = Path("data")
    data_folder.mkdir(exist_ok=True)

    db_path = data_folder / "drone_flight.db"

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flight_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp_seconds REAL NOT NULL,
            altitude_m REAL NOT NULL,
            battery_percent REAL NOT NULL,
            pitch_deg REAL NOT NULL,
            roll_deg REAL NOT NULL,
            yaw_deg REAL NOT NULL,
            motor_rpm INTEGER NOT NULL,
            gps_lat REAL NOT NULL,
            gps_lon REAL NOT NULL
        )
    """)
    connection.commit()
    connection.close()

    print("Database created successfully")
    print(f"Database path: {db_path}")
    print("Table created: flight_logs")

if __name__ == "__main__":
    main()