import numpy as np
import pytest
from aspose.psd import Image
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import CompressionMethod, PsdImage
from aspose.psd.fileformats.psd.layers import TextLayer
from aspose.psd.fileformats.psd.layers.layerresources import OSTypeStructure, PlacedResource
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.fileformats.psd.layers.warp import WarpStyles, WarpRotates
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import cast, is_assignable

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper


class Release_24_08_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Add handling for XObject Groups
    # https://issue.saltov.dynabic.com/issues/PSDNET-2091
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-81
    def PSDNET2091Test(self):
        pass

    # Enhance Warp transformation capabilities by adding WarpSettings for TextLayer and SmartObjectLayer
    # https://issue.saltov.dynabic.com/issues/PSDNET-1754
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-82
    def PSDNET1754Test(self):
        def GetWarpSettingsByIndex(warpParams, caseIndex):
            switcher = {
                0: {"Style": WarpStyles.RISE, "Rotate": WarpRotates.HORIZONTAL, "Value": 20},
                1: {"Style": WarpStyles.RISE, "Rotate": WarpRotates.VERTICAL, "Value": 10},
                2: {"Style": WarpStyles.FLAG, "Rotate": WarpRotates.HORIZONTAL, "Value": 30},
                3: {"Style": WarpStyles.CUSTOM}
            }
            params = switcher.get(caseIndex)
            if params:
                warpParams.style = params.get("Style")
                if params.get("Rotate") is not None:
                    warpParams.rotate = params.get("Rotate")
                if params.get("Value") is not None:
                    warpParams.value = params.get("Value")
                if caseIndex == 3:
                    warpParams.mesh_points[2].y += 70

            return warpParams

        sourceFile = self.GetFileInBaseFolder("smart_without_warp.psd")

        opt = PsdLoadOptions()
        opt.load_effects_resource = True
        opt.allow_warp_repaint = True
        outputImageFile = [None] * 4
        outputPsdFile = [None] * 4
        referencePngFile = [None] * 4
        pngOpt = PngOptions()
        pngOpt.compression_level = 9
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        for caseIndex in range(len(outputImageFile)):
            outputImageFile[caseIndex] = self.GetFileInOutputFolder("export_" + str(caseIndex) + ".png")
            outputPsdFile[caseIndex] = self.GetFileInOutputFolder("export_" + str(caseIndex) + ".psd")
            referencePngFile[caseIndex] = self.GetFileInBaseFolder("etalon_" + str(caseIndex + 1) + ".png")
            with PsdImage.load(sourceFile, opt) as image:
                img = cast(PsdImage, image)
                for layer in img.layers:
                    if is_assignable(layer, SmartObjectLayer):
                        smartLayer = cast(SmartObjectLayer, layer)
                        smartLayer.warp_settings = GetWarpSettingsByIndex(smartLayer.warp_settings, caseIndex)

                    if is_assignable(layer, TextLayer):
                        textLayer = cast(TextLayer, layer)
                        if caseIndex != 3:
                            textLayer.warp_settings = GetWarpSettingsByIndex(textLayer.warp_settings, caseIndex)

                img.save(outputPsdFile[caseIndex], PsdOptions())
                img.save(outputImageFile[caseIndex], PsdOptions())

            with PsdImage.load(outputPsdFile[caseIndex], opt) as img:
                img.save(outputImageFile[caseIndex], pngOpt)

            Comparison.CheckAgainstEthalon(outputImageFile[caseIndex], referencePngFile[caseIndex], 0)

    # Handle layers in content streams operators
    # https://issue.saltov.dynabic.com/issues/PSDNET-1836
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-83
    def PSDNET1836Test(self):
        sourceFile = self.GetFileInBaseFolder("Layers-NoPen.ai")
        outputFile = self.GetFileInOutputFolder("Layers-NoPen.output.png")
        referenceFile = self.GetFileInBaseFolder("Layers-NoPen.output.png")

        with AiImage.load(sourceFile) as image:
            image.save(outputFile, PngOptions())
        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0)

    # Rendering result of AI file is very different in comparison with Illustrator results
    # https://issue.saltov.dynabic.com/issues/PSDNET-2015
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-84
    def PSDNET2015Test(self):
        sourceFile = self.GetFileInBaseFolder("4.ai")
        outputFile = self.GetFileInOutputFolder("4_output.png")
        referenceFile = self.GetFileInBaseFolder("4_ethalon.png")

        with AiImage.load(sourceFile) as image:
            image.save(outputFile, PngOptions())
        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0)

    # Relink Smart Object doesn't apply to all Smart Objects in PSD file
    # https://issue.saltov.dynabic.com/issues/PSDNET-2093
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-85
    def PSDNET2093Test(self):
        files = ["simple_test", "w22"]
        change_file = self.GetFileInBaseFolder("image(19).png")

        for file in files:
            source_file = self.GetFileInBaseFolder(file + ".psd")
            reference_file = self.GetFileInBaseFolder(file + "_output.psd")
            output_file = self.GetFileInOutputFolder(file + "_output.psd")
            with Image.load(source_file) as img:
                image = cast(PsdImage, img)
                for layer in image.layers:
                    if is_assignable(layer, SmartObjectLayer):
                        smart_layer = cast(SmartObjectLayer, layer)
                        smart_layer.replace_contents(change_file)
                image.save(output_file)
                Comparison.CheckAgainstEthalon(output_file, reference_file, 0)

        self.remove_all_unzipped_files()

    def CUSTOMER1(self):
        source = "C:\\Users\\dimsa\\Downloads\\iphone13snapcase.psd\\iphone13snapcase.psd"
        change_file = "C:\\Users\\dimsa\\Downloads\\iphone13snapcase.psd\\Python_logo_and_wordmark.svg.png"
        output_file = "C:\\Users\\dimsa\\Downloads\\iphone13snapcase.psd\\output.png"
        with Image.load(source) as img:
            image = cast(PsdImage, img)
            for layer in image.layers:
                if (layer.display_name == "ARTHERE"):
                    smart_layer = cast(SmartObjectLayer, layer)
                    #smart_layer.update_modified_content()
                    ##smart_layer.()
                    smart_layer.relink_to_file(change_file)
                    #smart_layer.replace_contents(change_file)
            pngOpt = PngOptions
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            image.save(output_file, pngOpt)

LicenseHelper.set_license()
a = Release_24_08_Tests()
a.CUSTOMER1()