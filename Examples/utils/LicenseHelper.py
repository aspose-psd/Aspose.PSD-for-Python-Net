import os.path
from aspose.psd import License, Metered
from utils.FolderSettings import FolderSettings

class LicenseHelper:

    isLicensed = False

    @staticmethod
    def is_licensed():
        return LicenseHelper.isLicensed

    @staticmethod
    def set_license():

        # To Get Temporary License please check the url: https://purchase.aspose.com/temporary-license/

        if LicenseHelper.is_licensed():
            return
        license = License()
        licenseFolder = FolderSettings.BaseLicenseFolder()
        licensePath = os.path.join(licenseFolder, "Aspose.PSD.Python.NET.lic")
        license.set_license(licensePath)
        LicenseHelper.isLicensed = True
