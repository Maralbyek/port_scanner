import socket
import threading
import sys


def threaded_scan(target, port, results, lock):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            with lock:
                results.append(port)
        sock.close()
    except:
        pass


def fast_scan(target, port_range):
    print(f"[*] Starting fast scan on {target}")
    threads = []
    results = []
    lock = threading.Lock()

    for port in port_range:
        t = threading.Thread(
            target=threaded_scan,
            args=(target, port, results, lock)
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return sorted(results)


def scan_with_progress(target, port_range):
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
        bar = int(progress / 2)
        sys.stdout.write(
            f"\r[{'=' * bar}{' ' * (50 - bar)}] {progress:.1f}%"
        )
        sys.stdout.flush()

    print()
    return open_ports


def scan_ip_range(ip_base, start, end, port):
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
