# ==========================================================
# Just a short script that will gather all my predetermined
#   dependencies and download them on whatever machine.
#
# @author: Elliott Campbell
# ==========================================================

import subprocess
import site
import os
import shutil

def spacyDownload():
    print("Downloading spacy...")

    subprocess.check_call(["python3.6", "-m", "pip", "install", "spacy"])


    print("Downloading en...")

    subprocess.check_call(["python3.6", "-m", "spacy", "download", "en"])

def download(requirements):

    print("Downloading reuqirements...")
    subprocess.check_call(['python3.6', "-m", "pip", 'install', '-U', '-r', requirements])

def replaceFastai():
    print("For now, in order for the server to run, the fast-ai site-package needs to be replaced with the one supplied in the project.")
    consent = input("Do you consent? (Y/N) ")

    site_path = site.getsitepackages()[0]
    if consent.upper() in ["yes", "Y"]:
        print("Replacing package now...")
        # print(os.listdir(site.getsitepackages()[0]))
        for package in os.listdir(site_path):
            if package == "fastai":
                package_path = site_path + "/{}".format(package)
                replace_items = "./server/tools/ai_reqs/"
                shutil.rmtree(package_path)
                shutil.copytree(replace_items, package_path)

    else:
        print("Thank you for downloading SCoRe.")
        print("However, until it is fixed, the server will not be able to run without replacing the site-package.")


def nltkDownloads():
    
    import nltk

    print("There are packages required to be downloaded by NLTK in order for the server to work.")
    print("NLTK will now download these required packages...")

    packages = ["stopwords", "punkt"]
    for package in packages:
        nltk.download(package)

if __name__ == "__main__":
    spacyDownload()
    download("./requirements.txt")
    print("All dependencies have succesfully installed.")
    print("=" * 25, "\n")
    replaceFastai()
    nltkDownloads()

