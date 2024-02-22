import os.path
import re

# Class to make finding of the base folders easier
class FolderSettings:
    @staticmethod
    def BaseTestFolder():
        baseFolder = FolderSettings.find_gitignore_folder()
        baseTestFolder = os.path.join(baseFolder, "testdata")
        return baseTestFolder

    @staticmethod
    def BaseTestOutputFolder():
        baseFolder = FolderSettings.find_gitignore_folder()
        baseTestOutputFolder = os.path.join(baseFolder, "output")

        FolderSettings.create_folder_if_not_exists(baseTestOutputFolder)

        return baseTestOutputFolder

    @staticmethod
    def create_folder_if_not_exists(baseTestOutputFolder):
        if not os.path.exists(baseTestOutputFolder):
            os.makedirs(baseTestOutputFolder)

    @staticmethod
    def BaseLicenseFolder():
        baseFolder = FolderSettings.find_gitignore_folder()
        print(baseFolder)
        baseLicenseFolder = os.path.join(baseFolder, "license")
        return baseLicenseFolder

    @staticmethod
    def find_gitignore_folder():
        current_path = os.path.dirname(__file__)

        while current_path != '/' or not (current_path is None):
            if 'basefolder.mark' in os.listdir(current_path):
                return current_path

            current_path = os.path.dirname(current_path)
        return None

    @staticmethod
    def add_dash(string):
        pattern = r'([a-zA-Z])(\d)'
        replacement = r'\1-\2'
        result = re.sub(pattern, replacement, string)
        return result

    @staticmethod
    def GetFolderNameFromTestName(testName):
        #if not testName is None:
        if "testfunction" in testName:
            testName = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
            print(testName)
        else:
            # Remove all before the "." sign
            splits = testName.split(".")
            del splits[0]
            testName = "#".join(splits)

        # Remove brackets and all in brackets
        testName = re.sub(r'[\(\[].*[\)\]]', '', testName)

        # Remove part after "_"
        splits = testName.split("_")
        if (len(splits) > 1):
            del splits[len(splits) - 1]
            testName = "#".join(splits)

        # Remove word "Test" ignoring case
        testName = re.sub(r'test', '', testName, flags=re.IGNORECASE)

        # Remove spaces and line breaks
        testName = testName.strip()

        # Adds dash between letters and numbers to make folder of test looking like PSDNET-1608 instead of PSDNET1608
        testName = FolderSettings.add_dash(testName)

        print(testName)

        return testName