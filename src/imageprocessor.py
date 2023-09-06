import random

from PIL import Image


class Im:
    """Image Object"""

    def __init__(self, location) -> None:
        self.location = location
        self.image = Image.open(location)
        self.width, self.height = self.image.size

        self.image_new = Image.new("RGB", self.image.size, (255, 255, 255))
        self.image_data = []

    def split_image(self):
        """
        Splits the image into tiles of variable width.

        Returns a list of tuples -> (Pillow object, upper-left coordinates)
        """
        rows = 32
        min_width = self.width // 32
        tile_height = self.height // rows

        for i in range(rows):
            # define the remaining space in each row
            remaining = self.width
            while remaining > 0:
                tile_width = random.randint(min_width, self.width // 16)

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

                # add cropped image and its coordinates to image_data
                self.image_data.append((new_img, left, upper))
        return self.image_data

    def place_tiles(self, word_length):
        """Picks a random number of tiles to be placed on the game screen"""
        num_tiles = len(self.image_data) // word_length
        tiles = []

        for _ in range(num_tiles):
            tile = random.choice(self.image_data)
            tiles.append(tile)
            self.image_data.remove(tile)

        for tile in tiles:
            self.image_new.paste(tile[0], (tile[1], tile[2]))
        return self.image_new

    def remove_tiles(self):
        """Permantly blackens some of the placed tiles on the game board"""
        pass
