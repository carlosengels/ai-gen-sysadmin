You are an expert Python developer with a strong understanding of command-line tools and log parsing.

Your task is to write a Python script that acts as a log "Anomalous Error" Grouper.

Here's the desired functionality:

1.  **Input:** The script should accept a log file path as a command-line argument.
2.  **Parsing:**
    * Read the log file line by line.
    * Identify lines that likely represent error messages. A good heuristic is to look for keywords like "ERROR", "FAILURE", "FAILED", "EXCEPTION", "CRITICAL", "DENIED", "TIMEOUT", or "REFUSED". (Be case-insensitive for these keywords).
    * For identified error lines, strip out highly variable data that would make identical errors appear unique. This includes:
        * **Timestamps:** Remove common date/time patterns (e.g., `YYYY-MM-DD HH:MM:SS`, `MM/DD/YY HH:MM:SS`, ISO 8601 variations).
        * **UUIDs/Request IDs:** Remove alphanumeric strings that look like UUIDs (e.g., `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`).
        * **IP Addresses:** Remove IPv4 addresses (e.g., `xxx.xxx.xxx.xxx`).
        * **File Paths/Line Numbers:** Remove patterns like `(/path/to/file.py:123)`.
    * After stripping variable data, normalize multiple whitespace characters into a single space.
3.  **Grouping:** Group the processed (normalized) error lines and count their occurrences.
4.  **Output:**
    * Print the "Top N" most frequent anomalous error patterns (N should be configurable, default to 10).
    * Each output line should show the count and the normalized error pattern.
    * Sort the output by count in descending order.
5.  **Help/Usage:** Provide clear command-line help (`--help`).
6.  **Error Handling:** Gracefully handle cases where the file doesn't exist.

**Example Input Log Line:**
`2023-10-27 10:30:15,123 ERROR [main] c.e.a.SomeService - Failed to connect to database at 192.168.1.100 due to Connection refused. Request ID: abcdef12-3456-7890-abcd-ef1234567890.`

**Expected Normalized Output Pattern:**
`ERROR [main] c.e.a.SomeService - Failed to connect to database at <IP> due to Connection refused. Request ID: <UUID>.`

The script should be robust and efficient for potentially large log files. Use `argparse` for command-line arguments.