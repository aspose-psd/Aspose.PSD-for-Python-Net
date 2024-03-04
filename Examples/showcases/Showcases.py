import os
from io import BytesIO

import pytest
from aspose.psd import Image, Color, ResizeType, Rectangle, Point, PointF, RasterImage
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.core.blending import BlendMode
from aspose.psd.fileformats.core.vectorpaths import BezierKnotRecord
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage, CompressionMethod, ColorModes, FontBaseline, FontCaps
from aspose.psd.fileformats.psd.layers import TextLayer, Layer, ShapeLayer, LayerMaskDataShort, LayerMaskDataFull
from aspose.psd.fileformats.psd.layers.adjustmentlayers import BrightnessContrastLayer, LevelsLayer, CurvesLayer, \
    ExposureLayer, HueSaturationLayer, ColorBalanceAdjustmentLayer, BlackWhiteAdjustmentLayer, PhotoFilterLayer, \
    ChannelMixerLayer, RgbMixerChannel, InvertAdjustmentLayer, PosterizeLayer, ThresholdLayer, SelectiveColorLayer, \
    SelectiveColorsTypes, CmykCorrection
from aspose.psd.fileformats.psd.layers.filllayers import FillLayer
from aspose.psd.fileformats.psd.layers.fillsettings import GradientColorPoint, GradientTransparencyPoint, FillType, \
    ColorFillSettings, GradientFillSettings, PatternFillSettings
from aspose.psd.fileformats.psd.layers.layerresources import CurvesManager, CurvesContinuousManager, PathShape
from aspose.psd.fileformats.psd.layers.smartfilters import SharpenSmartFilter, NoiseDistribution, \
    GaussianBlurSmartFilter, AddNoiseSmartFilter
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.fileformats.tiff.enums import TiffExpectedFormat
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PsdOptions, PngOptions, PdfOptions, TiffOptions, JpegOptions, BmpOptions, \
    Jpeg2000Options, GifOptions
from aspose.psd.sources import StreamSource
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

    def create_regular_layer(self, left, top, width, height):
        layer = Layer()
        layer.left = left
        layer.top = top
        layer.right = left + width
        layer.bottom = top + height

        color = Color.aqua.to_argb()
        test_data = [color] * width * height
        layer.save_argb_32_pixels(layer.bounds, test_data)

        return layer

    def FillLayerManipulationTest(self):
        outputPng = self.GetFileInOutputFolderByIssue("ShowCases", "all_fill_layers.png")
        outputPsd = self.GetFileInOutputFolderByIssue("ShowCases", "all_fill_layers.psd")

        with PsdImage(100, 100) as image:
            layer1 = self.create_regular_layer(0, 0, 50, 50)
            image.add_layer(layer1)

            colorFillLayer = FillLayer.create_instance(FillType.COLOR)
            colorFillSettings = cast(ColorFillSettings, colorFillLayer.fill_settings)
            colorFillSettings.color = Color.coral
            colorFillLayer.clipping = 1

            colorFillLayer.display_name = "Color Fill Layer"
            image.add_layer(colorFillLayer)

            layer2 = self.create_regular_layer(50, 0, 50, 50)
            image.add_layer(layer2)

            gradientColorPoints = [
                GradientColorPoint(Color.red, 2048, 50),
                GradientColorPoint(Color.green, 3072, 50),
                GradientColorPoint(Color.blue, 4096, 50)
            ]

            tp1 = GradientTransparencyPoint()
            tp1.location = 0
            tp1.median_point_location = 50
            tp1.opacity = 128

            tp2 = GradientTransparencyPoint()
            tp2.location = 2048
            tp2.median_point_location = 50
            tp2.opacity = 176
            gradientTransparencyPoints = [tp1, tp2]

            gradientFillLayer = FillLayer.create_instance(FillType.GRADIENT)
            gradientFillLayer.display_name = "Gradient Fill Layer"
            gradientFillSettings = cast(GradientFillSettings, gradientFillLayer.fill_settings)
            gradientFillSettings.color_points = gradientColorPoints
            gradientFillSettings.angle = -45
            gradientFillSettings.transparency_points = gradientTransparencyPoints
            gradientFillLayer.clipping = 1
            image.add_layer(gradientFillLayer)

            layer3 = self.create_regular_layer(0, 50, 50, 50)
            image.add_layer(layer3)

            patternFillLayer = FillLayer.create_instance(FillType.PATTERN)
            patternFillLayer.display_name = "Pattern Fill Layer"
            patternFillLayer.opacity = 50
            patternFillLayer.clipping = 1
            patternFillSettings = cast(PatternFillSettings, patternFillLayer.fill_settings)
            patternFillSettings.pattern_data = [
                Color.red.to_argb(), Color.transparent.to_argb(), Color.transparent.to_argb(),
                Color.transparent.to_argb(), Color.red.to_argb(), Color.transparent.to_argb(),
                Color.transparent.to_argb(), Color.transparent.to_argb(), Color.red.to_argb()
            ]

            patternFillSettings.pattern_width = 3
            patternFillSettings.pattern_height = 3
            image.add_layer(patternFillLayer)

            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            image.save(outputPng, pngOpt)
            image.save(outputPsd)

    def LayerGroupManipulationTest(self):
        outputPsd = self.GetFileInOutputFolderByIssue("ShowCases", "LayerGroup.psd")

        psd_options = PsdOptions()
        stream = BytesIO()
        psd_options.source = StreamSource(stream)

        with PsdImage.create(psd_options, 100, 100) as image:
            psd_image = cast(PsdImage, image)
            layer_group = psd_image.add_layer_group("Folder", 0, True)
            layer1 = Layer()
            layer1.display_name = "Layer 1"
            layer2 = Layer()
            layer2.display_name = "Layer 2"
            layer_group.add_layer(layer1)
            layer_group.add_layer(layer2)

            assert layer_group.layers[0].display_name == "Layer 1"
            assert layer_group.layers[1].display_name == "Layer 2"

            psd_image.save(outputPsd)

    def LayerManipulationTest(self):
        source = self.GetFileInBaseFolderByIssue("ShowCases", "AllTypesLayerPsd2.psd")
        output_original = self.GetFileInOutputFolder("original_layer_manipulation.png")
        output_updated = self.GetFileInOutputFolder("updated_layer_manipulation.png")
        pngOpt = PngOptions()
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        psdLoadOpt = PsdLoadOptions()
        psdLoadOpt.load_effects_resource = True
        psdLoadOpt.allow_warp_repaint = True

        with Image.load(source, psdLoadOpt) as image:
            psd_image = cast(PsdImage, image)
            psd_image.save(output_original, pngOpt)

            # Resizing
            psd_image.layers[2].resize(25, 25, ResizeType.HIGH_QUALITY_RESAMPLE)

            # Rotating
            psd_image.layers[5].rotate(45, True, Color.yellow)

            # Simple Filters
            psd_image.layers[3].adjust_contrast(3)

            # Cropping
            psd_image.layers[10].crop(Rectangle(10, 10, 20, 20))
            # Aspose.PSD supports much more specific layer manipulation, please check https://reference.aspose.com/psd/python-net/

            psd_image.save(output_updated, pngOpt)

    def PointFToResourcePoint(self, point, imageSize):
        ImgToPsdRatio = 256 * 65535
        return Point(int(point.y * (ImgToPsdRatio / imageSize.height)), int(point.x * (ImgToPsdRatio / imageSize.width)))

    def ShapeLayerPathManipulationTest(self):
        sourceFileName = self.GetFileInBaseFolderByIssue("ShowCases", "ShapeLayerTest.psd")
        originalOutput = self.GetFileInOutputFolder("ShapeLayerTest_Res_or.psd")
        updatedOutput = self.GetFileInOutputFolder("ShapeLayerTest_Res_up.psd")

        with Image.load(sourceFileName) as image:
            im = cast(PsdImage, image)
            im.save(originalOutput)
            for layer in im.layers:
                # Finding Shape Layer
                if is_assignable(layer, ShapeLayer):
                    shapeLayer = cast(ShapeLayer, layer)
                    path = shapeLayer.path
                    pathShapes = path.get_items()
                    knotsList = []
                    for pathShape in pathShapes:
                        knots = pathShape.get_items()
                        knotsList.extend(knots)

                    # Change Path Shape properties
                    newShape = PathShape()

                    bn1 = BezierKnotRecord()
                    bn1.is_linked = True
                    bn1.points = [
                        self.PointFToResourcePoint(PointF(20, 100), shapeLayer.container.size),
                        self.PointFToResourcePoint(PointF(20, 100), shapeLayer.container.size),
                        self.PointFToResourcePoint(PointF(20, 100), shapeLayer.container.size),
                    ]

                    bn2 = BezierKnotRecord()
                    bn2.is_linked = True
                    bn2.points = [
                        self.PointFToResourcePoint(PointF(20, 490), shapeLayer.container.size),
                        self.PointFToResourcePoint(PointF(20, 490), shapeLayer.container.size),
                        self.PointFToResourcePoint(PointF(20, 490), shapeLayer.container.size),
                    ]

                    bn3 = BezierKnotRecord()
                    bn3.is_linked = True
                    bn3.points = [
                        self.PointFToResourcePoint(PointF(490, 20), shapeLayer.container.size),
                        self.PointFToResourcePoint(PointF(490, 20), shapeLayer.container.size),
                        self.PointFToResourcePoint(PointF(490, 20), shapeLayer.container.size),
                    ]

                    bezierKnots = [bn1, bn2, bn3]
                    newShape.set_items(bezierKnots)

                    newShapes = list(pathShapes)
                    newShapes.append(newShape)

                    pathShapeNew = newShapes
                    path.set_items(pathShapeNew)

                    shapeLayer.update()

                    im.save(updatedOutput)

                    break

    def SmartFilterDirectApply(self):
        source = self.GetFileInBaseFolderByIssue("ShowCases", "VerySmoothPicture.psd")
        output_original = self.GetFileInOutputFolder("original_smart.psd")
        output_updated = self.GetFileInOutputFolder("output_updated.psd")
        #renderCount = 10

        with Image.load(source) as image:
            im = cast(PsdImage, image)
            im.save(output_original)
            sharpenFilter = SharpenSmartFilter()
            regularLayer = im.layers[1]
            for i in range(3):
                sharpenFilter.apply(regularLayer)

            im.save(output_updated)

    def SmartFilterFeaturesTest(self):
        source = self.GetFileInBaseFolderByIssue("ShowCases", "r2_SmartFilters.psd")
        output_original = self.GetFileInOutputFolder("original_smart_features.psd")
        output_updated = self.GetFileInOutputFolder("output_updated_features.psd")

        with Image.load(source) as image:
            im = cast(PsdImage, image)
            im.save(output_original)
            smartObj = cast(SmartObjectLayer, im.layers[1])

            # edit smart filters
            gaussianBlur = cast(GaussianBlurSmartFilter, smartObj.smart_filters.filters[0])

            # update filter values including blend mode
            gaussianBlur.radius = 1
            gaussianBlur.blend_mode = BlendMode.DIVIDE
            gaussianBlur.opacity = 75
            gaussianBlur.is_enabled = False

            # Working with Add Noise Smart Filter
            addNoise = cast(AddNoiseSmartFilter, smartObj.smart_filters.filters[1])
            addNoise.distribution = NoiseDistribution.UNIFORM

            # add new filter items
            filters = list(smartObj.smart_filters.filters)
            filters.append(GaussianBlurSmartFilter())
            filters.append(AddNoiseSmartFilter())
            smartObj.smart_filters.filters = filters

            # apply changes
            smartObj.smart_filters.update_resource_values()

            # Apply filters directly to layer and mask of layer
            smartObj.smart_filters.filters[0].apply(im.layers[2])
            smartObj.smart_filters.filters[4].apply_to_mask(im.layers[2])

            im.save(output_updated)

    # Just inverts all data of image
    def invert_image(self, image):
        pixels = image.load_argb_32_pixels(image.bounds)
        for i in range(len(pixels)):
            pixel = pixels[i]
            alpha = pixel & 0xff000000
            pixels[i] = (~ (pixel & 0x00ffffff)) | alpha

        image.save_argb_32_pixels(image.bounds, pixels)

    # Demonstation of API to work woth Smart Object Layers
    def SmartObjectManipulationTest(self):
        source = self.GetFileInBaseFolderByIssue("ShowCases", "new_panama-papers-8-trans4.psd")
        export_content_path = self.GetFileInOutputFolder("export_content.jpg")
        output_original = self.GetFileInOutputFolder("smart_object_orig.psd")
        output_updated = self.GetFileInOutputFolder("smart_object.psd")

        with Image.load(source) as image:
            im = cast(PsdImage, image)
            im.save(output_original)
            smartLayer = cast(SmartObjectLayer, im.layers[0])

            # How to export content of Smart Object
            smartLayer.export_contents(export_content_path)

            # Creating Smart Object as a Copy
            newLayer = smartLayer.new_smart_object_via_copy()
            newLayer.is_visible = False
            newLayer.display_name = "Duplicate"

            # Get the content of Smart Object for manipulation
            with smartLayer.load_contents(None) as innerImage:
                layer = cast(RasterImage, innerImage)
                self.invert_image(layer)
                smartLayer.replace_contents(layer)

            im.smart_object_provider.update_all_modified_content()

            psd_options = PsdOptions(im)
            im.save(output_updated, psd_options)

    def TextLayerUpdatingTest(self):
        source_file = self.GetFileInBaseFolderByIssue("ShowCases", "text212.psd")
        output_file = self.GetFileInOutputFolder("Output_text212.psd")

        with PsdImage.load(source_file) as img:
            image = cast(PsdImage, img)
            # Smple way to update text layer
            simple_text = cast(TextLayer, image.layers[2])
            simple_text.update_text("Update", Color.red)

            # More powerful way to updateText Layer - using Text Portions with different styles and paragraphs
            text_layer = cast(TextLayer, image.layers[1])
            text_data = text_layer.text_data

            default_style = text_data.produce_portion().style
            default_paragraph = text_data.produce_portion().paragraph

            default_style.fill_color = Color.from_name("DimGray")
            default_style.font_size = 51

            text_data.items[1].style.strikethrough = True

            new_portions = text_data.produce_portions(
                [
                    "E=mc",
                    "2\r",
                    "Bold",
                    "Italic\r",
                    "Lowercasetext"
                ],
                default_style,
                default_paragraph
            )

            new_portions[0].style.underline = True  # edit text style "E=mc"
            new_portions[1].style.font_baseline = FontBaseline.SUPERSCRIPT  # edit text style "2\r"
            new_portions[2].style.faux_bold = True  # edit text style "Bold"
            new_portions[3].style.faux_italic = True  # edit text style "Italic\r"
            new_portions[3].style.baseline_shift = -25  # edit text style "Italic\r"
            new_portions[4].style.font_caps = FontCaps.SMALL_CAPS  # edit text style "Lowercasetext"

            for new_portion in new_portions:
                text_data.add_portion(new_portion)

            text_data.update_layer_data()
            image.save(output_file)

    def LayerMasksEditingTest(self):
        source = self.GetFileInBaseFolderByIssue("ShowCases", "MaskExample.psd")
        output_original = self.GetFileInOutputFolder("original_mask_features.psd")
        output_updated = self.GetFileInOutputFolder("updated_mask_features.psd")
        with PsdImage.load(source) as img:
            image = cast(PsdImage, img)
            image.save(output_original)

            # The most simple is the using of Clipping masks
            # Some Layer and Adjustment Layer Become Clipping Masks
            image.layers[4].clipping = 1
            image.layers[5].clipping = 1

            # Example how to add Mask to Layer
            mask = LayerMaskDataShort()
            mask.left = 50
            mask.top = 213
            mask.right = mask.left + 150
            mask.bottom = mask.top + 150
            maskData = [bytes] * (mask.right - mask.left) * (mask.bottom - mask.top)
            for index in range(len(maskData)):
                maskData[index] = 100 + index % 100

            byteMask = bytes(maskData)
            mask.image_data = byteMask
            image.layers[2].add_layer_mask(mask)

            image.save(output_updated)




















