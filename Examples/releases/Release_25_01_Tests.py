from datetime import datetime

import numpy as np
import pytest
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers import ShapeLayer
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.imageloadoptions import PsdLoadOptions
from aspose.psd.imageoptions import PngOptions, PsdOptions
from aspose.pycore import cast, as_of, is_assignable

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper


class Release_25_01_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Replace content in many smart objects that have the same source reference.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2233
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-150
    def PSDNET2233Test(self):
        src_file = self.GetFileInBaseFolder("Source.psd")
        replace_all = self.GetFileInBaseFolder("replaceAll.jpg")
        replace_one = self.GetFileInBaseFolder("replaceOne.jpg")
        out_file_img_all = self.GetFileInOutputFolder("output_All.png")
        out_file_img_one = self.GetFileInOutputFolder("output_one.png")
        ref_file_img_all = self.GetFileInBaseFolder("output_All.png")
        ref_file_img_one = self.GetFileInBaseFolder("output_one.png")

        # This will replace the same context in all smart layers with the same link.
        with PsdImage.load(src_file) as image:
            img = cast(PsdImage, image)
            smart_object_layer = cast(SmartObjectLayer, img.layers[1])  # Assuming the layer is at index 1
            # This will replace the content in all SmartLayers that use the same content.
            smart_object_layer.replace_contents(replace_all, False)
            smart_object_layer.update_modified_content()

            img.save(out_file_img_all, PngOptions())

        # This will replace the context of only the selected layer, leaving all others with the same context alone.
        with PsdImage.load(src_file) as image:
            img = cast(PsdImage, image)
            smart_object_layer = cast(SmartObjectLayer, img.layers[1])  # Again, assuming the layer is at index 1
            # It replaces the content in the selected SmartLayer only.
            smart_object_layer.replace_contents(replace_one, True)
            smart_object_layer.update_modified_content()

            img.save(out_file_img_one, PngOptions())

        Comparison.CheckAgainstEthalon(out_file_img_all, ref_file_img_all, 0)
        Comparison.CheckAgainstEthalon(out_file_img_one, ref_file_img_one, 0)

    # [AI Format] Resolving intersecting paths rendering issue.
    # https://issue.saltov.dynabic.com/issues/PSDNET-2286
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-151
    def PSDNET2286Test(self):
        source_file = self.GetFileInBaseFolder("ex.ai")
        output_file = self.GetFileInOutputFolder("ex.png")
        reference_file = self.GetFileInBaseFolder("ex.png")

        with AiImage.load(source_file) as image:  # Assuming AiImage has a similar load method
            img = cast(AiImage, image)
            img.active_page_index = 8  # Assuming the property name is similar
            img.save(output_file, PngOptions())

        Comparison.CheckAgainstEthalon(output_file, reference_file, 0)