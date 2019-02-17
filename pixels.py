from PIL import Image
from math import inf
import json

landmark_types = {
    "LEFT_EYE_PUPIL": 29,
    "RIGHT_EYE_PUPIL": 30,
    "MOUTH_LEFT": 11,
    "MOUTH_RIGHT": 12,
}

likelihoods = {
    "UNKNOWN": 0,
    "VERY_UNLIKELY": 0,
    "UNLIKELY": 0.25,
    "POSSIBLE": 0.5,
    "LIKELY": 0.75,
    "VERY_LIKELY": 1,
}

likelihood_name = (
    "UNKNOWN",
    "VERY_UNLIKELY",
    "UNLIKELY",
    "POSSIBLE",
    "LIKELY",
    "VERY_LIKELY",
)

kanyes = []

for i in range(1, 11):
    image = Image.open("static/kanyePhotos/kanye" + str(i) + ".png")
    with open("static/kanyePhotos/kanye" + str(i) + ".json") as f:
        json_obj = json.load(f)

    face = json_obj["faceAnnotations"][0]
    kanyes.append({"img": image, "face": face})


class Pixels:
    def __init__(self, image, faces):
        self.data = list(image.getdata())
        self.width = image.size[0]
        self.height = image.size[1]
        self.faces = faces

    def get(self, pixel):
        x, y = pixel
        color = self.data[int(self.width * y + x)]
        return (color[0], color[1], color[2])

    def set(self, pixel, color):
        x, y = pixel
        color = color if len(color) == 4 else (color[0], color[1], color[2], 255)
        self.data[int(self.width * y + x)] = color

    def setSquare(self, pixel, width, color):
        """
        Draws a square centered on pixel with width <width> if odd or <width - 1> if even.
        """
        x, y = pixel
        width = width - 1 if width % 2 == 0 else width
        half = (width - 1) // 2
        for i in range(-half, half + 1):
            for j in range(-half, half + 1):
                self.set((x + i, y + j), color)

    def pixels(self):
        """
        Returns a list of all pixels represented as tuples of the form (x, y).
        """
        return [(x, y) for x in range(0, self.width) for y in range(0, self.height)]

    def markFacesLandmarks(self):
        for face in self.faces:
            for vertex in face.landmarks:
                if vertex.type in landmark_types.values():
                    self.setSquare(
                        (int(vertex.position.x), int(vertex.position.y)),
                        45,
                        (255, 0, 0),
                    )

    def getKanyeIndex(self):
        best_kanye = 0
        best_delta = inf
        face = self.faces[0]
        print(face)
        for i in range(len(kanyes)):
            kanye = kanyes[i]["face"]
            delta = 0
            delta += abs(
                likelihoods[kanye["joyLikelihood"]]
                - likelihoods[likelihood_name[face.joy_likelihood]]
            )
            delta += abs(
                likelihoods[kanye["sorrowLikelihood"]]
                - likelihoods[likelihood_name[face.sorrow_likelihood]]
            )
            delta += abs(
                likelihoods[kanye["angerLikelihood"]]
                - likelihoods[likelihood_name[face.anger_likelihood]]
            )
            delta += abs(
                likelihoods[kanye["surpriseLikelihood"]]
                - likelihoods[likelihood_name[face.surprise_likelihood]]
            )
            if delta < best_delta:
                best_delta = delta
                best_kanye = i
        return best_kanye

    def faceSwap(self):
        face = self.faces[0]
        kanye = kanyes[self.getKanyeIndex()]

        kanye_left_pupil = next(
            x for x in kanye["face"]["landmarks"] if x["type"] == "LEFT_EYE_PUPIL"
        )
        kanye_right_pupil = next(
            x for x in kanye["face"]["landmarks"] if x["type"] == "RIGHT_EYE_PUPIL"
        )
        kanye_left_mouth = next(
            x for x in kanye["face"]["landmarks"] if x["type"] == "MOUTH_LEFT"
        )
        print(kanye_left_pupil)
        print(kanye_right_pupil)
        print(kanye_left_mouth)

        kanye_face_center = (
            int(
                (kanye_right_pupil["position"]["x"] + kanye_left_pupil["position"]["x"])
                / 2
            ),
            int(
                (kanye_left_mouth["position"]["y"] + kanye_left_pupil["position"]["y"])
                / 2
            ),
        )

        left_pupil = next(
            x for x in face.landmarks if x.type == landmark_types["LEFT_EYE_PUPIL"]
        )
        right_pupil = next(
            x for x in face.landmarks if x.type == landmark_types["RIGHT_EYE_PUPIL"]
        )
        left_mouth = next(
            x for x in face.landmarks if x.type == landmark_types["MOUTH_LEFT"]
        )

        print(left_pupil)
        print(right_pupil)
        print(left_mouth)

        face_center = (
            int((right_pupil.position.x + left_pupil.position.x) / 2),
            int((left_mouth.position.y + left_pupil.position.y) / 2),
        )

        self.setSquare(face_center, 95, (0, 0, 255))
        return kanye

