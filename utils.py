from datetime import datetime


def save_results(target, open_ports, filename="scan_results.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(filename, "a") as f:
        f.write(f"Port Scan Results for: {target}\n")
        f.write(f"Scan Time: {timestamp}\n")
        f.write("-" * 50 + "\n")

        if open_ports:
            for port in sorted(open_ports):
                f.write(f"Port {port:<5} : OPEN\n")
        else:
            f.write("No open ports found.\n")

        f.write("-" * 50 + "\n")
        f.write(f"Total Open Ports: {len(open_ports)}\n\n")

    print(f"[+] Scan results saved to '{filename}'")
