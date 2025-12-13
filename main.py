from datetime import datetime
from scanner import fast_scan
from services import grab_banner, detect_service
from utils import save_results


def advanced_scanner():
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
    elif choice == "3":
        start = int(input("Start port: "))
        end = int(input("End port: "))
        ports = range(start, end + 1)
    else:
        print("Invalid choice")
        return

    print(f"\n[*] Scanning {target}")
    print(f"[*] Start time: {datetime.now()}\n")

    open_ports = fast_scan(target, ports)

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)

    if open_ports:
        for port in open_ports:
            service = detect_service(port)
            banner = grab_banner(target, port)
            print(f"\n[+] Port {port} - {service}")
            if banner != "No banner":
                print(f"    Banner: {banner[:80]}")
    else:
        print("No open ports found")

    print(f"\n[*] End time: {datetime.now()}")
    print(f"[*] Open ports: {len(open_ports)}")

    if open_ports:
        save = input("\nSave results? (y/n): ")
        if save.lower() == "y":
            save_results(target, open_ports)


if __name__ == "__main__":
    advanced_scanner()
