from flask import Flask, render_template, request
from detect_face import detect_face

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/faceify",["POST"])
def faceify():
    base64_image = request.json
    Faces = detect_face(base64_image)
    print(Faces)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
