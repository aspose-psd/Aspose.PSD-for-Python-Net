from datetime import datetime

import numpy as np
import pytest
from aspose.psd import Color
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers import ShapeLayer, Layer
from aspose.psd.fileformats.psd.layers.fillsettings import GradientFillSettings
from aspose.psd.fileformats.psd.layers.layereffects import StrokeEffect
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import cast, as_of, is_assignable

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_25_03_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()


    # [Regression] Fixing regression after implementing APS rendering.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2170
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-175
    def PSDNET2170Test(self):
        inputFile = self.GetFileInBaseFolder("shortCurve.ai")
        outputFilePng = self.GetFileInOutputFolder("output_shortCurve.png")
        referenceFile = self.GetFileInBaseFolder("output_shortCurve.png")

        with AiImage.load(inputFile) as img:
            image = cast(AiImage, img)
            image.save(outputFilePng, PngOptions())

        Comparison.CheckAgainstEthalon(outputFilePng, referenceFile, 0, 1)

    # [AI Format] Fixing regression at AI rendering
    # https://issue.saltov.dynabic.com/issues/PSDNET-2283
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-172
    def PSDNET2283Test(self):
        sourceFile = self.GetFileInBaseFolder("Layers-NoImage.ai")
        outputFile = self.GetFileInOutputFolder("Layers-NoImage.png")
        referenceFile = self.GetFileInBaseFolder("Layers-NoImage.png")

        with AiImage.load(sourceFile) as image:
            image.save(outputFile, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # Unified blending method to improve blending in general
    # https://issue.saltov.dynabic.com/issues/PSDNET-2389
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-169
    def PSDNET2389Test(self):
        sourceFile = self.GetFileInBaseFolder("ApplyLayerStateTest_output_src.psd")
        outputPng = self.GetFileInOutputFolder("ApplyLayerStateTest_output.png")
        referenceFile = self.GetFileInBaseFolder("ApplyLayerStateTest_output.png")

        psdLoadOptions = PsdLoadOptions()
        psdLoadOptions.load_effects_resource = True

        with PsdImage.load(sourceFile, psdLoadOptions) as image:
            psdImage = cast(PsdImage, image)
            psdImage.save(outputPng, PngOptions())

        Comparison.CheckAgainstEthalon(outputPng, referenceFile, 0, 1)