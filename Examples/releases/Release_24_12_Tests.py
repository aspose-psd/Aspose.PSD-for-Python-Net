from datetime import datetime

import numpy as np
import pytest
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers import ShapeLayer
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import cast, as_of, is_assignable

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper

class Release_24_12_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Fix rendering of Shapes in PSD files created in an old version of the PS
    # https://issue.saltov.dynabic.com/issues/PSDNET-2132
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-136
    def PSDNET2132Test(self):
        input_file_stroke = self.GetFileInBaseFolder("Shape_Stroke.psd")
        output_file_stroke = self.GetFileInOutputFolder("output_Shape_Stroke.png")
        reference_file_stroke = self.GetFileInBaseFolder("output_Shape_Stroke.png")

        input_file_effects = self.GetFileInBaseFolder("Shape_Effects_PS2021.psd")
        output_file_effects = self.GetFileInOutputFolder("output_Shape_Effects_PS2021.png")
        reference_file_effects = self.GetFileInBaseFolder("output_Shape_Effects_PS2021.png")

        # Test that there is no cropping of outside part of stroke in old psd format files.
        with PsdImage.load(input_file_stroke) as img:
            image = cast(PsdImage, img)
            for layer in image.layers:
                if  is_assignable(layer, ShapeLayer):
                    # Shape layer is repainted in this test
                    shape_layer = cast(ShapeLayer, layer)
                    shape_layer.update()

            image.save(output_file_stroke, PngOptions())

        Comparison.CheckAgainstEthalon(output_file_stroke, reference_file_stroke, 0)

        opt = PsdLoadOptions()
        opt.load_effects_resource = True
        opt.allow_warp_repaint = True
        # Test effects rendering on Shape layers.
        with PsdImage.load(input_file_effects, opt) as img:
            image = cast(PsdImage, img)
            # Shape layer is not repainted in this test
            image.save(output_file_effects, PngOptions())

        Comparison.CheckAgainstEthalon(output_file_effects, reference_file_effects, 0)

    # Implement correct handling of PSD file with Shape layer and having vector and raster masks
    # https://issue.saltov.dynabic.com/issues/PSDNET-2133
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-137
    def PSDNET2133Test(self):
        input_file = self.GetFileInBaseFolder("mask_rastr_vector.psd")
        output_file = self.GetFileInOutputFolder("output_mask_rastr_vector.png")
        ref_file = self.GetFileInBaseFolder("output_mask_rastr_vector.png")

        with PsdImage.load(input_file, None) as img:
            image = cast(PsdImage, img)
            image.save(output_file, PngOptions())

        Comparison.CheckAgainstEthalon(output_file, ref_file, 0)

    # [AI Format] Incorrect rendering of AI file
    # https://issue.saltov.dynabic.com/issues/PSDNET-2174
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-144
    def PSDNET2174Test(self):
        source_file = self.GetFileInBaseFolder("Input1.ai")
        output_file = self.GetFileInOutputFolder("Input1.png")
        ref_file = self.GetFileInBaseFolder("Input1.png")

        with AiImage.load(source_file) as img:
            image = cast(AiImage, img)
            image.save(output_file, PngOptions())

        Comparison.CheckAgainstEthalon(output_file, ref_file, 0)

    # [AI Format] Implement Gradient Shading (type 7)
    # https://issue.saltov.dynabic.com/issues/PSDNET-2214
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-139
    def PSDNET2214Test(self):
        source_file = self.GetFileInBaseFolder("2214.ai")
        output_file = self.GetFileInOutputFolder("2214.png")
        ref_file = self.GetFileInBaseFolder("2214.png")

        with AiImage.load(source_file) as img:
            image = cast(AiImage, img)
            image.save(output_file, PngOptions())

        Comparison.CheckAgainstEthalon(output_file, ref_file, 0)

    # [AI Format] Implement blending support.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2238
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-141
    def PSDNET2238Test(self):
        source_file = self.GetFileInBaseFolder("2238.ai")
        output_file = self.GetFileInOutputFolder("2238.png")
        ref_file = self.GetFileInBaseFolder("2238.png")

        with AiImage.load(source_file) as img:
            image = cast(AiImage, img)
            image.save(output_file, PngOptions())

        Comparison.CheckAgainstEthalon(output_file, ref_file, 0)


    # [AI Format] Implement Gradient Shading (type 7)
    # https://issue.saltov.dynabic.com/issues/PSDNET-2241
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-145
    def PSDNET2241Test(self):
        source_file = self.GetFileInBaseFolder("2241.ai")

        output_files = []
        ref_files = []
        for i in range(3):
            output_files.append(self.GetFileInOutputFolder(f"2241_pageNumber_{str(i)}.png"))
            ref_files.append(self.GetFileInBaseFolder(f"2241_pageNumber_{str(i)}.png"))

        with AiImage.load(source_file) as img:
            image = cast(AiImage, img)
            assert image.page_count == 3

            for i in range(image.page_count):
                image.active_page_index = i
                image.save(output_files[i], PngOptions())

        for i in range(3):
            Comparison.CheckAgainstEthalon(output_files[i], ref_files[i], 0)

    # [AI Format] Implement Axial Shading (type 2)
    # https://issue.saltov.dynabic.com/issues/PSDNET-2249
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-142
    def PSDNET2249Test(self):
        source_file = self.GetFileInBaseFolder("2249.ai")
        output_file = self.GetFileInOutputFolder("2249.png")
        ref_file = self.GetFileInBaseFolder("2249.png")

        with AiImage.load(source_file) as img:
            image = cast(AiImage, img)
            image.save(output_file, PngOptions())

        Comparison.CheckAgainstEthalon(output_file, ref_file, 0)

    # The GlobalResources property is null when PSD Image is just created that leads to errors with SmartObjects.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2255
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-146
    def PSDNET2255Test(self):
        with PsdImage(300, 100) as psdImage:
            assert hasattr(psdImage, 'global_layer_resources')
            assert psdImage.global_layer_resources is not None

    # [Ai Format] Add handling of Layers data defined as DictionaryObject in Properties object of the Page
    # https://issue.saltov.dynabic.com/issues/PSDNET-2257
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-147
    def PSDNET2257Test(self):
        source_file = self.GetFileInBaseFolder("Input_2.ai")
        output_file = self.GetFileInOutputFolder("output.png")
        ref_file = self.GetFileInBaseFolder("output.png")

        with AiImage.load(source_file) as img:
            image = cast(AiImage, img)
            image.save(output_file, PngOptions())

        Comparison.CheckAgainstEthalon(output_file, ref_file, 0)

    # [AI Format] Rework Compound Paths to work through APS
    # https://issue.saltov.dynabic.com/issues/PSDNET-2272
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-143
    def PSDNET2272Test(self):
        source_file = self.GetFileInBaseFolder("page-3.ai")
        output_file = self.GetFileInOutputFolder("page-3.png")
        ref_file = self.GetFileInBaseFolder("page-3.png")

        with AiImage.load(source_file) as img:
            image = cast(AiImage, img)
            image.save(output_file, PngOptions())

        Comparison.CheckAgainstEthalon(output_file, ref_file, 0)