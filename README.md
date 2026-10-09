Add minimal Flask web interface with IP input
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

## Usage
```bash
python main.py
