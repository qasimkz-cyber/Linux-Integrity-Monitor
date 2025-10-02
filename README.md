# Linux Integrity Monitor

A simple Host-based Intrusion Detection System (HIDS) written in Python to monitor critical Linux files for unauthorized changes.

## Core Functionality

On its first run, the script establishes a secure baseline by storing the SHA-256 hashes of specified system files in `baseline.json`.

On all subsequent runs, it re-calculates the hashes and compares them to the baseline. Any mismatches are reported as potential integrity violations. The script is designed for automated background execution using `cron`.

## Built With

  * Python 3
  * `hashlib` & `json` (Standard Libraries)
  * `cron` (for automation)

## Usage

### Manual Scan

The script requires `sudo` to read protected system files.


`sudo python3 main.py`


### Automated Scans

To automate the script, add the following line to the root crontab (`sudo crontab -e`). This example runs the scan every minute and saves the output.


`* * * * * cd /path/to/your/project && /path/to/your/venv/bin/python3 main.py >> /path/to/your/project/scan.log 2>&1`
