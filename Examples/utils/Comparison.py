from io import BytesIO
from utils.OpenHelper import OpenHelper

# This class can be used to check the output file and the reference
class Comparison:
    def CompareImages(self, referenceImage, testingImage):
        if (referenceImage.width != testingImage.width):
            raise Exception("Comparison Error", "Width is different")
        if referenceImage.height != testingImage.height:
            raise Exception("Comparison Error", "Height is different")
        refPixels = referenceImage.load_argb_32_pixels(referenceImage.bounds)
        testPixels = referenceImage.load_argb_32_pixels(referenceImage.bounds)
        if refPixels.length != testPixels.length:
            raise Exception("")
        for i in range(refPixels.length):
            if (refPixels[i] != testPixels[i]):
                raise Exception("Pixel are different", "Issue in pixel number " + i)

    def ComparePsd(self, referenceImage, testingImage):
        self.CompareImages(referenceImage, testingImage)

        if (referenceImage.layers.length != testingImage.layers.length):
            raise Exception("Count of Layers is different", "Expected " + refPsd.layers.lenth + ", but was " + testPsd.layers.length)

    @staticmethod
    def CompareAsStreams(output_file, reference_file, allowed_diff = 0):
        errors = 0
        comparisons = 0
        with open(output_file, "rb", buffering=0) as filestream1:
            output = BytesIO(filestream1.read())
            output.seek(0)
            with open(reference_file, "rb", buffering=0) as filestream2:
                reference = BytesIO(filestream2.read())
                reference.seek(0)

                for x, y in zip(output, reference):
                    comparisons = comparisons + 1
                    if x != y:
                        errors = errors + 1
                        if errors > allowed_diff:
                            raise Exception("Streams has differences. Last mistaken byte is number " + str(comparisons))
                return True

    @staticmethod
    def CheckAgainstEthalon(output_file, reference_file, allowed_diff, allowed_diff_pixels = 0):
        compare = Comparison()
        with OpenHelper.open_file_by_path(reference_file) as referenceImage:
            with OpenHelper.open_file_by_path(output_file) as testingImage:
                compare.ComparePsd(referenceImage, testingImage)