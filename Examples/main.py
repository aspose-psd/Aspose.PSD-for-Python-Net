# This is a main file of Aspose.PSD for Python via .NET Examples.
# You can debug any tests and check the showcases of PSD, PSB, AI FileFormat API
from aspose.psd import License

from Examples.releases.Release_24_10_Tests import Release_24_10_Tests
from Examples.releases.Release_24_11_Tests import Release_24_11_Tests
from Examples.releases.Release_24_12_Tests import Release_24_12_Tests
from releases.Release_24_09_Tests import Release_24_09_Tests
from releases.Release_24_07_Tests import Release_24_07_Tests
from releases.Release_24_08_Tests import Release_24_08_Tests
from releases.Release_24_05_Tests import Release_24_05_Tests
from releases.Release_24_04_Tests import Release_24_04_Tests
from releases.Release_24_03_Tests import Release_24_03_Tests
from releases.Release_24_02_Tests import Release_24_02_Tests
from releases.Release_23_12_Tests import Release_23_12_Tests
from releases.Release_24_01_Tests import Release_24_01_Tests
from releases.Release_24_06_Tests import Release_24_06_Tests
from showcases.Showcases import Showcases

def run_releases_tests():

    release24_12 = Release_24_12_Tests()
    release24_12.RunAllTests()

    release24_11 = Release_24_11_Tests()
    release24_11.RunAllTests()

    release24_10 = Release_24_10_Tests()
    release24_10.RunAllTests()

    release24_09 = Release_24_09_Tests()
    release24_09.RunAllTests()

    release24_08 = Release_24_08_Tests()
    release24_08.RunAllTests()

    release24_07 = Release_24_07_Tests()
    release24_07.RunAllTests()

    release24_06 = Release_24_06_Tests()
    release24_06.RunAllTests()

    release24_05 = Release_24_05_Tests()
    release24_05.RunAllTests()

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