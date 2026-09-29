import pytest
from aspose.psd import Color
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.core.rawcolor import RawColorHelper
from aspose.psd.fileformats.psd.layers.adjustmentlayers import GradientMapLayer
from aspose.psd.fileformats.psd.layers.fillsettings import GradientMapSettings, InterpolationMethod, \
    GradientFillSettings
from aspose.psd.fileformats.psd.layers.gradient import SolidGradient
from aspose.psd.fileformats.psd.layers.layereffects import GradientOverlayEffect
from aspose.psd.fileformats.psd.layers.layerresources import GrdmResource
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper


class Release_26_06_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Implement rendering of Gradient with Linear method.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2722
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-304
    def PSDNET2722Test(self):
        source_file = self.GetFileInBaseFolder("Gradients_Linear.psd")
        output_file = self.GetFileInOutputFolder("output_Gradients_Linear.png")
        reference_file = self.GetFileInBaseFolder("output_Gradients_Linear.png")

        load_opt = PsdLoadOptions()
        load_opt.load_effects_resource = True

        with PsdImage.load(source_file, load_opt) as img:
            psd_image = cast(PsdImage, img)
            png_opt = PngOptions()
            png_opt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            psd_image.save(output_file, png_opt)

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)

    # Implement rendering of Gradient with Stripes method.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2771
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-305
    def PSDNET2771Test(self):
        source_file = self.GetFileInBaseFolder("Gradients_Stripes.psd")
        output_file = self.GetFileInOutputFolder("output_Gradients_Stripes.png")
        reference_file = self.GetFileInBaseFolder("output_Gradients_Stripes.png")

        load_opt = PsdLoadOptions()
        load_opt.load_effects_resource = True

        with PsdImage.load(source_file, load_opt) as img:
            psd_image = cast(PsdImage, img)
            png_opt = PngOptions()
            png_opt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            psd_image.save(output_file, png_opt)

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)

    # Implement the change functionality of version of GrdmResource.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2752
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-306
    def PSDNET2752Test(self):
        source_file = self.GetFileInBaseFolder("Grdm_Classic.psd")
        output_file_psd = self.GetFileInOutputFolder("output_Grdm_Smooth.psd")
        output_file_png = self.GetFileInOutputFolder("output_Grdm_Smooth.png")
        reference_file_psd = self.GetFileInBaseFolder("output_Grdm_Smooth.psd")
        reference_file_png = self.GetFileInBaseFolder("output_Grdm_Smooth.png")

        load_opt = PsdLoadOptions()
        load_opt.load_effects_resource = True

        # First pass: modify gradient map layer and save
        with PsdImage.load(source_file, load_opt) as img:
            psd_image = cast(PsdImage, img)
            gradient_map_layer = cast(GradientMapLayer, psd_image.layers[4])
            gradient_settings = cast(GradientMapSettings, gradient_map_layer.gradient_settings)
            grdm_resource = cast(GrdmResource, gradient_map_layer.resources[0])

            assert grdm_resource.psd_version == 1

            gradient_settings.interpolation_method = InterpolationMethod.SMOOTH
            gradient_map_layer.update()

            psd_image.save(output_file_psd)

            png_opt = PngOptions()
            png_opt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            psd_image.save(output_file_png, png_opt)

        # Second pass: verify version change
        with PsdImage.load(output_file_psd, load_opt) as img:
            psd_image = cast(PsdImage, img)
            gradient_map_layer = cast(GradientMapLayer, psd_image.layers[4])
            grdm_resource = cast(GrdmResource, gradient_map_layer.resources[0])

            assert grdm_resource.psd_version == 3

        Comparison.CheckAgainstEthalon(output_file_psd, reference_file_psd, 0)
        Comparison.CheckAgainstEthalon(output_file_png, reference_file_png, 0)

    # Tests RawColorHelper functionality.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2801
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-308
    def PSDNET2801Test(self):
        # Create ARGB8 bit color without parameters
        color = RawColorHelper.create_argb_8_bit_color(0, 0, 0, 0)
        assert color.get_bit_depth() == 32
        assert color.get_color_mode_name() == "ARGB"
        assert len(color.components) == 4
        expected_names = ["A Alpha", "R Red", "G Green", "B Blue"]
        for i in range(4):
            assert color.components[i].full_name == expected_names[i]
            assert int(color.components[i].value) == 0

        # Create ARGB8 bit color from System.Drawing.Color equivalent
        sys_color = Color.from_argb(15, 25, 35, 45)
        color = RawColorHelper.create_argb_8_bit_color(sys_color)
        assert color.get_bit_depth() == 32
        assert color.get_color_mode_name() == "ARGB"
        assert color.get_as_int() == sys_color.to_argb()

        # Create ARGB16 bit color
        color = RawColorHelper.create_argb_16_bit_color(1000, 2000, 3000, 4000)
        assert color.get_bit_depth() == 64
        assert color.get_color_mode_name() == "ARGB"
        assert len(color.components) == 4
        assert color.components[0].full_name == "A Alpha"
        assert int(color.components[0].value) == 1000
        assert color.components[1].full_name == "R Red"
        assert int(color.components[1].value) == 2000
        assert color.components[2].full_name == "G Green"
        assert int(color.components[2].value) == 3000
        assert color.components[3].full_name == "B Blue"
        assert int(color.components[3].value) == 4000

        # Create CMYK8 bit color
        color = RawColorHelper.create_cmyk_8_bit_color(10, 20, 30, 40)
        assert color.get_bit_depth() == 32
        assert color.get_color_mode_name() == "CMYK"
        assert len(color.components) == 4
        assert int(color.components[0].value) == 10
        assert int(color.components[1].value) == 20
        assert int(color.components[2].value) == 30
        assert int(color.components[3].value) == 40

        # Create CMYK16 bit color
        color = RawColorHelper.create_cmyk_16_bit_bit_color(1000, 2000, 3000, 4000)
        assert color.get_bit_depth() == 64
        assert color.get_color_mode_name() == "CMYK"
        assert len(color.components) == 4
        assert int(color.components[0].value) == 1000
        assert int(color.components[1].value) == 2000
        assert int(color.components[2].value) == 3000
        assert int(color.components[3].value) == 4000

    # Adding the RawColorHelper to public API make the work with color simple.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2800
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-309
    def PSDNET2800Test(self):
        opt = PsdLoadOptions()
        opt.allow_warp_repaint = True
        opt.load_effects_resource = True
        opt.allow_non_changed_layer_repaint = True

        source_file = self.GetFileInBaseFolder("GradientFillExampleRawColor.psd")
        output_file = self.GetFileInOutputFolder("GradientFillExampleRawColor.png")
        reference_file = self.GetFileInBaseFolder("GradientFillExampleRawColor.png")

        with PsdImage.load(source_file, opt) as img:
            psd_image = cast(PsdImage, img)
            for i in range(psd_image.layers.length):
                layer = psd_image.layers[i]
                effect = cast(GradientOverlayEffect, layer.blending_options.effects[0])
                gradient_settings = cast(GradientFillSettings, effect.settings)
                gr = cast(SolidGradient, gradient_settings.gradient)

                gr.color_points[0].raw_color = RawColorHelper.create_argb_8_bit_color(255, 0, 255, 64)
                gr.color_points[0].location = 32
                gr.color_points[1].raw_color = RawColorHelper.create_argb_8_bit_color(255, 0, 64, 255)
                gr.color_points[1].location = 128

                new_point = gr.add_color_point()
                new_point.raw_color = RawColorHelper.create_argb_8_bit_color(255, 255, 64, 255)
                new_point.location = 255

                gr.remove_color_point(gr.color_points[0])

            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            psd_image.save(output_file, pngOpt)

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)