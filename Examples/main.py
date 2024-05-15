# This is a main file of Aspose.PSD for Python via .NET Examples.
# You can debug any tests and check the showcases of PSD, PSB, AI FileFormat API
from aspose.psd import License

from releases.Release_24_04_Tests import Release_24_04_Tests
from releases.Release_24_03_Tests import Release_24_03_Tests
from releases.Release_24_02_Tests import Release_24_02_Tests
from releases.Release_23_12_Tests import Release_23_12_Tests
from releases.Release_24_01_Tests import Release_24_01_Tests
from showcases.Showcases import Showcases

def run_releases_tests():
    release24_04 = Release_24_04_Tests()
    release24_04.RunAllTests()

    release24_03 = Release_24_03_Tests()
    release24_03.RunAllTests()

    release24_02 = Release_24_02_Tests()
    release24_02.RunAllTests()

    release24_01 = Release_24_01_Tests()
    release24_01.RunAllTests()

    release23_12 = Release_23_12_Tests()
    release23_12.RunAllTests()

def run_showcases_tests():
    showcases = Showcases()
    showcases.RunAllTests()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Don't forget install Aspose.PSD for Python via .NET
    # pip install aspose-psd
    # Temporary license can be obtained on https://purchase.aspose.com/temporary-license/

    #lic = License()
    #lic.set_license("PathToLicense")
    run_showcases_tests()
    run_releases_tests()