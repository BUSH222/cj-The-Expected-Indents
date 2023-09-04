import base64
import io

from PIL import Image


class Im:
    """Image Object"""

    def __init__(self, location) -> None:
        self.location = location
        self.image = Image.open(location)
        self.width, self.height = self.image.size

    def split(self, rows, cols):
        """Splits the image into nxn tiles"""
        tile_width = self.width // cols
        tile_height = self.height // rows

        image_data = []
        tiles = 0
        for i in range(rows):
            for j in range(cols):
                left = j * tile_width
                upper = i * tile_height
                right = left + tile_width
                lower = upper + tile_height
                new_img = self.image.crop((left, upper, right, lower))

                # encode the new image and append to image_data
                data = io.BytesIO()
                new_img.save(data, "JPEG")
                img_b64 = base64.b64encode(data.getvalue()).decode("utf-8")
                image_data.append(img_b64)

                new_img.save(f"C:/Users/zikek/Desktop/tiles/tile_{tiles+1}.jpg")
                tiles += 1

        return image_data
