import base64
import sys
import io
from google.cloud import vision
from google.cloud.vision import types


def detect_face(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    return faces


if __name__ == "__main__":
    b64_str = (open(sys.argv[1], 'r').read().replace('\n', '').strip()).split(',')[1]

    faces = detect_face(b64_str)

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = (
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLOKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
    )

    print("Faces:")

    for face in faces:
        print("anger: {}".format(likelihood_name[face.anger_likelihood]))
        print("joy: {}".format(likelihood_name[face.joy_likelihood]))
        print("surprise: {}".format(likelihood_name[face.surprise_likelihood]))

        vertices = [
            "({},{})".format(vertex.x, vertex.y)
            for vertex in face.bounding_poly.vertices
        ]

        print("face bounds: {}".format(",".join(vertices)))
