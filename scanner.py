import socket
import threading
import sys
import time

open_ports = []
lock = threading.Lock()


def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        sock.close()

        if result == 0:
            with lock:
                open_ports.append(port)

    except:
        pass


def threaded_scan(target, start_port, end_port):
    threads = []

    print(f"[*] Scanning {target} from port {start_port} to {end_port}")

    start_time = time.time()

    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.time()

    print("\nScan completed.")
    print(f"Time taken: {end_time - start_time:.2f} seconds")

    if open_ports:
        print("\nOpen ports:")
        for port in sorted(open_ports):
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
