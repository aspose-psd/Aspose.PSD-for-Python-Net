import io

import numpy as np
import pytest
from aspose.psd import FontSettings, DataRecoveryMode
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.pdf import PdfCoreOptions
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PdfOptions, JpegOptions
from aspose.pydrawing.text import InstalledFontCollection

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper


class Release_24_07_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # "Image loading failed." exception when open AI document
    # https://issue.saltov.dynabic.com/issues/PSDNET-1029
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-86
    def PSDNET1029Test(self):
        sourceFile = self.GetFileInBaseFolder("[SA]_ID_card_template.ai")
        referenceFile = self.GetFileInBaseFolder("[SA]_ID_card_template_ethalon.png")
        outputFile = self.GetFileInOutputFolder("[SA]_ID_card_template.png")

        with AiImage.load(sourceFile) as image:
            image.save(outputFile, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # Text rendered incorrectly in output PDF files
    # https://issue.saltov.dynabic.com/issues/PSDNET-2022
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-87
    def PSDNET2022Test(self):
        src = self.GetFileInBaseFolder("CVFlor.psd")
        referenceFile = self.GetFileInBaseFolder("etalon.png")
        output = self.GetFileInOutputFolder("output.pdf")
        outFilePng = self.GetFileInOutputFolder("output.png")

        with PsdImage.load(src) as psdImage:
            psdImage.save(outFilePng, PngOptions())
            saveOptions = PdfOptions()
            saveOptions.pdf_core_options = PdfCoreOptions()

            psdImage.save(output, saveOptions)

        Comparison.CheckAgainstEthalon(outFilePng, referenceFile, 0, 1)

    # Fix ImageSaveException: Image export failed for the given file on Linux
    # https://issue.saltov.dynabic.com/issues/PSDNET-2061
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-88
    def PSDNET2061Test(self):
        sourceFile = self.GetFileInBaseFolder("Bed_Roll-Sticker4_1.psd")
        outputFile = self.GetFileInOutputFolder("output.jpg")
        referenceFile = self.GetFileInBaseFolder("output.jpg")

        loadOpt = PsdLoadOptions()
        loadOpt.load_effects_resource = True
        saveOpt = JpegOptions()
        saveOpt.quality = 70
        with PsdImage.load(sourceFile, loadOpt) as psdImage:
            psdImage.save(outputFile, saveOpt)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # Fix fonts loading when using Aspose.Drawing
    # https://issue.saltov.dynabic.com/issues/PSDNET-2080
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-89
    def PSDNET2080Test(self):
        with InstalledFontCollection() as installedFonts:
            print("- Before update. Installed fonts count: " + str(len(installedFonts.families)))
            print("- Refresh the font cache by trying to get the Adobe font name for 'Arial': ")
            FontSettings.get_adobe_font_name("Arial")
            print("- After update. Installed fonts count: " + str(len(installedFonts.families)))

            assert len(installedFonts.families) > 1

    # 'Arithmetic operation resulted in an overflow' when creating smart object layer using large JPEG
    # https://issue.saltov.dynabic.com/issues/PSDNET-2085
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-90
    #def PSDNET2085Test(self):
        #srcFile = self.GetFileInBaseFolder("source.psd")
        #imageJpg = self.GetFileInBaseFolder("test.jpg")

        #loadOpt = PsdLoadOptions()
        #loadOpt.data_recovery_mode = DataRecoveryMode.MAXIMAL_RECOVER
        #with PsdImage.load(srcFile, loadOpt) as image:
            #with open(imageJpg, "rb", buffering=0) as stream:
                #addedLayer = SmartObjectLayer(stream)
                #addedLayer.Name = "Test Layer"
                #image.AddLayer(addedLayer)

    # The AI file can not be converted into a JPG file
    # https://issue.saltov.dynabic.com/issues/PSDNET-2100
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-91
    def PSDNET2100Test(self):
        sourceFile = self.GetFileInBaseFolder("aaa.ai")
        outputFile = self.GetFileInOutputFolder("aaa.png")
        referenceFile = self.GetFileInOutputFolder("aaa.png")

        with AiImage.load(sourceFile) as image:
            image.save(outputFile, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)