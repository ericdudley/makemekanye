import base64
import sys
import io
from google.cloud import vision
from google.cloud.vision import types

def detect_face(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    try:
        faces = response.face_annotations
    except:
        Exception("No faces detected")

    return faces


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    faces = detect_face(sys.argv[1])

    print("Faces:")

    for face in faces:
        print(face)
