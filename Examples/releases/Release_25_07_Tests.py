import pytest
from aspose.psd import Rectangle, Image
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers import TextLayer, Layer
from aspose.psd.fileformats.psd.layers.fillsettings import GradientType, GradientFillSettings
from aspose.psd.fileformats.psd.layers.gradient import NoiseGradient, GradientKind, NoiseColorModel, SolidGradient
from aspose.psd.fileformats.psd.layers.layereffects import StrokeEffect
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import cast, as_of, is_assignable

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_25_07_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Add support for exporting Layers with Layer Effects to raster formats
    # https://issue.saltov.dynabic.com/issues/PSDNET-1958
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-205
    def PSDNET1958Test(self):
        srcFile = self.GetFileInBaseFolder("1958.psd")
        outputFile = self.GetFileInOutputFolder("out_1958.png")
        reference = self.GetFileInBaseFolder("out_1958.png")

        loadOpt = PsdLoadOptions()
        loadOpt.load_effects_resource = True
        with PsdImage.load(srcFile, loadOpt) as img:
            psdImage = cast(PsdImage, img)
            layer1 = psdImage.layers[1]

            layerBounds = layer1.bounds
            for effect in layer1.blending_options.effects:
                effectBounds = effect.get_effect_bounds(layer1.bounds, psdImage.global_angle)
                layerBounds = Rectangle.union(layerBounds, effectBounds)

            boundsToExport = Rectangle.empty  # The default value is to save only the layer with effects.
            # boundsToExport = psdImage.bounds  # To save within the PsdImage bounds at the original layer location

            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            layer1.save(
                outputFile,
                pngOpt,
                boundsToExport)

            with open(outputFile, 'rb') as imgStream:
                loadedLayer = Layer(imgStream)
                if loadedLayer.size == layerBounds.size:
                    print("The size is calculated correctly.")

            Comparison.CheckAgainstEthalon(outputFile, reference, 0, 1)

    # Add a property to toggle all layer effects visibility.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2485
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-206
    def PSDNET2485Test(self):
        srcFile = self.GetFileInBaseFolder("2485.psd")
        outputOnFile = self.GetFileInOutputFolder("on_2485.png")
        outputOffFile = self.GetFileInOutputFolder("off_2485.png")
        referenceOnFile = self.GetFileInBaseFolder("on_2485.png")
        referenceOffFile = self.GetFileInBaseFolder("off_2485.png")

        loadOpt = PsdLoadOptions()
        loadOpt.load_effects_resource = True
        with PsdImage.load(srcFile, loadOpt) as img:
            psdImage = cast(PsdImage, img)
            psdImage.save(outputOnFile)
            psdImage.layers[1].blending_options.are_effects_enabled = False
            psdImage.save(outputOffFile)

        Comparison.CheckAgainstEthalon(outputOnFile, referenceOnFile, 0, 1)
        Comparison.CheckAgainstEthalon(outputOffFile, referenceOffFile, 0, 1)


    # Update the structure of Gradient classes. Create base class for Gradient specific classes.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2282
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-209
    def PSDNET2282Test(self):
        inputFile = self.GetFileInBaseFolder("StrokeNoise.psd")
        outputFile = self.GetFileInOutputFolder("output.psd")
        referenceFile = self.GetFileInBaseFolder("output.psd")

        loadOpt = PsdLoadOptions()
        loadOpt.load_effects_resource = True

        # First pass - load and modify
        with PsdImage.load(inputFile, loadOpt) as img:
            psdImage = cast(PsdImage, img)
            gradientStroke = cast(StrokeEffect, psdImage.layers[0].blending_options.effects[0])
            gradientFillSettings = cast(GradientFillSettings, gradientStroke.fill_settings)

            # Check common gradient fill settings properties
            assert gradientFillSettings is not None
            assert gradientFillSettings.align_with_layer == True
            assert gradientFillSettings.dither == True
            assert gradientFillSettings.reverse == True
            assert gradientFillSettings.angle == 116.0
            assert gradientFillSettings.scale == 122
            assert gradientFillSettings.gradient_type == GradientType.ANGLE

            # Check Noise gradient properties
            noiseGradient = cast(NoiseGradient, gradientFillSettings.gradient)
            assert noiseGradient is not None
            assert noiseGradient.gradient_mode == GradientKind.NOISE
            assert noiseGradient.rnd_number_seed == 2107422935
            assert noiseGradient.show_transparency == False
            assert noiseGradient.use_vector_color == False
            assert noiseGradient.roughness == 2048
            assert noiseGradient.color_model == NoiseColorModel.RGB
            assert noiseGradient.minimum_color.get_as_long() == 0
            assert noiseGradient.maximum_color.get_as_long() == 28147819798528050

            # Change gradient settings
            gradientFillSettings.align_with_layer = False
            gradientFillSettings.dither = False
            gradientFillSettings.reverse = False
            gradientFillSettings.angle = 30
            gradientFillSettings.scale = 80
            gradientFillSettings.gradient_type = GradientType.LINEAR

            solidGradient = SolidGradient()
            solidGradient.interpolation = 2048
            solidGradient.color_points[0].raw_color.components[0].value = 255  # A
            solidGradient.color_points[0].raw_color.components[1].value = 255  # R
            solidGradient.color_points[0].raw_color.components[2].value = 0  # G
            solidGradient.color_points[0].raw_color.components[3].value = 0  # B
            solidGradient.transparency_points[1].opacity = 50
            gradientFillSettings.gradient = solidGradient

            psdImage.save(outputFile)

        # Second pass - verify changes
        with PsdImage.load(outputFile) as img:
            psdImage = cast(PsdImage, img)
            gradientStroke = cast(StrokeEffect, psdImage.layers[0].blending_options.effects[0])
            gradientFillSettings = cast(GradientFillSettings, gradientStroke.fill_settings)

            # Check common gradient fill settings properties
            assert gradientFillSettings is not None
            assert gradientFillSettings.align_with_layer == False
            assert gradientFillSettings.dither == False
            assert gradientFillSettings.reverse == False
            assert gradientFillSettings.angle == 30.0
            assert gradientFillSettings.scale == 80
            assert gradientFillSettings.gradient_type == GradientType.LINEAR

            solidGradient = cast(SolidGradient, gradientFillSettings.gradient)
            assert solidGradient is not None
            assert solidGradient.interpolation == 2048
            assert solidGradient.color_points[0].raw_color.components[0].value == 255
            assert solidGradient.color_points[0].raw_color.components[1].value == 255
            assert solidGradient.color_points[0].raw_color.components[2].value == 0
            assert solidGradient.color_points[0].raw_color.components[3].value == 0
            assert solidGradient.transparency_points[1].opacity == 50.0

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # Make correct initializing of Layers with Linked Layers Registry
    # https://issue.saltov.dynabic.com/issues/PSDNET-1818
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-212
    def PSDNET1818Test(self):
        files = ["add.jpg", "add.psd"]

        for i in range(len(files)):
            sourceFile = self.GetFileInBaseFolder("input.psd")
            addFile = self.GetFileInBaseFolder(files[i])
            outputFile = self.GetFileInOutputFolder("output.psd")
            refFile = self.GetFileInBaseFolder("output.psd")

            with PsdImage.load(sourceFile) as img:
                psdImage = cast(PsdImage, img)
                with open(addFile, 'rb') as stream:
                    with SmartObjectLayer(stream) as smartLayer:
                        psdImage.add_layer(smartLayer)

                        layer1 = psdImage.layers[1]
                        layer2 = psdImage.layers[2]

                        size1Before = layer1.size
                        size2Before = layer2.size

                        psdImage.linked_layers_manager.link_layers([layer1, layer2])

                        layer1.resize(100, 100)

                        size1After = layer1.size
                        size2After = layer2.size

                        assert size1Before != size1After
                        assert size2Before != size2After
                        psdImage.save(outputFile)

            # Result file is weird
            #Comparison.CheckAgainstEthalon(outputFile, refFile, 0, 1)

    # Inaccurate rendering of Smart Object Layer
    # https://issue.saltov.dynabic.com/issues/PSDNET-2411
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-219
    def PSDNET2411Test(self):
        sourceFile = self.GetFileInBaseFolder("test.psd")
        newContent = self.GetFileInBaseFolder("newImage.png")
        export = self.GetFileInOutputFolder("export.png")
        reference = self.GetFileInBaseFolder("export.png")

        loadOpt = PsdLoadOptions()
        loadOpt.allow_warp_repaint = True

        with PsdImage.load(sourceFile, loadOpt) as img:
            psdImage = cast(PsdImage, img)
            with Image.load(newContent) as replaceImage:
                layers = psdImage.layers
                for i in range(len(layers)):
                    if isinstance(layers[i], SmartObjectLayer):
                        smart_layer = cast(SmartObjectLayer, layers[i])
                        smart_layer.replace_contents(replaceImage)
                        smart_layer.update_modified_content()
                        break

            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            psdImage.save(export, pngOpt)

        Comparison.CheckAgainstEthalon(export, reference, 0, 1)

    # Error when applying deformation due to invalid ‘Processing Area’ value is 2
    # https://issue.saltov.dynabic.com/issues/PSDNET-2451
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-220
    def PSDNET2451Test(self):
        sourceFile = self.GetFileInBaseFolder("Warping.psd")
        outputFile = self.GetFileInOutputFolder("export2.png")
        referenceFile = self.GetFileInBaseFolder("export2.png")

        loadOpt = PsdLoadOptions()
        loadOpt.load_effects_resource = True
        loadOpt.allow_warp_repaint = True

        with PsdImage.load(sourceFile, loadOpt) as img:
            psdImage = cast(PsdImage, img)

            # Get WarpSettings from Smart Layer
            smart_layer = cast(SmartObjectLayer, psdImage.layers[1])
            warp_settings = smart_layer.warp_settings

            # Set size of warp processing area
            warp_settings.processing_area = 2
            smart_layer.warp_settings = warp_settings

            # Save with PNG options
            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            psdImage.save(outputFile, pngOpt)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)