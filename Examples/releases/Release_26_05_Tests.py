from datetime import datetime

import pytest
from aspose.psd import Rectangle, FontSettings
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage, JustificationMode
from aspose.psd.fileformats.psd.layers import Layer, TextLayer

from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, JpegOptions
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper


class Release_26_05_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Handle Interpolation Method in Gradient Map Layer.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2721
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-299
    def PSDNET2721Test(self):
        source_files = [
            "Grdm_Classic.psd",
            "Grdm_Smooth.psd",
            "Grdm_Perceptual.psd",
            "Grdm_Linear.psd",
            "Grdm_Stripes.psd",
            "Grdm_Stripes_Blue.psd",
        ]

        for src_file_name in source_files:
            source_file = self.GetFileInBaseFolder(src_file_name)
            output_file = self.GetFileInOutputFolder("output_" + src_file_name + ".png")
            reference_file = self.GetFileInBaseFolder("output_" + src_file_name + ".png")

            load_opt = PsdLoadOptions()
            load_opt.load_effects_resource = True

            with PsdImage.load(source_file, load_opt) as img:
                psd_image = cast(PsdImage, img)
                png_opt = PngOptions()
                png_opt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
                psd_image.save(output_file, png_opt)

            Comparison.CheckAgainstEthalon(output_file, reference_file, 0)

    # Implement rendering of Gradient with Perceptual method.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2725
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-300
    def PSDNET2725Test(self):
        source_file = self.GetFileInBaseFolder("Gradients.psd")
        output_file = self.GetFileInOutputFolder("output_Gradients.png")
        reference_file = self.GetFileInBaseFolder("output_Gradients.png")

        load_opt = PsdLoadOptions()
        load_opt.load_effects_resource = True

        png_opt = PngOptions()
        png_opt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        with PsdImage.load(source_file, load_opt) as img:
            psd_image = cast(PsdImage, img)
            psd_image.save(output_file, png_opt)

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)

    # Text becomes shifted in PSD on the trying of edit after the changing of Text Layer in Aspose.PSD.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2380
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-301
    def PSDNET2380Test(self):
        input_png_path = self.GetFileInBaseFolder("9.jpg")
        output_jpg_path = self.GetFileInOutputFolder("9_OK.jpg")
        output_psd_path = self.GetFileInBaseFolder("9_OK.psd")

        # Load image as a layer from stream
        with open(input_png_path, "rb") as stream:
            background_layer = Layer(stream)  # Create layer directly from stream
            width = background_layer.width
            height = background_layer.height

            # Create a new PSD image using the layer dimensions
            with PsdImage(width, height) as psd_image:

                # Add background layer
                background_layer.name = "Background"
                psd_image.add_layer(background_layer)

                # Add text layer
                # If you also use the modern or legacy versions of Aspose.PSD and get null error, please try remove cache
                # FontSettings.remove_font_cache_file()
                text_height = 50  # Approximate text height equal to font size
                rect = Rectangle(0, int((psd_image.height - text_height) / 2), psd_image.width, psd_image.height)
                text_layer = psd_image.add_text_layer("TextLayer", rect)

                # Update text layer content
                text_data = text_layer.text_data
                text_portion = text_data.items[0]  # Get the default text portion
                text_portion.text = "今天真高兴"  # Set text content

                # Set text style
                font_name = FontSettings.get_adobe_font_name("Microsoft YaHei")
                text_portion.style.font_size = 72
                text_portion.style.font_name = font_name

                # Set paragraph style for center alignment
                text_portion.paragraph.justification = JustificationMode.CENTER

                # Update text layer data
                text_data.update_layer_data()

                # Save PSD file
                psd_image.save(output_jpg_path, JpegOptions())
                psd_image.save(output_psd_path)

        # Compare results with reference files
        ref_jpg = self.GetFileInBaseFolder(output_jpg_path)
        ref_psd = self.GetFileInBaseFolder(output_psd_path)

        Comparison.CheckAgainstEthalon(output_jpg_path, ref_jpg, 0)
        Comparison.CheckAgainstEthalon(output_psd_path, ref_psd, 0)

    # [AI Format] Resolving rendering issues with shading and soft mask.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2676
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-302
    def PSDNET2676Test(self):
        source_file_name = self.GetFileInBaseFolder("example_2.ai")
        output_file_path = self.GetFileInOutputFolder("example_2_output.png")
        reference_file = self.GetFileInBaseFolder("example_2_output.png")

        with AiImage.load(source_file_name) as img:
            image = cast(AiImage, img)
            png_opt = PngOptions()
            image.save(output_file_path, png_opt)

        Comparison.CheckAgainstEthalon(output_file_path, reference_file, 0)