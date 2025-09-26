import io
from contextlib import redirect_stdout
from pathlib import Path

import ovito
import pytest
from ovito.qt_compat import QtGui
from ovito.vis import TachyonRenderer


def image_comperator(img1: QtGui.QImage, img2: QtGui.QImage):
    color_threshold = 6

    if img1.isNull():
        return False
    if img2.isNull():
        return False
    if img1.format() != img2.format():
        return False
    if img1.width() != img2.width():
        return False
    if img1.height() != img2.height():
        return False

    deviation_count = 0
    for y in range(img1.height()):
        for x in range(img1.width()):
            c1 = img1.pixelColor(x, y)
            c2 = img2.pixelColor(x, y)
            rgba1 = (c1.red(), c1.green(), c1.blue(), c1.alpha())
            rgba2 = (c2.red(), c2.green(), c2.blue(), c2.alpha())
            if (
                abs(rgba1[0] - rgba2[0]) > color_threshold
                or abs(rgba1[1] - rgba2[1]) > color_threshold
                or abs(rgba1[2] - rgba2[2]) > color_threshold
                or abs(rgba1[3] - rgba2[3]) > color_threshold
            ):
                deviation_count += 1
    deviation_rate = deviation_count / (img1.width() * img1.height())
    return deviation_rate


@pytest.fixture
def get_rendered_image():
    scene = ovito.scene
    scene.load(str(Path("tests", "test.ovito")))
    settings = ovito.scene.render_settings
    renderer = TachyonRenderer(direct_light_intensity=0.6)
    settings.renderer = renderer
    if not settings.render_all_viewports:
        viewport_layout = [(scene.viewports.active_vp, (0.0, 0.0, 1.0, 1.0))]
    else:
        viewport_layout = scene.viewports.get_viewport_rectangles()
    with redirect_stdout(io.StringIO()):
        frame_buffer = settings.render_scene(scene.anim, viewport_layout)

    frame_buffer.image.save(str(Path("tests", "img.png")))
    yield frame_buffer.image


@pytest.fixture
def get_ref_img():
    return QtGui.QImage(str(Path("tests", "reference.png")))


def test_rendered_image(get_rendered_image, get_ref_img):
    max_deviation_rate = 0.15 * 1e-2
    deviation_rate = image_comperator(get_rendered_image, get_ref_img)
    assert deviation_rate < max_deviation_rate
