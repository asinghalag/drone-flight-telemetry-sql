import sqlite3
from pathlib import Path


def main() -> None:
    # Build path to database
    db_path = Path("data") / "drone_flight.db"

    # Connect to database
    connection = sqlite3.connect(db_path)

    # Create cursor for SQL
    cursor = connection.cursor()

    # Query SQLite's internal index list for the flight_logs table
    cursor.execute("PRAGMA index_list(flight_logs)")
    indexes = cursor.fetchall()

    print("\nIndexes on flight_logs:")
    print("-----------------------")
    for index_row in indexes:
        print(index_row)

    # Close database connection
    connection.close()


if __name__ == "__main__":
    main()