"""
Simple CSV data logging for the greenhouse monitoring system.

Each plant monitor script logs one row per sensor reading to its own
CSV file under the data folder, so history can be reviewed later in
any spreadsheet program, even if no one was watching the dashboard
when something happened.
"""

import csv
import os


def log_row(csv_path, fieldnames, row_dict):
    """
    Appends one row to csv_path, writing a header row first if the
    file does not already exist.
    """
    file_exists = os.path.exists(csv_path)
    directory = os.path.dirname(csv_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(csv_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_dict)
