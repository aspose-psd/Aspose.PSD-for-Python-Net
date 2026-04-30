from datetime import datetime

import pytest
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers import LayerGroup
from aspose.psd.fileformats.psd.layers.fillsettings import InterpolationMethod
from aspose.psd.fileformats.psd.layers.layereffects import GradientOverlayEffect
from aspose.psd.fileformats.psd.layers.layerresources import IfxsResource, ImfxResource, Hue2Resource
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_26_04_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Add support for a resource containing effects in a group layer.
    # https://issue.saltov.dynabic.com/issues/PSDNET-548
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-295
    def PSDNET548Test(self):
        source_file = self.GetFileInBaseFolder("Example.psd")
        output_file = self.GetFileInOutputFolder("export.psd")
        reference_file = self.GetFileInBaseFolder("export.psd")

        load_opt = PsdLoadOptions()
        load_opt.load_effects_resource = True

        with PsdImage.load(source_file, load_opt) as img:
            psd_image = cast(PsdImage, img)
            layer_group_one = cast(LayerGroup, psd_image.layers[2])
            layer_group_many = cast(LayerGroup, psd_image.layers[5])

            effect_count_one = len(layer_group_one.blending_options.effects)
            effect_count_many = len(layer_group_many.blending_options.effects)

            ifxs_resource = cast(IfxsResource, layer_group_one.resources[0])
            imfx_resource = cast(ImfxResource, layer_group_many.resources[0])

            layer_group_many.blending_options.add_drop_shadow()

            psd_image.save(output_file)

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)

    # Implement rendering of Gradient with Smooth method.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2701
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-296
    def PSDNET2701Test(self):
        source_file = self.GetFileInBaseFolder("GradientOverlay.psd")
        output_file = self.GetFileInOutputFolder("output_GradientOverlay.psd")
        output_file_png = self.GetFileInOutputFolder("output_GradientOverlay.png")
        reference_file_psd = self.GetFileInBaseFolder("output_GradientOverlay.psd")
        reference_file_png = self.GetFileInBaseFolder("output_GradientOverlay.png")

        src_method = InterpolationMethod.LINEAR
        new_method = InterpolationMethod.SMOOTH

        load_opt = PsdLoadOptions()
        load_opt.load_effects_resource = True

        with PsdImage.load(source_file, load_opt) as img:
            psd_image = cast(PsdImage, img)
            effect = cast(GradientOverlayEffect, psd_image.layers[1].blending_options.effects[0])
            gradient_settings = effect.settings
            assert gradient_settings.interpolation_method == src_method
            gradient_settings.interpolation_method = new_method

            psd_image.save(output_file)
            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            psd_image.save(output_file_png, pngOpt)

        with PsdImage.load(output_file, load_opt) as img:
            psd_image = cast(PsdImage, img)
            effect = cast(GradientOverlayEffect, psd_image.layers[1].blending_options.effects[0])
            gradient_settings = effect.settings
            assert gradient_settings.interpolation_method == new_method

        Comparison.CheckAgainstEthalon(output_file, reference_file_psd, 0)
        Comparison.CheckAgainstEthalon(output_file_png, reference_file_png, 0)

    # PSD files with adjusted Hue/Saturation will throw the exception PsdImageArgumentException - Invalid Hue2 Resource data.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2710
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-297
    def PSDNET2710Test(self):
        hue2 = Hue2Resource(bytearray(136))

#LicenseHelper.set_license()
#a = Release_26_04_Tests()
#a.PSDNET548Test()