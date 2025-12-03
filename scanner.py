import socket
import threading
from datetime import datetime
import sys

def threaded_scan(target, port, results):
    """Scan a single port (used in threads)"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            results.append(port)
        sock.close()
    except:
        pass

def fast_scan(target, port_range):
    """Scan multiple ports using threads"""
    print(f"[*] Starting fast scan on {target}")
    threads = []
    results = []
    
    for port in port_range:
        thread = threading.Thread(target=threaded_scan, args=(target, port, results))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return sorted(results)

def grab_banner(target, port):
    """Try to grab service banner"""
    try:
        sock = socket.socket()
        sock.settimeout(2)
        sock.connect((target, port))
        sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
        banner = sock.recv(1024).decode().strip()
        sock.close()
        return banner
    except:
        return "No banner"

def detect_service(target, port):
    """Detect service running on port"""
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((target, port))
        
        try:
            service = socket.getservbyport(port)
        except:
            service = "unknown"
        
        sock.close()
        return service
    except:
        return None

def save_results(target, open_ports, filename="scan_results.txt"):
    """Save scan results to file"""
    with open(filename, 'w') as f:
        f.write(f"Port Scan Results for {target}\n")
        f.write(f"Scan Time: {datetime.now()}\n")
        f.write("=" * 50 + "\n\n")
        
        for port in open_ports:
            f.write(f"Port {port}: OPEN\n")
        
        f.write(f"\nTotal Open Ports: {len(open_ports)}\n")
    
    print(f"[+] Results saved to {filename}")

def scan_with_progress(target, port_range):
    """Scan with progress indicator"""
    total = len(port_range)
    open_ports = []
    
    for i, port in enumerate(port_range, 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        
        if result == 0:
            open_ports.append(port)
        
        sock.close()
        
        progress = (i / total) * 100
        sys.stdout.write(f"\r[{'=' * int(progress/2)}{' ' * (50-int(progress/2))}] {progress:.1f}%")
        sys.stdout.flush()
    
    print()  
    return open_ports

def scan_ip_range(ip_base, start, end, port):
    """Scan multiple IPs for a specific port"""
    print(f"[*] Scanning {ip_base}.{start}-{end} on port {port}")
    live_hosts = []
    
    for i in range(start, end + 1):
        target = f"{ip_base}.{i}"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        result = sock.connect_ex((target, port))
        
        if result == 0:
            print(f"[+] {target}:{port} is OPEN")
            live_hosts.append(target)
        
        sock.close()
    
    return live_hosts

def advanced_scanner():
    """Complete scanner with all features"""
    print("=" * 60)
    print("ADVANCED PORT SCANNER")
    print("=" * 60)
    
    target = input("Enter target: ")
    print("\n[1] Quick Scan (common ports)")
    print("[2] Full Scan (1-1000)")
    print("[3] Custom Range")
    choice = input("Choice: ")
    
    if choice == "1":
        ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 8080]
    elif choice == "2":
        ports = range(1, 1001)
    else:
        start = int(input("Start port: "))
        end = int(input("End port: "))
        ports = range(start, end + 1)
    
    print(f"\n[*] Scanning {target}...")
    print(f"[*] Start time: {datetime.now()}\n")
    
    open_ports = fast_scan(target, ports)
    
    print("\n" + "=" * 60)
    print("RESULTS:")
    print("=" * 60)
    
    if open_ports:
        for port in open_ports:
            service = detect_service(target, port)
            banner = grab_banner(target, port)
            print(f"\n[+] Port {port} - {service}")
            if banner != "No banner":
                print(f"    Banner: {banner[:50]}...")
    else:
        print("No open ports found!")
    
    print(f"\n[*] End time: {datetime.now()}")
    print(f"[*] Found {len(open_ports)} open port(s)")
    
    if open_ports:
        save = input("\nSave results? (y/n): ")
        if save.lower() == 'y':
            save_results(target, open_ports)
