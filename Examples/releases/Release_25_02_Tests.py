from datetime import datetime

import numpy as np
import pytest
from aspose.psd import Color
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers import ShapeLayer, Layer
from aspose.psd.fileformats.psd.layers.fillsettings import GradientFillSettings, IGradientFillSettings
from aspose.psd.fileformats.psd.layers.layereffects import StrokeEffect
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import cast, as_of, is_assignable

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper
class Release_25_02_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Saving of PSB Files with size more than 2Gb
    # https://issue.saltov.dynabic.com/issues/PSDNET-2344
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-153
    def PSDNET2344Test(self):
        outputFilePng = self.GetFileInOutputFolder("bigpsd.psd")

        with PsdImage(25000, 15000) as psdImage:
            newLayers = [None] * 2
            for lindex in range(2):
                layer = Layer()

                layer.left = 0
                layer.top = 0
                layer.right = psdImage.width
                layer.bottom = psdImage.height
                layer.display_name = "layer1"

                pixels = [int] * layer.width * layer.height;

                cols = [Color.red.to_argb(),Color.red.to_argb(),Color.red.to_argb(),Color.red.to_argb(),Color.red.to_argb(),
                        Color.aquamarine.to_argb(), Color.aquamarine.to_argb()]

                for i in range(len(pixels)):
                    modul = i % 7
                    pixels[i] = cols[modul]

                layer.save_argb_32_pixels(layer.bounds, pixels)
                newLayers[lindex] = layer

            psdImage.layers = newLayers
            psdImage.save(outputFilePng, PsdOptions())

    # Implement handling of Noise gradient in Layer Effects
    # https://issue.saltov.dynabic.com/issues/PSDNET-2243
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-154
    def PSDNET2243Test(self):
        inputFile = self.GetFileInBaseFolder("Stroke.psd")
        outputFile = self.GetFileInOutputFolder("output_Stroke.psd")
        reference =  self.GetFileInBaseFolder("output_Stroke.psd")

        loadOptions = PsdLoadOptions()
        loadOptions.load_effects_resource = True

        with PsdImage.load(inputFile, loadOptions) as img:
            image = cast(PsdImage, img)
            layerEffect = cast(StrokeEffect, image.layers[1].blending_options.effects[0])
            settings = cast(IGradientFillSettings, layerEffect.fill_settings)

            assert settings is not None

            newFillSettings = GradientFillSettings()
            newFillSettings.angle = 35
            layerEffect.fill_settings = newFillSettings

            image.save(outputFile)

        with PsdImage.load(outputFile, loadOptions) as img:
            image = cast(PsdImage, img)
            layerEffect = cast(StrokeEffect, image.layers[1].blending_options.effects[0])
            updatedFillSettings = cast(IGradientFillSettings, layerEffect.fill_settings)

            assert updatedFillSettings is not None
            assert 35.0 == updatedFillSettings.angle
        Comparison.CheckAgainstEthalon(outputFile, reference, 1, 1)

    # Fix, shadow not drawn for file
    # https://issue.saltov.dynabic.com/issues/PSDNET-2338
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-155
    def PSDNET2338Test(self):
        srcFile = self.GetFileInBaseFolder("test.psd")
        outFile = self.GetFileInOutputFolder("output.png")
        reference = self.GetFileInBaseFolder("output.png")
        loadOpt = PsdLoadOptions()
        pngOpt = PngOptions()
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA;
        loadOpt.load_effects_resource = True
        with PsdImage.load(srcFile, loadOpt) as psdImage:
            psdImage.save(outFile, pngOpt)

        Comparison.CheckAgainstEthalon(outFile, reference, 1, 1)

    # Remake Drop Shadow effect
    # https://issue.saltov.dynabic.com/issues/PSDNET-2182
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-156
    def PSDNET2182Test(self):
        sourceFile = self.GetFileInBaseFolder("shadow.psd")
        outputFilePng = self.GetFileInOutputFolder("output.png")
        reference =  self.GetFileInBaseFolder("output.png")
        loadOpt = PsdLoadOptions()
        pngOpt = PngOptions()
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        with PsdImage.load(sourceFile, loadOpt) as psdImage:
            psdImage.save(outputFilePng, pngOpt)

        Comparison.CheckAgainstEthalon(outputFilePng, reference, 1, 1)