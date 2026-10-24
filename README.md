# NetProbe-CLI: Multi-Threaded TCP Port Scanner & Banner Grabber

![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Category](https://img.shields.io/badge/category-Network%20Security-orange.svg)

A high-performance, lightweight TCP network scanner built from scratch using pure Python. `NetProbe-CLI` features multi-threaded port identification, service banner extraction, CLI interface parsing, and structured JSON telemetry export for vulnerability assessment reporting.

---

## Key Features

* **Multi-Threaded Architecture:** Utilizes Python's `concurrent.futures.ThreadPoolExecutor` to perform rapid parallel socket connections.
* **Banner Grabbing & Fingerprinting:** Captures initial service headers upon successful TCP handshakes (e.g., SSH versions, FTP server headers, exposed shell prompts).
* **Flexible CLI Interface:** Offers customizable target IPs, domain names, port ranges, thread limits, and socket timeouts via `argparse`.
* **Structured Output:** Automatically exports scan findings, telemetry, and service responses to formatted JSON files for SOC/SIEM pipeline ingestion.
* **Zero External Dependencies:** Built entirely with Python standard libraries (`socket`, `argparse`, `json`, `threading`).

---

## Installation & Setup
Clone the repository and run it with python: 
- git clone https://github.com/LX0ps/NetProbe-CLI.git
- cd NetProbe-CLI
- py scanner.py 


**Verify Python Installation**:
Requires Python 3.10+ (Tested on Windows 11 with Python 3.12.10). Install on windows via ms store or winget 
check python version to have 3.10+. I tested on windows 11 with python 3.12.10

Basic local scan: Scan ports 1 through 100 on the loopback interface
python scanner.py -t 127.0.0.1 -p 1-100 

<img width="875" height="214" alt="python net scan 1" src="https://github.com/user-attachments/assets/5f47e58a-4d0f-4dc0-85ea-77a35746025d" />


Public Authorized Testing (scanme.nmap.org)1-100

python scanner.py -t scanme.nmap.org -p 20-100 
<img width="961" height="250" alt="scan nmap" src="https://github.com/user-attachments/assets/c26a6d27-448a-4552-9cd8-c71c2dd036d5" />



Full Target Assessment (Exporting JSON Report)
Scan a target virtual machine (e.g., Metasploitable 2) with 150 threads and export results:
python scanner.py -t 192.168.56.101 -p 1-2000 -th 150 -o metasploitable_results.json

explain the command: 

- python: invokes the Python 3 interpreter to execute the code.
- scanner.py: the name of the custom script.
- -t 192.168.56.101: the target ip of the local metasploit 2 vm.
- -p 1-2000: the port range. tell the script to check every port sequentially from 1 up to 2000.
- -th 150: the threads. controls the speed of the check instead of checking one port at a time.
- -o metasploitable_results.json: Tells the script to take all the open ports and service banners it finds and automatically package them into a structured JSON file named metasploitable_results.json in your folder.

<img width="1433" height="557" alt="full scan json" src="https://github.com/user-attachments/assets/cba9cb6c-3820-4a20-a147-cdf8a734674b" />




🛡️ Ethical Disclaimer:
**This tool is created strictly for educational purposes, defensive network administration, and authorized security testing (such as bug bounties or lab environments with explicit permission). Unauthorized scanning of targets you do not own or have explicit written authorization to test is illegal and violates terms of service. The author assumes no liability for misuse or damage caused by this program.**


# Acknowledgements

* Thanks to [VickyCantCode](https://github.com/VickyCantCode) for the inspiration on building this project!









   
