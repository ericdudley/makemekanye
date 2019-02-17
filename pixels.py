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
    "LIKELY": 0.75
    "VERY_LIKELY": 1,
}

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
        for i in range(len(kanyes)):
            kanye = kanyes[i]
            delta = 0
            delta += abs(kanye["joy_likelihood"] - face["joy_likelihood"])
            delta += abs(kanye["sorrow_likelihood"] - face["sorrow_likelihood"])
            delta += abs(kanye["anger_likelihood"] - face["anger_likelihood"])
            delta += abs(kanye["surprise_likelihood"] - face["surprise_likelihood"])
            if delta < best_delta:
                best_delta = delta
                best_kanye = i
        return best_kanye

    def faceSwap(self):
        print(self.getKanyeIndex())

