from flask import *

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/faceify")
def faceify():
    pass


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
