import sqlite3
from pathlib import Path


def get_altitude_series(cursor):
    # Get altitude values ordered by time
    cursor.execute("""
        SELECT altitude_m
        FROM flight_logs
        ORDER BY timestamp_seconds
    """)
    return [row[0] for row in cursor.fetchall()]


def draw_ascii_plot(values, width=80, height=20):
    # Stop early if there is no data
    if not values:
        print("No data to plot.")
        return

    min_val = min(values)
    max_val = max(values)

    print(f"Number of altitude points: {len(values)}")
    print(f"Min altitude: {min_val:.2f}")
    print(f"Max altitude: {max_val:.2f}")

    # Scale altitude values into plot height
    scaled = [
        int((v - min_val) / (max_val - min_val) * (height - 1))
        if max_val != min_val else 0
        for v in values
    ]

    # Downsample if there are more points than plot width
    step = max(1, len(values) // width)
    sampled = scaled[::step][:width]

    print(f"Plot width used: {len(sampled)} points")

    # Create blank canvas
    canvas = [[" " for _ in range(width)] for _ in range(height)]

    # Put stars on the canvas
    for x, y in enumerate(sampled):
        canvas[height - 1 - y][x] = "*"

    print("\nALTITUDE PROFILE (ASCII PLOT)")
    print("-" * width)

    for row in canvas:
        print("".join(row))

    print("-" * width)
    print("Time →")


def main():
    # Build path to database
    db_path = Path("data") / "drone_flight.db"
    print(f"Reading database from: {db_path}")

    # Connect to database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Get altitude series
    altitude_values = get_altitude_series(cursor)

    # Draw plot
    draw_ascii_plot(altitude_values)

    # Close connection
    connection.close()


if __name__ == "__main__":
    main()