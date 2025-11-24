import io

import pytest
from aspose.psd import Rectangle, Image, DataRecoveryMode, Color, ResolutionSetting, FontSettings
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage, CompressionMethod
from aspose.psd.fileformats.psd.layers import TextLayer
from aspose.psd.fileformats.psd.layers.layerresources import SoLdResource, Lnk2Resource, PlLdResource, FxrpResource, \
    LnkeResource, SoLeResource
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.imageloadoptions import PsdLoadOptions, ReadOnlyMode
from aspose.psd.imageoptions import PngOptions, PsdOptions, GifOptions, BmpOptions
from aspose.psd.xmp import XmpPacketWrapper
from aspose.pycore import cast, as_of, is_assignable

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper


class Release_25_10_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # [AI Format] Implementing Type 3 (Radial) Shading
    # https://issue.saltov.dynabic.com/issues/PSDNET-2437
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-246
    def PSDNET2437Test(self):
        sourceFile = self.GetFileInBaseFolder("Input_2.ai")
        outputFile = self.GetFileInOutputFolder("Input_2.png")
        referenceFile = self.GetFileInBaseFolder("Input_2.png")

        with AiImage.load(sourceFile) as image:
            image.save(outputFile, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # Optimization of Aspose.PSD rendering performance for large images
    # https://issue.saltov.dynabic.com/issues/PSDNET-2542
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-247
    def PSDNET2542Test(self):
        sourceFile = self.GetFileInBaseFolderByIssue("PSDNET-2052", "bigfile.psd")
        outputFile = self.GetFileInOutputFolder("output_raw.psd")

        loadOptions = PsdLoadOptions()
        loadOptions.load_effects_resource = True
        loadOptions.use_disk_for_load_effects_resource = True

        opt = PsdOptions()
        opt.compression_method = CompressionMethod.RLE
        with PsdImage.load(sourceFile, loadOptions) as psdImage:
            psdImage.save(outputFile, )

        # No comparison here. Because nothing changed
        self.remove_all_unzipped_files()

    # If you modify the TextLayer and save the PSD file, an error occurs
    # https://issue.saltov.dynabic.com/issues/PSDNET-1953
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-248
    def PSDNET1953Test(self):
        sourceFile = self.GetFileInBaseFolder("35dd4d12-1301-4750-8cac-45052ac8678a_083_007.psd")
        outputFile = self.GetFileInOutputFolder("output.psd")
        referenceFile = self.GetFileInBaseFolder("output.psd")

        FontSettings.remove_font_cache_file()

        opt = PsdLoadOptions()
        opt.load_effects_resource = True

        with PsdImage.load(sourceFile, opt) as img:
            image = cast(PsdImage, img)
            for layer in image.layers:
                if (is_assignable(layer, TextLayer)):
                    textLayer = as_of(layer, TextLayer)
                    if textLayer is not None:
                        textLayer.update_text("SUCCESS")

            image.save(outputFile)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)
        self.remove_all_unzipped_files()

    # Editing of text in the specific PSD File throws a null reference exception on fontStyleRecord parsing
    # https://issue.saltov.dynabic.com/issues/PSDNET-2032
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-249
    def PSDNET2032Test(self):
        sourceFile = self.GetFileInBaseFolder("bd-worlds-best-pink.psd")
        outputFile = self.GetFileInOutputFolder("output.psd")
        referenceFile = self.GetFileInBaseFolder("output.psd")

        psdLoadOptions = PsdLoadOptions()
        psdLoadOptions.load_effects_resource = True
        psdLoadOptions.allow_warp_repaint = True
        FontSettings.remove_font_cache_file()

        with PsdImage.load(sourceFile, psdLoadOptions) as img:
            image = cast(PsdImage, img)
            for layer in image.layers:
                if (is_assignable(layer, TextLayer)):
                    textLayer = cast(TextLayer, layer)
                    if textLayer is not None and textLayer.name == "best":
                        textLayer.update_text("SUCCESS")
            image.save(outputFile)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)
        self.remove_all_unzipped_files()


    # Fix the issue with saving large files
    # https://issue.saltov.dynabic.com/issues/PSDNET-2087
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-250
    def PSDNET2087Test(self):
        sourceFile = self.GetFileInBaseFolder("bigfile.psd")
        outputFile = self.GetFileInOutputFolder("export.png")
        referenceFile = self.GetFileInBaseFolder("export.png")

        loadOptions = PsdLoadOptions()
        loadOptions.load_effects_resource = True
        loadOptions.allow_warp_repaint = True

        pngOpt = PngOptions()
        pngOpt.compression_level = 9
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        with PsdImage.load(sourceFile, loadOptions) as img:
            img.save(outputFile, pngOpt)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)
        self.remove_all_unzipped_files()

    # Regression. An exception occurs whenever saving PSD files with a size of more than 200 MB and large dimensions
    # https://issue.saltov.dynabic.com/issues/PSDNET-2294
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-251
    def PSDNET2294Test(self):
        sourceFile = self.GetFileInBaseFolderByIssue("PSDNET-2052", "bigfile.psd")

        loadOptions = PsdLoadOptions()
        loadOptions.load_effects_resource = True
        loadOptions.use_disk_for_load_effects_resource = True

        with PsdImage.load(sourceFile, loadOptions) as img:
             with io.BytesIO() as saveAsStream:
                img.save(saveAsStream)

        self.remove_all_unzipped_files()

    # Impossible to open the PSD file because of a null reference in SmartObjectResource
    # https://issue.saltov.dynabic.com/issues/PSDNET-2346
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-252
    def PSDNET2346Test(self):
        sourceFile = self.GetFileInBaseFolder("Mixer_ipad_Hand_W_crash.psd")
        outputFile = self.GetFileInOutputFolder("export.png")
        referenceFile = self.GetFileInBaseFolder("export.png")


        loadOptions = PsdLoadOptions()
        loadOptions.load_effects_resource = True
        loadOptions.allow_warp_repaint = True

        pngOpt = PngOptions()
        pngOpt.compression_level = 9
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        with PsdImage.load(sourceFile, loadOptions) as img:
            img.save(outputFile, pngOpt)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)
        self.remove_all_unzipped_files()

    # Smart Object Replace in the specific file doesn't work
    # https://issue.saltov.dynabic.com/issues/PSDNET-2395
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-253
    def PSDNET2395Test(self):
        fileName = self.GetFileInBaseFolder("etikett var 3d.psd")
        replaceFileName = self.GetFileInBaseFolder("Komplett2.jpg")
        outputFile = self.GetFileInOutputFolder("output.png")
        referenceFile = self.GetFileInBaseFolder("output.png")

        psdOptions = PsdLoadOptions()
        psdOptions.allow_warp_repaint = True
        psdOptions.load_effects_resource = True

        pngOpt = PngOptions()
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        with PsdImage.load(fileName, psdOptions) as img:
            psdImage = cast(PsdImage, img)
            for myLayer in psdImage.layers:
                if isinstance(myLayer, SmartObjectLayer):
                    mySmartObjectLayer = cast(SmartObjectLayer, myLayer)
                    mySmartObjectLayer.replace_contents(replaceFileName, True)
                    mySmartObjectLayer.update_modified_content()

            psdImage.save(outputFile, pngOpt)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # The ImageLoadException occurs when loading AI files
    # https://issue.saltov.dynabic.com/issues/PSDNET-2476
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-254
    def PSDNET2476Test(self):
        sourceFile_1 = self.GetFileInBaseFolder("3.ai")
        outputFile_1 = self.GetFileInOutputFolder("3.png")
        referenceFile_1 = self.GetFileInBaseFolder("3.png")

        with AiImage.load(sourceFile_1) as image:
            image.save(outputFile_1, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile_1, referenceFile_1, 0, 1)

        sourceFile_2 = self.GetFileInBaseFolder("IcoMoon.ai")
        outputFile_2 = self.GetFileInOutputFolder("IcoMoon.png")
        referenceFile_2 = self.GetFileInBaseFolder("IcoMoon.png")

        with AiImage.load(sourceFile_2) as image:
            image.save(outputFile_2, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile_2, referenceFile_2, 0, 1)

    # [AI Format] The NullReferenceException occurs when loading specific files
    # https://issue.saltov.dynabic.com/issues/PSDNET-2477
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-255
    def PSDNET2477Test(self):
        sourceFile = self.GetFileInBaseFolder("Strawberry_jam_packaging.ai")
        outputFile = self.GetFileInOutputFolder("Strawberry_jam_packaging.png")
        referenceFile = self.GetFileInBaseFolder("Strawberry_jam_packaging.png")

        with AiImage.load(sourceFile) as image:
            image.save(outputFile, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # [AI Format] The ImageLoadingException occurs on opening of a specific AI File
    # https://issue.saltov.dynabic.com/issues/PSDNET-2494
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-256
    def PSDNET2494Test(self):
        sourceFile = self.GetFileInBaseFolder("379569.ai")
        outputFile_0 = self.GetFileInOutputFolder("379569_0.png")
        outputFile_1 = self.GetFileInOutputFolder("379569_1.png")
        referenceFile_0 = self.GetFileInBaseFolder("379569_0.png")
        referenceFile_1 = self.GetFileInBaseFolder("379569_1.png")

        with AiImage.load(sourceFile) as img:
            image = cast(AiImage, img)
            image.active_page_index = 0
            image.save(outputFile_0, PngOptions())

            image.active_page_index = 1
            image.save(outputFile_1, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile_0, referenceFile_0, 0, 1)
        Comparison.CheckAgainstEthalon(outputFile_1, referenceFile_1, 0, 1)

    # Rendering of the Gradient Effect in specific files doesn't work
    # https://issue.saltov.dynabic.com/issues/PSDNET-2565
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-257
    def PSDNET2565Test(self):
        inputFile = self.GetFileInBaseFolder("iphone15snapcase(1).psd")
        outputFile = self.GetFileInOutputFolder("output.png")
        referenceFile = self.GetFileInBaseFolder("output.png")

        psdOpt = PsdLoadOptions()
        psdOpt.load_effects_resource = True

        pngOpt = PngOptions()
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        with PsdImage.load(inputFile, psdOpt) as img:
            img.save(outputFile, pngOpt)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # [Regression] Fix updating the LnkeResource on replacing smart objects
    # https://issue.saltov.dynabic.com/issues/PSDNET-2570
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-258
    def PSDNET2570Test(self):
        inputFile = self.GetFileInBaseFolder("w22.psd")
        changeFile = self.GetFileInBaseFolder("image(19).png")
        outputFile = self.GetFileInOutputFolder("output.psd")
        referenceFile = self.GetFileInBaseFolder("output.psd")

        with PsdImage.load(inputFile) as img:
            image = cast(PsdImage, img)
            lnkeResource = cast(LnkeResource, image.global_layer_resources[5])

            assert 1 == lnkeResource.data_source_count
            oldUniqueId = lnkeResource[0].unique_id

            for layer in image.layers:
                if is_assignable(layer, SmartObjectLayer):
                    smart = cast(SmartObjectLayer, layer)
                    smart.replace_contents(changeFile)

            # Check that old data source has changed
            assert 1 == lnkeResource.data_source_count
            assert lnkeResource[0].unique_id != oldUniqueId

            image.save(outputFile)

        self.remove_all_unzipped_files()