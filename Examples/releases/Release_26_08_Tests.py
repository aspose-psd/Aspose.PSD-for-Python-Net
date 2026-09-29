from datetime import datetime

import pytest
from aspose.psd import Image
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers import ShapeLayer
from aspose.psd.fileformats.psd.layers.smartfilters import DisplaceSmartFilter, DisplacementMethod, UndefinedAreas
from aspose.psd.fileformats.psd.layers.smartobjects import (
    SmartObjectLayer,
)
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import cast, as_of, is_assignable

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper


class Release_26_08_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Support of Grayscale ColorMode PSD Image saving with 32 bit per channel.
    # https://issue.saltov.dynabic.com/issues/PSDNET-125
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-324
    def PSDNET125Test(self):
        name = "inGrayscale32no"
        source_file = self.GetFileInBaseFolder(f"{name}.psd")
        output_file_psd = self.GetFileInOutputFolder(f"{name}_out.psd")
        output_file_png = self.GetFileInOutputFolder(f"{name}_out.png")
        reference_file_psd = self.GetFileInBaseFolder(f"{name}_out.psd")
        reference_file_png = self.GetFileInBaseFolder(f"{name}_out.png")

        # Load the original 32‑bit/channel Grayscale PSD
        with Image.load(source_file) as img:
            psd = cast(PsdImage, img)

            assert psd.bits_per_channel == 32, "Bits per channel should be 32 on start"

            psdOpt = PsdOptions()
            psdOpt.channel_bits_count = 32

            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            psd.save(output_file_psd, psdOpt)
            psd.save(output_file_png, pngOpt)

        # Reload the saved file – no exception should be thrown
        with Image.load(output_file_psd) as img:
            psd = cast(PsdImage, img)
            assert psd.bits_per_channel == 32, "Bits per channel should remain 32 after round‑trip."

        Comparison.CheckAgainstEthalon(output_file_psd, reference_file_psd, 0)
        Comparison.CheckAgainstEthalon(output_file_png, reference_file_png, 0)

    # Implement reading/writing Displace smart filter data.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2810
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-325
    def PSDNET2810Test(self):
        src_file_name = "no_displace_filter.psd"
        source_file = self.GetFileInBaseFolder(src_file_name)
        output_file = self.GetFileInOutputFolder("output_displace_filter.psd")
        displace_map_path = self.GetFileInBaseFolder("displace_map.psd")

        # First pass – add Displace filter and save
        with PsdImage.load(source_file) as img:
            psd_image = cast(PsdImage, img)
            smart_obj = cast(SmartObjectLayer, psd_image.layers[1])

            displace = DisplaceSmartFilter(displace_map_path, True)
            displace.horizontal_scale = 12.5
            displace.vertical_scale = 15.0
            displace.displacement_method = DisplacementMethod.TILE
            displace.undefined_areas = UndefinedAreas.WRAP_AROUND

            filters = list(smart_obj.smart_filters.filters)
            filters.append(displace)
            smart_obj.smart_filters.filters = filters
            smart_obj.smart_filters.update_resource_values()

            psd_image.save(output_file)

        # Second pass – verify filter properties
        with PsdImage.load(output_file) as img:
            psd_image = cast(PsdImage, img)
            smart_obj = cast(SmartObjectLayer, psd_image.layers[1])
            displace = cast(DisplaceSmartFilter, smart_obj.smart_filters.filters[-1])

            assert displace.horizontal_scale == 12.5
            assert displace.vertical_scale == 15.0
            assert displace.displacement_method == DisplacementMethod.TILE
            assert displace.undefined_areas == UndefinedAreas.WRAP_AROUND
            assert displace.is_displacement_map_embedded is True
            assert displace.displace_map_data is not None

    # Improving Layer Effects processing according to the logic of the new Overlay Effects Blending algorithm.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2668
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-326
    def PSDNET2668Test(self):
        source_file = self.GetFileInBaseFolder("gradient-2668.psd")
        output_file = self.GetFileInOutputFolder("out_gradient-2668.png")
        reference_file = self.GetFileInBaseFolder("out_gradient-2668.png")

        load_opt = PsdLoadOptions()
        load_opt.load_effects_resource = True

        with PsdImage.load(source_file, load_opt) as img:
            img.save(output_file, PngOptions())

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)

    # Arithmetic operation resulted in an overflow on Image.Load in file with complex smart filter Liquify.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2265
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-327
    def PSDNET2265Test(self):
        source_file = self.GetFileInBaseFolder("m28719.psd")

        with PsdImage.load(source_file) as img:
            psd_image = cast(PsdImage, img)
            # No further actions; test ensures loading does not raise.

    # [AI Format] Implementing the Type 1 (function) Shading.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2772
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-328
    def PSDNET2772Test(self):
        source_file = self.GetFileInBaseFolder("shadingType1.ai")
        output_file = self.GetFileInOutputFolder("shadingType1.png")
        reference_file = self.GetFileInBaseFolder("shadingType1.png")

        with AiImage.load(source_file) as img:
            ai_image = cast(AiImage, img)
            ai_image.save(output_file, PngOptions())

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)

    # Effect loss when working with smart objects.
    # https://issue.saltov.dynabic.com/issues/PSDNET-1472
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-329
    def PSDNET1472Test(self):
        src_file = self.GetFileInBaseFolder("1472_sampledog.psd")
        out_file2 = self.GetFileInOutputFolder("out_2_sampledog.png")
        out_file3 = self.GetFileInOutputFolder("out_3_sampledog.png")
        ref_file2 = self.GetFileInBaseFolder("out_2_sampledog.png")
        ref_file3 = self.GetFileInBaseFolder("out_3_sampledog.png")

        psd_load_options = PsdLoadOptions()
        psd_load_options.load_effects_resource = True

        with PsdImage.load(src_file, psd_load_options) as img:
            psd_image = cast(PsdImage, img)
            smart_object = cast(SmartObjectLayer, psd_image.layers[1])
            smart_object_psd = cast(PsdImage, smart_object.load_contents(psd_load_options))

            smart_object2 = smart_object_psd.smart_object_provider.convert_to_smart_object(smart_object_psd.layers)
            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            smart_object_psd.save(out_file2, pngOpt)
            smart_object2.save(out_file3, pngOpt)

        Comparison.CheckAgainstEthalon(out_file2, ref_file2, 0)
        Comparison.CheckAgainstEthalon(out_file3, ref_file3, 0)

#LicenseHelper.set_license()
#a = Release_26_08_Tests()
#a.PSDNET1472Test()