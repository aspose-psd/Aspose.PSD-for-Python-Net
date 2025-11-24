import pytest
from aspose.psd import Color, FontSettings, Image
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage, PsdVersion, CompressionMethod
from aspose.psd.fileformats.psd.layers import Layer, LayerMaskDataShort
from aspose.psd.fileformats.psd.layers.filllayers import FillLayer
from aspose.psd.fileformats.psd.layers.fillsettings import FillType
from aspose.psd.fileformats.psd.layers.layerresources import LnsrResource, LnsrResourceType, Lfx2Resource, \
    PattResource, UnknownResource, ImfxResource
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.fileformats.psd.layers.warp import WarpSettings
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import cast, as_of, is_assignable

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_25_05_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Create default layer mask for Fill layer.
    # https://issue.saltov.dynabic.com/issues/PSDNET-1460
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-184
    def PSDNET1460Test(self):
        referenceFile = self.GetFileInBaseFolder("example_1460_output.psd")
        outputPsd = self.GetFileInOutputFolder("FillLayer_output.psd")

        with PsdImage(100, 100) as psdImage:
            fillLayer = FillLayer.create_instance(FillType.COLOR)
            fillLayer.fill_settings.color = Color.red
            psdImage.add_layer(fillLayer)

            psdImage.save(outputPsd)


        with PsdImage.load(outputPsd) as image:
            psdImage = cast(PsdImage, image)
            fillLayer = cast(FillLayer, psdImage.layers[1])

            lnsrResource = cast(LnsrResource, fillLayer.resources[2])
            assert (lnsrResource.value == LnsrResourceType.CONT)

            assert (is_assignable(fillLayer.layer_mask_data, LayerMaskDataShort))
            assert (fillLayer.channel_information[4].channel_id == -2)

        Comparison.CheckAgainstEthalon(outputPsd, referenceFile, 0, 1)

    # Add Support of multiple Effects, new resource (imfx). Add setter to effects property.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2003
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-185
    def PSDNET2003Test(self):
        sourceFile = self.GetFileInBaseFolder("MultiExample.psd")

        output_files = []
        reference_files = []
        for i in range(3):
            output_files.append(self.GetFileInOutputFolder(f"export{i + 1}.png"))
            reference_files.append(self.GetFileInBaseFolder(f"export{i + 1}.png"))

        loadOpt = PsdLoadOptions()
        loadOpt.load_effects_resource = True
        with PsdImage.load(sourceFile, loadOpt) as img:
            image = cast(PsdImage, img)
            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            image.save(output_files[0], pngOpt)

            blendingOptions = image.layers[0].blending_options

            dropShadowEffect3 = blendingOptions.add_drop_shadow()
            dropShadowEffect3.color = Color.red
            dropShadowEffect3.distance = 50
            dropShadowEffect3.angle = 0

            image.save(output_files[1], pngOpt)

            imfx = cast(ImfxResource, image.layers[0].resources[0])
            assert imfx is not None

            blendingOptions.effects = []
            dropShadowEffect1 = blendingOptions.add_drop_shadow()
            dropShadowEffect1.color = Color.blue
            dropShadowEffect1.distance = 10

            image.save(output_files[2], pngOpt)

            lfx2 = cast(Lfx2Resource, image.layers[0].resources[14])
            assert lfx2 is not None

            for i in range(3):
                Comparison.CheckAgainstEthalon(output_files[i], reference_files[i], 0, 1)

    # Implementing stroke style operators: line dash pattern, line cap style, line join style, miter limit.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2397
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-186
    def PSDNET2397Test(self):
        sourceFile = self.GetFileInBaseFolder("linesStyle.ai")
        outputFile = self.GetFileInOutputFolder("linesStyle.png")
        referenceFile = self.GetFileInBaseFolder("linesStyle.png")

        with Image.load(sourceFile) as image:
            image.save(outputFile, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # Fix incorrect deformation transformation in a specific file, add "Processing area" field, smooth out deformation rendering steps.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2253
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-187
    def PSDNET2253Test(self):
        sourceFile = self.GetFileInBaseFolder("Warping.psd")
        outputFiles = []
        referenceFiles = []

        areaValues = [5, 10, 25, 40]

        loadOpt = PsdLoadOptions()
        loadOpt.load_effects_resource = True
        loadOpt.allow_warp_repaint = True

        pngOpt = PngOptions()
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
        for areaValue in areaValues:
            with PsdImage.load(sourceFile, loadOpt) as image:
                psdImage = cast(PsdImage, image)
                layer = cast(SmartObjectLayer, psdImage.layers[1])
                warpSettings = cast(WarpSettings, layer.warp_settings)

                warpSettings.processing_area = areaValue
                layer.warp_settings = warpSettings

                outputFile = self.GetFileInOutputFolder(f"export{areaValue}.png")
                referenceFile = self.GetFileInBaseFolder(f"export{areaValue}.png")
                outputFiles.append(outputFile)
                referenceFiles.append(referenceFile)

                psdImage.save(outputFile, pngOpt)
            Comparison.CheckAgainstEthalon(outputFiles[-1], referenceFiles[-1], 0, 1)

    # Improve drop shadow: Correct distance and scope. Speed up code.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2341
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-188
    def PSDNET2341Test(self):
        sourceFile = self.GetFileInBaseFolder("distance.psd")
        outputFile = self.GetFileInOutputFolder("export.png")
        referenceFile = self.GetFileInBaseFolder("export.png")

        psdLoadOpt = PsdLoadOptions()
        psdLoadOpt.load_effects_resource = True

        pngOpt = PngOptions()
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
        with PsdImage.load(sourceFile, psdLoadOpt) as psdImage:
            psdImage.save(outputFile, pngOpt)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)


    # Saving of newly created PSD File to PSB format creates broken file.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2358
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-189
    def PSDNET2358Test(self):
        outputPsd = self.GetFileInOutputFolder("example_output.psb")
        referencePsd = self.GetFileInBaseFolder("example_output.psb")

        with PsdImage(200, 100) as image:
            psdImage = cast(PsdImage, image)
            layer = Layer()
            layer.left = 0
            layer.top = 0
            layer.right = psdImage.width
            layer.bottom = psdImage.height

            pixels = [0] * (layer.width * layer.height)
            row = [0] * layer.width
            for x in range(layer.width):
                col = Color.from_argb((x % 256 * (x % 4) % 256), (x % 256 * (x % 5)) % 256, (x % 256 * (x % 3)) % 256)
                row[x] = col.to_argb()

            for y in range(layer.height):
                pixels[y * layer.width * 4: (y + 1) * layer.width * 4] = row

            layer.save_argb_32_pixels(layer.bounds, pixels)

            psdImage.layers = [layer]

            psdOpt = PsdOptions()
            psdOpt.psd_version = PsdVersion.PSB
            psdOpt.compression_method = CompressionMethod.RLE
            psdImage.save(outputPsd, psdOpt)

        with PsdImage.load(outputPsd) as image:
            psdImage = cast(PsdImage, image)
            assert 2 == len(psdImage.global_layer_resources)
            assert is_assignable(psdImage.global_layer_resources[0], PattResource)
            assert is_assignable(psdImage.global_layer_resources[1], UnknownResource)

        Comparison.CheckAgainstEthalon(outputPsd, referencePsd, 0, 1)

    # [AI Format] Fixing regression after shading reworking. Improving shading rendering, improving opacity rendering, implementing correct rendering order for different layers.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2413
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-190
    def PSDNET2413Test(self):
        input_files = ["Input1.ai", "Input_2.ai", "2249.ai"]

        for index in range(len(input_files)):
            input = self.GetFileInBaseFolder(input_files[index])
            output = self.GetFileInOutputFolder(f"output{index + 1}.png")
            reference = self.GetFileInBaseFolder(f"output{index + 1}.png")
            with AiImage.load(input) as image:
                pngOpt = PngOptions()
                image.save(output, pngOpt)

            Comparison.CheckAgainstEthalon(output, reference, 0, 1)