import numpy
import os
from io import BytesIO
from core import Log

# Pillow
from PIL import ImageChops, ImageOps, ImageStat
from PIL import Image as ImagePil

# OpenCV
try:
    import cv2
except ImportError:
    pass


class Image(object):
    def __init__(self, pil_image=None, opencv_image=None, raw=None, path=None):
        # init
        self.__opencv = self.__pil = None
        self.__zones = []

        # PIL
        if pil_image:
            self.__pil = pil_image

        elif path:
            self.__pil = ImagePil.open(path)

        elif raw:
            self.__pil = ImagePil.open(BytesIO(raw))

        # OpenCV
        elif opencv_image is not None:
            self.__opencv = opencv_image

        else:
            attr = ('pil_image', 'opencv_image', 'raw', 'path')
            raise AttributeError('%s is required' % ' or '.join(attr))

    def __eq__(self, other_image):
        return self.diff_percent(other_image) <= 1 # jpeg compression

    def add_rectangle_zone(self, x1, y1, x2, y2, name, **kwargs):
        """ Add a rectangle zone in image.

        :param x1: first point x position
        :param y1: first point y position
        :param x2: second point x position
        :param y2: second point y position
        :param name: zone name
        :param kwargs: zone infos dictionary
        """
        return self.add_zone([(x1, y1),(x2, y2)], name, **kwargs)

    def add_zone(self, points, name, **kwargs):
        """ Add a zone in image.

        :param points: list of points (x, y)
        :param name: zone name
        :param kwargs: zone infos dictionary
        """
        self.__zones.append({
            'name': name,
            'points': points,
            'infos': kwargs,
        })
        return self

    def diff_percent(self, other_image):
        """Calculate difference percent.

        :param other_image:
        :return: difference percent.
        """
        img1 = self.get_pil()
        img2 = other_image.get_pil()

        if img1.mode != img2.mode:
            Log.debug('Image diff percent: Different kinds of images.')
            return 100

        if img1.size != img2.size:
            Log.debug('Image diff percent: Different sizes.')
            return 100

        pairs = zip(img1.getdata(), img2.getdata())
        if len(img1.getbands()) == 1:
            dif = sum(abs(p1-p2) for p1,p2 in pairs)  # for gray-scale jpegs
        else:
            dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))

        ncomponents = img1.size[0] * img1.size[1] * 3
        return (dif / 255.0 * 100) / ncomponents

    def get_opencv(self):
        """Get OpenCV image object."""
        if self.__pil:
            return numpy.array(self.__pil)[:, :, ::-1].copy()

        if self.__opencv is not None:
            return self.__opencv

        raise NotImplementedError

    def get_pil(self):
        """Get pil image object."""
        if self.__pil:
            return self.__pil

        if self.__opencv is not None:
            img_array = cv2.cvtColor(self.__opencv , cv2.COLOR_BGR2RGB)
            return ImagePil.fromarray(img_array)

    def save(self, path, **kwargs):
        """Save image on file."""
        dir_path = os.sep.join(path.split(os.sep)[:-1])

        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        self.get_pil().save(path, **kwargs)
        return self

    def greyscale(self):
        """convert the resulting image into greyscale"""
        self.__pil = ImageOps.grayscale(self.get_pil())
        self.__opencv = None
        return self