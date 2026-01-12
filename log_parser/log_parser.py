#!/usr/bin/env python3
import argparse
import re
from collections import Counter
import os


def normalize_log_line(line):
    """
    Strips variable data (timestamps, UUIDs, IPs, file paths/line numbers)
    from a log line and normalizes whitespace.
    """
    # Define regex patterns for various variable data
    # ISO 8601, common date/time formats
    line = re.sub(r'\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(,\d{3}|\.\d{3})?Z?', '<TIMESTAMP>', line)
    line = re.sub(r'\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}', '<TIMESTAMP>', line)
    line = re.sub(r'\w{3}\s\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2}', '<TIMESTAMP>', line)  # e.g., "Mon Oct 26 12:34:56"

    # UUIDs
    line = re.sub(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}', '<UUID>', line)

    # IPv4 addresses
    line = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '<IP>', line)

    # File paths and line numbers (e.g., /path/to/file.py:123 or at com.example.Class.method(Class.java:123))
    line = re.sub(r'\(?([a-zA-Z0-9_/\.-]+\.(py|java|go|js|php|rb|cpp|c|h|cs):(\d+))\)?', '<FILE_LOCATION>', line)

    # Normalize whitespace
    line = re.sub(r'\s+', ' ', line).strip()
    return line


def find_anomalous_errors(log_file_path, top_n=10):
    """
    Reads a log file, processes lines identified as errors, groups them,
    and prints the top N most frequent patterns.
    """
    error_keywords = ['ERROR', 'FAILURE', 'FAILED', 'EXCEPTION', 'CRITICAL', 'DENIED', 'TIMEOUT', 'REFUSED']
    error_patterns = Counter()

    try:
        with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # Check if the line contains any error keyword (case-insensitive)
                if any(keyword in line.upper() for keyword in error_keywords):
                    normalized_line = normalize_log_line(line)
                    error_patterns[normalized_line] += 1
    except FileNotFoundError:
        print(f"Error: Log file not found at '{log_file_path}'")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    print(f"\n--- Top {top_n} Anomalous Error Patterns in '{os.path.basename(log_file_path)}' ---")
    if not error_patterns:
        print("No error patterns found.")
        return

    for pattern, count in error_patterns.most_common(top_n):
        print(f"Count: {count:<5} | Pattern: {pattern}")
    print("------------------------------------------------------------------")


def main():
    parser = argparse.ArgumentParser(
        description="A Log Anomalous Error Grouper. "
                    "Parses log files, normalizes error messages by stripping variable data, "
                    "and reports the most frequent error patterns."
    )
    parser.add_argument(
        "log_file",
        help="Path to the log file to analyze."
    )
    parser.add_argument(
        "-n", "--top-n",
        type=int,
        default=10,
        help="Number of top error patterns to display (default: 10)."
    )

    args = parser.parse_args()

    find_anomalous_errors(args.log_file, args.top_n)


if __name__ == "__main__":
    main()