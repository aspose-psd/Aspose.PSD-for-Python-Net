from datetime import datetime

import numpy as np
import pytest
from aspose.psd import FontSettings, Image, Color
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage, CompressionMethod
from aspose.psd.fileformats.psd.layers.filllayers import FillLayer
from aspose.psd.fileformats.psd.layers.fillsettings import GradientType, NoiseGradientFillSettings, ColorFillSettings
from aspose.psd.fileformats.psd.layers.layerresources import BaseArtboardInfoResource, AbddResource, ArtBResource, \
    ArtDResource, LyvrResource, GdFlResource, SoCoResource
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import cast, as_of

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_24_11_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Implement correct change of FillSettings object
    # https://issue.saltov.dynabic.com/issues/PSDNET-1954
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-116
    def PSDNET1954Test(self):
        inputFile = self.GetFileInBaseFolder("FillLayer_GradientNoise.psd")
        outputFile = self.GetFileInOutputFolder("output_FillLayer_GradientNoise.psd")
        referenceFile = self.GetFileInBaseFolder("output_FillLayer_GradientNoise.psd")

        with PsdImage.load(inputFile) as img:
            image = cast(PsdImage, img)
            fill_layer = cast(FillLayer, image.layers[1])  # Assuming index of the fill layer is 1

            src_fill_settings = cast(NoiseGradientFillSettings, fill_layer.fill_settings)
            assert src_fill_settings is not None

            new_fill_settings = ColorFillSettings()
            new_fill_settings.color = Color.red

            fill_layer.fill_settings = new_fill_settings
            fill_layer.update()
            image.save(outputFile)
        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0)

        # Check changed fill settings
        with PsdImage.load(outputFile) as img:
            image = cast(PsdImage, img)
            fill_layer = cast(FillLayer, image.layers[1])
            dst_fill_settings = as_of(fill_layer.fill_settings, ColorFillSettings)
            assert dst_fill_settings is not None

            # Check that Gradient resource GdFlResource is removed from Resources array of a layer
            assert Release_24_11_Tests.check_resource_is_removed(fill_layer.resources, GdFlResource)

    def check_resource_is_removed(resources, resource_type_to_remove):
        for resource in resources:
            if isinstance(resource, resource_type_to_remove):
                return False
        return True

    def assert_are_equal(expected, actual, message=None):
        if not expected == actual:
            raise Exception(message or "Objects are not equal.")

    def assert_is_not_null(actual):
        if actual is None:
            raise Exception("Layer is null.")

    # Add support of Artboard layer
    # https://issue.saltov.dynabic.com/issues/PSDNET-2167
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-120
    def PSDNET2167Test(self):
        srcFile = self.GetFileInBaseFolder("artboard1.psd")

        output = [None] * 4
        references = [None] * 4
        for i in range(0, 4, 1):
            output[i] = self.GetFileInOutputFolder("art" + str(i) + ".png")
            references[i] = self.GetFileInBaseFolder("art" + str(i) + ".png")

        with PsdImage.load(srcFile) as image:
            psdImage = cast(PsdImage, image)
            art1 = psdImage.layers[4]
            art2 = psdImage.layers[9]
            art3 = psdImage.layers[14]

            pngSaveOptions = PngOptions()
            pngSaveOptions.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            art1.save(output[1], pngSaveOptions)
            art2.save(output[2], pngSaveOptions)
            art3.save(output[3], pngSaveOptions)

            psdImage.save(output[0], pngSaveOptions)

        for i in range(0, 4, 1):
            Comparison.CheckAgainstEthalon(output[i], references[i], 0)

    # No support of UnitTypes.Millimeters for vector origin bounds
    # https://issue.saltov.dynabic.com/issues/PSDNET-2114
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-117
    def PSDNET2114Test(self):
        sourceFile = self.GetFileInBaseFolder("30x20.psd")

        with PsdImage.load(sourceFile):
            # Should be no exception
            pass

    # [Ai format] Handle the situation when Ai file has no layers (OCG)
    # https://issue.saltov.dynabic.com/issues/PSDNET-2143
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-118
    def PSDNET2143Test(self):
        inputFile = self.GetFileInBaseFolder("NoLayers.ai")
        outputFilePng = self.GetFileInOutputFolder("output_NoLayers.png")
        referenceFilePng = self.GetFileInBaseFolder("output_NoLayers.png")

        with AiImage.load(inputFile) as image:
            image.save(outputFilePng, PngOptions())

        Comparison.CheckAgainstEthalon(outputFilePng, referenceFilePng, 0)

    # Rework updating of FillSettings of FillLayer
    # https://issue.saltov.dynabic.com/issues/PSDNET-2145
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-119
    def PSDNET2145Test(self):
        inputFile = self.GetFileInBaseFolder("FillLayer_UpdateColorFillSettings.psd")

        with PsdImage.load(inputFile) as img:
            image = cast(PsdImage, img)
            fill_layer = cast(FillLayer, image.layers[1])

            before_fill_settings = cast(ColorFillSettings, fill_layer.fill_settings)
            assert Color.from_argb(255, 0, 101, 207), before_fill_settings.color

            soCoResource = cast(SoCoResource, fill_layer.resources[0])
            soCoResource.color = Color.green

            # Emulate change of Resource collection to force update of FillLayer.FillSettings
            fill_layer.resources = fill_layer.resources
            after_fill_settings = cast(ColorFillSettings, fill_layer.fill_settings)

            # Check that fillLayer.FillSettings is updated, not recreated
            assert before_fill_settings, after_fill_settings
            assert Color.green, before_fill_settings.color