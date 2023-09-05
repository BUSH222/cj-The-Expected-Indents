import base64
import io
import random

from PIL import Image


class Im:
    """Image Object"""

    def __init__(self, location) -> None:
        self.location = location
        self.image = Image.open(location)
        self.width, self.height = self.image.size
        self.image_data = []

    def split_image(self):
        """Splits the image into tiles of variable width. Returns a list of tuples -> (image data, upper-left coordinates)

        Args:
            rows (int): Number of tile rows to be included

        Returns:
            list: Encoded image data
        """
        rows = 10
        min_width = self.width // 25
        tile_height = self.height // rows

        for i in range(rows):
            # define the remaining space in each row
            remaining = self.width
            while remaining > 0:
                tile_width = random.randint(min_width, remaining)

                if (remaining - tile_width) < min_width:
                    tile_width = remaining

                # define boundaries for where the image should be cropped
                left = self.width - remaining
                upper = i * tile_height
                right = left + tile_width
                lower = upper + tile_height

                # deduct tile width of the newly created image from remaining space
                remaining -= tile_width

                new_img = self.image.crop((left, upper, right, lower))

                # encode the new image and append to image_data
                data = io.BytesIO()
                new_img.save(data, "JPEG")
                img_b64 = base64.b64encode(data.getvalue()).decode("utf-8")
                self.image_data.append((img_b64, left, upper))
        return self.image_data

    def display_image(self):
        """Returns the full image to be displayed"""
        data = io.BytesIO()
        self.image.save(data, "JPEG")

        return base64.b64encode(data.getvalue()).decode("utf-8")

    def place_tiles(self, word_length):
        """Picks a random number of tiles to be placed on the game screen"""
        num_tiles = len(self.image_data) // word_length
        tiles = []

        for _ in range(num_tiles):
            tile = random.choice(self.image_data)
            tiles.append(tile)
            self.image_data.remove(tile)

        return tiles

    def remove_tiles(self):
        """Permantly blackens some of the placed tiles on the game board"""
        pass
