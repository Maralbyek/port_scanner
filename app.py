from datetime import datetime
import ipaddress
import socket

from flask import Flask, render_template, request

from scanner import scan_ports
from services import detect_service

app = Flask(__name__)

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 8080]


def parse_ports(scan_type, value):
    if scan_type == "common":
        return COMMON_PORTS
    if scan_type == "full":
        return range(1, 1001)
    if scan_type != "custom":
        raise ValueError("Choose a supported scan type.")

    parts = value.strip().split("-")
    if len(parts) != 2:
        raise ValueError("Custom ports must use the format start-end.")
    start, end = (int(part.strip()) for part in parts)
    if not 1 <= start <= end <= 65535:
        raise ValueError("Ports must be between 1 and 65535.")
    if end - start > 2000:
        raise ValueError("Custom scans are limited to 2,000 ports.")
    return range(start, end + 1)


def format_results(target, open_ports):
    return [
        {"port": port, "service": detect_service(port)}
        for port in open_ports
    ]


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    error = None
    target = ""
    scan_type = "common"
    ports = ""
    duration = None

    if request.method == "POST":
        target = request.form.get("ip", "").strip()
        scan_type = request.form.get("scan_type", "common")
        ports = request.form.get("ports", "").strip()

        try:
            if not target:
                raise ValueError("Enter an IP address or hostname.")
            try:
                ipaddress.ip_address(target)
            except ValueError:
                socket.gethostbyname(target)
            selected_ports = parse_ports(scan_type, ports)
            started = datetime.now()
            results = format_results(target, scan_ports(target, selected_ports))
            duration = (datetime.now() - started).total_seconds()
        except (ValueError, socket.gaierror, socket.timeout) as exc:
            error = str(exc) or "The target could not be scanned."

    return render_template(
        "index.html",
        target=target,
        scan_type=scan_type,
        ports=ports,
        results=results,
        error=error,
        duration=duration,
    )

if __name__ == "__main__":
    app.run(debug=True)
