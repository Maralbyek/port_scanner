from datetime import datetime


def save_results(target, open_ports, filename="scan_results.txt"):
    with open(filename, "w") as f:
        f.write(f"Port Scan Results for {target}\n")
        f.write(f"Scan Time: {datetime.now()}\n")
        f.write("=" * 50 + "\n\n")

        for port in open_ports:
            f.write(f"Port {port}: OPEN\n")

        f.write(f"\nTotal Open Ports: {len(open_ports)}\n")

    print(f"[+] Results saved to {filename}")
