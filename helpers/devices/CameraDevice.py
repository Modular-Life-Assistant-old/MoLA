import time

try:
    from PIL import Image, ImageChops, ImageOps, ImageStat  # Pillow
except:
    import Image, ImageChops, ImageOps, ImageStat
from io import BytesIO

from helpers.devices.BaseDevice import BaseDevice


class CameraDevice(BaseDevice):
    motion_threshold = 6.0
    snapshot_cache = 1  # seconde
    __snapshot = None
    __snapshot_timestamp = None

    def __init__(self, *args, **kwargs):
        super(CameraDevice, self).__init__(*args, **kwargs)

        # bind snapshot_decorator to _make_snapshot_done with decorator
        def make_snapshot_decorator(make_snapshot):
            def inner():
                return self._make_snapshot_done(make_snapshot())

            return inner

        self.make_snapshot = make_snapshot_decorator(self.make_snapshot)

    def get_snapshot(self):
        """Get an snapshot"""
        if self.snapshot_cache < time.time() - self.__snapshot_timestamp:
            self.make_snapshot()

        return self.__snapshot

    def make_snapshot(self):
        """Use camera to make a snapshot"""
        pass

    def move_bottom(self):
        """Move camera to down"""
        pass

    def move_left(self):
        """Move camera to left"""
        pass

    def move_right(self):
        """Move camera to right"""
        pass

    def move_top(self):
        """Move camera to up"""
        pass

    def update(self):
        """This device update."""
        self.make_snapshot()

    def zoom_in(self):
        """Increase zoom"""
        pass

    def zoom_out(self):
        """Decrease zoom"""
        pass

    def _make_snapshot_done(self, result):
        """Process after make_snapshot method"""

        if not result:
            return

        image = Image.open(BytesIO(result))

        # motion detection check
        if self.__snapshot:
            score = self.get_motion_detection_score(image, self.__snapshot)
            if score > self.motion_threshold:
                self.fire('motion_detection', new=image, old=self.__snapshot,
                          device=self, score=score)

        self.__snapshot_timestamp = time.time()
        self.__snapshot = image
        return image

    def get_motion_detection_score(self, image1, image2):
        # get the difference between the two images
        image_diff = ImageChops.difference(image1, image2)
        # convert the resulting image into greyscale
        image_diff = ImageOps.grayscale(image_diff)
        # find the medium value of the grey pixels
        image_stat = ImageStat.Stat(image_diff)
        return image_stat.mean[0]
