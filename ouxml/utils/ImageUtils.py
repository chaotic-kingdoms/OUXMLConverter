import os
from PIL import Image
from PIL import ImageDraw

import settings
from PIL import ImageFont

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


        width_percent = (settings.IMG_OPTIMIZED_WIDTH / float(image.size[0]))
        new_width = settings.IMG_OPTIMIZED_WIDTH
        new_height = int((float(image.size[1]) * float(width_percent)))

        image.thumbnail((new_width, new_height), Image.ANTIALIAS)
        extension = source_path.split(".")[-1]
        try:
            if extension == 'jpg':
                image.save(dest_path, optimize=True, quality=90)
            else:
                image.save(dest_path)
        except IOError as e:
            print "Error optimizing image"
            print e

        final_size = os.stat(dest_path).st_size
        return initial_size - final_size

    @staticmethod
    def generate_glossary_thumbnail(chars_title, dest_path, drop_shadow=True):

        text_pos = settings.GLOSSARY_TEXT_MARGIN
        x_pad = settings.GLOSSARY_TEXT_HORIZONTAL_PAD
        if len(chars_title) == 1:
            x_pad *= 4
        bgcolor = settings.GLOSSARY_BACKGROUND

        font = ImageFont.truetype(settings.GLOSSARY_THUMB_FONT, size=settings.GLOSSARY_TEXT_FONTSIZE)
        image = Image.new('RGBA', settings.GLOSSARY_THUMB_SIZE, color=bgcolor)
        draw = ImageDraw.Draw(image)

        if drop_shadow:
            shadow_color = bgcolor[0] - 20, bgcolor[1] - 20, bgcolor[2] - 20
            for pos in range(text_pos, image.height):
                draw.text((pos+x_pad,pos), chars_title, fill=shadow_color, font=font)

        draw.text((text_pos+x_pad,text_pos), chars_title, fill=settings.GLOSSARY_FOREGROUND, font=font)
        image.save(dest_path, optimize=True, quality=90)
