import pytest
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers import TextLayer
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import cast, as_of, is_assignable

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_25_06_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Add API to Apply Layer Mask to Layer
    # https://issue.saltov.dynabic.com/issues/PSDNET-1870
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-197
    def PSDNET1870Test(self):
        sourceFile = self.GetFileInBaseFolder("example.psd")
        referenceFile = self.GetFileInBaseFolder("export.png")
        outFile = self.GetFileInOutputFolder("export.png")

        with PsdImage.load(sourceFile, PsdLoadOptions()) as img:
            psdImage = cast(PsdImage, img)
            psdImage.layers[1].apply_layer_mask()

            opt = PngOptions()
            opt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            psdImage.save(outFile, opt)

        Comparison.CheckAgainstEthalon(outFile, referenceFile, 0, 1)

    # Make TextLayer rendering not automatic to save original pixels before changes
    # https://issue.saltov.dynabic.com/issues/PSDNET-2400
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-198
    def PSDNET2400Test(self):
        srcFile = self.GetFileInBaseFolder("psdnet2400.psd")
        output1 = self.GetFileInOutputFolder("unchanged-2400.png")
        output2 = self.GetFileInOutputFolder("updated-2400.png")
        ref1 = self.GetFileInBaseFolder("unchanged-2400.png")
        ref2 = self.GetFileInBaseFolder("updated-2400.png")

        opt = PsdLoadOptions()
        opt.allow_non_changed_layer_repaint = False
        with PsdImage.load(srcFile, opt) as img:
            psdImage = cast(PsdImage, img)
            psdImage.save(output1, PngOptions())

            textLayer = cast(TextLayer, psdImage.layers[1])
            textLayer.text_data.update_layer_data()

            psdImage.save(output2, PngOptions())

        Comparison.CheckAgainstEthalon(output1, ref1, 0, 1)
        Comparison.CheckAgainstEthalon(output1, ref2, 0, 1)