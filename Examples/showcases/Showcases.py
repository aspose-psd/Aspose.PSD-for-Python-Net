import os

import pytest
from aspose.psd import Image, Color
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.core.blending import BlendMode
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage, CompressionMethod, ColorModes
from aspose.psd.fileformats.psd.layers import TextLayer
from aspose.psd.fileformats.psd.layers.adjustmentlayers import BrightnessContrastLayer, LevelsLayer, CurvesLayer, \
    ExposureLayer, HueSaturationLayer, ColorBalanceAdjustmentLayer, BlackWhiteAdjustmentLayer, PhotoFilterLayer, \
    ChannelMixerLayer, RgbMixerChannel, InvertAdjustmentLayer, PosterizeLayer, ThresholdLayer, SelectiveColorLayer, \
    SelectiveColorsTypes, CmykCorrection
from aspose.psd.fileformats.psd.layers.fillsettings import GradientColorPoint, GradientTransparencyPoint, FillType, \
    ColorFillSettings, GradientFillSettings, PatternFillSettings
from aspose.psd.fileformats.psd.layers.layerresources import CurvesManager, CurvesContinuousManager
from aspose.psd.fileformats.tiff.enums import TiffExpectedFormat
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PsdOptions, PngOptions, PdfOptions, TiffOptions, JpegOptions, BmpOptions, \
    Jpeg2000Options, GifOptions
from aspose.pycore import cast, is_assignable

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper


class Showcases(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    def ConvertBetweenColorModesAndBitDepthTest(self):
        source_file_name = self.GetFileInBaseFolderByIssue("ShowCases", "John-OConnor_Spring-Reflections_example.psd")
        output_file_name = self.GetFileInOutputFolder("result.psd")

        with PsdImage.load(source_file_name) as image:
            psdSaveOpt = PsdOptions()
            psdSaveOpt.channels_count = 5
            psdSaveOpt.color_mode = ColorModes.CMYK
            psdSaveOpt.compression_method = CompressionMethod.RLE
            image.save(output_file_name, psdSaveOpt)

    def ManipulatingBlendingOptionsTest(self):
        source = self.GetFileInBaseFolderByIssue("ShowCases", "AllTypesLayerPsd2.psd")
        output_original = self.GetFileInOutputFolder("original.png")
        output_updated = self.GetFileInOutputFolder("output_updated.png")

        with PsdImage.load(source) as image:
            psdImage = cast(PsdImage, image)
            pngSaveOpt = PngOptions()
            pngSaveOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            image.save(output_original, pngSaveOpt)

            # Change opacity and/or blending mode of layer
            psdImage.layers[1].opacity = 100
            psdImage.layers[4].blend_mode_key = BlendMode.HUE

            # Add effects and set it up
            shadow = psdImage.layers[7].blending_options.add_drop_shadow()
            shadow.angle = 30
            shadow.color = Color.from_argb(255, 255, 0)

            psdImage.layers[9].blend_mode_key = BlendMode.LIGHTEN
            colorOverlay = psdImage.layers[5].blending_options.add_color_overlay()
            colorOverlay.color = Color.from_argb(200, 30, 50)
            colorOverlay.opacity = 150
            image.save(output_updated, pngSaveOpt)


    def LayerEffectsTest(self):
        source = self.GetFileInBaseFolderByIssue("ShowCases", "AllTypesLayerPsd2.psd")
        output_original = self.GetFileInOutputFolder("original.png")
        output_updated = self.GetFileInOutputFolder("output_updated.png")

        with PsdImage.load(source) as image:
            psdImage = cast(PsdImage, image)
            pngSaveOpt = PngOptions()
            pngSaveOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            image.save(output_original, pngSaveOpt)

            # Change opacity and/or blending mode of layer
            psdImage.layers[1].opacity = 100
            psdImage.layers[4].blend_mode_key = BlendMode.HUE

            # Add effects and set it up
            shadow = psdImage.layers[7].blending_options.add_drop_shadow()
            shadow.angle = 30
            shadow.color = Color.from_argb(255, 255, 0)

            psdImage.layers[9].blend_mode_key = BlendMode.LIGHTEN
            colorOverlay = psdImage.layers[5].blending_options.add_color_overlay()
            colorOverlay.color = Color.from_argb(200, 30, 50)
            colorOverlay.opacity = 150
            image.save(output_updated, pngSaveOpt)

    def LayerEffectsFullTest(self):
        source = self.GetFileInBaseFolderByIssue("ShowCases", "nines.psd")
        result_orig = self.GetFileInOutputFolder("nines_orig.png")
        result_psd = self.GetFileInOutputFolder("nines_mod.psd")
        result_mod = self.GetFileInOutputFolder("nines_mod.png")

        # Set the PNG options
        png_opt = PngOptions()
        png_opt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        # Set the PSD load options
        psd_opt = PsdLoadOptions()
        psd_opt.load_effects_resource = True

        # Load the PSD image
        with Image.load(source, psd_opt) as img:
            # Cast to PsdImage
            image = cast(PsdImage, img)

            # Save the original image as PNG
            image.save(result_orig, png_opt)

            # Test data for gradient
            gradient_color_points = [
                GradientColorPoint(Color.red, 0, 50),
                GradientColorPoint(Color.green, 1024, 50),
                GradientColorPoint(Color.blue, 2048, 50)
            ]

            tp1 = GradientTransparencyPoint()
            tp1.location = 0
            tp1.median_point_location = 50
            tp1.opacity = 128

            tp2 = GradientTransparencyPoint()
            tp2.location = 2048
            tp2.median_point_location = 50
            tp2.opacity = 176
            gradient_transparency_points = [tp1, tp2]

            # Add stroke to layer 1
            stroke = image.layers[1].blending_options.add_stroke(FillType.GRADIENT)
            stroke.size = 3
            gradient_fill = cast(GradientFillSettings, stroke.fill_settings)
            gradient_fill.color_points = gradient_color_points
            gradient_fill.transparency_points = gradient_transparency_points

            # Add inner shadow to layer 2
            inner_shadow = image.layers[2].blending_options.add_inner_shadow()
            inner_shadow.angle = 60
            inner_shadow.color = Color.yellow

            # Add drop shadow to layer 3
            drop_shadow = image.layers[3].blending_options.add_drop_shadow()
            drop_shadow.angle = 30
            drop_shadow.color = Color.violet

            # Add gradient overlay to layer 4
            gradient_overlay = image.layers[4].blending_options.add_gradient_overlay()
            gradient_overlay.settings.color_points = gradient_color_points
            gradient_overlay.settings.transparency_points = gradient_transparency_points

            # Add color overlay to layer 5
            color_overlay = image.layers[5].blending_options.add_color_overlay()
            color_overlay.color = Color.azure
            color_overlay.opacity = 120

            # Add pattern overlay to layer 6
            pattern_overlay = image.layers[6].blending_options.add_pattern_overlay()

            patSettings = cast(PatternFillSettings, pattern_overlay.settings)

            patSettings.pattern_data = [
                Color.red.to_argb(), Color.transparent.to_argb(),
                Color.transparent.to_argb(), Color.red.to_argb()
            ]

            patSettings.pattern_width = 2
            patSettings.pattern_height = 2

            # Add outer glow to layer 7
            outer_glow = image.layers[7].blending_options.add_outer_glow()
            outer_glow.size = 10
            outer_glow.fill_color = ColorFillSettings()
            outer_glow.fill_color.color = Color.crimson

            # Save the modified image as PNG and PSD
            image.save(result_mod, png_opt)
            image.save(result_psd)

    def ExportPsdAndAIToDifferentFormatsTest(self):
        # Saving to PNG
        pngSaveOpt = PngOptions()
        pngSaveOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        # Saving to PDF
        pdfSaveOpt = PdfOptions()

        # Saving to Tiff
        tiffSaveOpt = TiffOptions(TiffExpectedFormat.TIFF_NO_COMPRESSION_RGBA)

        # Saving to Jpeg
        jpegSaveOpt = JpegOptions()
        jpegSaveOpt.quality = 90

        # Saving to BMP
        bmpSaveOpt = BmpOptions()

        # Saving to JPEG2000
        j2kSaveOpt = Jpeg2000Options()

        # Saving to GIF
        gifSaveOpt = GifOptions()

        # Saving to PSB
        psbSaveOpt = PsdOptions()
        psbSaveOpt.version = 2

        # Saving to PSD
        psdSaveOpt = PsdOptions()

        formats = {
            "pdf": pdfSaveOpt,
            "jpg": jpegSaveOpt,
            "png": pngSaveOpt,
            "tif": tiffSaveOpt,
            "gif": gifSaveOpt,
            "j2k": j2kSaveOpt,
            "bmp": bmpSaveOpt,
            "psb": psbSaveOpt,
            "psd": psdSaveOpt
        }

        # Saving PSD to other formats
        sourcePsd = self.GetFileInBaseFolderByIssue("ShowCases", "AllTypesLayerPsd2.psd")

        with PsdImage.load(sourcePsd) as image:
            for format, saveOpt in formats.items():
                fn = self.GetFileInOutputFolderByIssue("ShowCases", "export.psd.to." + format)
                image.save(fn, saveOpt)

        # Saving AI to other formats
        sourceAi = self.GetFileInBaseFolderByIssue("ShowCases", "ai_one_text_3.ai")
        with AiImage.load(sourceAi) as image:
            for format, saveOpt in formats.items():
                fn = self.GetFileInOutputFolderByIssue("ShowCases", "export.ai.to." + format)
                image.save(fn, saveOpt)

    def AdjustmentLayerEnhancementTest(self):
        sourcePsd = self.GetFileInBaseFolderByIssue("ShowCases", "AllAdjustments.psd")
        outputOrigPng = self.GetFileInOutputFolderByIssue("ShowCases", "AllAdjustments_orig.png")
        outputModPng = self.GetFileInOutputFolderByIssue("ShowCases", "AllAdjustments_mod.png")
        pngOpt = PngOptions()
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        with PsdImage.load(sourcePsd) as image:
            psdImage = cast(PsdImage, image)
            psdImage.save(outputOrigPng, pngOpt)
            layers = psdImage.layers

            for layer in layers:
                if is_assignable(layer, BrightnessContrastLayer):
                    br = cast(BrightnessContrastLayer, layer)
                    br.brightness = -br.brightness
                    br.contrast = -br.contrast

                if is_assignable(layer, LevelsLayer):
                    levels = cast(LevelsLayer, layer)
                    levels.master_channel.output_shadow_level = 30
                    levels.master_channel.input_shadow_level = 5
                    levels.master_channel.input_midtone_level = 2
                    levels.master_channel.output_highlight_level = 213
                    levels.master_channel.input_highlight_level = 120

                if is_assignable(layer, CurvesLayer):
                    curves = cast(CurvesLayer, layer)
                    manager = curves.get_curves_manager()
                    curveManager = cast(CurvesContinuousManager, manager)
                    curveManager.add_curve_point(2, 150, 180)

                if is_assignable(layer, ExposureLayer):
                    exp = cast(ExposureLayer, layer)
                    exp.exposure = exp.exposure + 0.1

                if is_assignable(layer, HueSaturationLayer):
                    hue = cast(HueSaturationLayer, layer)
                    hue.hue = -15
                    hue.saturation = 30

                if is_assignable(layer, ColorBalanceAdjustmentLayer):
                    colorBal = cast(ColorBalanceAdjustmentLayer, layer)
                    colorBal.midtones_cyan_red_balance = 30

                if is_assignable(layer, BlackWhiteAdjustmentLayer):
                    bw = cast(BlackWhiteAdjustmentLayer, layer)
                    bw.reds = 30
                    bw.greens = 25
                    bw.blues = 40

                if is_assignable(layer, PhotoFilterLayer):
                    photoFilter = cast(PhotoFilterLayer, layer)
                    photoFilter.color = Color.azure

                if is_assignable(layer, ChannelMixerLayer):
                    channelMixer = cast(ChannelMixerLayer, layer)
                    channel = channelMixer.get_channel_by_index(0)
                    if is_assignable(channel, RgbMixerChannel):
                        rgbChannel = cast(RgbMixerChannel, channel)
                        rgbChannel.green = 120
                        rgbChannel.red = 50
                        rgbChannel.blue = 70
                        rgbChannel.constant += 10

                if is_assignable(layer, InvertAdjustmentLayer):
                    # Here is nothing to do ¯\_(ツ)_/¯ If this layer is presented than all colors will be inverted under it.
                    # Also, you can add it to the new image
                    #img = PsdImage(100, 100)
                    #img.AddInvertAdjustmentLayer()
                    pass

                if is_assignable(layer, PosterizeLayer):
                    post = cast(PosterizeLayer, layer)
                    post.levels = 3

                if is_assignable(layer, ThresholdLayer):
                    threshold = cast(ThresholdLayer, layer)
                    threshold.level = 15

                if is_assignable(layer, SelectiveColorLayer):
                    selectiveColor = cast(SelectiveColorLayer, layer)
                    correction = CmykCorrection()
                    correction.cyan = 25
                    correction.magenta = 10
                    correction.yellow = -15
                    correction.black = 5
                    selectiveColor.set_cmyk_correction(SelectiveColorsTypes.CYANS, correction)

            psdImage.save(outputModPng, pngOpt)












