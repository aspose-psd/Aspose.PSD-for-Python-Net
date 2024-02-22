from utils.BaseTests import BaseTests
from utils.LicenseHelper import LicenseHelper


class Showcases(BaseTests):
    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        LicenseHelper.set_license()
