import os
import cv2
from helpers.objects.Image import Image

try:
    from PIL import Image as ImagePil  # Pillow
except:
    import Image as ImagePil


TEST_IMAGE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'test.jpg')


def test_image_cast():
    """cast image check"""
    img = Image(path=TEST_IMAGE_PATH)
    cast_img = Image(path=TEST_IMAGE_PATH)

    # cast loop
    for _ in range(10):
        cast_img = Image(opencv_image=cast_img.get_opencv())
        cast_img = Image(pil_image=cast_img.get_pil())

    assert img == cast_img


def test_image_empty_parameter():
    try:
        Image()
        assert False, 'no raise (empty parameter)'
    except:
        pass


def test_image_from_opencv():
    """load image from OpenCV object check"""
    img1 = Image(path=TEST_IMAGE_PATH)
    img2 = Image(opencv_image=cv2.imread(TEST_IMAGE_PATH))
    assert img1.diff_percent(img2) == 0
    assert img1 == img2


def test_image_from_pil():
    """load image from PIL object check"""
    img1 = Image(path=TEST_IMAGE_PATH)
    img2 = Image(pil_image=ImagePil.open(TEST_IMAGE_PATH))
    assert img1.diff_percent(img2) == 0
    assert img1 == img2


def test_image_from_row():
    """load image from raw string check"""
    with open(TEST_IMAGE_PATH, 'rb') as f:
        raw = f.read()

    img1 = Image(path=TEST_IMAGE_PATH)
    img2 = Image(raw=raw)
    assert img1.diff_percent(img2) == 0
    assert img1 == img2


def test_image_diff_percent():
    """different_percent method check"""
    img = Image(path=TEST_IMAGE_PATH)

    assert img.diff_percent(img) == 0
    assert img == img

    img2 = Image(path=TEST_IMAGE_PATH).greyscale()
    assert img.diff_percent(img2) == 100
    assert img != img2


def test_image_save():
    """save image check"""
    path_save = '/tmp/MoLA_test/test.jpg'

    img = Image(path=TEST_IMAGE_PATH)
    img.save(path_save, quality=100)

    assert Image(path=path_save) == img
