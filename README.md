## Advanced Port Scanner

A multi-threaded TCP port scanner written in Python for educational purposes.

## Features
- Fast multi-threaded scanning
- Service detection
- Banner grabbing
- Custom port ranges
- Result export to file

## Web dashboard

Install the web dependency and start the dashboard:

```bash
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in your browser. The dashboard supports common
ports, ports 1-1000, and custom ranges up to 2,000 ports. Only scan systems
you are authorized to assess.

The dashboard uses the bundled PortWatch 3D network-atlas interface in
`templates/index.html` and `static/portwatch/`. No frontend build step is
required to run the Flask application. The visual atlas is an illustration of
the current scan; it does not claim to discover physical network topology.

## Usage
```bash
python main.py
