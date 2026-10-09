import socket
import threading
import sys
import time

def scan_port(target, port, timeout=0.5):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        sock.close()
        return port if result == 0 else None
    except:
        return None


def scan_ports(target, ports, timeout=0.5):
    open_ports = []
    lock = threading.Lock()
    threads = []

    def scan_and_collect(port):
        result = scan_port(target, port, timeout)
        if result is not None:
            with lock:
                open_ports.append(result)

    for port in ports:
        t = threading.Thread(target=scan_and_collect, args=(port,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return sorted(open_ports)


def threaded_scan(target, start_port, end_port):
    print(f"[*] Scanning {target} from port {start_port} to {end_port}")
    start_time = time.time()
    open_ports = scan_ports(target, range(start_port, end_port + 1))

    print("\nScan completed.")
    print(f"Time taken: {time.time() - start_time:.2f} seconds")

    if open_ports:
        print("\nOpen ports:")
        for port in open_ports:
            print(f" - Port {port}")
    else:
        print("\nNo open ports found.")


def main():
    if len(sys.argv) != 4:
        print("Usage: python port_scanner.py <target> <start_port> <end_port>")
        sys.exit(1)

    target = sys.argv[1]

    try:
        start_port = int(sys.argv[2])
        end_port = int(sys.argv[3])
    except ValueError:
        print("Ports must be integers.")
        sys.exit(1)

    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print("Invalid port range.")
        sys.exit(1)

    threaded_scan(target, start_port, end_port)


if __name__ == "__main__":
    main()
