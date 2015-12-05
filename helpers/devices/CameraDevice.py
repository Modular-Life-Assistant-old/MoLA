import time

try:
    from PIL import Image, ImageChops, ImageOps, ImageStat  # Pillow
except:
    import Image, ImageChops, ImageOps, ImageStat
from io import BytesIO

from helpers.devices.BaseDevice import BaseDevice


CAMERA_STREAMING_FLAG   = 1
CAMERA_MOVE_TOP_FLAG    = 2
CAMERA_MOVE_BOTTOM_FLAG = 4
CAMERA_MOVE_RIGHT_FLAG  = 8
CAMERA_MOVE_LEFT_FLAG   = 16
CAMERA_ZOOM_IN_FLAG     = 32
CAMERA_ZOOM_OUT_FLAG    = 64


class CameraDevice(BaseDevice):
    motion_threshold = 6.0
    snapshot_cache = 1  # seconde
    flags = 0
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

        # set flag
        assoc = (
            (self.get_streaming, CAMERA_STREAMING_FLAG),
            (self.move_top, CAMERA_MOVE_TOP_FLAG),
            (self.move_bottom, CAMERA_MOVE_BOTTOM_FLAG),
            (self.move_right, CAMERA_MOVE_RIGHT_FLAG),
            (self.move_left, CAMERA_MOVE_LEFT_FLAG),
            (self.zoom_in, CAMERA_ZOOM_IN_FLAG),
            (self.zoom_out, CAMERA_ZOOM_OUT_FLAG),
        )
        for handler, flag in assoc:
            print(handler.__name__, len(handler.__code__.co_code))
            if len(handler.__code__.co_code) > 4: # handler has implemented ?
                self.flags |= flag

        print(self.flags)

    def get_snapshot(self):
        """Get an snapshot"""
        if self.snapshot_cache < time.time() - self.__snapshot_timestamp:
            self.make_snapshot()

        return self.__snapshot

    def get_streaming(self):
        """Use camera to make a snapshot"""
        pass

    def has_move_bottom(self):
        """Camera can move to down?"""
        return self.flags & CAMERA_MOVE_BOTTOM_FLAG

    def has_move_left(self):
        """Camera can move to left?"""
        return self.flags & CAMERA_MOVE_LEFT_FLAG

    def has_move_right(self):
        """Camera can move to right?"""
        return self.flags & CAMERA_MOVE_RIGHT_FLAG

    def has_move_top(self):
        """Camera can move to up?"""
        return self.flags & CAMERA_MOVE_TOP_FLAG

    def has_streaming(self):
        """Camera can stream?"""
        return self.flags & CAMERA_STREAMING_FLAG

    def has_zoom_in(self):
        """Camera can zoom in?"""
        return self.flags & CAMERA_ZOOM_IN_FLAG

    def has_zoom_out(self):
        """Camera can zoom out?"""
        return self.flags & CAMERA_ZOOM_OUT_FLAG

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

    def get_motion_detection_score(self, image1, image2):
        # get the difference between the two images
        image_diff = ImageChops.difference(image1, image2)
        # convert the resulting image into greyscale
        image_diff = ImageOps.grayscale(image_diff)
        # find the medium value of the grey pixels
        image_stat = ImageStat.Stat(image_diff)
        return image_stat.mean[0]

    def _make_snapshot_done(self, result):
        """Process after make_snapshot method"""

        if not result:
            return

        image = Image.open(BytesIO(result))

        # motion detection check
        if self.__snapshot:
            score = self.get_motion_detection_score(image, self.__snapshot)
            if score > self.motion_threshold:
                event = self.fire('motion_detection', new=image,
                                  old=self.__snapshot, device=self, score=score)
                self.fire('analyse_image', image=image, device=self, parent=event)

        self.__snapshot_timestamp = time.time()
        self.__snapshot = image
        return image
