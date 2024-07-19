import ctypes
import struct
import time
import uuid
from ctypes import c_long, c_int, c_int32
import numpy as np


import psutil
import pytest
from aspose.psd import Image, FontSettings, FileFormat, Rectangle, Color, PointF, Point, PixelDataFormat
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.core.vectorpaths import BezierKnotRecord
from aspose.psd.fileformats.pdf import PdfCoreOptions
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage, ColorModes, CompressionMethod
from aspose.psd.fileformats.psd.core.rawcolor import RawColor
from aspose.psd.fileformats.psd.layers import ShapeLayer, TextLayer
from aspose.psd.fileformats.psd.layers.filllayers import FillLayer
from aspose.psd.fileformats.psd.layers.layereffects import StrokePosition
from aspose.psd.fileformats.psd.layers.layerresources import PattResource, Lr16Resource, Lr32Resource, PathShape
from aspose.psd.fileformats.psd.layers.layerresources.strokeresources import LineCapType, LineJoinType
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions, PdfOptions
from aspose.pycore import cast, as_of, is_assignable

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper


class Release_24_05_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Semi transparency is processed wrong on the psd file preview
    # https://issue.saltov.dynabic.com/issues/PSDNET-1755
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-50
    def PSDNET1755Test(self):
        sourceFile = self.GetFileInBaseFolder("frog_nosymb.psd")
        outputFile = self.GetFileInOutputFolder("frog_nosymb_backgroundcontents_output.psd")
        referenceFile = self.GetFileInBaseFolder("frog_nosymb_backgroundcontents_output.psd")

        with PsdImage.load(sourceFile) as psdImage:

            backgroundColor = RawColor(PixelDataFormat.rgb_32_bpp, 0)

            argbValue = ctypes.c_int32(255 << 24 | 255 << 16 | 255 << 8 | 255).value

            backgroundColor.set_as_int(argbValue)  # White

            psdOptions = PsdOptions(psdImage)
            psdOptions.color_mode = ColorModes.RGB
            psdOptions.compression_method = CompressionMethod.RLE
            psdOptions.channels_count = 4
            psdOptions.background_contents = backgroundColor

            psdImage.save(outputFile, psdOptions)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)


    # [AI Format] Add support for handling AI Files with EPSF header.
    # https://issue.saltov.dynabic.com/issues/PSDNET-1897
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-60
    def PSDNET1897Test(self):
        sourceFile = self.GetFileInBaseFolder("example.ai")
        outputFilePath = self.GetFileInOutputFolder("example.png")
        referenceFile = self.GetFileInBaseFolder("example.png")

        def assert_are_equal(expected, actual):
            if expected != actual:
                raise Exception("Objects are not equal.")

        with AiImage.load(sourceFile) as img:
            image = cast(AiImage, img)
            assert_are_equal(len(image.layers), 2)
            assert_are_equal(image.layers[0].has_multi_layer_masks, False)
            assert_are_equal(image.layers[0].color_index, -1)
            assert_are_equal(image.layers[1].has_multi_layer_masks, False)
            assert_are_equal(image.layers[1].color_index, -1)

            image.save(outputFilePath, PngOptions())

        Comparison.CheckAgainstEthalon(outputFilePath, referenceFile, 0, 1)

    ImgToPsdRatio = 256 * 65535

    def PointFToResourcePoint(point, imageSize):
        return Point(
            round(point.y * (Release_24_05_Tests.ImgToPsdRatio / imageSize.height)),
            round(point.x * (Release_24_05_Tests.ImgToPsdRatio / imageSize.width))
        )

    def assert_are_equal(expected, actual, message=None):
        if expected != actual:
            raise Exception(message or "Objects are not equal.")

    # Rendering of Shape Layer Partially incorrect
    # https://issue.saltov.dynabic.com/issues/PSDNET-1942
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-61
    def PSDNET1942Test(self):
        sourceFile = self.GetFileInBaseFolder("ShapeLayerTest.psd")
        outputFile = self.GetFileInOutputFolder("ShapeLayerTest_output.psd")
        referenceFile = self.GetFileInBaseFolder("ShapeLayerTest_output.psd")

        with PsdImage.load(sourceFile) as image:
            im = cast(PsdImage, image)
            shapeLayer = cast(ShapeLayer, im.layers[2])
            path = shapeLayer.path
            pathShapes = path.get_items()
            knotsList = []
            for pathShape in pathShapes:
                knots = pathShape.get_items()
                knotsList.extend(knots)

            newShape = PathShape()

            bezierKnot1 = BezierKnotRecord()
            bezierKnot1.is_linked=True
            bezierKnot1.points=[
                    Release_24_05_Tests.PointFToResourcePoint(PointF(100, 100), shapeLayer.container.size),
                    Release_24_05_Tests.PointFToResourcePoint(PointF(100, 100), shapeLayer.container.size),
                    Release_24_05_Tests.PointFToResourcePoint(PointF(100, 100), shapeLayer.container.size)
                ]

            bezierKnot2 = BezierKnotRecord()
            bezierKnot2.is_linked=True
            bezierKnot2.points=[
                    Release_24_05_Tests.PointFToResourcePoint(PointF(50, 490), shapeLayer.container.size),
                    Release_24_05_Tests.PointFToResourcePoint(PointF(100, 490), shapeLayer.container.size),
                    Release_24_05_Tests.PointFToResourcePoint(PointF(150, 490), shapeLayer.container.size)
                ]

            bezierKnot3 = BezierKnotRecord()
            bezierKnot3.is_linked=True
            bezierKnot3.points=[
                    Release_24_05_Tests.PointFToResourcePoint(PointF(490, 150), shapeLayer.container.size),
                    Release_24_05_Tests.PointFToResourcePoint(PointF(490, 50), shapeLayer.container.size),
                    Release_24_05_Tests.PointFToResourcePoint(PointF(490, 20), shapeLayer.container.size)
                ]

            bezierKnots = [
                bezierKnot1,
                bezierKnot2,
                bezierKnot3
            ]

            newShape.set_items(bezierKnots)

            newShapes = list(pathShapes)
            newShapes.append(newShape)

            pathShapeNew = newShapes
            path.set_items(pathShapeNew)

            shapeLayer.update()

            im.save(outputFile, PsdOptions())

        with PsdImage.load(outputFile) as image:
            im = cast(PsdImage, image)
            shapeLayer = cast(ShapeLayer, im.layers[2])
            path = shapeLayer.path
            pathShapes = path.get_items()
            knotsList = []
            for pathShape in pathShapes:
                knots = pathShape.get_items()
                knotsList.extend(knots)

            assert len(pathShapes) == 3
            assert shapeLayer.left == 42
            assert shapeLayer.top == 14
            assert shapeLayer.bounds.width == 1600
            assert shapeLayer.bounds.height == 1086

        Comparison.CheckAgainstEthalon(sourceFile, referenceFile, 0, 1)

    # Exception whenever saving PSD files with size more than 200 MB and large dimensions
    # https://issue.saltov.dynabic.com/issues/PSDNET-1957
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-62
    def PSDNET1957Test(self):
        sourceFile = self.GetFileInBaseFolder("bigfile.psd")
        outputFile = self.GetFileInOutputFolder("output_raw.psd")
        referenceFile = self.GetFileInBaseFolder("output_raw.psd")

        loadOptions = PsdLoadOptions()
        loadOptions.load_effects_resource = True
        loadOptions.use_disk_for_load_effects_resource = True

        with PsdImage.load(sourceFile, loadOptions) as psdImage:
            opt = PsdOptions()
            opt.compression_method = CompressionMethod.RLE
            psdImage.save(outputFile, opt)

        Comparison.CheckAgainstEthalon(sourceFile, referenceFile, 0, 1)

        self.remove_all_unzipped_files()


    # Image saving failed exception when saving to PDF after update from 23.7 to 24.3
    # https://issue.saltov.dynabic.com/issues/PSDNET-1998
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-63
    def PSDNET1998Test(self):
        sourceFile = self.GetFileInBaseFolder("CVFlor.psd")
        outputFile = self.GetFileInOutputFolder("_export.pdf")

        with PsdImage.load(sourceFile) as psdImage:
            saveOptions = PdfOptions()
            saveOptions.pdf_core_options = PdfCoreOptions()

            psdImage.save(outputFile, saveOptions)

    # Fix the issue in GetFontInfoRecords method for the Chinese Fonts
    # https://issue.saltov.dynabic.com/issues/PSDNET-2033
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-64
    def PSDNET2033Test(self):
        fontFolder = self.GetFileInBaseFolder("Font")
        sourceFile = self.GetFileInBaseFolder("bd-worlds-best-pink.psd")

        psdLoadOptions = PsdLoadOptions()
        psdLoadOptions.load_effects_resource = True
        psdLoadOptions.allow_warp_repaint = True

        try:
            FontSettings.set_fonts_folders([fontFolder], True)
            FontSettings.update_fonts()

            with PsdImage.load(sourceFile, psdLoadOptions) as img:
                image = cast(PsdImage, img)
                for layer in image.layers:
                    if is_assignable(layer, TextLayer):
                        textLayer = cast(TextLayer, layer)
                        if textLayer.text == "best":
                            # Without this fix here will be exception because of Chinese font.
                            textLayer.update_text("SUCCESS")
        finally:
            FontSettings.reset()
            FontSettings.update_fonts()