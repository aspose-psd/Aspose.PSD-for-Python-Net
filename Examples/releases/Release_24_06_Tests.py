import numpy as np
import pytest
from aspose.psd import Image, FontSettings
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import CompressionMethod, PsdImage
from aspose.psd.fileformats.psd.layers import TextLayer
from aspose.psd.fileformats.psd.layers.adjustmentlayers import GradientMapLayer
from aspose.psd.fileformats.psd.layers.fillsettings import GradientFillSettings, GradientType
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.psd.xmp import Namespaces, XmpPacketWrapper
from aspose.psd.xmp.schemas.xmpbaseschema import XmpBasicPackage
from aspose.pycore import cast, is_assignable

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper


class Release_24_06_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Implement support of Gradient map layer
    # https://issue.saltov.dynabic.com/issues/PSDNET-1450
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-69
    def PSDNET1450Test(self):
        sourceFile = self.GetFileInBaseFolder("gradient_map_src.psd")
        outputFile = self.GetFileInOutputFolder("gradient_map_src_output.psd")
        referenceFile = self.GetFileInBaseFolder("gradient_map_src_output.psd")

        def AssertAreEqual(expected, actual, message=None):
            if expected != actual:
                raise Exception(message or "Objects are not equal.")

        with PsdImage.load(sourceFile) as image:
            im = cast(PsdImage, image)
            layer = im.add_gradient_map_adjustment_layer()
            layer.gradient_settings.reverse = True

            im.save(outputFile)

        with PsdImage.load(outputFile) as image:
            im = cast(PsdImage, image)
            gradient_map_layer = cast(GradientMapLayer, im.layers[1])
            gradient_settings = cast(GradientFillSettings, gradient_map_layer.gradient_settings)

            AssertAreEqual(0.0, gradient_settings.angle)
            AssertAreEqual(4096, gradient_settings.interpolation)
            AssertAreEqual(True, gradient_settings.reverse)
            AssertAreEqual(False, gradient_settings.align_with_layer)
            AssertAreEqual(False, gradient_settings.dither)
            AssertAreEqual(GradientType.LINEAR, gradient_settings.gradient_type)
            AssertAreEqual(100, gradient_settings.scale)
            AssertAreEqual(0.0, gradient_settings.horizontal_offset)
            AssertAreEqual(0.0, gradient_settings.vertical_offset)
            AssertAreEqual("Custom", gradient_settings.gradient_name)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # [AI Format] Add support of XPacket Metadata to AI Format
    # https://issue.saltov.dynabic.com/issues/PSDNET-1670
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-70
    # This test ignored because Python Wrapper Can not Wrap indexers with string arguments. Fix is planned on 2024H2-2025H1
    # def PSDNET1670Test(self):
    #     sourceFile = self.GetFileInBaseFolder("ai_one.ai")
    #
    #     def AssertAreEqual(expected, actual):
    #         if expected != actual:
    #             raise Exception("Objects are not equal.")
    #
    #     def AssertIsNotNull(test_object):
    #         if test_object is None:
    #             raise Exception("Test object is null.")
    #
    #     creator_tool_key = ":CreatorTool"
    #     n_pages_key = "xmpTPg:NPages"
    #     unit_key = "stDim:unit"
    #     height_key = "stDim:h"
    #     width_key = "stDim:w"
    #
    #     expected_creator_tool = "Adobe Illustrator CC 22.1 (Windows)"
    #     expected_n_pages = "1"
    #     expected_unit = "Pixels"
    #     expected_height = 768
    #     expected_width = 1366
    #
    #     with AiImage.load(sourceFile) as img:
    #         image = cast(AiImage, img)
    #
    #         xmp_metadata = image.xmp_data
    #        # XmpPacketWrapper a
    #         AssertIsNotNull(xmp_metadata)
    #
    #         basic_package = cast(XmpBasicPackage, xmp_metadata.get_package(Namespaces.XMP_BASIC))
    #         package = xmp_metadata.packages[4]
    #
    #         creator_tool = basic_package.g[creator_tool_key].to_string()
    #         n_pages = package[n_pages_key]
    #         unit = package[unit_key]
    #         height = np.double.parse(package[height_key].to_string())
    #         width = np.double.parse(package[width_key].to_string())
    #
    #         AssertAreEqual(creator_tool, expected_creator_tool)
    #         AssertAreEqual(n_pages, expected_n_pages)
    #         AssertAreEqual(unit, expected_unit)
    #         AssertAreEqual(height, expected_height)
    #         AssertAreEqual(width, expected_width)

    # Implement Inflate, Squeeze, and Twist types of warp
    # https://issue.saltov.dynabic.com/issues/PSDNET-1831
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-71
    def PSDNET1831Test(self):
        files = ["Twist", "Squeeze", "Squeeze_vert", "Inflate"]

        for prefix in files:
            sourceFile = self.GetFileInBaseFolder(prefix + ".psd")
            ethalonFile = self.GetFileInBaseFolder(prefix + "_export.png")
            outputFile = self.GetFileInOutputFolder(prefix + "_export.png")

            loadOpt = PsdLoadOptions()
            loadOpt.allow_warp_repaint = True
            loadOpt.load_effects_resource = True

            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            with PsdImage.load(sourceFile, loadOpt) as psdImage:
                psdImage.save(outputFile, pngOpt)

            Comparison.CheckAgainstEthalon(outputFile, ethalonFile, 0)

    # Rgb and Lab modes can not contain less than 3 channels and more than 4 channels in the file with ArtBoard Layers
    # https://issue.saltov.dynabic.com/issues/PSDNET-1653
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-72
    def PSDNET1653Test(self):
        sourceFile = self.GetFileInBaseFolder("Rgb5Channels.psb")
        referenceFile = self.GetFileInBaseFolder("Rgb5Channels_output.psd")
        outputFile = self.GetFileInOutputFolder("Rgb5Channels_output.psd")

        with PsdImage.load(sourceFile) as image:
            image.save(outputFile)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0)

    # The processing area top must be positive. (Parameter ‘areaToProcess’) on the processing of specific file
    # https://issue.saltov.dynabic.com/issues/PSDNET-1775
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-73
    def PSDNET1775Test(self):
        sourceFile = self.GetFileInBaseFolder("BANNERS_2_Intel-Gamer_psak.psd")
        referenceFile = self.GetFileInBaseFolder("BANNERS_2_Intel-Gamer_psak_out.psd")
        outputFile = self.GetFileInOutputFolder("BANNERS_2_Intel-Gamer_psak_out.psd")
        psdLoadOptions = PsdLoadOptions()
        psdLoadOptions.load_effects_resource = True
        psdLoadOptions.allow_warp_repaint = True

        with PsdImage.load(sourceFile, psdLoadOptions) as image:
            image.save(outputFile)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0)

    # Expanded over the canvas image is cropped after the saving. Data is lost but Preview looks correct
    # https://issue.saltov.dynabic.com/issues/PSDNET-2052
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-74
    def PSDNET2052Test(self):
        sourceFile = self.GetFileInBaseFolder("bigfile.psd")
        referenceFile = self.GetFileInBaseFolder("bigfile_output.psd")
        outputFile = self.GetFileInOutputFolder("bigfile_output.psd")
        outputPicture = self.GetFileInOutputFolder("bigfile.png")
        referencePicture = self.GetFileInBaseFolder("bigfile_etalon.png")

        loadOptions = PsdLoadOptions()
        loadOptions.load_effects_resource = True
        loadOptions.use_disk_for_load_effects_resource = True

        with PsdImage.load(sourceFile, loadOptions) as image:
            psdImage = cast(PsdImage, image)
            psdOpt = PsdOptions()
            psdOpt.compression_method = CompressionMethod.RLE
            psdImage.save(outputFile, psdOpt)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0)

        with PsdImage.load(outputFile, loadOptions) as image:
            psdImage = cast(PsdImage, image)
            psdImage.resize(int(psdImage.width/10), int(psdImage.height/10))
            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            psdImage.save(outputPicture, PngOptions())

        Comparison.CheckAgainstEthalon(outputPicture, referencePicture, 0)

        self.remove_all_unzipped_files()

    # Expanded over the canvas image is cropped after the saving. Data is lost but Preview looks correct
    # https://issue.saltov.dynabic.com/issues/PSDNET-2105
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-56
    def PSDNET2105Test(self):
        source_file = self.GetFileInBaseFolder("source.psd")
        output_file = self.GetFileInOutputFolder("output.psd")
        reference_file = self.GetFileInBaseFolder("output.psd")

        load_options = PsdLoadOptions()
        load_options.load_effects_resource = True
        load_options.allow_warp_repaint = True
        load_options.read_only_mode = False
        load_options.ignore_text_layer_width_on_update = False

        NAME_TEXT_MAPPING = {
            'tt1_text': 'test_text at tt1_text!!!',
            'tt2_text': '中文字測試',
            'award1_text': 'text at award1 !'
        }

        with Image.load(source_file, load_options) as image:
            psdImage = cast(PsdImage, image)
            for layer in psdImage.layers:
                if NAME_TEXT_MAPPING.get(layer.name):
                    replace_text = NAME_TEXT_MAPPING.get(layer.name)
                    text_layer = cast(TextLayer, layer)
                    text_data = text_layer.text_data
                    # This will not work for Asian Fonts because Arial hasn't asian characters
                    #text_layer.update_text(replace_text)
                    textData = text_layer.text_data

                    for i in range(text_data.items.length - 1, 0, -1):
                        textData.remove_portion(i)

                    portion = textData.items[0]
                    portion.text = replace_text

                    # It's important to change the font to one which supports Asian Characters
                    font_name = FontSettings.get_adobe_font_name("Microsoft YaHei")
                    portion.style.font_name = font_name
                    textData.update_layer_data()

            psdImage.save(output_file)
            Comparison.CheckAgainstEthalon(output_file, reference_file, 1)