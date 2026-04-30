import pytest
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_26_03_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Update processing of parameter Technique-Softer of Outer glow effect on rendering.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2665
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-290
    def PSDNET2665Test(self):
        source_file = self.GetFileInBaseFolder("OuterGlow_Softer.psd")
        output_file = self.GetFileInOutputFolder("output_OuterGlow_Softer.png")
        reference_file = self.GetFileInBaseFolder("output_OuterGlow_Softer.png")

        load_opt = PsdLoadOptions()
        load_opt.load_effects_resource = True

        with PsdImage.load(source_file, load_opt) as img:
            png_opt = PngOptions()
            png_opt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            img.save(output_file, png_opt)

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)

    # Warp transformation grid is incorrect for specific cases.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2644
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-291
    def PSDNET2644Test(self):
        source_file = self.GetFileInBaseFolder("input.psd")
        output_file = self.GetFileInOutputFolder("export.png")
        reference_file = self.GetFileInBaseFolder("export.png")

        load_opt = PsdLoadOptions()
        load_opt.allow_warp_repaint = True
        load_opt.load_effects_resource = True

        png_opt = PngOptions()
        png_opt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        with PsdImage.load(source_file, load_opt) as img:
            psd_image = cast(PsdImage, img)
            psd_image.save(output_file, png_opt)

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)

    # Rendering of outer glow differs from the original PS rendering noticeable.
    # https://issue.saltov.dynabic.com/issues/PSDNET-1969
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-292
    def PSDNET1969Test(self):
        source_file = self.GetFileInBaseFolder("OuterGlow.psd")
        output_file = self.GetFileInOutputFolder("output_OuterGlow.png")
        reference_file = self.GetFileInBaseFolder("output_OuterGlow.png")

        load_opt = PsdLoadOptions()
        load_opt.load_effects_resource = True

        png_opt = PngOptions()
        png_opt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        with PsdImage.load(source_file, load_opt) as img:
            psd_image = cast(PsdImage, img)
            psd_image.save(output_file, png_opt)

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)

    # The warp arc algorithm must be changed.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2331
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-293
    def PSDNET2331Test(self):
        # First arc warp
        arc_source_file = self.GetFileInBaseFolder("arc_warp.psd")
        arc_output_file = self.GetFileInOutputFolder("arc_export.png")
        arc_reference_file = self.GetFileInBaseFolder("arc_export.png")

        # Second vertical arc warp
        arcv_source_file = self.GetFileInBaseFolder("arc_v_warp.psd")
        arcv_output_file = self.GetFileInOutputFolder("arc_v_export.png")
        arcv_reference_file = self.GetFileInBaseFolder("arc_v_export.png")

        load_opt = PsdLoadOptions()
        load_opt.allow_warp_repaint = True
        load_opt.load_effects_resource = True

        png_opt = PngOptions()
        png_opt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        with PsdImage.load(arc_source_file, load_opt) as img:
            psd_image = cast(PsdImage, img)
            psd_image.save(arc_output_file, png_opt)

        with PsdImage.load(arcv_source_file, load_opt) as img:
            psd_image = cast(PsdImage, img)
            psd_image.save(arcv_output_file, png_opt)

        Comparison.CheckAgainstEthalon(arc_output_file, arc_reference_file, 0)
        Comparison.CheckAgainstEthalon(arcv_output_file, arcv_reference_file, 0)


#LicenseHelper.set_license()
#a = Release_26_03_Tests()
#a.PSDNET2331Test()