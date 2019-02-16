import base64
from io import BytesIO
from google.cloud import vision
from google.cloud.vision import types


def detect_face(string):
    client = vision.ImageAnnotatorClient()

    content = BytesIO(base64.b64decode(string))
    image = types.Image(content=content)
    response = client.face_detection(image=image)
    faces = response.face_annotations

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
