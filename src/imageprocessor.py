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

    def split(self, rows):
        """Splits the image into tiles of variable width"""
        min_width = self.width // 25
        tile_height = self.height // rows

        image_data = []
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
                image_data.append(img_b64)
        return image_data
