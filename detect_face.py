import base64
import sys
import io
from google.cloud import vision
from google.cloud.vision import types


# def _select_fields(faces):
#     for face in faces:
#         face = {
#             "roll_angle": face.roll_angle,
#             "pan_angle": face.pan_angle,
#             "tilt_angle": face.tilt_angle,
#             "joy_likelihood": face.joy_likelihood,
#             "sorrow_likelihood": face.sorrow_likelihood,
#             "anger_likelihood": face.anger_likelihood,
#             "surprise_likelihood": face.surprise_likelihood,
#             "landmarks": face.landmarks
#         }
#     return faces


def detect_face(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    #faces = _select_fields(faces)
    return faces


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    faces = detect_face(sys.argv[1])

    print("Faces:")

    for face in faces:
        print(face)
