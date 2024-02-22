import os
from io import BytesIO

import pytest
from aspose.psd import Image, Color
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers import TextLayer, Layer
from aspose.psd.fileformats.psd.layers.filllayers import FillLayer
from aspose.psd.fileformats.psd.layers.fillsettings import GradientColorPoint, GradientTransparencyPoint
from aspose.psd.fileformats.psd.layers.gradient import GradientKind, NoiseColorModel
from aspose.psd.fileformats.psd.layers.layerresources import GdFlResource
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import is_assignable, cast, as_of

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper


class Release_23_12_Tests(BaseTests):

    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # [AI Format] Add support of Raster Image rendering in new version of AI
    # https://issue.saltov.dynabic.com/issues/PSDNET-1679
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-7
    def PSDNET1679Test(self):
        sourceFile = self.GetFileInBaseFolder("raster.ai")
        referenceFile = self.GetFileInBaseFolder("raster_output.png")
        outputFile = self.GetFileInOutputFolder("raster_output.png")

        with Image.load(sourceFile) as image:
            image.save(outputFile, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 1)
        os.remove(outputFile)

    # Handle Gradient type Noise in GdflResrource
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-8
    # https://issue.saltov.dynabic.com/issues/PSDNET-1454
    def PSDNET1454Test(self):
        sourceFile = self.GetFileInBaseFolder("Gradient-Fill.psd")
        referenceFile = self.GetFileInBaseFolder("Gradient-Fill-out.psd")
        destFile = self.GetFileInOutputFolder("Gradient-Fill-out.psd")

        with Image.load(sourceFile, PsdLoadOptions()) as image:
            psdImage = cast(PsdImage, image)
            layer = psdImage.layers[1]

            for res in layer.resources:
                resource = as_of(res, GdFlResource)
                if (resource != None):
                    resource.scale = 90
                    resource.angle = 30
                    resource.dither = False
                    resource.align_with_layer = True
                    resource.reverse = False

                    break

            psdImage.save(destFile, PsdOptions())

        Comparison.CheckAgainstEthalon(destFile, referenceFile, 1)
        os.remove(destFile)
        self.remove_all_unzipped_files()

    # Handle Gradient type Noise in GdflResrource
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-8
    # https://issue.saltov.dynabic.com/issues/PSDNET-1454
    def PSDNET1454_SolidTest(self):
        sourceFile = self.GetFileInBaseFolder("ComplexGradientFillLayer.psd")
        referenceFile = self.GetFileInBaseFolder("ComplexGradientFillLayer_output.psd")
        outputFile = self.GetFileInOutputFolder("ComplexGradientFillLayer_output.psd")

        with Image.load(sourceFile) as image:
            im = cast(PsdImage, image)
            for layer in im.layers:
                if is_assignable(layer, FillLayer):
                    fillLayer = as_of(layer, FillLayer)
                    gradientFillSettings = fillLayer.fill_settings

                    # Reading
                    assert gradientFillSettings.align_with_layer == False
                    assert abs(gradientFillSettings.angle - 45.0) < 0.001

                    assert gradientFillSettings.dither == True
                    assert gradientFillSettings.reverse == False
                    assert gradientFillSettings.color == Color.empty
                    assert gradientFillSettings.horizontal_offset == -39
                    assert gradientFillSettings.vertical_offset == -5

                    assert len(gradientFillSettings.transparency_points) == 3
                    assert len(gradientFillSettings.color_points) == 2

                    point = gradientFillSettings.transparency_points[0]
                    assert abs(100.0 - point.opacity) < 0.25
                    assert point.location == 0
                    assert point.median_point_location == 50

                    point = gradientFillSettings.transparency_points[1]
                    assert abs(50.0 - point.opacity) < 0.25
                    assert point.location == 2048
                    assert point.median_point_location == 50

                    point = gradientFillSettings.transparency_points[2]
                    assert abs(100.0 - point.opacity) < 0.25
                    assert point.location == 4096
                    assert point.median_point_location == 50

                    color_point = gradientFillSettings.color_points[0]
                    assert color_point.color == Color.from_argb(203, 64, 140)
                    assert color_point.location == 0
                    assert color_point.median_point_location == 50

                    color_point = gradientFillSettings.color_points[1]
                    assert color_point.color == Color.from_argb(203, 0, 0)
                    assert color_point.location == 4096
                    assert color_point.median_point_location == 50

                    # Editing
                    gradientFillSettings.angle = 30.0
                    gradientFillSettings.dither = False
                    gradientFillSettings.align_with_layer = True
                    gradientFillSettings.reverse = True
                    gradientFillSettings.horizontal_offset = 25
                    gradientFillSettings.vertical_offset = -15

                    color_points = list(gradientFillSettings.color_points)
                    transparency_points = list(gradientFillSettings.transparency_points)

                    gradPoint1 = GradientColorPoint()
                    gradPoint1.color = Color.violet
                    gradPoint1.location = 4096
                    gradPoint1.median_point_location = 75
                    color_points.append(gradPoint1)

                    color_points[1].location = 3000

                    gradPoint2 = GradientTransparencyPoint()
                    gradPoint2.opacity = 80.0
                    gradPoint2.location = 4096
                    gradPoint2.median_point_location = 25
                    transparency_points.append(gradPoint2)

                    transparency_points[2].location = 3000

                    gradientFillSettings.color_points = color_points
                    gradientFillSettings.transparency_points = transparency_points

                    im.save(outputFile)

        with Image.load(outputFile) as image:
            im = cast(PsdImage, image)
            for layer in im.layers:
                if isinstance(layer, FillLayer):
                    fillLayer = layer
                    gradientFillSettings = fillLayer.fill_settings

                    assert abs(gradientFillSettings.angle - 30) < 0.001
                    assert gradientFillSettings.align_with_layer == True
                    assert gradientFillSettings.dither == False
                    assert gradientFillSettings.reverse == True
                    assert gradientFillSettings.horizontal_offset == 25
                    assert gradientFillSettings.vertical_offset == -15

                    assert len(gradientFillSettings.transparency_points) == 4
                    assert len(gradientFillSettings.color_points) == 3

                    point = gradientFillSettings.transparency_points[0]
                    assert abs(100.0 - point.opacity) < 0.25
                    assert point.location == 0
                    assert point.median_point_location == 50

                    point = gradientFillSettings.transparency_points[1]
                    assert abs(50.196 - point.opacity) < 0.25
                    assert point.location == 2048
                    assert point.median_point_location == 50

                    point = gradientFillSettings.transparency_points[2]
                    assert abs(100.0 - point.opacity) < 0.25
                    assert point.location == 3000
                    assert point.median_point_location == 50

                    point = gradientFillSettings.transparency_points[3]
                    assert abs(80 - point.opacity) < 0.25
                    assert point.location == 4096
                    assert point.median_point_location == 25

                    color_point = gradientFillSettings.color_points[0]
                    assert color_point.color == Color.FromArgb(203, 64, 140)
                    assert color_point.location == 0
                    assert color_point.median_point_location == 50

                    color_point = gradientFillSettings.color_points[1]
                    assert color_point.color == Color.FromArgb(203, 0, 0)
                    assert color_point.location == 3000
                    assert color_point.median_point_location == 50

                    color_point = gradientFillSettings.color_points[2]
                    assert color_point.color == Color.FromArgb(238, 130, 238)
                    assert color_point.location == 4096
                    assert color_point.median_point_location == 75

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 1)
        os.remove(outputFile)
        self.remove_all_unzipped_files()

    # Handle Gradient type Noise in GdflResrource
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-8
    # https://issue.saltov.dynabic.com/issues/PSDNET-1454
    def PSDNET1454_NoiseTest(self):
        sourceFile = self.GetFileInBaseFolder("FillLayerGradientNoise.psd")
        referenceFile = self.GetFileInBaseFolder("FillLayerGradientNoise_output.psd")
        outputFile = self.GetFileInOutputFolder("FillLayerGradientNoise_output.psd")

        with Image.load(sourceFile) as image:
            im = cast(PsdImage, image)
            for layer in im.layers:
                if is_assignable(layer, FillLayer):
                    fillLayer = as_of(layer, FillLayer)
                    if fillLayer is not None:
                        gradientFillSettings = fillLayer.fill_settings

                        assert gradientFillSettings.align_with_layer == False
                        assert abs(gradientFillSettings.angle - 41.0) < 0.001
                        assert gradientFillSettings.dither == True
                        assert gradientFillSettings.reverse == True
                        assert gradientFillSettings.scale == 133
                        assert gradientFillSettings.gradient_mode == GradientKind.NOISE

                        assert gradientFillSettings.show_transparency == True
                        assert gradientFillSettings.use_vector_color == True
                        assert gradientFillSettings.color_model == NoiseColorModel.RGB
                        assert gradientFillSettings.rnd_number_seed == 2015172547
                        assert gradientFillSettings.roughness == 3727

                        assert gradientFillSettings.minimum_color.components[1].value == 15
                        assert gradientFillSettings.minimum_color.components[2].value == 33
                        assert gradientFillSettings.minimum_color.components[3].value == 56
                        assert gradientFillSettings.minimum_color.components[0].value == 0

                        assert gradientFillSettings.maximum_color.components[1].value == 234
                        assert gradientFillSettings.maximum_color.components[2].value == 209
                        assert gradientFillSettings.maximum_color.components[3].value == 186
                        assert gradientFillSettings.maximum_color.components[0].value == 255

                        # Editing
                        gradientFillSettings.angle = 30.0
                        gradientFillSettings.dither = False
                        gradientFillSettings.align_with_layer = True
                        gradientFillSettings.reverse = False
                        gradientFillSettings.scale = 60
                        gradientFillSettings.show_transparency = False
                        gradientFillSettings.use_vector_color = False
                        gradientFillSettings.color_model = NoiseColorModel.HSB
                        gradientFillSettings.roughness = 4096
                        gradientFillSettings.rnd_number_seed = 12345678

                        gradientFillSettings.minimum_color.components[1].value = 0
                        gradientFillSettings.minimum_color.components[2].value = 0
                        gradientFillSettings.minimum_color.components[3].value = 0
                        gradientFillSettings.minimum_color.components[0].value = 0

                        gradientFillSettings.maximum_color.components[1].value = 255
                        gradientFillSettings.maximum_color.components[2].value = 255
                        gradientFillSettings.maximum_color.components[3].value = 255
                        gradientFillSettings.maximum_color.components[0].value = 255

                        im.save(outputFile)

        with Image.load(outputFile) as image:
            im = cast(PsdImage, image)
            for layer in im.layers:
                if is_assignable(layer, FillLayer):
                    fillLayer = as_of(layer, FillLayer)
                    gradientFillSettings = fillLayer.fill_settings

                    assert gradientFillSettings.align_with_layer == True
                    assert abs(gradientFillSettings.angle - 30.0) < 0.001
                    assert gradientFillSettings.dither == False
                    assert gradientFillSettings.reverse == False
                    assert gradientFillSettings.scale == 60

                    assert gradientFillSettings.show_transparency == False
                    assert gradientFillSettings.use_vector_color == False
                    assert gradientFillSettings.color_model == NoiseColorModel.HSB
                    assert gradientFillSettings.rnd_number_seed == 12345678
                    assert gradientFillSettings.roughness == 4096

                    assert gradientFillSettings.minimum_color.components[1].value == 0
                    assert gradientFillSettings.minimum_color.components[2].value == 0
                    assert gradientFillSettings.minimum_color.components[3].value == 0
                    assert gradientFillSettings.minimum_color.components[0].value == 0

                    assert gradientFillSettings.maximum_color.components[1].value == 255
                    assert gradientFillSettings.maximum_color.components[2].value == 255
                    assert gradientFillSettings.maximum_color.components[3].value == 255
                    assert gradientFillSettings.maximum_color.components[0].value == 255

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 1)
        os.remove(outputFile)
        self.remove_all_unzipped_files()

    # Handle Gradient type Noise in GdflResrource
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-8
    # https://issue.saltov.dynabic.com/issues/PSDNET-1454
    def PSDNET1827Test(self):
        sourceFile = self.GetFileInBaseFolder("input_1827.psd")
        referenceFile = self.GetFileInBaseFolder("out_1827.psd")
        outputFile = self.GetFileInOutputFolder("out_1827.psd")

        with Image.load(sourceFile) as image:
            psdImage = cast(PsdImage, image)
            for layer in psdImage.layers:
                if (is_assignable(layer, TextLayer)):
                    textLayer = cast(TextLayer, layer)
                    textLayer.text_data.update_layer_data()

            # There should be no error here
            psdImage.save(outputFile)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 1)
        os.remove(outputFile)
        self.remove_all_unzipped_files()


    # AllowWarpRepaint in the PsdLoadOptions leads to the exception
    # https://issue.saltov.dynabic.com/issues/PSDNET-1536
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-11
    def PSDNET1536Test(self):
        sourceFile = self.GetFileInBaseFolder("SizeChart - 4 Colors.psd")
        referenceFile = self.GetFileInBaseFolder("_export.png")
        outputFile = self.GetFileInOutputFolder("_export.png")

        psdLoadOptions = PsdLoadOptions()
        psdLoadOptions.allow_warp_repaint = True
        psdLoadOptions.load_effects_resource = True

        with Image.load(sourceFile, psdLoadOptions) as psdImage:
            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            pngOpt.progressive = True
            pngOpt.compression_level = 9
            # If the save is successful, the test is passed
            psdImage.save(outputFile, pngOpt)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 1)
        os.remove(outputFile)
        self.remove_all_unzipped_files()

    # License Control for VectorPathDataResource works incorrectly
    # https://issue.saltov.dynabic.com/issues/PSDNET-1834
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-13
    def PSDNET1834Test(self):
        sourceFile = self.GetFileInBaseFolder("DifferentLayerMasks.psd")
        referenceFile = self.GetFileInBaseFolder("DifferentLayerMasks_output.psd")
        outputFile = self.GetFileInOutputFolder("DifferentLayerMasks_output.psd")

        licensed = LicenseHelper.isLicensed

        if licensed:
            LicenseHelper.remove_license()

        try:
            with Image.load(sourceFile) as im:
                im.save(outputFile)
            Comparison.CheckAgainstEthalon(outputFile, referenceFile, 1)
            os.remove(outputFile)
            self.remove_all_unzipped_files()
        finally:
            if licensed:
                LicenseHelper.set_license()

    # Open any image file as an embedded smart object in the PSD image.
    # https://issue.saltov.dynabic.com/issues/PSDNET-770
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-16
    @pytest.mark.skip(reason="This test doesn't work for Python. Created tasks: https://issue.saltov.dynabic.com/issues/PSDNET-1931 and https://issue.saltov.dynabic.com/issues/PSDPYTHON-16")
    def PSDNET770Test(self):
        sourceFile = self.GetFileInBaseFolder("empty.psd")
        addTreeFile = self.GetFileInBaseFolder("tree.psd")
        addFrostFile = self.GetFileInBaseFolder("frost.png")
        outputTreeFile = self.GetFileInOutputFolder("tree_export.psd")
        outputFrostFile = self.GetFileInOutputFolder("frost_export.psd")
        referenceTreeFile = self.GetFileInOutputFolder("tree_export.psd")
        referenceFrostFile = self.GetFileInOutputFolder("frost_export.psd")

        #with open(inputFile, "rb", buffering=0) as filestream:
         #   stream = BytesIO(filestream.read())
          #  stream.seek(0)


        loadOpt = PsdLoadOptions()
        loadOpt.load_effects_resource = True
        with Image.load(sourceFile, loadOpt) as image:
            psdImage = cast(PsdImage, image)
            with open(addTreeFile, "rb", buffering=0) as filestream:

                stream = BytesIO(filestream.read())
                stream.seek(0)
                #layer = Layer(stream)

                with SmartObjectLayer(stream) as smartLayer:
                    psdImage.add_layer(smartLayer)
                    psdImage.save(outputTreeFile, PsdOptions())

        with Image.load(sourceFile, loadOpt) as image:
            psdImage = cast(PsdImage, image)
            with open(addFrostFile, "rb", buffering=0) as stream:
                with SmartObjectLayer(stream) as smartLayer:
                    psdImage.add_layer(smartLayer)
                    psdImage.save(outputFrostFile, PsdOptions())

        Comparison.CheckAgainstEthalon(outputFrostFile, referenceFrostFile, 1)
        Comparison.CheckAgainstEthalon(outputTreeFile, referenceTreeFile, 1)
        os.remove(outputTreeFile)
        os.remove(outputFrostFile)
        self.remove_all_unzipped_files()

#c = Release_23_12_Tests()
#c.PSDNET770Test()