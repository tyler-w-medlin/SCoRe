# ==========================================================
# Just a short script that will gather all my predetermined
#   dependencies and download them on whatever machine.
#
# @author: Elliott Campbell
# ==========================================================

import subprocess

def spacyDownload():
    print("Downloading spacy...")

    subprocess.check_call(["python3.6", "-m", "pip", "install", "spacy"])


    print("Downloading en...")

    subprocess.check_call(["python3.6", "-m", "spacy", "download", "en"])

def download(requirements):

    print("Downloading reuqirements...")
    subprocess.check_call(['python3.6', "-m", "pip", 'install', "-r", requirements])


if __name__ == "__main__":
    spacyDownload()
    download("./requirements.txt")
