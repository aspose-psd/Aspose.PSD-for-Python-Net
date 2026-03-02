import base64
import io

import pytest
from aspose.psd import Rectangle, Image, DataRecoveryMode, Color, ResolutionSetting, FontSettings, Graphics, Size, \
    ResizeType
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.png import PngColorType
from aspose.psd.fileformats.psd import PsdImage, CompressionMethod
from aspose.psd.fileformats.psd.layers import TextLayer
from aspose.psd.fileformats.psd.layers.layerresources import SoLdResource, Lnk2Resource, PlLdResource, FxrpResource, \
    LnkeResource, SoLeResource
from aspose.psd.fileformats.psd.layers.smartobjects import SmartObjectLayer
from aspose.psd.fileformats.psd.layers.warp import WarpStyles
from aspose.psd.imageloadoptions import PsdLoadOptions, ReadOnlyMode
from aspose.psd.imageoptions import PngOptions, PsdOptions, GifOptions, BmpOptions
from aspose.psd.xmp import XmpPacketWrapper
from aspose.pycore import cast, as_of, is_assignable

from utils.BaseTests import BaseTests
from utils.Comparison import Comparison
from utils.LicenseHelper import LicenseHelper


class Release_25_11_Tests(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()

    # Can not load pixels from PSD Files after the Aspose.PSD manipulation
    # https://issue.saltov.dynabic.com/issues/PSDNET-1917
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-267
    def PSDNET1917Test(self):
        # Assuming baseFolder is defined somewhere
        input_file = self.GetFileInBaseFolder("effect_bug.psd")

        # Load the PSD image
        with Image.load(input_file) as image:
            img = cast(PsdImage, image)
            # Exception raise is fixed in 23.09
            pix = img.load_argb_32_pixels(img.bounds)

            assert len(pix) > 0 & pix[100] != -2448096

    # Non-destructive crop and resize do not work as expected
    # https://issue.saltov.dynabic.com/issues/PSDNET-2269
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-266
    def PSDNET2269Test(self):
        # Port the main PSD creation code
        output_file = self.GetFileInOutputFolder("output.psd")
        reference_file = self.GetFileInBaseFolder("output.psd")

        with PsdImage(300, 100) as psd_img:
            graphics = Graphics(psd_img)
            graphics.clear(Color.black)

            with self.get_test_png_image() as f_stream:
                so_layer = SmartObjectLayer(f_stream)
                psd_img.add_layer(so_layer)

                width = so_layer.width
                height = so_layer.height
                so_layer.resize(width // 20, height // 20, ResizeType.HIGH_QUALITY_RESAMPLE)

                # There should be no error when trying to resize a smart layer in PS (using CTRL+T)
                # There should be no error when trying to edit a smart layer in PS.
                psd_img.save(output_file, PsdOptions())

        # Port the verification code
        with Image.load(output_file) as psd_image:
            if isinstance(psd_image, PsdImage):
                smart_object_layer = psd_image.layers[1]

                if isinstance(smart_object_layer, SmartObjectLayer):
                    assert "New item.png" != smart_object_layer.contents_source.original_file_name
                    assert WarpStyles.NONE != smart_object_layer.warp_settings.style

        Comparison.CheckAgainstEthalon(output_file, reference_file, 1)

    def get_test_png_image(self):
        png = "iVBORw0KGgoAAAANSUhEUgAAAQ4AAAAyCAMAAACaoMX1AAACmlBMVEVHcEz////////////////////////a18n////////////S4M7///////////////////////////////////86lDn////////////////////////2+v3////////////////Alyr///////////////////////////////////////+5tT/////////////////////////////////////////////byiz///////////////9aoznrnk7///////////8smc5Ens3y1lB/sN7///9Bmsp2rUyyoRD3k0j////3fS0tl8/020DzaypNnTz///8tl81DmTyynw8rltH2di08lTr1cSr4jT4sl9S0nxA+mdN5r+W2sDr1eyu3pRRZpM1rqd/0dSr8gzj54kM5ksz2hS7byDL51lc9ljaTv0iQu+amvWG1ohL3hDMsmc46lDo5lDn5hzj+yWz3cSbzbSp7sEU3kzqxohCMu1H4fCSFs+D+tlSLrc84kzr8jT87lTqwsJ7ezDeXwUyxnQ/9jD2wnQ6ZwkWs0DxFmT9epDFBmDlUodJvqUgwltbp1i3/0HZvq0Sxnw6DtkOMvT/NuSk7lUFqqDr8r02eqr6+rhr6i0GYw0G8qxdGmjmkyTr5nkjNuyP33kdHmjcrmMzs3UWOvFv+znFcoNZmqjfyayrx5D6BreI1kcn350Gkx/6fwfLbxCasz0Py6FP62kTybStZojf///8tmM5rpNX3i0eynxAykspNnTr2iC33ki5/slHMuiNCmDq/rRnUwyZ1p9bi0zP5qEnn2jr4oDWHuFD4nEvFsh31fS1uqVA7kMmOu0fzbyq5phT8vVxXntFlpUr7sk/t4j45nNDx4kjy5k32kD6kykRWz45yAAAA1HRSTlMA9QYy+ppVAfL+nwTbDDYgkH+rprn9PjrqePeEF2Xuz9UJCA9cGkhEyLMUwhEmCa7elCloiXpu5v7SdCy9/hgvT+LKEiz9SyX/Ov1jR6OqthdxOC2xhyNcaThdU27MI7TILe7kxZbz2HpJT+P8G5Px83vnpOSXe/ijenkssJpKyYXUJ5xn7LHa+1T+spJboLSIIjzzy7I5uNfyZLRzn+vPP8bS7UXhzZXzop1W1WntwULVVni1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"

        # Decode base64 and create a BytesIO stream
        png_bytes = base64.b64decode(png)
        ms = io.BytesIO(png_bytes)
        ms.seek(0)
        return ms

    # Support for non-standard mesh points in warp
    # https://issue.saltov.dynabic.com/issues/PSDPYTHON-262
    # https://issue.saltov.dynabic.com/issues/PSDNET-2583
    def PSDNET2583Test(self):
        source_file = self.GetFileInBaseFolder("pirate_x3.psd")
        output_file = self.GetFileInOutputFolder("export.png")
        reference_file = self.GetFileInBaseFolder("export.png")

        # Create load options with settings
        load_options = PsdLoadOptions()
        load_options.allow_warp_repaint = True
        load_options.load_effects_resource = True

        with Image.load(source_file, load_options) as loaded_image:
            psd_image = cast(PsdImage, loaded_image)

            # Get warp settings
            smart_layer = cast(SmartObjectLayer, psd_image.layers[0])
            warp_settings = smart_layer.warp_settings

            # Set new size
            # For Photoshop, the value can be between 1 and 50, and you will not be able to save a valid PSD file.
            warp_settings.grid_size = Size(100, 100)

            # Set valid value
            warp_settings.grid_size = Size(3, 3)

            # Render example file with x3 grid
            png_options = PngOptions()
            png_options.color_type = PngColorType.TRUECOLOR_WITH_ALPHA

            psd_image.save(output_file, png_options)

        Comparison.CheckAgainstEthalon(output_file, reference_file, 1)

#LicenseHelper.set_license()
#a = Release_25_11_Tests()
#a.PSDNET2583Test()