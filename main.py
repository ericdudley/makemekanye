from flask import Flask, render_template, request, redirect, url_for
from detect_face import detect_face
from uuid import uuid1
from pixels import Pixels
from PIL import Image
from os import remove

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MAX_WIDTH = 400
MAX_HEIGHT = 400


@app.route("/", methods=["GET", "POST"])
@app.route("/<id>", methods=["GET", "POST"])
def main(id=None):
    if request.method == "POST":
        file = request.files["file"]
        if file:
            id = str(uuid1())
            upload_path = "static/done/"
            temp_path = "img/"
            temp_file_path = temp_path + id + file.filename
            orig_file_path = upload_path + "orig_" + id + ".png"
            done_file_path = upload_path + id + ".png"

            file.save(temp_file_path)

            faces = detect_face(temp_file_path)

            img = Image.open(temp_file_path)

            if img.width > MAX_WIDTH:
                ratio = img.width / MAX_WIDTH
                img = img.resize((int(img.width / ratio), int(img.height / ratio)))
            elif img.height > MAX_HEIGHT:
                ratio = img.height / MAX_HEIGHT
                img = img.resize((int(img.width / ratio), int(img.height / ratio)))

            img.save(orig_file_path)

            remove(temp_file_path)

            pixels = Pixels(img, faces)
            # pixels.markFacesLandmarks()
            kanye = pixels.faceSwap(), faces

            img.putdata(pixels.data)
            img.save(done_file_path)

            return redirect("/" + id)
    else:
        return render_template("main.html", id=id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
