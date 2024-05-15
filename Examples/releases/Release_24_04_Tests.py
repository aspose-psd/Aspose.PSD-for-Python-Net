import time
import uuid

import psutil
import pytest
from aspose.psd import Image, FontSettings, FileFormat, Rectangle, Color, PointF, Point
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.core.vectorpaths import BezierKnotRecord
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage, ColorModes, CompressionMethod
from aspose.psd.fileformats.psd.layers import ShapeLayer
from aspose.psd.fileformats.psd.layers.filllayers import FillLayer
from aspose.psd.fileformats.psd.layers.layereffects import StrokePosition
from aspose.psd.fileformats.psd.layers.layerresources import PattResource, Lr16Resource, Lr32Resource, PathShape
from aspose.psd.fileformats.psd.layers.layerresources.strokeresources import LineCapType, LineJoinType
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import cast, as_of

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper


class Release_24_04_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # [AI Format] Add XObjectForm resource handling
    # https://issue.saltov.dynabic.com/issues/PSDNET-1871
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-50
    def PSDNET1871Test(self):
        sourceFileName = self.GetFileInBaseFolder("example.ai")
        ethalonFilePath = self.GetFileInBaseFolder("example.png")
        outputFilePath = self.GetFileInOutputFolder("example_output.png")

        with AiImage.load(sourceFileName) as image:
            image.save(outputFilePath, PngOptions())

        Comparison.CheckAgainstEthalon(outputFilePath, ethalonFilePath, 20, 40)


    # Fix conversion of Psd file from RGB to CMYK
    # https://issue.saltov.dynabic.com/issues/PSDNET-1879
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-52
    def PSDNET1879Test(self):
        sourceFile = self.GetFileInBaseFolder("frog_nosymb.psd")
        ethalonFilePath = self.GetFileInBaseFolder("frog_nosymb_output.psd")
        outputFile = self.GetFileInOutputFolder("frog_nosymb_output.psd")

        with PsdImage.load(sourceFile) as image:
            psdImage = cast(PsdImage, image)
            psdImage.has_transparency_data = False

            psdOptions = PsdOptions(psdImage)
            psdOptions.color_mode = ColorModes.CMYK
            psdOptions.compression_method = CompressionMethod.RLE
            psdOptions.channels_count = 4

            psdImage.save(outputFile, psdOptions)

        with PsdImage.load(outputFile) as image:
            psdImage = cast(PsdImage, image)
            assert not psdImage.has_transparency_data
            assert psdImage.layers[0].channels_count == 4

        def assert_are_equal(expected, actual, message=None):
            if expected != actual:
                raise Exception(message or "Objects are not equal.")

        Comparison.CheckAgainstEthalon(outputFile, ethalonFilePath, 0, 1)



    # Add Constructor for the ShapeLayer.
    # https://issue.saltov.dynabic.com/issues/PSDNET-1961
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-51
    def PSDNET1961Test(self):
        ethalonFilePath = self.GetFileInBaseFolder("AddShapeLayer_output.psd")
        outputFile = self.GetFileInOutputFolder("AddShapeLayer_output.psd")

        with PsdImage(600, 400) as newPsd:
            shapeLayer = newPsd.add_shape_layer()

            newShape = Release_24_04_Tests.generate_new_shape(newPsd.size)
            newShapes = [newShape]
            shapeLayer.path.set_items(newShapes)

            shapeLayer.update()

            newPsd.save(outputFile)

        with PsdImage.load(outputFile) as img:
            image = cast(PsdImage, img)
            assert len(image.layers) == 2

            shapeLayer = cast(ShapeLayer, image.layers[1])
            internalFill = shapeLayer.fill
            strokeSettings = shapeLayer.stroke
            strokeFill = shapeLayer.stroke.fill

            assert len(shapeLayer.path.get_items()) == 1
            assert len(shapeLayer.path.get_items()[0].get_items()) == 3

            assert internalFill.color.to_argb() == -16127182

            assert strokeSettings.size == 7.41
            assert not strokeSettings.enabled
            assert strokeSettings.line_alignment == StrokePosition.CENTER
            assert strokeSettings.line_cap == LineCapType.BUTT_CAP
            assert strokeSettings.line_join == LineJoinType.MITER_JOIN
            assert strokeFill.color.to_argb() == -16777216

    def generate_new_shape(imageSize):
        newShape = PathShape()

        point1 = PointF(20, 100)
        point2 = PointF(200, 100)
        point3 = PointF(300, 10)

        knot1 = BezierKnotRecord()
        knot1.is_linked = True
        knot1.points = [
                    Release_24_04_Tests.PointFToResourcePoint(point1, imageSize),
                    Release_24_04_Tests.PointFToResourcePoint(point1, imageSize),
                    Release_24_04_Tests.PointFToResourcePoint(point1, imageSize)
                ]

        knot2 = BezierKnotRecord()
        knot2.is_linked = True
        knot2.points = [
                    Release_24_04_Tests.PointFToResourcePoint(point2, imageSize),
                    Release_24_04_Tests.PointFToResourcePoint(point2, imageSize),
                    Release_24_04_Tests.PointFToResourcePoint(point2, imageSize)
                ]

        knot3 = BezierKnotRecord()
        knot3.is_linked = True
        knot3.points = [
                    Release_24_04_Tests.PointFToResourcePoint(point3, imageSize),
                    Release_24_04_Tests.PointFToResourcePoint(point3, imageSize),
                    Release_24_04_Tests.PointFToResourcePoint(point3, imageSize)
                ]

        bezierKnots = [
            knot1,
            knot2,
            knot3
        ]

        newShape.set_items(bezierKnots)

        return newShape


    # Specific PSD file can not be exported using Aspose.PSD
    # https://issue.saltov.dynabic.com/issues/PSDNET-1966
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-53
    def PSDNET1966Test(self):
        sourceFile = self.GetFileInBaseFolder("1966source.psd")
        refenceFile = self.GetFileInBaseFolder("output.png")
        outputPng =self.GetFileInOutputFolder("output.png")

        loadOpt = PsdLoadOptions()
        loadOpt.load_effects_resource = True

        with PsdImage.load(sourceFile, loadOpt) as psdImage:
            psdImage.save(outputPng, PngOptions())

        Comparison.CheckAgainstEthalon(outputPng, refenceFile, 0, 1)

    def PointFToResourcePoint(point, imageSize):
        ImgToPsdRatio = 256 * 65535
        return Point(
            int(round(point.y * (ImgToPsdRatio / imageSize.height))),
            int(round(point.x * (ImgToPsdRatio / imageSize.width)))
        )

    def assert_are_equal(expected, actual, message=None):
        if expected != actual:
            raise Exception(message or "Objects are not equal.")