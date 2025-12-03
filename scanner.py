import socket

PORT_SERVICES = {
     20: "FTP Data Transfer",
    21: "FTP Control",
    22: "SSH (Secure Shell)",
    23: "Telnet",
    25: "SMTP (Email)",
    53: "DNS",
    80: "HTTP (Web)",
    110: "POP3 (Email)",
    143: "IMAP (Email)",
    443: "HTTPS (Secure Web)",
    445: "SMB (File Sharing)",
    3306: "MySQL Database",
    3389: "RDP (Remote Desktop)",
    5432: "PostgreSQL Database",
    8080: "HTTP Alternate",
    8443: "HTTPS Alternate"
}

print("=" * 50)
print("Port Scanner with Service Detection")
print("=" * 50)

target = input("Enter target IP or domain: ")
print(f"\nScanning {target}...\n")

open ports = []

for port in range(1, 101):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
     result = sock.connect_ex((target, port))

    if result == 0:
         service = PORT_SERVICES.get(port, "Unknown Service")
        print(f"[+] Port {port:5d} is OPEN | Service: {service}")
        open_ports.append(port)
    else:
        print(f"[-] Port {port} is closed thus try again.")

    sock.close()

print("Done!")

