from datetime import datetime

import os
import zipfile

import pytest
from aspose.psd import Image
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers import ShapeLayer
from aspose.psd.fileformats.psd.layers.layerresources import FXidResource
from aspose.psd.fileformats.psd.layers.smartfilters import EmbossSmartFilter
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, JpegOptions, PsdOptions
from aspose.pycore import cast, as_of, is_assignable

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper


class Release_26_09_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Implement handling of Emboss smart filter data.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2834
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-334
    def PSDNET2834Test(self):
        srcFileName = "no_filter.psd"
        sourceFile = self.GetFileInBaseFolder(srcFileName)
        outputFile = self.GetFileInOutputFolder("out_PSDNET2834.psd")
        referenceFile = self.GetFileInBaseFolder("out_PSDNET2834.psd")

        # First pass – add EmbossSmartFilter and save
        with PsdImage.load(sourceFile) as img:
            psdImage = cast(PsdImage, img)
            smartObj = cast(SmartObjectLayer, psdImage.layers[1])

            filters = list(smartObj.smart_filters.filters)
            emboss = EmbossSmartFilter()
            emboss.angle = 180
            emboss.height = 10
            emboss.amount = 120
            filters.append(emboss)

            smartObj.smart_filters.filters = filters
            smartObj.smart_filters.update_resource_values()

            psdImage.save(outputFile)

        # Second pass – verify properties
        with PsdImage.load(outputFile) as img:
            psdImage = cast(PsdImage, img)
            smartObj = cast(SmartObjectLayer, psdImage.layers[1])
            emboss = cast(EmbossSmartFilter, smartObj.smart_filters.filters[0])

            assert emboss.angle == 180
            assert emboss.height == 10
            assert emboss.amount == 120

        Comparison.CheckAgainstEthalon(referenceFile, outputFile, 0)



    # Layer effects structures don't support Grayscale color mode and can not be saved.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2830
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-335
    def PSDNET2830Test(self):
        sourceFile = self.GetFileInBaseFolder("inGrayscale32.psd")
        outputFile = self.GetFileInOutputFolder("inGrayscale32_out.psd")
        referenceFile = self.GetFileInBaseFolder("inGrayscale32_out.psd")

        loadOpt = PsdLoadOptions()
        loadOpt.load_effects_resource = True

        with PsdImage.load(sourceFile, loadOpt) as img:
            psd = cast(PsdImage, img)
            if psd.bits_per_channel != 32:
                raise Exception("Bits per channel should be 32 on start")
            psd.save(outputFile)

        Comparison.CheckAgainstEthalon(referenceFile, outputFile, 0)

        os.remove(outputFile)

    # Implement assigning filter masks data of FXidResource from Smart layer channels.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2873
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-336
    def PSDNET2873Test(self):
        srcFileName = "no_filter.psd"
        sourceFile = self.GetFileInBaseFolder(srcFileName)
        outputFile = self.GetFileInOutputFolder("out_PSDNET2873.psd")
        referenceFile = self.GetFileInBaseFolder("out_PSDNET2873.psd")

        # First pass – add EmbossSmartFilter
        with PsdImage.load(sourceFile) as img:
            psdImage = cast(PsdImage, img)

            # 1.1. Search for FXidResource
            fxidResource = None
            for resource in psdImage.global_layer_resources:
                if is_assignable(resource, FXidResource):
                    fxidResource = cast(FXidResource, resource)
                    break

            # 1.2. Make sure that FXidResource does not exist now
            assert fxidResource is None

            # 1.3. Create EmbossSmartFilter and add it to the SmartFilters collection of Smart layer
            smartObj = cast(SmartObjectLayer, psdImage.layers[1])
            filters = list(smartObj.smart_filters.filters)
            emboss = EmbossSmartFilter()
            emboss.angle = 180
            emboss.height = 10
            emboss.amount = 120
            filters.append(emboss)

            smartObj.smart_filters.filters = filters
            smartObj.smart_filters.update_resource_values()

            psdImage.save(outputFile)

        # Second pass – verify FXidResource and mask
        with PsdImage.load(outputFile) as img:
            psdImage = cast(PsdImage, img)

            # 2.1. Search for FXidResource
            fxidResource = None
            for resource in psdImage.global_layer_resources:
                if is_assignable(resource, FXidResource):
                    fxidResource = cast(FXidResource, resource)
                    break

            # 2.2. Make sure that FXidResource exists now and has 1 filter mask
            assert fxidResource is not None
            assert len(fxidResource.filter_effect_masks) == 1

            maskData = fxidResource.filter_effect_masks[0]

            # 2.3. Check parameters of newly added filter mask to FXidResource
            assert maskData.user_mask is not None
            assert maskData.sheet_mask is not None
            assert maskData.channels is not None
            assert len(maskData.channels) == 3

        Comparison.CheckAgainstEthalon(referenceFile, outputFile, 0)

    # [AI Format] Implementing the CFF font file handling with APS.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2540
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-337
    def PSDNET2540Test(self):
        sourceFile = self.GetFileInBaseFolder("cff_font_example.ai")
        outputFilePath = self.GetFileInOutputFolder("cff_font_example.png")

        with AiImage.load(sourceFile) as img:
            aiImage = cast(AiImage, img)
            aiImage.save(outputFilePath, PngOptions())

    # Loading of large PSB image 50.000×40.000 with artboard layers can not be loaded.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2788
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-338
    def PSDNET2788Test(self):
        source_zip = self.GetFileInBaseFolder("PRUEBA_PSB_COMPRESSED.zip")
        folder = os.path.dirname(source_zip)
        with zipfile.ZipFile(source_zip) as zf:
            zf.extractall(folder, pwd=None)

        source_file = self.GetFileInBaseFolder("PRUEBA_PSB_COMPRESSED.psb")
        output_file = self.GetFileInOutputFolder("PRUEBA_PSB_COMPRESSED.jpg")

        with PsdImage.load(source_file) as img:
            psd_image = cast(PsdImage, img)
            jpeg_opts = JpegOptions()
            jpeg_opts.quality = 60
            psd_image.save(output_file, jpeg_opts)

        os.remove(source_file)

    # [AI Format] Adding Aspose.Font into Aspose.PSD.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2758
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-339
    def PSDNET2758Test(self):
        sourceFile = self.GetFileInBaseFolder("cff_font_example.ai")
        outputFilePath = self.GetFileInOutputFolder("cff_font_example.png")

        with AiImage.load(sourceFile) as img:
            aiImage = cast(AiImage, img)
            aiImage.save(outputFilePath, PngOptions())

    # Support of modern blend mode names in Vstk Resource.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2860
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-340
    def PSDNET2860Test(self):
        srcFile = self.GetFileInBaseFolder("all_new_blend_modes_dont_resave.psd")
        outFile = self.GetFileInOutputFolder("all_new_blend_modes_dont_resave.png")

        loadOpt = PsdLoadOptions()
        loadOpt.load_effects_resource = True

        with Image.load(srcFile, loadOpt) as img:
            img.save(outFile, PngOptions())

        os.remove(outFile)

    # [AI Format] Fixing an issue with the dashed lines rendering.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2863
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-341
    def PSDNET2863Test(self):
        sourceFile = self.GetFileInBaseFolder("line_dash_example.ai")
        outputFilePath = self.GetFileInOutputFolder("line_dash_example.png")

        with AiImage.load(sourceFile) as img:
            aiImage = cast(AiImage, img)
            aiImage.save(outputFilePath, PngOptions())

    # [AI Format] Fixing rendering artifacts and missing content in text, gradients, clipping paths, lines, and blending.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2222
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-342
    def PSDNET2222Test(self):
        sourceFile = self.GetFileInBaseFolder("Input_4.ai")
        outputFilePath = self.GetFileInOutputFolder("Input_4.png")

        with AiImage.load(sourceFile) as img:
            aiImage = cast(AiImage, img)
            aiImage.save(outputFilePath, PngOptions())

LicenseHelper.set_license()
a = Release_26_09_Tests()
a.PSDNET2758Test()
