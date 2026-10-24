PYTHON CODE EXPLANATION FOR SCANNER.PY





This is a network port scanner — it checks which ports (communication endpoints) on a computer are open and listening for connections. Think of ports like doors on a building: some are open and accepting visitors, some are locked. This tool checks which "doors" are open and tries to see what service is behind each one (like SSH, web servers, etc.).





* parse\_ports() Function



This function takes your port input and converts it into a list of ports to scan. It handles three formats:



&#x20;   Single port: "80" → \[80]

&#x20;   Range: "1-1024" → \[1, 2, 3, ..., 1024]

&#x20;   Comma-separated: "22,80,443" → \[22, 80, 443]





* grab\_banner() Function



Once a port is found open, this function tries to read the banner — the text a service sends when you connect. For example:



&#x20;   An SSH server might say: "SSH-2.0-OpenSSH\_7.4"

&#x20;   A web server might send HTTP headers



If nothing comes automatically, it sends an HTTP request to web ports (80, 443, 8080, 8443) to get a response.







* scan\_port() Function



This is the core scanning function. It:



&#x20;   Creates a socket (network connection)

&#x20;   Tries to connect to a specific port on the target

&#x20;   If the connection succeeds (port is open), grabs the banner

&#x20;   Returns the result





* main() Function



This orchestrates everything:

Step	What It Does

Parse arguments	Reads your command-line options (target IP, ports, threads, etc.)

Resolve hostname	Converts domain names to IP addresses

Set up threading	Creates multiple worker threads to scan ports simultaneously (faster)

Run scans	Launches all port scans in parallel using ThreadPoolExecutor

Display results	Prints open ports and their banners to the screen

Export JSON	Optionally saves results to a file





USAGE EXP: 



python3 netprobe.py -t 192.168.1.1 -p 1-1024 -th 50



Flag	Meaning

\-t	Target IP or domain

\-p	Ports to scan (default: 1-1024)

\-th	Number of threads (default: 100)

\--timeout	How long to wait for a response (default: 1 second)

\-o	Save results to JSON file













