import psutil
import pytest
from aspose.psd import Image, FontSettings
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper


class Release_24_01_Tests(BaseTests):

    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # [AI Format] Add basic handling for multipage AI images
    # https://issue.saltov.dynabic.com/issues/PSDNET-1835
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-19
    def PSDNET1835Test(self):
        sourceFile = self.GetFileInBaseFolder("threePages.ai")
        firstPageOutputPng = self.GetFileInOutputFolder("firstPageOutput.png")
        secondPageOutputPng = self.GetFileInOutputFolder("secondPageOutput.png")
        thirdPageOutputPng = self.GetFileInOutputFolder("thirdPageOutput.png")

        # Load the AI image.
        with Image.load(sourceFile) as img:
            image = cast(AiImage, img)
            # By default, the ActivePageIndex is 0.
            # So if you save the AI image without changing this property, the first page will be rendered and saved.
            image.save(firstPageOutputPng, PngOptions())

            # Change the active page index to the second page.
            image.active_page_index = 1

            # Save the second page of the AI image as a PNG image.
            image.save(secondPageOutputPng, PngOptions())

            # Change the active page index to the third page.
            image.active_page_index = 2

            # Save the third page of the AI image as a PNG image.
            image.save(thirdPageOutputPng, PngOptions())

        referenceFile1 = self.GetFileInBaseFolder("firstPageOutput.png")
        referenceFile2 = self.GetFileInBaseFolder("secondPageOutput.png")
        referenceFile3 = self.GetFileInBaseFolder("thirdPageOutput.png")

        Comparison.CheckAgainstEthalon(firstPageOutputPng, referenceFile1, 1)
        Comparison.CheckAgainstEthalon(secondPageOutputPng, referenceFile2, 1)
        Comparison.CheckAgainstEthalon(thirdPageOutputPng, referenceFile3, 1)

    # PSDNET-718. Warp Text Effect doesn’t apply to text
    # https://issue.saltov.dynabic.com/issues/PSDNET-718
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-22
    def PSDNET718Test(self):
        sourceFile = self.GetFileInBaseFolder("text_warp.psd")
        outputFile = self.GetFileInOutputFolder("export.png")

        opt = PsdLoadOptions()
        opt.load_effects_resource = True
        opt.allow_warp_repaint = True

        pngOpt = PngOptions()
        pngOpt.compression_level = 9
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        with PsdImage.load(sourceFile, opt) as img:
            img.save(outputFile, pngOpt)

        referenceFile = self.GetFileInBaseFolder("etalon.png")
        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 1)

    # PSDNET-1620. Incorrect rendering of mask in the specific file
    # https://issue.saltov.dynabic.com/issues/PSDNET-718
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-23
    def PSDNET1620Test(self):
        sourceFile1 = self.GetFileInBaseFolder("mask_problem.psd")
        sourceFile2 = self.GetFileInBaseFolder("puh_softLight3_1.psd")
        outputFile1 = self.GetFileInOutputFolder("mask_export.png")
        outputFile2 = self.GetFileInOutputFolder("puh_export.png")

        opt = PsdLoadOptions()
        opt.load_effects_resource = True

        pngOpt = PngOptions()
        pngOpt.compression_level = 9
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        with PsdImage.load(sourceFile1, opt) as img:
            img.save(outputFile1, pngOpt)

        with PsdImage.load(sourceFile2, opt) as img:
            img.save(outputFile2, pngOpt)

        referenceFile1 = self.GetFileInBaseFolder("mask_problem_etalon.png")
        referenceFile2 = self.GetFileInBaseFolder("puh_softLight3_1_etalon.png")
        Comparison.CheckAgainstEthalon(outputFile1, referenceFile1, 1)
        Comparison.CheckAgainstEthalon(outputFile2, referenceFile2, 1)

    # PSDNET-1855. NullReferenceException at Aspose.PSD.FontParsing.OpenType.Serialization.OpenTypeFontInfo..ctor
    # https://issue.saltov.dynabic.com/issues/PSDNET-1855
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-24
    def PSDNET1855Test(self):
        fontsFolder = self.GetFileInBaseFolder("Fonts")
        FontSettings.set_fonts_folders([fontsFolder], True)


        inputFile = self.GetFileInBaseFolder("1.psd")
        outputFile = self.GetFileInOutputFolder("out_1855.png")
        referenceFile = self.GetFileInBaseFolder("out_1855.png")

        with PsdImage.load(inputFile) as psdImage:
            psdImage.save(outputFile, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 1)
        self.remove_all_unzipped_files()

    # PSDNET-1883. [AI Format] Fixing the memory usage in AiExporterUtils
    # https://issue.saltov.dynabic.com/issues/PSDNET-1883
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-25
    def PSDNET1883Test(self):
        sourceFile = self.GetFileInBaseFolder("threePages.ai")
        firstPageOutputPng = self.GetFileInOutputFolder("firstPageOutput.png")
        secondPageOutputPng = self.GetFileInOutputFolder("secondPageOutput.png")
        thirdPageOutputPng = self.GetFileInOutputFolder("thirdPageOutput.png")

        # C# Memory usage is 220, but for python we have no direct access to GC activities.
        MemoryLimit = 1500
        process = psutil.Process()
        startMemory = process.memory_info().rss
        pngOpt = PngOptions()
        # Load the AI image.
        with Image.load(sourceFile) as img:
            image = cast(AiImage, img)

            # Save the first page of the AI image as a PNG image.
            image.save(firstPageOutputPng, pngOpt)

            # Change the active page index to the second page.
            image.active_page_index = 1

            # Save the second page of the AI image as a PNG image.
            image.save(secondPageOutputPng, pngOpt)

            # Change the active page index to the third page.
            image.active_page_index = 2

            # Save the third page of the AI image as a PNG image.
            image.save(thirdPageOutputPng, pngOpt)

        endMemory = process.memory_info().rss

        memoryUsed = (endMemory - startMemory) / 1024 / 1024

        if memoryUsed > MemoryLimit:
            raise Exception("Usage of memory is too big. {} instead of {:.1f}".format(memoryUsed, MemoryLimit))