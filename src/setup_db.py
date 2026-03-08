import sqlite3
from pathlib import Path


def main() -> None:
    # Create the data folder if it does not exist
    data_folder = Path("data")
    data_folder.mkdir(exist_ok=True)

    # Create the database file path
    db_path = data_folder / "drone_flight.db"

    # Connect to the SQLite database
    connection = sqlite3.connect(db_path)

    # Create a cursor for running SQL commands
    cursor = connection.cursor()

    # Create the flight_logs table with a new phase column
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flight_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp_seconds REAL NOT NULL,
            phase TEXT NOT NULL,
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

    # Save the table creation
    connection.commit()

    print("Database setup complete.")
    print(f"Database path: {db_path}")
    print("Table ready: flight_logs (with phase column)")

    # Close the database connection
    connection.close()


if __name__ == "__main__":
    main()