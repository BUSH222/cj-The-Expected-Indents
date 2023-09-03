from PIL import Image


class Im:
    """Image Object"""

    def __init__(self, location) -> None:
        self.location = location
        self.image = Image.open(location)
        self.width, self.height = self.image.size

    def split(self):
        """Splits the image into tiles of random width, random height"""
        pass
