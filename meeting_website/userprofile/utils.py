import random
import string
import requests

from io import BytesIO
from PIL import Image

from meeting_website.settings import MEDIA_ROOT


def watermark_with_transparency(input_image_path, position):
    base_image = Image.open(input_image_path)
    base_image = resize_image(base_image, 600)

    watermark_url = requests.get(
        'https://static.tildacdn.com/tild3064-3830-4666-a536-663731356663/newapptrix_white.png')
    watermark = Image.open(BytesIO(watermark_url.content))
    watermark = resize_image(watermark, 150)

    width, height = base_image.size
    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, position, mask=watermark)

    name = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
    watermarked_image = f'{MEDIA_ROOT / name}.png'
    transparent.save(watermarked_image)

    return watermarked_image


def resize_image(img, width):
    ratio = (width / float(img.size[0]))
    height = int((float(img.size[1]) * float(ratio)))
    return img.resize((width, height), Image.ANTIALIAS)
