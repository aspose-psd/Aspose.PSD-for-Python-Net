import time
import uuid

import psutil
import pytest
from aspose.psd import Image, FontSettings, FileFormat, Rectangle, Color
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers import ShapeLayer
from aspose.psd.fileformats.psd.layers.filllayers import FillLayer
from aspose.psd.fileformats.psd.layers.layerresources import PattResource
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import cast, as_of

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper


class Release_24_02_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Handle Angle property for PatternFillSettings
    # https://issue.saltov.dynabic.com/issues/PSDNET-1503
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-28
    def PSDNET1503Test(self):
        fileName = "PatternFillLayerWide_0"
        sourceFile = self.GetFileInBaseFolder(fileName + ".psd")
        outputFile = self.GetFileInOutputFolder(fileName + "_output.psd")
        etalonFile = self.GetFileInBaseFolder(fileName + "_etalon.psd")

        loadOpt = PsdLoadOptions()
        loadOpt.load_effects_resource = True
        with PsdImage.load(sourceFile, loadOpt) as img:
            image = cast(PsdImage, img)
            fillLayer = cast(FillLayer, image.layers[1])
            fillSettings = fillLayer.fill_settings
            fillSettings.angle = 70
            fillLayer.update()
            image.save(outputFile, PsdOptions())

        with PsdImage.load(outputFile, loadOpt) as img:
            image = cast(PsdImage, img)
            fillLayer = cast(FillLayer, image.layers[1])
            fillSettings = fillLayer.fill_settings

            assert fillSettings.angle == 70

        Comparison.CheckAgainstEthalon(outputFile, etalonFile, 1)

    # Support of vertical and horizontal scale for TextLayer
    # https://issue.saltov.dynabic.com/issues/PSDNET-1719
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-29
    def PSDNET1719Test(self):
           sourceFile = self.GetFileInBaseFolder("1719_src.psd")
           etalonFile = self.GetFileInBaseFolder("out_1719.png")
           outputFile = self.GetFileInOutputFolder("output.png")

           # Add a few fonts
           fontsFolder = self.GetFileInBaseFolder("1719_Fonts")
           fontFolders = list(FontSettings.get_fonts_folders())
           fontFolders.append(fontsFolder)
           FontSettings.set_fonts_folders(fontFolders, True)

           with PsdImage.load(sourceFile) as image:
               image.save(outputFile, PngOptions())

           Comparison.CheckAgainstEthalon(outputFile, etalonFile, 1)

    # [AI Format] Implement correct rendering of background in PDF-Based AI Format.
    # https://issue.saltov.dynabic.com/issues/PSDNET-1783
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-33
    def PSDNET1783Test(self):
           sourceFile = self.GetFileInBaseFolder("pineapples.ai")
           outputFile  = self.GetFileInOutputFolder("pineapples.png")
           etalonFile = self.GetFileInBaseFolder("pineapples.png")

           with AiImage.load(sourceFile) as image:
               image.save(outputFile, PngOptions())

           Comparison.CheckAgainstEthalon(outputFile, etalonFile, 1)

    # "Image loading failed." exception when open document
    # https://issue.saltov.dynabic.com/issues/PSDNET-995
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-36
    def PSDNET995Test(self):
        # Porting the following code in the same way:
        sourceFile1 = self.GetFileInBaseFolder("PRODUCT.ai")
        referenceFile1 = self.GetFileInBaseFolder("PRODUCT.png")
        outputFile1 = self.GetFileInOutputFolder("PRODUCT.png")

        with AiImage.load(sourceFile1) as image:
            image.save(outputFile1, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile1, referenceFile1, 1)

        sourceFile2 = self.GetFileInBaseFolder("Dolota.ai")
        referenceFile2 = self.GetFileInBaseFolder("Dolota.png")
        outputFile2 = self.GetFileInOutputFolder("Dolota.png")

        with AiImage.load(sourceFile2) as image:
            image.save(outputFile2, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile2, referenceFile2, 1)

        sourceFile3 = self.GetFileInBaseFolder("ARS_novelty_2108_out_01(1).ai")
        referenceFile3 = self.GetFileInBaseFolder("ARS_novelty_2108_out_01(1).png")
        outputFile3 = self.GetFileInOutputFolder("ARS_novelty_2108_out_01(1).png")

        with AiImage.load(sourceFile3) as image:
            image.save(outputFile3, PngOptions())

        Comparison.CheckAgainstEthalon(outputFile3, referenceFile3, 1)

        sourceFile4 = self.GetFileInBaseFolder("bit_gear.ai")
        referenceFile4 = self.GetFileInBaseFolder("bit_gear.png")
        outputFile4 = self.GetFileInOutputFolder("bit_gear.png")

        with AiImage.load(sourceFile4) as image:
            image.save(outputFile4, PngOptions())
        Comparison.CheckAgainstEthalon(outputFile4, referenceFile4, 1)

        sourceFile5 = self.GetFileInBaseFolder("test.ai")
        referenceFile5 = self.GetFileInBaseFolder("test.png")
        outputFile5 = self.GetFileInOutputFolder("test.png")

        with AiImage.load(sourceFile5) as image:
            image.save(outputFile5, PngOptions())
        Comparison.CheckAgainstEthalon(outputFile5, referenceFile5, 1)

    # Fix saving psd files having Stroke Pattern
    # https://issue.saltov.dynabic.com/issues/PSDNET-1491
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-37
    def PSDNET1491Test(self):
        sourceFile = self.GetFileInBaseFolder("StrokeShapePattern.psd")
        referenceFile = self.GetFileInBaseFolder("StrokeShapePattern_output.psd")
        outputFile = self.GetFileInOutputFolder("StrokeShapePattern_output.psd")

        newPatternBounds = Rectangle(0, 0, 4, 4)
        guid = str(uuid.uuid4())
        newPatternName = "$$$/Presets/Patterns/HorizontalLine1=Horizontal Line 9\0"
        newPattern = [
            Color.aqua.to_argb(), Color.red.to_argb(), Color.red.to_argb(), Color.aqua.to_argb(),
            Color.aqua.to_argb(), Color.white.to_argb(), Color.white.to_argb(), Color.aqua.to_argb(),
            Color.aqua.to_argb(), Color.white.to_argb(), Color.white.to_argb(), Color.aqua.to_argb(),
            Color.aqua.to_argb(), Color.red.to_argb(), Color.red.to_argb(), Color.aqua.to_argb(),
        ]

        with PsdImage.load(sourceFile) as img:
            image = cast(PsdImage, img)
            shapeLayer = cast(ShapeLayer, image.layers[1])
            strokeInternalFillSettings = shapeLayer.fill

            pattResource = None
            for globalLayerResource in image.global_layer_resources:


                pattResource = as_of(globalLayerResource, PattResource)
                if pattResource is not None:
                    patternItem = pattResource.patterns[0]  # Stroke internal pattern data

                    patternItem.pattern_id = guid
                    patternItem.name = newPatternName
                    patternItem.set_pattern(newPattern, newPatternBounds)
                    break


            strokeInternalFillSettings.pattern_name = newPatternName
            strokeInternalFillSettings.pattern_id = guid + "\0"

            shapeLayer.update()

            image.save(outputFile)

        # Check changed data.
        with PsdImage.load(outputFile) as img:
            image = cast(PsdImage, img)
            shapeLayer = cast(ShapeLayer, image.layers[1])
            strokeInternalFillSettings = shapeLayer.fill

            assert guid.upper() == strokeInternalFillSettings.pattern_id
            assert newPatternName == strokeInternalFillSettings.pattern_name + "\0"
        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 1)

    # Handle Angle property for PatternFillSettings
    # https://issue.saltov.dynabic.com/issues/PSDNET-1642
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-38
    def PSDNET1642Test(self):
        inputFile = self.GetFileInBaseFolder("source.psd")
        reference = self.GetFileInBaseFolder("output.png")
        output2 = self.GetFileInOutputFolder("output.png")

        psdLoadOptions = PsdLoadOptions()
        psdLoadOptions.load_effects_resource = True

        with PsdImage.load(inputFile, psdLoadOptions) as image:
            psdImage = cast(PsdImage, image)
            smartObject = cast(SmartObjectLayer, psdImage.layers[1])

            smartObjectImage = cast(PsdImage, smartObject.load_contents(psdLoadOptions))

            with smartObjectImage:
                smartObject.replace_contents(smartObjectImage)

            pngOpt = PngOptions()
            pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
            psdImage.save(output2, pngOpt)

        Comparison.CheckAgainstEthalon(output2, reference, 1)

    # [AI Format] Fix the Cubic Bezier rendering at AI file
    # https://issue.saltov.dynabic.com/issues/PSDNET-1884
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-39
    def PSDNET1884Test(self):
        sourceFile = self.GetFileInBaseFolder("Typography.ai")
        reference = self.GetFileInBaseFolder("Typography.png")
        outputFilePath = self.GetFileInOutputFolder("Typography.png")

        with AiImage.load(sourceFile) as image:
            image.save(outputFilePath, PngOptions())

        Comparison.CheckAgainstEthalon(outputFilePath, reference, 1)

    # Change Distort mechanism in warp
    # https://issue.saltov.dynabic.com/issues/PSDNET-1611
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-34
    def PSDNET1611Test(self):
        sourceFile = self.GetFileInBaseFolder("crow_grid.psd")
        reference = self.GetFileInBaseFolder("export.png")
        outputFile = self.GetFileInOutputFolder("export.png")

        opt = PsdLoadOptions()
        opt.load_effects_resource = True
        opt.allow_warp_repaint = True

        pngOpt = PngOptions()
        pngOpt.compression_level = 9
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA
        with PsdImage.load(sourceFile, opt) as img:
            img.save(outputFile, pngOpt)

        Comparison.CheckAgainstEthalon(outputFile, reference, 1)

        # Change Distort mechanism in warp
        # https://issue.saltov.dynabic.com/issues/PSDNET-1611

    # Speed up warp
    # https://issue.saltov.dynabic.com/issues/PSDNET-1802
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-35
    def PSDNET1802Test(self):
        sourceFile = self.GetFileInBaseFolder("output.psd")
        referenceFile = self.GetFileInBaseFolder("export.png")
        outputFile = self.GetFileInOutputFolder("export.png")

        opt = PsdLoadOptions()
        opt.load_effects_resource = True
        opt.allow_warp_repaint = True

        start_time = time.time()

        pngOpt = PngOptions()
        pngOpt.compression_level = 9
        pngOpt.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

        with PsdImage.load(sourceFile, opt) as img:
            img.save(outputFile, pngOpt)

        elapsed_time = time.time() - start_time

        # old value = 193300
        # new value =  55500
        time_in_sec = int(elapsed_time * 1000)
        if time_in_sec > 100000:
            raise Exception("Process time is too long")

        Comparison.CheckAgainstEthalon(outputFile, referenceFile, 1)

#LicenseHelper.set_license()
#a = Release_24_02_Tests()
#a.PSDNET1491Test()