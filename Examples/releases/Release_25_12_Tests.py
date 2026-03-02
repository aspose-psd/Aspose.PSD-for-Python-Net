import pytest
from aspose.psd import DataRecoveryMode
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers.layerresources import LsdkResource, SoLdResource
from aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures import DescriptorStructure, ListStructure, \
    ReferenceStructure, NameStructure
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import cast

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_25_12_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # [AI Format] Implement Soft Mask.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2325
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-269
    def PSDNET2325Test(self):
        source_file = self.GetFileInBaseFolder("Strawberry_jam_packaging.ai")
        output_file = self.GetFileInOutputFolder("Strawberry_jam_packaging.png")
        reference_file = self.GetFileInBaseFolder("Strawberry_jam_packaging.png")

        with AiImage.load(source_file) as img:
            img.save(output_file, PngOptions())

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)

    # [AI Format] Implementing the DeviceN ColorSpace handling.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2458
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-270
    def PSDNET2458Test(self):
        source_file = self.GetFileInBaseFolder("2458.ai")
        output_file = self.GetFileInOutputFolder("2458.png")
        reference_file = self.GetFileInBaseFolder("2458.png")

        with AiImage.load(source_file) as img:
            ai_image = cast(AiImage, img)
            ai_image.save(output_file, PngOptions())

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)

    # Implement support for LsdkResource.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2594
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-271
    def PSDNET2594Test(self):
        inputFile = self.GetFileInBaseFolder("123 1.psd")
        outputFile = self.GetFileInOutputFolder("output.psd")
        referenceFile = self.GetFileInBaseFolder("output.psd")

        loadOpt = PsdLoadOptions()
        loadOpt.load_effects_resource = True

        # First pass - load and modify
        with PsdImage.load(inputFile, loadOpt) as img:
            psdImage = cast(PsdImage, img)
            res = cast(LsdkResource, psdImage.layers[8].resources[3])
            assert res.length == 4

            psdImage.save(outputFile)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0)

        # Second pass - verify changes
        with PsdImage.load(outputFile, loadOpt) as img:
            psdImage = cast(PsdImage, img)
            res = cast(LsdkResource, psdImage.layers[8].resources[3])
            assert res.length == 4

    # [AI Format] Resolving rendering issues.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2220
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-181
    def PSDNET2220Test(self):
        source_file = self.GetFileInBaseFolder("Input_2.ai")
        output_file = self.GetFileInOutputFolder("Input_2.png")
        reference_file = self.GetFileInBaseFolder("Input_2.png")

        with AiImage.load(source_file) as img:
            img.save(output_file, PngOptions())

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)

    # Abnormal export of a specific Image to PNG/JPG Format.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2373
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-272
    def PSDNET2373Test(self):
        srcFile = self.GetFileInBaseFolder("123.psd")
        outFile = self.GetFileInOutputFolder("output.png")
        refFile = self.GetFileInBaseFolder("output.png")

        loadOpt = PsdLoadOptions()
        loadOpt.load_effects_resource = True

        with PsdImage.load(srcFile, loadOpt) as img:
            psdImage = cast(PsdImage, img)
            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            psdImage.save(outFile, pngOpt)

        Comparison.CheckAgainstEthalon(outFile, refFile, 0)

    # In the file with the specified SmartObject, throws an exception: Unable to cast object of type System.Int32 to type ‘System.Collections.Generic.Dictionary.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2469
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-273
    def PSDNET2469Test(self):
        sourceFilePath = self.GetFileInBaseFolder("Test_File.psd")
        outputFilePath = self.GetFileInOutputFolder("output.psd")
        referenceFilePath = self.GetFileInBaseFolder("output.psd")

        with PsdImage.load(sourceFilePath) as img:
            psdImageCopy = cast(PsdImage, img)
            imageOptions = PsdOptions(psdImageCopy)
            psdImageCopy.save(outputFilePath, imageOptions)

        Comparison.CheckAgainstEthalon(outputFilePath, referenceFilePath, 0)

    # [AI Format] Fixing regression at AI rendering.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2564
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-172
    def PSDNET2564Test(self):
        sourceFile = self.GetFileInBaseFolder("example.ai")
        outputFile = self.GetFileInOutputFolder("example.png")
        reference_file = self.GetFileInBaseFolder("example.png")

        with AiImage.load(sourceFile) as img:
            psdImage = cast(AiImage, img)
            psdImage.save(outputFile, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile, reference_file, 0)

    # Aspose.PSD generates a corrupted PSD file if a SmartObject is present.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2616
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-274
    def PSDNET2616Test(self):
        inputFile = self.GetFileInBaseFolder("LogoOutside.psd")
        outputFile = self.GetFileInOutputFolder("output.psd")
        referenceFile = self.GetFileInBaseFolder("output.psd")

        with PsdImage.load(inputFile) as img:
            psdImage = cast(PsdImage, img)
            imageOptions = PsdOptions(psdImage)
            psdImage.save(outputFile, imageOptions)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0)

    # Layers with a clipping mask render with some stroke from base pixels.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2634
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-275
    def PSDNET2634Test(self):
        inputFile = self.GetFileInBaseFolder("foldersAndFigures.psd")
        outputFile = self.GetFileInOutputFolder("output.png")
        referenceFile = self.GetFileInBaseFolder("output.png")

        with PsdImage.load(inputFile) as psdImage:
            psdImage.save(outputFile, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0)