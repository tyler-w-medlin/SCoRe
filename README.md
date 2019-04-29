# SCoRe
Source Code Recommendation

Environment setup steps:

Dataset initialization:
  1 - Download data/ folder from https://drive.google.com/drive/folders/15qfLjw4kjt79bUzMwLP4cqg_ffUC3C1V?usp=sharing
  2 - copy/paste into SCoRe/data_init/
  3 - run SCoRe/data_init/data_init.py
  4 - copy SCoRe/data_init/data and paste into SCoRe/server/tools
  
  
Command line search:
  1 - run SCoRe/data_init/command_line_search.py
  
---

## How to run

### Requirements

- `python3.6`
- `python3-dev`
- `libsm6`
- `libxext6`
- `libxrender1`
- `libfontconfig1`
- `python-dev`
- `python3-distutils`
- `gcc`
- `g++`
- All required python packages can be installed using the setup.py script
- Replace the site-package for the Python `fastai` package with the files found in `SCoRe/server/tools/ai-reqs`
- Download the data models from the links above
- nltk will need to download packages for itself
    - `punkt`
    - `stopwords`



### Linux & macOS

1. Ensure `python3.6` is installed on the system along with its corresponding `pip` module (`get-pip.py` should be supplied in the repo).
2. Change directories into the main directory (e.g. `SCoRe/`)
3. Run `setup.py` (`python3.6 setup.py`, this might have to be run using `sudo`)
4. Ensure the above dataset items are downloaded and place them into `Score/server/tools/data/`
5. Change directories to `SCoRe/server/`
6. Run the command `python3.6 main.py`
7. From here, the server should be running on `0.0.0.0:5000` (localhost and given IP from networks DNS)

### Windows

1. Download and install a Linux subsystem for Windows.
    - This was tested on the Ubuntu distribution
2. Follow the above steps for Linux environment.

***The tutorial to download the Ubuntu Linux subsystem can be found on the microsoft documentation website. Here is a link to that tutorial: https://docs.microsoft.com/en-us/windows/wsl/install-win10***

### ERRORs

If any errors occur during installation (`setup.py`), the following packages may need to be installed:

- `python3-dev`
- `libsm6`
- `libxext6`
- `libxrender1`
- `libfontconfig1`
- `python-dev`
- `python3-distutils`
- `g++`
- `gcc`

#### Linux & Linux Subsystem for Windows

`sudo apt install python3-dev libsm6 libxext6 libxrender1 libfontconfig1 python-dev python3-distutils gcc g++`

---
