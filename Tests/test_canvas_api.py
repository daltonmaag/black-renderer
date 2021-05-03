import pathlib
import pytest
from fontTools.misc.transform import Identity
from fontTools.ttLib.tables.otTables import ExtendMode
from blackrenderer.backends import getSurface


testDir = pathlib.Path(__file__).resolve().parent
dataDir = testDir / "data"
tmpOutputDir = testDir / "tmpOutput"
if not tmpOutputDir.exists():
    tmpOutputDir.mkdir()


backends = [
    (name, getSurface(name)) for name in ["cairo", "coregraphics", "skia", "svg"]
]
backends = [(name, surface) for name, surface in backends if surface is not None]


test_colorStops = [
    (0, 1),
]

test_extendModes = [ExtendMode.PAD, ExtendMode.REPEAT, ExtendMode.REFLECT]


@pytest.mark.parametrize("stopOffsets", test_colorStops)
@pytest.mark.parametrize("extend", test_extendModes)
@pytest.mark.parametrize("backendName, surfaceFactory", backends)
def test_colorStops(backendName, surfaceFactory, stopOffsets, extend):
    surface = surfaceFactory(0, 0, 600, 100)
    canvas = surface.canvas
    point1 = (200, 0)
    point2 = (400, 0)
    color1 = (1, 0, 0, 1)
    color2 = (0, 0, 1, 1)
    stop1, stop2 = stopOffsets
    colorLine = [(stop1, color1), (stop2, color2)]
    canvas.drawRectLinearGradient(
        (0, 0, 600, 100), colorLine, point1, point2, extend, Identity
    )

    for pos in [200, 400]:
        canvas.drawRectSolid((pos, 0, 1, 100), (0, 0, 0, 1))

    ext = surface.fileExtension
    stopsString = "_".join(str(s) for s in stopOffsets)
    surface.saveImage(
        tmpOutputDir / f"colorStops_{extend.name}_{stopsString}_{backendName}{ext}"
    )


@pytest.mark.parametrize("extend", test_extendModes)
@pytest.mark.parametrize("backendName, surfaceFactory", backends)
def test_sweepGradient(backendName, surfaceFactory, extend):
    surface = surfaceFactory(0, 0, 200, 200)
    canvas = surface.canvas
    center = (100, 100)
    startAngle = 45
    endAngle = 315
    color1 = (1, 0, 0, 1)
    color2 = (0, 0, 1, 1)
    stopOffsets = [0, 1]
    stop1, stop2 = stopOffsets
    colorLine = [(stop1, color1), (stop2, color2)]
    canvas.drawRectSweepGradient(
        (0, 0, 200, 200), colorLine, center, startAngle, endAngle, extend, Identity
    )

    ext = surface.fileExtension
    stopsString = "_".join(str(s) for s in stopOffsets)
    surface.saveImage(
        tmpOutputDir / f"sweepGradient_{extend.name}_{stopsString}_{backendName}{ext}"
    )