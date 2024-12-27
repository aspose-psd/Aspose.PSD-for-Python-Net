from datetime import datetime

import numpy as np
import pytest
from aspose.psd import FontSettings, Image
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage, CompressionMethod
from aspose.psd.fileformats.psd.layers import ShapeLayer, TextLayer
from aspose.psd.fileformats.psd.layers.fillsettings import GradientType, NoiseGradientFillSettings
from aspose.psd.fileformats.psd.layers.gradient import NoiseColorModel, GradientKind
from aspose.psd.fileformats.psd.layers.layerresources import BaseArtboardInfoResource, AbddResource, ArtBResource, ArtDResource, LyvrResource
from aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures import IntegerStructure, StringStructure
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_24_10_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Optimize rendering speed of Gradient Effect
    # https://issue.saltov.dynabic.com/issues/PSDNET-2060
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-107
    def PSDNET2060Test(self):
        inputFile = self.GetFileInBaseFolder("PsdDockerExample.psd")
        outputFilePsd = self.GetFileInOutputFolder("PsdDockerExample_output.psd")

        psdOpt = PsdLoadOptions()
        psdOpt.load_effects_resource = True

        pngOpt = PngOptions()
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        with PsdImage.load(inputFile, psdOpt) as img:
            start = datetime.now()
            img.save(outputFilePsd, pngOpt)
            end = datetime.now()

        if (end - start).seconds > 18:
            raise Exception("Performance problem. Saving should not take more than 10 seconds.")

    # Fix the issue of updating text with multiple new line symbols
    # https://issue.saltov.dynabic.com/issues/PSDNET-1308
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-108
    def PSDNET1308Test(self):
        sourceFile = self.GetFileInBaseFolder("TestFileForAsianCharsBig 2.psd")
        testData = "咸咹咺咻咼咽咾咿\r\n哀品哂哃哄哅哆哇哈哉哊哋哌响哎哏"

        with PsdImage.load(sourceFile) as img:
            image = cast(PsdImage, img)
            layer = cast(TextLayer, image.layers[0])
            # Here should be no exception.
            layer.update_text(testData)

    # Open any image file as an embedded smart object in the PSD image doesn't work
    # https://issue.saltov.dynabic.com/issues/PSDNET-1931
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-109
    def PSDNET1931Test(self):
        sourceFile = self.GetFileInBaseFolder("smart.psd")
        addFile = self.GetFileInBaseFolder("DragonFly.jpeg")
        outputFile = self.GetFileInOutputFolder("DragonFly_export.png")
        outputPsd = self.GetFileInOutputFolder("DragonFly_export.psd")
        referencePsd = self.GetFileInBaseFolder("DragonFly_export.psd")

        psdOpt = PsdLoadOptions()
        psdOpt.load_effects_resource = True
        with PsdImage.load(sourceFile, psdOpt) as image:
            psdImage = cast(PsdImage, image)
            with open(addFile, "rb", buffering=0) as stream:
                with SmartObjectLayer(stream) as smartLayer:
                    psdImage.add_layer(smartLayer)
                    pngOpt = PngOptions()
                    pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
                    psdImage.save(outputFile, pngOpt)
                    psdImage.save(outputPsd, PsdOptions())
        Comparison.CheckAgainstEthalon(outputPsd, referencePsd, 0)

    # Error of processing clipping mask in big image
    # https://issue.saltov.dynabic.com/issues/PSDNET-2084
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-110
    def PSDNET2084Test(self):
        src = self.GetFileInBaseFolder("input.psd")
        output = self.GetFileInOutputFolder("out_PSDNET2084.psd")
        reference = self.GetFileInBaseFolder("out_PSDNET2084.psd")

        with PsdImage.load(src) as image:
            psdImage = cast(PsdImage, image)
            layers = psdImage.layers

            # Select issue layers to speed up processing
            psdImage.layers = [layers[174], layers[175]]

            # Here should be no exception on saving
            psdImage.save(output)
        Comparison.CheckAgainstEthalon(output, reference, 0)

    # (PSD .NET) UpdateText cutting last letter
    # https://issue.saltov.dynabic.com/issues/PSDNET-2183
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-111
    def PSDNET2183Test(self):
        srcFile = self.GetFileInBaseFolder("frenteee.psd")
        outFilePng = self.GetFileInOutputFolder("out_frenteee.png")
        referenceFile = self.GetFileInOutputFolder("out_frenteee.png")

        with PsdImage.load(srcFile) as psdImage:
            psdImage.save(outFilePng, PngOptions())
        Comparison.CheckAgainstEthalon(outFilePng, referenceFile, 0)

    # After saving the PSD file in 3rd party editor, SmartObject.ReplaceContents throws Null Reference but the file still can be opened in Photoshop
    # https://issue.saltov.dynabic.com/issues/PSDNET-2184
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-112
    def PSDNET2184Test(self):
        sourceFile = self.GetFileInBaseFolder("snapcase.psd")
        changeFile = self.GetFileInBaseFolder("snapcase_change.png")

        with PsdImage.load(sourceFile) as image:
            psdImage = cast(PsdImage, image)
            for layer in psdImage.layers:
                if isinstance(layer, SmartObjectLayer) and layer.name == "ARTHERE":
                    smartObjectLayer = SmartObjectLayer(layer)

                    # Exception was here
                    smartObjectLayer.replace_contents(changeFile)
                    smartObjectLayer.embed_linked()

                    break

    # Fix the problem with an exception on the reading of PSD file with Gradient shape
    # https://issue.saltov.dynabic.com/issues/PSDNET-2192
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-113
    def PSDNET2192Test(self):
        # Temporary disabled. Fixed in 24.11
        pass
        inputFile = self.GetFileInBaseFolder("vectormasks.psd")
        outputFilePsd = self.GetFileInOutputFolder("vectormasks_output.psd")
        referenceFilePsd = self.GetFileInBaseFolder("vectormasks_output.psd")

        with PsdImage.load(inputFile) as img:
            image = cast(PsdImage, img)
            # Should be no exception

            # Test Gradient parameters
            shapeLayer = cast(ShapeLayer, image.layers[1])
            gradientSettings = cast(NoiseGradientFillSettings, shapeLayer.stroke.fill)

            assert True == gradientSettings.dither
            assert True == gradientSettings.reverse
            assert 90.0 == gradientSettings.angle
            assert 80 == gradientSettings.scale
            assert True == gradientSettings.align_with_layer
            assert GradientType.Radial == gradientSettings.gradient_type
            assert GradientKind.Noise == gradientSettings.gradient_mode
            assert 1837065285 == gradientSettings.rndNumberSeed
            assert False == gradientSettings.show_transparency
            assert False == gradientSettings.use_vector_color
            assert 2048 == gradientSettings.roughness
            assert NoiseColorModel.HSB == gradientSettings.color_model
            assert 0 == gradientSettings.expansion_count

            # Edit
            gradientSettings.dither = False
            gradientSettings.reverse = False
            gradientSettings.angle = 54.0
            gradientSettings.scale = 34
            gradientSettings.align_with_layer = False
            gradientSettings.gradient_type = GradientType.LINEAR
            gradientSettings.show_transparency = True
            gradientSettings.use_vector_color = True
            gradientSettings.roughness = 3072
            gradientSettings.color_model = NoiseColorModel.RGB

            image.save(outputFilePsd)

        with PsdImage.load(outputFilePsd) as img:
            image = cast(PsdImage, img)

            # Should be no exception

            # Test Gradient parameters
            shapeLayer = cast(ShapeLayer, image.layers[1])
            gradientSettings = cast(NoiseGradientFillSettings, shapeLayer.stroke.fill)

            assert False == gradientSettings.dither
            assert False == gradientSettings.reverse
            assert 54.0 == gradientSettings.angle
            assert 34 == gradientSettings.scale
            assert False == gradientSettings.align_with_layer
            assert GradientType.LINEAR == gradientSettings.gradient_type
            assert GradientKind.NOISE == gradientSettings.gradient_mode
            assert 1837065285 == gradientSettings.rndNumberSeed
            assert True == gradientSettings.show_transparency
            assert True == gradientSettings.use_vector_color
            assert 3072 == gradientSettings.roughness
            assert NoiseColorModel.RGB == gradientSettings.color_model
            assert 0 == gradientSettings.expansion_count

            def AssertAreEqual(self, expected, actual, message=None):
                if expected != actual:
                    raise Exception(message or "Objects are not equal.")
        Comparison.CheckAgainstEthalon(outputFilePsd, referenceFilePsd, 0)