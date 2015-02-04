import logging
import os
import cStringIO
import numpy as np
from PIL import Image, ImageDraw, ImageOps

from django.http import HttpResponse
from django.conf import settings
from django.templatetags.static import static


def player_icon(request):
    width = request.GET.get('width', None)
    height = request.GET.get('height', None)
    color = request.GET.get('color', 'FFCCCC')

    logging.info(os.path.join(settings.STATIC_ROOT, 'img/arrow-128.png'))
    original = Image.open(os.path.join(settings.STATIC_ROOT, 'img/arrow-128.png'))
    original = original.convert('RGBA')


    if width is None and height is None:
        width, height = original.size
    elif width is None and height:
        width = original.size[0]
    elif width and height is None:
        height = original.size[1]

    height = int(height)
    width = int(width)
    aspect = float(width) / float(height)

    data = np.array(original)   # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    black_areas = (red == 0) & (blue == 0) & (green == 0)
    logging.info(tuple(ord(c) for c in color.decode('hex')))
    data[..., :-1][black_areas] = tuple(ord(c) for c in color.decode('hex'))

    icon = Image.fromarray(data)

    icon = icon.resize((int(width), int(height)), Image.ANTIALIAS)

    response = HttpResponse(content_type="image/png")
    icon.save(response, "PNG")
    return response