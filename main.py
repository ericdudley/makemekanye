from flask import Flask, render_template, request
from detect_face import detect_face

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/faceify",methods=["POST"])
def faceify():
    base64_image = request.json
    Faces = detect_face(base64_image)
    print(Faces)
    return(request.json)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
