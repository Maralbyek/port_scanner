from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    ip = scan_type = ports = None

    if request.method == "POST":
        ip = request.form.get("ip")
        scan_type = request.form.get("scan_type")
        ports = request.form.get("ports")

    return render_template(
        "index.html",
        ip=ip,
        scan_type=scan_type,
        ports=ports
    )

if __name__ == "__main__":
    app.run(debug=True)
