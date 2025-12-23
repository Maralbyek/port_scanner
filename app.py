from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    ip = None
    if request.method == "POST":
        ip = request.form.get("ip")

    return render_template("index.html", ip=ip)
return "<h1>Network Scanner Interface </h1><p>Web interface is working. </p>"

if __name__ == "__main__":

    app.run(debug=True)
