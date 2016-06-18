import os
from PIL import Image
from PIL import ImageDraw

import settings
from PIL import ImageFont

OPTIMIZATION_WIDTH = 300

class ImageUtils(object):

    @staticmethod
    def save_optimized_image(source_path, dest_path=""):
        if dest_path is "":
            dest_path = source_path

        if not os.path.exists(source_path):
            # Nothing to optimize here :)
            return 0

        initial_size = os.stat(source_path).st_size
        image = Image.open(source_path)


        width_percent = (OPTIMIZATION_WIDTH / float(image.size[0]))
        new_width = OPTIMIZATION_WIDTH
        new_height = int((float(image.size[1]) * float(width_percent)))

        image.thumbnail((new_width, new_height), Image.ANTIALIAS)
        extension = source_path.split(".")[-1]
        if extension == 'jpg':
            image.save(dest_path, optimize=True, quality=90)
        else:
            image.save(dest_path)

        final_size = os.stat(dest_path).st_size
        return initial_size - final_size


