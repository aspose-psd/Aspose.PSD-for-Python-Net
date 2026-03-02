from datetime import datetime

import io
import pytest
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.fileformats.psd.resources import PrintScaleResource
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_26_02_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # IndexOutOfRangeException in the large file 2500x36667 (DPI 300).
    # https://issue.saltov.dynabic.com/issues/PSDNET-2663
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-276
    def PSDNET2663Test(self):
        sourceFile = self.GetFileInBaseFolder("blind3_nolock.psb")
        outputFile = self.GetFileInOutputFolder("blind3_nolock.png")
        referenceFile = self.GetFileInBaseFolder("blind3_nolock.png")

        loadOpt = PsdLoadOptions()
        loadOpt.load_effects_resource = True

        with PsdImage.load(sourceFile, loadOpt) as img:
            psdImage = cast(PsdImage, img)
            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            psdImage.save(outputFile, pngOpt)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0)
        self.remove_all_unzipped_files()

    # The file loses a large amount of resources after saving.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2631
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-286
    def PSDNET2631Test(self):
        srcFile = self.GetFileInBaseFolder("Alexandria.psd")
        outFile = self.GetFileInOutputFolder("output.psd")
        referenceFile = self.GetFileInBaseFolder("output.psd")

        DefaultResourcesCount = 2
        SeveralResourcesCount = 3

        # Save all resources as default (options.resources = None)
        with PsdImage.load(srcFile) as img:
            psdImage = cast(PsdImage, img)
            options = PsdOptions()
            assert options.resources is None

            imageResourcesCount = len(psdImage.image_resources)
            psdImage.save(outFile, PsdOptions())

            assert options.resources is None

        # Verify resources count after default save
        with PsdImage.load(outFile) as img:
            psdImage = cast(PsdImage, img)
            assert imageResourcesCount == len(psdImage.image_resources)

        # Save without resources
        with PsdImage.load(srcFile) as img:
            psdImage = cast(PsdImage, img)
            options = PsdOptions()
            options.resources = []
            assert len(options.resources) == 0

            psdImage.save(outFile, options)

            assert len(options.resources) == 0

        # Verify resources count after saving without resources
        with PsdImage.load(outFile) as img:
            psdImage = cast(PsdImage, img)
            assert DefaultResourcesCount == len(psdImage.image_resources)

        # Save with several resources
        with PsdImage.load(srcFile) as img:
            psdImage = cast(PsdImage, img)
            psdOptions = PsdOptions()
            newResources = []
            newResources.append(PrintScaleResource())
            psdOptions.resources = newResources

            psdImage.save(outFile, psdOptions)

        # Verify resources count after saving several resources
        with PsdImage.load(outFile) as img:
            psdImage = cast(PsdImage, img)
            assert SeveralResourcesCount == len(psdImage.image_resources)

        Comparison.CheckAgainstEthalon(outFile, referenceFile, 0)
        self.remove_all_unzipped_files()

    # ArgumentException on loading section resource.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2686
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-287
    def PSDNET2686Test(self):
        srcFile = self.GetFileInBaseFolder("test-2026-02-05.psd")

        loadOpt = PsdLoadOptions()
        loadOpt.use_disk_for_load_effects_resource = True
        loadOpt.allow_warp_repaint = True
        loadOpt.use_icc_profile_conversion = False

        with PsdImage.load(io.BytesIO(open(srcFile, "rb").read()), loadOpt) as img:
            psdImage = cast(PsdImage, img)

        self.remove_all_unzipped_files()

    # SmartObjectLayer the size is changed after setContents and updateModifiedContent.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2367
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-288
    def PSDNET2367Test(self):
        def AreSizesEqual(expectedSize, actualSize):
            if expectedSize != actualSize:
                raise Exception("Sizes are not equal")

        etalonPsdPath = self.GetFileInBaseFolder("expected2000x2000.psd")
        psdFilePath = self.GetFileInBaseFolder("file.psd")
        replaceFilePath = self.GetFileInBaseFolder("2000x2000.png")

        expectedSize1 = None
        expectedSize3 = None

        with PsdImage.load(etalonPsdPath) as img:
            etalonPsd = cast(PsdImage, img)
            smartObj1 = cast(SmartObjectLayer, etalonPsd.layers[0])
            smartObj3 = cast(SmartObjectLayer, etalonPsd.layers[1])
            expectedSize1 = smartObj1.size
            expectedSize3 = smartObj3.size

        with PsdImage.load(psdFilePath) as img:
            psdImage = cast(PsdImage, img)
            smartObj1 = cast(SmartObjectLayer, psdImage.layers[0])
            smartObj3 = cast(SmartObjectLayer, psdImage.layers[1])

            smartObj1.replace_contents(replaceFilePath)
            smartObj1.update_modified_content()

            smartObj3.replace_contents(replaceFilePath)
            smartObj3.update_modified_content()

            AreSizesEqual(expectedSize1, smartObj1.size)
            AreSizesEqual(expectedSize3, smartObj3.size)

        self.remove_all_unzipped_files()

#LicenseHelper.set_license()
#a = Release_26_02_Tests()
#a.PSDNET2663Test()