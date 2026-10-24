#!/usr/bin/env python3
"""
NetProbe-CLI: A multi-threaded TCP port scanner with banner grabbing.
Author: John Georgakopoulos
Disclaimer: For authorized educational and testing purposes only.
"""

import argparse
import concurrent.futures
import json
import socket
import sys
import time


def parse_ports(port_str):
    """Parses port argument (supports ranges like '1-1024' or lists like '22,80,443')."""
    ports = []
    try:
        if "-" in port_str:
            start, end = map(int, port_str.split("-"))
            ports = list(range(start, end + 1))
        elif "," in port_str:
            ports = [int(p.strip()) for p in port_str.split(",")]
        else:
            ports = [int(port_str)]
    except ValueError:
        print("[-] Error: Invalid port format. Use format like '80', '1-1024', or '22,80,443'.")
        sys.exit(1)
    return ports


def grab_banner(s, port):
    """Attempts to grab the service banner from an open port."""
    try:
        s.settimeout(2.0)
        # Try receiving data sent automatically by the service (e.g., SSH, FTP)
        banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
        
        # If nothing received immediately, probe common web ports
        if not banner and port in [80, 443, 8080, 8443]:
            s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
            
        return banner if banner else "Open (No banner returned)"
    except socket.timeout:
        return "Open (Banner read timeout)"
    except Exception:
        return "Open (Banner grab failed)"


def scan_port(target_ip, port, timeout):
    """Scans a single TCP port and grabs banner if open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target_ip, port))
            if result == 0:
                banner = grab_banner(s, port)
                return {"port": port, "status": "open", "banner": banner}
    except Exception:
        pass
    return None


def main():
    parser = argparse.ArgumentParser(
        description="NetProbe-CLI: Fast Multi-Threaded Port Scanner & Banner Grabber"
    )
    parser.add_argument("-t", "--target", required=True, help="Target IP address or domain name")
    parser.add_argument(
        "-p", "--ports", default="1-1024", help="Port range (default: 1-1024, e.g., 22,80,443 or 1-1000)"
    )
    parser.add_argument(
        "-th", "--threads", type=int, default=100, help="Number of concurrent threads (default: 100)"
    )
    parser.add_argument(
        "--timeout", type=float, default=1.0, help="Socket connection timeout in seconds (default: 1.0)"
    )
    parser.add_argument(
        "-o", "--output", help="Export results to a JSON file (e.g., results.json)"
    )

    args = parser.parse_args()

    # Resolve target domain/IP
    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"[-] Error: Could not resolve hostname {args.target}")
        sys.exit(1)

    ports = parse_ports(args.ports)
    
    print(f"\n[+] Starting scan on target: {args.target} ({target_ip})")
    print(f"[+] Total ports to scan: {len(ports)} | Threads: {args.threads} | Timeout: {args.timeout}s")
    print("-" * 65)

    open_ports = []
    start_time = time.time()

    # Multi-threaded execution using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_port = {
            executor.submit(scan_port, target_ip, port, args.timeout): port 
            for port in ports
        }
        
        for future in concurrent.futures.as_completed(future_to_port):
            res = future.result()
            if res:
                open_ports.append(res)
                print(f"[+] Port {res['port']:<5} OPEN — {res['banner']}")

    duration = time.time() - start_time
    print("-" * 65)
    print(f"[+] Scan completed in {duration:.2f} seconds.")
    print(f"[+] Found {len(open_ports)} open port(s).")

    # Optional JSON Export
    if args.output:
        output_data = {
            "target": args.target,
            "target_ip": target_ip,
            "scan_duration_seconds": round(duration, 2),
            "open_ports": open_ports
        }
        try:
            with open(args.output, "w") as f:
                json.dump(output_data, f, indent=4)
            print(f"[+] Results successfully exported to {args.output}")
        except IOError as e:
            print(f"[-] Error saving file: {e}")


if __name__ == "__main__":
    main()
