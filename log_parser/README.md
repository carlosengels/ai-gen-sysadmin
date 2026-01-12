This README.md is designed to be placed inside the log_parser/ directory of your repository. It highlights the utility of the tool from an SRE perspective while explicitly calling out the AI-assisted workflow used to create it.

📊 Log Anomalous Error Grouper
During a high-severity incident, an SRE is often drowned in thousands of lines of logs. Searching for the "needle in the haystack" is classic toil. This tool was created to solve that by semantically grouping error patterns, allowing you to see the frequency of unique issues rather than a raw stream of data.

🤖 AI-Assisted Creation
This tool was generated using Large Language Models (LLMs).

The Intent: I defined the operational logic, the regex requirements for scrubbing variable data (IPs, UUIDs, Timestamps), and the SRE-focused output format.

The Execution: The AI handled the boilerplate for argparse and the complex regex implementation.

Prompting Strategy: See PROMPT.md for the exact technical instructions used to generate this tool.

🛠 Features
Pattern Recognition: Automatically groups similar errors by stripping out dynamic data (IP addresses, UUIDs, Timestamps, and file paths).

Smart Filtering: Specifically targets SRE-relevant keywords like ERROR, CRITICAL, TIMEOUT, and EXCEPTION.

Toil Reduction: Converts a 10,000-line log file into a concise "Top 10" summary in seconds.

Zero Dependencies: Uses only Python standard libraries for maximum portability across legacy servers.

🚀 Usage
Prerequisites
Python 3.6+

Linux/macOS (or WSL)

Running the Tool
Make it executable:

Bash

chmod +x log_parser.py
Analyze a log file:

Bash

./log_parser.py /var/log/syslog
Customizing the output (Top 5 errors):

Bash

./log_parser.py app_error.log -n 5
📋 Sample Output
When run against a noisy application log, the tool produces a clean summary:

Plaintext

--- Top 5 Anomalous Error Patterns in 'production.log' ---
Count: 142   | Pattern: ERROR [worker] Database query FAILED: Table <STRING> not found.
Count: 89    | Pattern: ERROR [network] Connection TIMEOUT to external service.
Count: 12    | Pattern: Exception in thread "main" java.lang.NullPointerException at <FILE_LOCATION>
Count: 5     | Pattern: CRITICAL [api] User <USER> attempted unauthorized access from <IP>.
------------------------------------------------------------------
🛡 SRE Best Practices Included
Portability: Uses #!/usr/bin/env python3 for cross-distro compatibility.

Robustness: Includes basic error handling for missing files and encoding issues (common in "dirty" production logs).

Transparency: Every log transformation is documented in the code, ensuring the "Scrubbing" logic is audit-ready.