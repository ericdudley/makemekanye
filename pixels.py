from PIL import Image


class Pixels:
    def __init__(self, image):
        self.data = list(image.getdata())
        self.width = image.size[0]
        self.height = image.size[1]

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
