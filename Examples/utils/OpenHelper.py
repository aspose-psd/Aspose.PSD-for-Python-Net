import pathlib
from io import BytesIO

from aspose.psd import Image
from aspose.psd.fileformats.ai import AiImage
from aspose.psd.fileformats.psd import PsdImage
from aspose.psd.fileformats.psd.layers import Layer
from aspose.pycore import cast

class OpenHelper:
    @staticmethod
    def get_extension(file_path):
        return pathlib.Path(file_path).suffix.lower()

    @staticmethod
    def open_psd_file(stream, load_options):
        img = Image.load(stream)
        return cast(PsdImage, img)

    @staticmethod
    def open_file_as_psd(stream):
        #with PsdImage(500, 500) as psdImage:
        #psdImage = PsdImage()
        layer = Layer(stream)
        psdImage = PsdImage(layer.width, layer.height)
        psdImage.layers = [layer]
        psdImage.load_argb_32_pixels(layer.bounds);
        #psdImage.add_layer(layer)
        return psdImage

    @staticmethod
    def open_ai_file(stream, load_options):
        with Image.load(stream) as image:
            return cast(AiImage, image)

    @staticmethod
    def open_file_by_path(file_path, load_options = None):
        with open(file_path, "rb", buffering=0) as filestream:
            stream = BytesIO(filestream.read())
            stream.seek(0)
            ext = OpenHelper.get_extension(file_path)
            if (ext == ".psd" or ext == ".psb"):
                return OpenHelper.open_psd_file(stream, load_options)
            if (ext == ".ai" or ext == ".pdf"):
                return OpenHelper.open_ai_file(stream, load_options)

            img = OpenHelper.open_file_as_psd(stream)
            return img