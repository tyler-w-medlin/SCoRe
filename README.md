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
  
GUI Search
  1 - start the server; run SCoRe/server/main.py
  2 - open the GUI; open SCoRe/ui/score.html
---

## How to run

### Requirements

- `python3.6`
- `python3-dev`
- `libsm6`
- `libxext6`
- `libxrender1`
- `libfontconfig1`
- All required python packages can be installed using the setup.py script
- `gcc`


### Linux & macOS

1. Ensure `python3.6` is installed on the system along with its corresponding `pip` module
2. Change directories into the main directory (e.g. `SC0Re/`)
3. Run `setup.py` (`python3 setup.py`, this might have to be run using `sudo`)
4. Ensure the above dataset items are downloaded and place them into `Score/server/tools/data/`
5. Change directories to `SCoRe/server/`
6. Run the command `python3.6 main.py`
7. From here, the server should be running on `0.0.0.0:5000` (localhost and given IP from networks DNS)

### Windows

1. Download and install a Linux subsystem for Windows.
    - This was tested on the Ubuntu distribution
2. Follow the above steps for Linux environment.

### ERRORs

If any errors occur during installation (`setup.py`), the following packages may need to be installed:

- `python3-dev`
- `libsm6`
- `libxext6`
- `libxrender1`
- `libfontconfig1`

#### Linux & Subsystem for Windows

`sudo apt install python3-dev libsm6 libxext6 libxrender1 libfontconfig1`
