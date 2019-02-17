from flask import Flask, render_template, request, redirect, url_for
from detect_face import detect_face
from stat import S_ISREG, ST_CTIME, ST_MODE
from uuid import uuid1
from pixels import Pixels
from random import randint, choice
import time
from PIL import Image
from coolname import generate_slug, RandomGenerator
import os
from PIL import Image, ExifTags

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MAX_WIDTH = 400
MAX_HEIGHT = 400
MAX_FILES = 1024


def fix_orientation(img):
    if hasattr(img, "_getexif"):
        exifdata = img._getexif()
        try:
            orientation = exifdata.get(274)
        except:
            # There was no EXIF Orientation Data
            orientation = 1
    else:
        orientation = 1

    if orientation is 1:  # Horizontal (normal)
        pass
    elif orientation is 2:  # Mirrored horizontal
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation is 3:  # Rotated 180
        img = img.rotate(180)
    elif orientation is 4:  # Mirrored vertical
        img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation is 5:  # Mirrored horizontal then rotated 90 CCW
        img = img.rotate(-90).transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation is 6:  # Rotated 90 CCW
        img = img.rotate(-90)
    elif orientation is 7:  # Mirrored horizontal then rotated 90 CW
        img = img.rotate(90).transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation is 8:  # Rotated 90 CW
        img = img.rotate(90)

    # save the result and overwrite the originally uploaded image
    return img


@app.route("/", methods=["GET", "POST"])
@app.route("/<id>", methods=["GET", "POST"])
def main(id=None):
    if not id:
        id = "example" + str(randint(1, 2))
    upload_path = "static/done/"
    temp_path = "img/"

    entries = (os.path.join(upload_path, fn) for fn in os.listdir(upload_path))
    entries = ((os.stat(path), path) for path in entries)
    entries = (
        (stat[ST_CTIME], path) for stat, path in entries if S_ISREG(stat[ST_MODE])
    )
    sorted_entries = sorted(entries)
    sorted_ids = [
        cpath.split("/")[-1][:-4]
        for ctime, cpath in sorted_entries
        if "orig_" not in cpath
    ]

    if len(sorted_entries) > MAX_FILES:
        for i in range(0, len(sorted_entries) - MAX_FILES):
            path = sorted_entries[i][1]
            if "example" not in path:
                os.remove(path)

    if request.method == "POST":
        file = request.files["file"]
        if file:
            id = generate_slug(2)
            orig_file_path = upload_path + "orig_" + id + ".png"
            done_file_path = upload_path + id + ".png"

        img = Image.open(file)
        img = fix_orientation(img)

        if img.width > MAX_WIDTH:
            ratio = img.width / MAX_WIDTH
            img = img.resize((int(img.width / ratio), int(img.height / ratio)))
        elif img.height > MAX_HEIGHT:
            ratio = img.height / MAX_HEIGHT
            img = img.resize((int(img.width / ratio), int(img.height / ratio)))

        img.save(orig_file_path)

        faces = detect_face(orig_file_path)

        os.remove(orig_file_path)

        if len(faces) > 0:
            face = faces[0]
            pixels = Pixels(img, faces)
            pixels.faceSwap()
            emotions = pixels.getEmotions(faces[0])
            max_emotion_level = 0
            max_emotion = "neutral"
            for emotion, level in emotions.items():
                if level > max_emotion_level:
                    max_emotion_level = level
                    max_emotion = emotion

            id = max_emotion + "-" + id

            orig_file_path = upload_path + "orig_" + id + ".png"
            done_file_path = upload_path + id + ".png"

            img.save(orig_file_path)

            img.putdata(pixels.data)
            img.save(done_file_path)
        else:
            img.save(orig_file_path)
            img.save(done_file_path)

        return redirect("/" + id)
    else:
        if len(sorted_ids) > 0:
            try:
                curr_idx = sorted_ids.index(id)
                prev_id = sorted_ids[
                    len(sorted_ids) - 1 if curr_idx - 1 < 0 else curr_idx - 1
                ]
                next_id = sorted_ids[
                    0 if curr_idx + 1 >= len(sorted_ids) else curr_idx + 1
                ]
            except:
                rand_id = choice(sorted_ids)
                return redirect("/" + rand_id)
        if "-" in id:
            emotion = id.split("-")[0]
        else:
            emotion = "example"
        return render_template(
            "main.html", emotion=emotion, id=id, prev_id=prev_id, next_id=next_id
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
