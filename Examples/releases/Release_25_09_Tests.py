import pytest
from aspose.psd import Rectangle, Image, DataRecoveryMode, Color, ResolutionSetting
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
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


class Release_25_09_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Create for PSD load options a parameter that gives the ability to edit XmpData in Read-Only Mode
    # https://issue.saltov.dynabic.com/issues/PSDNET-2382
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-235
    def PSDNET2382Test(self):
        sourceFile = self.GetFileInBaseFolder("psdnet2382.psd")
        outputFile = self.GetFileInOutputFolder("output.psd")
        referenceFile = self.GetFileInBaseFolder("output.psd")
        testMetadata = "Updated metadata text"

        opt = PsdLoadOptions()

        opt.read_only_mode = True
        opt.read_only_type = ReadOnlyMode.METADATA_EDIT
        with PsdImage.load(sourceFile, opt) as image:
            psdImage = cast(PsdImage, image)
            xmp_data = cast(XmpPacketWrapper, psdImage.xmp_data)

            assert testMetadata != xmp_data.meta.adobe_xmp_toolkit

            psdImage.xmp_data.meta.adobe_xmp_toolkit = testMetadata

            psdImage.save(outputFile)

        with PsdImage.load(outputFile) as image:
            psdImage = cast(PsdImage, image)
            xmp_data = cast(XmpPacketWrapper, psdImage.xmp_data)
            assert testMetadata == xmp_data.meta.adobe_xmp_toolkit

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # [AI Format] Investigate an AIImage rendering problem that appears on macOS
    # https://issue.saltov.dynabic.com/issues/PSDNET-2284
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-236
    def PSDNET2284Test(self):
        sourceFile = self.GetFileInBaseFolder("ai_one.ai")
        outputFile = self.GetFileInOutputFolder("ai_one.png")
        referenceFile = self.GetFileInBaseFolder("ai_one.png")

        with AiImage.load(sourceFile) as image:
            image.save(outputFile, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # The saved PSD file cannot be opened
    # https://issue.saltov.dynabic.com/issues/PSDNET-2300
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-237
    def PSDNET2300Test(self):
        inputFile = self.GetFileInBaseFolder("ZNDX.psd")
        replaceFile = self.GetFileInBaseFolder("TRF6242.png")
        outputFile = self.GetFileInOutputFolder("output.psd")
        referenceFile = self.GetFileInBaseFolder("output.psd")

        with PsdImage.load(inputFile, PsdLoadOptions()) as image:
            psdImage = cast(PsdImage, image)
            with open(replaceFile, "rb") as stream:
                smartObjectLayer = SmartObjectLayer(stream)
                layers = list(psdImage.layers)

                if layers:
                    layers.pop(0)

                layers.insert(0, smartObjectLayer)
                psdImage.layers = layers

                lnk2Resource = cast(Lnk2Resource, psdImage.global_layer_resources[1])
                assert lnk2Resource.data_source_count == 1

                psdImage.save(outputFile)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # The error: Image saving failed in the file with Artboard Layers
    # https://issue.saltov.dynabic.com/issues/PSDNET-2431
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-238
    def PSDNET2431Test(self):
        sourceFile = self.GetFileInBaseFolder("2431_src_file.psd")
        outputFile = self.GetFileInOutputFolder("output.psd")
        referenceFile = self.GetFileInBaseFolder("output.psd")

        with Image.load(sourceFile) as image:
            imageOptions = PsdOptions(image)
            image.save(outputFile, imageOptions)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)
        self.remove_all_unzipped_files()

    # A specific PSD file can not be exported to BMP format
    # https://issue.saltov.dynabic.com/issues/PSDNET-2449
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-239
    def PSDNET2449Test(self):
        inputFile = self.GetFileInBaseFolder("06-01-2.psd")
        outputFile = self.GetFileInOutputFolder("output.bmp")
        referenceFile = self.GetFileInBaseFolder("output.bmp")

        with Image.load(inputFile) as image:
            image.save(outputFile, BmpOptions())

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # Replacement of a smart object using an image instead of a path doesn't work
    # https://issue.saltov.dynabic.com/issues/PSDNET-2505
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-240
    def PSDNET2505Test(self):
        sourceFile = self.GetFileInBaseFolder("B.psd")
        replacementImagePath = self.GetFileInBaseFolder("logo.png")
        outputFile = self.GetFileInOutputFolder("output.png")
        referenceFile = self.GetFileInBaseFolder("output.png")
        layerName = "GC-LARGE"

        loadOptions = PsdLoadOptions()
        loadOptions.load_effects_resource = True
        loadOptions.allow_warp_repaint = True

        with PsdImage.load(sourceFile, loadOptions) as img:
            image = cast(PsdImage, img)
            for layer in image.layers:
                if layer.name == layerName:
                    smartLayer = cast(SmartObjectLayer, layer)
                    if smartLayer:
                        resolution = ResolutionSetting(96, 96)

                        with Image.load(replacementImagePath) as rep:
                            smartLayer.replace_contents(rep, resolution)

                        smartLayer.update_modified_content()
                        break

            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            image.save(outputFile, pngOpt)

            Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)
            self.remove_all_unzipped_files()

    # Transparency lost after replacing smart object layers
    # https://issue.saltov.dynabic.com/issues/PSDNET-2506
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-241
    def PSDNET2506Test(self):
        sourceFile = self.GetFileInBaseFolder("B.psd")
        replacementImagePath = self.GetFileInBaseFolder("logo.png")
        outputFile = self.GetFileInOutputFolder("output.png")
        referenceFile = self.GetFileInBaseFolder("output.png")
        layerName = "GC-LARGE"


        loadOptions = PsdLoadOptions()
        loadOptions.load_effects_resource = True
        loadOptions.allow_warp_repaint = True

        with PsdImage.load(sourceFile, loadOptions) as img:
            image = cast(PsdImage, img)
            for layer in image.layers:
                if layer.name == layerName:
                    smartLayer = cast(SmartObjectLayer, layer)
                    if smartLayer:
                        resolution = ResolutionSetting(96, 96)

                        smartLayer.replace_contents(replacementImagePath, resolution)

                        smartLayer.update_modified_content()
                        break

            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            image.save(outputFile, pngOpt)

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)
        self.remove_all_unzipped_files()

    # Broken PSD file after export
    # https://issue.saltov.dynabic.com/issues/PSDNET-2515
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-242
    def PSDNET2515Test(self):
        inputFile = self.GetFileInBaseFolder("smart_Test.psd")
        replaceFile = self.GetFileInBaseFolder("newImage.png")
        outputFile = self.GetFileInOutputFolder("export.psd")
        referenceFile = self.GetFileInBaseFolder("export.psd")

        with PsdImage.load(inputFile) as image:
            psdImage = cast(PsdImage, image)
            smartObjectLayer = cast(SmartObjectLayer, psdImage.layers[1])

            assert is_assignable(smartObjectLayer.resources[9], PlLdResource)
            assert is_assignable(smartObjectLayer.resources[10], SoLdResource)
            assert is_assignable(smartObjectLayer.resources[11], FxrpResource)

            lnk2Resource = cast(Lnk2Resource, psdImage.global_layer_resources[1])
            lnkeResrource = cast(LnkeResource, psdImage.global_layer_resources[2])
            assert lnk2Resource
            assert lnkeResrource
            assert lnk2Resource.data_source_count == 1
            assert lnkeResrource.data_source_count == 0

            smartObjectLayer.replace_contents(replaceFile)

            assert is_assignable(smartObjectLayer.resources[9], SoLeResource)
            assert is_assignable(smartObjectLayer.resources[10], FxrpResource)
            assert lnk2Resource.data_source_count == 0
            assert lnkeResrource.data_source_count == 1

            smartObjectLayer.embed_linked()

            assert is_assignable(smartObjectLayer.resources[9], PlLdResource)
            assert is_assignable(smartObjectLayer.resources[10], SoLdResource)
            assert is_assignable(smartObjectLayer.resources[11], FxrpResource)
            assert lnk2Resource.data_source_count == 1
            assert lnkeResrource.data_source_count == 0

            psdImage.save(outputFile, PsdOptions())

            Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # [Regression] Fix freeze on export AiImage while parsing of EPSF files
    # https://issue.saltov.dynabic.com/issues/PSDNET-2541
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-243
    def PSDNET2541Test(self):
        inputFile = self.GetFileInBaseFolder("[SA]_ID_card_template.ai")
        outputFile = self.GetFileInOutputFolder("output.png")
        referenceFile = self.GetFileInBaseFolder("output.png")

        with AiImage.load(inputFile) as image:
            image.save(outputFile, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 0, 1)

    # Missed the Header of AiImage
    # https://issue.saltov.dynabic.com/issues/PSDNET-2543
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-244
    def PSDNET2543Test(self):
        inputFile = self.GetFileInBaseFolder("PdfbasedAi.ai")

        with AiImage.load(inputFile) as img:
            image = cast(AiImage, img)
            assert image.header
            assert image.header.title == "PdfbasedAi"
            assert image.header.creator == "Adobe Illustrator 25.4 (Windows)"
            assert image.header.creation_date == "D:20241218201621+04'00'"

#LicenseHelper.set_license()
#a = Release_25_09_Tests()
#a.PSDNET2543Test()