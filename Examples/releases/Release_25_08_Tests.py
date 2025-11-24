import pytest
from aspose.psd import Rectangle, Image, DataRecoveryMode, Color, ResolutionSetting
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers import TextLayer, Layer
from aspose.psd.fileformats.psd.layers.fillsettings import GradientType, GradientFillSettings
from aspose.psd.fileformats.psd.layers.layereffects import StrokeEffect
from aspose.psd.fileformats.psd.layers.layerresources import SoLdResource
from aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures import DescriptorStructure, ListStructure, \
    ReferenceStructure
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions, GifOptions
from aspose.pycore import cast, as_of, is_assignable

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper
class Release_25_08_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # [AI Format] Add processing of Text in PDF-Based AI Format
    # https://issue.saltov.dynabic.com/issues/PSDNET-1675
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-221
    def PSDNET1675Test(self):
        sourceFile = self.GetFileInBaseFolder("text_test.ai")
        outputFile = self.GetFileInOutputFolder("text_test.png")
        referenceFile = self.GetFileInBaseFolder("text_test.png")

        with AiImage.load(sourceFile) as image:
            image.save(outputFile, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # [Regression] Fix the export of Ai file to a gif file
    # https://issue.saltov.dynabic.com/issues/PSDNET-2394
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-223
    def PSDNET2394Test(self):
        sourceFile = self.GetFileInBaseFolder("rect2_color.ai")
        outPng_WithAlpha_Back_White = self.GetFileInOutputFolder("output_WithAlpha_Back_White.png")
        outPng_WithAlpha_Back_Transparent = self.GetFileInOutputFolder("output_WithAlpha_Back_Transparent.png")
        outPng_NoAlpha_Back_Transparent = self.GetFileInOutputFolder("output_NoAlpha_Back_Transparent.png")
        outGif_Back_Transparent = self.GetFileInOutputFolder("output_Back_Transparent.gif")
        outGif_Back_White = self.GetFileInOutputFolder("output_Back_White.gif")

        refPng_WithAlpha_Back_White = self.GetFileInOutputFolder("output_WithAlpha_Back_White.png")
        refPng_WithAlpha_Back_Transparent = self.GetFileInOutputFolder("output_WithAlpha_Back_Transparent.png")
        refPng_NoAlpha_Back_Transparent = self.GetFileInOutputFolder("output_NoAlpha_Back_Transparent.png")
        refGif_Back_Transparent = self.GetFileInOutputFolder("output_Back_Transparent.gif")
        refGif_Back_White = self.GetFileInOutputFolder("output_Back_White.gif")

        with AiImage.load(sourceFile) as image:
            # AiImage.BackgroundColor = White, Png file with Alpha
            # We should get White background
            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            image.save(outPng_WithAlpha_Back_White, pngOpt)

            # AiImage.BackgroundColor = Transparent, Png file with Alpha
            # We should get Transparent background
            image.background_color = Color.transparent
            image.save(outPng_WithAlpha_Back_Transparent, pngOpt)

            # AiImage.BackgroundColor = Transparent, Png file without Alpha
            # We should get black background
            image.save(outPng_NoAlpha_Back_Transparent, PngOptions())

            # AiImage.BackgroundColor = Transparent, Gif file
            # We should get black background
            gifOpt = GifOptions()
            gifOpt.do_palette_correction = False
            image.save(outGif_Back_Transparent, gifOpt)

            # AiImage.BackgroundColor = White, Gif file
            # We should get White background
            image.background_color = Color.white
            image.save(outGif_Back_White, gifOpt)

        Comparison.CheckAgainstEthalon(outPng_WithAlpha_Back_White, refPng_WithAlpha_Back_White, 0, 1)
        Comparison.CheckAgainstEthalon(outPng_WithAlpha_Back_Transparent, refPng_WithAlpha_Back_Transparent, 0, 1)
        Comparison.CheckAgainstEthalon(outPng_NoAlpha_Back_Transparent, refPng_NoAlpha_Back_Transparent, 0, 1)
        Comparison.CheckAgainstEthalon(outGif_Back_Transparent, refGif_Back_Transparent, 0, 1)
        Comparison.CheckAgainstEthalon(outGif_Back_White, refGif_Back_White, 0, 1)

    # Incorrect Multiple Stroke Rendering
    # https://issue.saltov.dynabic.com/issues/PSDNET-2503
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-224
    def PSDNET2503Test(self):
        sourceFile = self.GetFileInBaseFolder("2503.psd")
        outputFile = self.GetFileInOutputFolder("out_2503.png")
        referenceFile = self.GetFileInBaseFolder("out_2503.png")

        psdOpt = PsdLoadOptions()
        psdOpt.load_effects_resource = True

        pngOpt = PngOptions()
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        with PsdImage.load(sourceFile, psdOpt) as image:
            image.save(outputFile, pngOpt)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # Layer was exported with effects bounds even when AreEffectsEnabled is False
    # https://issue.saltov.dynabic.com/issues/PSDNET-2512
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-225
    def PSDNET2512Test(self):
        srcFile = self.GetFileInBaseFolder("2512.psd")
        outputFile = self.GetFileInOutputFolder("out_2512.png")
        referenceFile = self.GetFileInBaseFolder("out_2512.png")

        psdOpt = PsdLoadOptions()
        psdOpt.load_effects_resource = True

        with PsdImage.load(srcFile, psdOpt) as img:
            psdImage = cast(PsdImage, img)
            layer1 = psdImage.layers[1]
            layer1.blending_options.are_effects_enabled = False

            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

            # The result should contain only layer pixels, without reserved for effects bounds.
            layer1.save(outputFile, pngOpt)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # Fix rendering of pattern with transparent pixels
    # https://issue.saltov.dynabic.com/issues/PSDNET-2514
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-226
    def PSDNET2514Test(self):
        sourceFile = self.GetFileInBaseFolder("2514.psd")
        outputFile = self.GetFileInOutputFolder("out_2514.png")
        referenceFile = self.GetFileInBaseFolder("out_2514.png")

        psdOpt = PsdLoadOptions()
        psdOpt.load_effects_resource = True

        pngOpt = PngOptions()
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        with PsdImage.load(sourceFile, psdOpt) as img:
            psdImage = cast(PsdImage, img)
            psdImage.save(outputFile, pngOpt)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)