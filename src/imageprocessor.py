import random

from PIL import Image


class Im:
    """Image Object"""

    def __init__(self, image) -> None:
        self.image = image
        self.width, self.height = self.image.size
        self.image_new = Image.new("RGB", self.image.size, (255, 255, 255))
        self.placed_tiles = []
        self.image_data = []

    def split_image(self):
        """Splits the image into tiles of variable width"""
        rows = 32
        min_width = self.width // rows
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

    def place_tiles(self, word, guessed_letter):
        """Picks a random number of tiles to be placed on the game screen

        Args:
            word (str): Full word /  Secret Code
            guessed_letter (str): Guessed letter
        """
        num_tiles = (len(self.image_data) * word.count(guessed_letter)) // len(word)

        for _ in range(num_tiles):
            if not self.image_data:
                # return if no tiles remaining
                return
            tile = random.choice(self.image_data)
            self.placed_tiles.append(tile)
            self.image_data.remove(tile)

        for tile in self.placed_tiles:
            self.image_new.paste(tile[0], (tile[1], tile[2]))

    def remove_tiles(self):
        """Permantly blackens some of the placed tiles on the game board"""
        n = random.randint(len(self.placed_tiles) // 4, len(self.placed_tiles) // 2)

        for _ in range(n):
            if not self.placed_tiles:
                # return if no placed tiles
                return
            tile_to_remove = random.choice(self.placed_tiles)
            black_tile = Image.new("RGB", tile_to_remove[0].size, (0, 0, 0))
            self.image_new.paste(black_tile, (tile_to_remove[1], tile_to_remove[2]))
            self.placed_tiles.remove(tile_to_remove)
