from datetime import datetime

import numpy as np
import pytest
from aspose.psd import FontSettings, Image
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.psd import PsdImage, CompressionMethod
from aspose.psd.fileformats.psd.layers import ShapeLayer, TextLayer
from aspose.psd.fileformats.psd.layers.layerresources import BaseArtboardInfoResource, AbddResource, ArtBResource, ArtDResource, LyvrResource
from aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures import IntegerStructure, StringStructure
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_24_09_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # [AI Format] Replace standard rendering with APS conversion to reduce file loading speed
    # https://issue.saltov.dynabic.com/issues/PSDNET-2119
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-95
    def PSDNET2119Test(self):
        sourceFile = self.GetFileInBaseFolder("patternstokOnePage.ai")
        start = datetime.now()

        with AiImage.load(sourceFile) as image:
            end = datetime.now()
            if (end - start).seconds > 18:
                raise Exception("The file loading time is too long.")

    # Support of artb/artd/abdd/lyvr resources for Artboard
    # https://issue.saltov.dynabic.com/issues/PSDNET-407
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-96
    def PSDNET407Test(self):
        srcFile = self.GetFileInBaseFolder("artboard1.psd")

        with PsdImage.load(srcFile) as image:
            psdImage = cast(PsdImage, image)
            artDResource = cast(ArtDResource, psdImage.global_layer_resources[2])
            artBResource1 = cast(ArtBResource, psdImage.layers[2].resources[7])
            artBResource2 = cast(ArtBResource, psdImage.layers[5].resources[7])
            lyvrResource1 = cast(LyvrResource, psdImage.layers[2].resources[9])
            lyvrResource2 = cast(LyvrResource, psdImage.layers[5].resources[9])

            countStruct = cast(IntegerStructure, artDResource.items[0])
            assert countStruct.value == 2

            presetNameStruct1 = cast(StringStructure, artBResource1.items[2])
            assert presetNameStruct1.value == "iPhone X\x00"


            presetNameStruct2 = cast(StringStructure, artBResource2.items[2])
            assert presetNameStruct2.value == "iPhone X\x00"

            assert lyvrResource1.version == 160
            assert lyvrResource2.version == 160

    # Fix detection of Fill layer
    # https://issue.saltov.dynabic.com/issues/PSDNET-1839
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-97
    def PSDNET1839Test(self):
        inputFile = self.GetFileInBaseFolder("FillLayer_ShapeLayer.psd")

        with PsdImage.load(inputFile) as img:
            image = cast(PsdImage, img)
            shapeLayer0 = cast(ShapeLayer, image.layers[0])
            shapeLayer1 = cast(ShapeLayer, image.layers[1])
            shapeLayer2 = cast(ShapeLayer, image.layers[2])
            shapeLayer3 = cast(ShapeLayer, image.layers[3])
            shapeLayer4 = cast(ShapeLayer, image.layers[4])
            shapeLayer8 = cast(ShapeLayer, image.layers[8])
            shapeLayer9 = cast(ShapeLayer, image.layers[9])

            assert shapeLayer0 is not None
            assert shapeLayer1 is not None
            assert shapeLayer2 is not None
            assert shapeLayer3 is not None
            assert shapeLayer4 is not None
            assert shapeLayer8 is not None
            assert shapeLayer9 is not None

    # IndexOutOfRangeException on the updating of TextLayer
    # https://issue.saltov.dynabic.com/issues/PSDNET-2071
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-98
    def PSDNET2071Test(self):
        fontsFolder = self.GetFileInBaseFolder("Fonts")

        FontSettings.set_fonts_folders([fontsFolder], True)

        # Inits fonts loading to check if an exception is thrown
        FontSettings.get_adobe_font_name("none")

    # Long opening of AI file
    # https://issue.saltov.dynabic.com/issues/PSDNET-2101
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-99
    def PSDNET2101Test(self):
        sourceFile = self.GetFileInBaseFolder("choco-kopiya-5_1FfIn55h.ai")

        start = datetime.now()

        with AiImage.load(sourceFile) as image:
            end = datetime.now()
            if (end - start).seconds > 18:
                raise Exception("The file loading time is too long.")

    # Failed to load FillLayer from Embedded resource stream for Performance report
    # https://issue.saltov.dynabic.com/issues/PSDNET-2156
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-100
    def PSDNET2156Test(self):
        srcFile = self.GetFileInBaseFolder("FillLayersTest.psd")

        with open(srcFile, "rb", buffering=0) as fileStream:
        #with File.open_read(srcFile) as fileStream:
            with Image.load(fileStream) as image:
                # No exception to be thrown here
                pass

    # Exception on reading invalid color value
    # https://issue.saltov.dynabic.com/issues/PSDNET-2166
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-101
    def PSDNET2166Test(self):
        srcFile = self.GetFileInBaseFolder("Layer123Problem.psd")

        with Image.load(srcFile) as img:
            psdImage = cast(PsdImage, img)
            textLayer = cast(TextLayer, psdImage.layers[0])
            # Here should be no exception
            textData = textLayer.text_data

    # Starting with Aspose.PSD 24.7.0 issue with the particular document when iterating through Layers: Index was out of range
    # https://issue.saltov.dynabic.com/issues/PSDNET-2176
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-104
    def PSDNET2176Test(self):
        srcFile = self.GetFileInBaseFolder("2176.psd")

        with Image.load(srcFile) as img:
            psdImage = cast(PsdImage, img)
            textLayer = cast(TextLayer, psdImage.layers[100])
            # Here should be no exception
            textData = textLayer.text_data