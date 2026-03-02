import os

import pytest
from aspose.psd import DataRecoveryMode, Image
from aspose.psd.fileformats.core.blending import BlendMode
from aspose.psd.fileformats.psd.layers.filllayers import FillLayer
from aspose.psd.fileformats.psd.layers.fillsettings import GradientFillSettings, GradientType
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers.layerresources import LsdkResource, SoLdResource, LayerSectionResource, \
    LayerSectionType, BaseLayerSectionResource, LayerSectionSubtype
from aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures import DescriptorStructure, ListStructure, \
    ReferenceStructure, NameStructure
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import cast, is_assignable, as_of

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_26_01_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # After replacing, the image becomes blurry with jagged edges
    # https://issue.saltov.dynabic.com/issues/PSDNET-2613
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-280
    def PSDNET2613Test(self):
        source_file = self.GetFileInBaseFolder("Clipping_Blending.psd")
        output_file = self.GetFileInOutputFolder("output_Clipping_Blending.png")
        reference_file = self.GetFileInBaseFolder("output_Clipping_Blending.png")

        with Image.load(source_file) as psd_image:
            opt = PngOptions()
            opt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            psd_image.save(output_file, opt)

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)

    # Update saving to resource of GradientFillSettings for FillLayer
    # https://issue.saltov.dynabic.com/issues/PSDNET-2507
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-281
    def PSDNET2507Test(self):
        source_file = self.GetFileInBaseFolder("ComplexGradientFillLayer.psd")
        output_file = self.GetFileInOutputFolder("output_ComplexGradientFillLayer.psd")
        reference_file = self.GetFileInBaseFolder("output_ComplexGradientFillLayer.psd")

        # Edit and save
        with Image.load(source_file) as img:
            image = cast(PsdImage, img)
            fill_layer = cast(FillLayer, image.layers[1])
            fill_settings = cast(GradientFillSettings, fill_layer.fill_settings)
            # Reading
            assert fill_settings.gradient_type == GradientType.LINEAR
            assert fill_settings.gradient.gradient_name == "Custom\0"

            # Editing
            fill_settings.gradient_type = GradientType.DIAMOND
            fill_settings.gradient.gradient_name = "UpdatedGradient"
            fill_layer.update()
            image.save(output_file)

        # Verify
        with Image.load(output_file) as image:
            image = cast(PsdImage, image)
            fill_layer = cast(FillLayer, image.layers[1])
            fill_settings = cast(GradientFillSettings, fill_layer.fill_settings)

            assert fill_settings.gradient_type == GradientType.DIAMOND
            assert fill_settings.gradient.gradient_name == "UpdatedGradient"

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)

    # Linear burn blend mode works incorrectly if pixel alpha is less than 255
    # https://issue.saltov.dynabic.com/issues/PSDNET-545
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-282
    def PSDNET545Test(self):
        source_file = self.GetFileInBaseFolder("StripesLb.psd")
        output_file = self.GetFileInOutputFolder("output_StripesLb.png")
        reference_file = self.GetFileInBaseFolder("output_StripesLb.png")

        load_options = PsdLoadOptions()
        load_options.load_effects_resource = True

        pngOpt = PngOptions()
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
        with PsdImage.load(source_file, load_options) as img:
            img.save(output_file, pngOpt)

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)

    # Linear burn blend mode works incorrectly if pixel alpha is less than 255
    # https://issue.saltov.dynabic.com/issues/PSDNET-545
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-282
    def PSDNET545Test(self):
        source_file = self.GetFileInBaseFolder("StripesLb.psd")
        output_file = self.GetFileInOutputFolder("output_StripesLb.png")
        reference_file = self.GetFileInBaseFolder("output_StripesLb.png")

        load_options = PsdLoadOptions()
        load_options.load_effects_resource = True

        pngOpt = PngOptions()
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
        with PsdImage.load(source_file, load_options) as img:
            img.save(output_file, pngOpt)

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)

    # After the re-export of the PSD file, the result became much larger that original PSD file
    # https://issue.saltov.dynabic.com/issues/PSDNET-2212
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-278
    def PSDNET2212Test(self):
        source_file = self.GetFileInBaseFolder("input_1129.psd")
        output_file = self.GetFileInOutputFolder("output_input_1129.psd")
        source_file_size = os.path.getsize(source_file)

        load_options = PsdLoadOptions()
        load_options.allow_non_changed_layer_repaint = True

        with Image.load(source_file, load_options) as image:
                image.save(output_file)

        # Verify file size
        assert source_file_size * 1.5 >= os.path.getsize(output_file)

        # Verify file can be opened
        with Image.load(output_file) as test_image:
            print("File opened successfully")

        self.remove_all_unzipped_files()

    # The incorrect blending of pixels with transparency for some blending modes.
    # https://issue.saltov.dynabic.com/issues/PSDNET-901
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-283
    def PSDNET901Test(self):
        source_file = self.GetFileInBaseFolder("input.psd")
        output_file = self.GetFileInOutputFolder("output_input.png")
        reference_file = self.GetFileInBaseFolder("output_input.png")

        load_options = PsdLoadOptions()
        load_options.load_effects_resource = True

        with PsdImage.load(source_file, load_options) as img:
            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            img.save(output_file, pngOpt)

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)
        self.remove_all_unzipped_files()

    # Refactor layer section resources
    # https://issue.saltov.dynabic.com/issues/PSDNET-2645
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-279
    def PSDNET2645Test(self):
        src_file = self.GetFileInBaseFolder("123 1.psd")
        out_file = self.GetFileInOutputFolder("output.psd")

        load_options = PsdLoadOptions()
        load_options.load_effects_resource = True

        # Test before saving
        with Image.load(src_file, load_options) as img:
            psd_image = cast(PsdImage, img)

            assert as_of(psd_image.layers[3].resources[3], LayerSectionResource).section_type == LayerSectionType.SECTION_DIVIDER
            assert as_of(psd_image.layers[8].resources[3], LsdkResource).section_type == LayerSectionType.SECTION_DIVIDER

            assert as_of(psd_image.layers[3].resources[3], BaseLayerSectionResource).section_type == LayerSectionType.SECTION_DIVIDER
            assert as_of(psd_image.layers[8].resources[3], BaseLayerSectionResource).section_type == LayerSectionType.SECTION_DIVIDER

            assert as_of(psd_image.layers[8].resources[3], BaseLayerSectionResource).length == 4
            assert as_of(psd_image.layers[8].resources[3], BaseLayerSectionResource).blend_mode_key == BlendMode.ABSENT
            assert as_of(psd_image.layers[8].resources[3], BaseLayerSectionResource).subtype == LayerSectionSubtype.NOT_USED

            psd_image.save(out_file)

            # Test after saving
        with Image.load(src_file, load_options) as img:
            psd_image = cast(PsdImage, img)

            assert as_of(psd_image.layers[3].resources[3], LayerSectionResource).section_type == LayerSectionType.SECTION_DIVIDER
            assert as_of(psd_image.layers[8].resources[3], LsdkResource).section_type == LayerSectionType.SECTION_DIVIDER

            assert as_of(psd_image.layers[3].resources[3], BaseLayerSectionResource).section_type == LayerSectionType.SECTION_DIVIDER
            assert as_of(psd_image.layers[8].resources[3], BaseLayerSectionResource).section_type == LayerSectionType.SECTION_DIVIDER

            assert as_of(psd_image.layers[8].resources[3], BaseLayerSectionResource).length == 4
            assert as_of(psd_image.layers[8].resources[3], BaseLayerSectionResource).blend_mode_key == BlendMode.ABSENT
            assert as_of(psd_image.layers[8].resources[3], BaseLayerSectionResource).subtype == LayerSectionSubtype.NOT_USED