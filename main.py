from flask import Flask, render_template, request, redirect, url_for
from detect_face import detect_face
from uuid import uuid1
from pixels import Pixels
from PIL import Image
from os import remove

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
@app.route("/<id>", methods=["GET", "POST"])
def main(id=None):
    if request.method == "POST":
        file = request.files["file"]
        if file:
            id = str(uuid1())
            upload_path = "static/done/"
            temp_path = "img/"
            temp_file_path = temp_path + "id" + file.filename
            orig_file_path = upload_path + "orig_" + id + ".png"
            done_file_path = upload_path + id + ".png"

            file.save(temp_file_path)

            faces = detect_face(temp_file_path)

            img = Image.open(temp_file_path)

            img.save(orig_file_path)

            remove(temp_file_path)

            pixels = Pixels(img)

            for pixel in pixels.pixels():
                x, y = pixel
                if x % 8 < 4:
                    pixels.set(pixel, (0, 0, 0))

            img.putdata(pixels.data)
            img.save(done_file_path)

            return redirect("/" + id)
    else:
        return render_template("main.html", id=id)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
