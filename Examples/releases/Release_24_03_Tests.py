import time
import uuid

import psutil
import pytest
from aspose.psd import Image, FontSettings, FileFormat, Rectangle, Color
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers import ShapeLayer
from aspose.psd.fileformats.psd.layers.filllayers import FillLayer
from aspose.psd.fileformats.psd.layers.layerresources import PattResource, Lr16Resource, Lr32Resource
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import cast, as_of

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

import io, os, shutil
from aspose.psd import License
from aspose.psd import Image
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers import TextLayer
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions
from aspose.pycore import cast


class Release_24_03_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()



    # PSD File after the converting from 8 bit to 16 bit became unreadable.
    # https://issue.saltov.dynabic.com/issues/PSDNET-1905
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-45
    def PSDNET1905Test(self):
        sourceFile = self.GetFileInBaseFolder("test_smart_layer.psd")
        outputFile = self.GetFileInOutputFolder("export.psd")

        with PsdImage.load(sourceFile) as psdImage8:
            psdOptions16 = PsdOptions()
            psdOptions16.channel_bits_count = 16

            psdImage8.save(outputFile, psdOptions16)

        with PsdImage.load(outputFile) as image:
            psdImage16 = cast(PsdImage, image)

            testResource = as_of(psdImage16.global_layer_resources[0], Lr16Resource)
            if testResource is not None:
                # is ok
                pass
            else:
                raise Exception("Wrong global resource, the first resource should be Lr16Resource")

    # PSD File after the converting from 8 bit to 32 bit became unreadable.
    # https://issue.saltov.dynabic.com/issues/PSDNET-1906
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-46
    def PSDNET1906Test(self):
        sourceFile = self.GetFileInBaseFolder("test_smart_layer.psd")
        outputFile = self.GetFileInOutputFolder("export.psd")

        with PsdImage.load(sourceFile) as psdImage8:
            psdOptions32 = PsdOptions()
            psdOptions32.channel_bits_count = 32

            psdImage8.save(outputFile, psdOptions32)

        with PsdImage.load(outputFile) as image:
            psdImage32 = cast(PsdImage, image)

            testResource = as_of(psdImage32.global_layer_resources[0], Lr32Resource)
            if testResource is not None:
                # is ok
                pass
            else:
                raise Exception("Wrong global resource, the first resource should be Lr32Resource")

    # [AI Format] Fix the Short Curve rendering at AI file.
    # https://issue.saltov.dynabic.com/issues/PSDNET-1921
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-47
    def PSDNET1921Test(self):
        sourceFile = self.GetFileInBaseFolder("shortCurve.ai")
        outputFilePath = self.GetFileInOutputFolder("shortCurve.png")
        referenceFile = self.GetFileInBaseFolder("shortCurve_ethalon.png")

        with AiImage.load(sourceFile) as image:
            image.save(outputFilePath, PngOptions())

        Comparison.CheckAgainstEthalon(outputFilePath, referenceFile, 1)
