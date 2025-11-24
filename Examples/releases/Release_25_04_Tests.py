from datetime import datetime

import pytest
from aspose.psd import Color, FontSettings
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import cast, as_of, is_assignable

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_25_04_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # [AI Format] Handle inline images in content streams
    # https://issue.saltov.dynabic.com/issues/PSDNET-1838
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-177
    def PSDNET1838Test(self):
        FontSettings.remove_font_cache_file();
        inputFile = self.GetFileInBaseFolder("Inline_Image1.ai")
        outputFile = self.GetFileInOutputFolder("output_Inline_Image1.png")
        referenceFile = self.GetFileInBaseFolder("output_Inline_Image1.png")

        with AiImage.load(inputFile) as image:
            image.save(outputFile, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # Error on reading structures from VogkResource on NetFramework project
    # https://issue.saltov.dynabic.com/issues/PSDNET-1967
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-179
    def PSDNET1967Test(self):
        inputFile = self.GetFileInBaseFolder("AllTypesLayerPsd2_ok.psd")

        with PsdImage.load(inputFile) as psdImage:
            # Should be no exception
            pass

    # [AI Format] Resolving rendering issues on NET7.0 framework
    # https://issue.saltov.dynabic.com/issues/PSDNET-2280
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-180
    def PSDNET2280Test(self):
        sourceFile = self.GetFileInBaseFolder("Elements-01.ai")
        outputFile = self.GetFileInOutputFolder("Elements-01.png")
        referenceFile = self.GetFileInBaseFolder("Elements-01.png")

        with AiImage.load(sourceFile) as image:
            image.save(outputFile, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # [AI Format] Resolving rendering issues with Type 2 Shading
    # https://issue.saltov.dynabic.com/issues/PSDNET-2316
     # https://issue.saltov.dynabic.com/issues/PSDPYTHON-181
    def PSDNET2316Test(self):
        files = [
            ("Input1.ai", "output_1.png"),
            ("Input_3.ai", "output_3.png"),
            ("Input_4.ai", "output_4.png")
        ]

        for sourceFile, outputFile in files:
            sourceFilePath = self.GetFileInBaseFolder(sourceFile)
            outputFilePath = self.GetFileInOutputFolder(outputFile)
            referenceFilePath = self.GetFileInBaseFolder(outputFile)

            with AiImage.load(sourceFilePath) as image:
                image.save(outputFilePath, PngOptions())

            Comparison.CheckAgainstEthalon(outputFilePath, referenceFilePath, 0, 1)

    # [Ai format] Remove the crop of bottom part of Ai image on rendering
    # https://issue.saltov.dynabic.com/issues/PSDNET-2379
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-182
    def PSDNET2379Test(self):
        inputFile = self.GetFileInBaseFolder("raster.ai")
        outputFile = self.GetFileInOutputFolder("output_raster.png")
        referenceFile = self.GetFileInBaseFolder("output_raster.png")

        with AiImage.load(inputFile) as image:
            image.save(outputFile, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)