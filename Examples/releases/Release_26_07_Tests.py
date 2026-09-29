from datetime import datetime

import os
import pytest
from aspose.psd import Image
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import cast, as_of, is_assignable

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper


class Release_26_07_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Resaving of 32bit RGB Image leads to the exception on the reopening.
    # https://issue.saltov.dynabic.com/issues/PSDNET-123
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-311
    def PSDNET123Test(self):
        source_file = self.GetFileInBaseFolder("inRgb32.psd")
        output_file = self.GetFileInOutputFolder("inRgb32_out.psd")

        with PsdImage.load(source_file) as img:
            psd_image = cast(PsdImage, img)
            assert psd_image.bits_per_channel == 32, "Bits per channel should be 32 on start"
            psd_image.save(output_file)

        with PsdImage.load(output_file) as img:
            psd_image = cast(PsdImage, img)
            assert psd_image.bits_per_channel == 32, "Bits per channel should remain 32 after round‑trip."

        if os.path.exists(output_file):
            os.remove(output_file)

    # The rectangle has no common processing area in the PSD File with Artboards.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2409
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-312
    def PSDNET2409Test(self):
        src = self.GetFileInBaseFolder("2409_resized.psd")
        output = self.GetFileInOutputFolder("test1234.png")

        png_opt = PngOptions()
        png_opt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        with Image.load(src) as img:
            img.save(output, png_opt)

        if os.path.exists(output):
            os.remove(output)

    # Fix processing of transparent color in gradient of Gradient Fill Layer.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2749
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-313
    def PSDNET2749Test(self):
        source_file = self.GetFileInBaseFolder("Effect_Smooth_shape_type_variants.psd")
        output_file = self.GetFileInOutputFolder("output_Effect_Smooth_shape_type_variants.png")
        reference_file = self.GetFileInBaseFolder("output_Effect_Smooth_shape_type_variants.png")

        load_opt = PsdLoadOptions()
        load_opt.load_effects_resource = True

        with PsdImage.load(source_file, load_opt) as img:
            psd_image = cast(PsdImage, img)
            png_opt = PngOptions()
            png_opt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            psd_image.save(output_file, png_opt)

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)

#LicenseHelper.set_license()
#a = Release_26_07_Tests()
#a.PSDNET2749Test()