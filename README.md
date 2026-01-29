![image](https://raw.githubusercontent.com/cubert-hyperspectral/cuvis.sdk/main/branding/logo/banner.png)

# cuvis.python.examples

## Building the examples

To get the exampels running, first set up a project directory and clone this git repository.

For running some of the examples, you have to use sample data (provided [here](https://drive.google.com/drive/folders/1Cjb0v_a2p1cCmhKH8w2OuRtnhXCJGz61?usp=sharing)).

### Windows

1. Install Python 3.10 or newer (Python 3.12 is recommended) https://www.python.org/downloads/ \
Make sure to tick the box “Add Python to PATH”

2. Install the latest version of Cuvis SDK or Cuvis Full via the installer provided [here](https://cloud.cubert-gmbh.de/s/qpxkyWkycrmBK9m?path=%2F))

3. Create a new virtual environment
```
python -m venv .venv
```

4. Activate the virtual environment
```
.venv\Scripts\activate.bat
```
(If you're using PowerShell, use: )
```
.venv\Scripts\Activate.ps1
```

5. Install the necessary requirements from the requirements.txt
```
pip install -r requirements.txt
```

### Ubuntu

1. Install Python 3.10 or newer (Python 3.12 is recommended)
https://www.python.org/downloads/source/ 
or `sudo apt install python3 python3-venv python3-pip`
2. Download the latest version of Cuvis SDK or Cuvis Full for your Ubuntu machine [here](https://cloud.cubert-gmbh.de/s/qpxkyWkycrmBK9m?path=%2F).\
If you are using an arm64 system, check the additional instructions in the Application notes document [here](https://cloud.cubert-gmbh.de/s/qpxkyWkycrmBK9m?dir=undefined&path=%2FCuvis%203.4.0&openfile=3928) before continuing.
    - Install the cuviscommon package first via `sudo apt install ./cuviscommon_X.X.X-X.deb` (installs external dependencies, internet connection necessary)
    - Install the rest of the .deb files in the same way.

3. Create a new virtual environment
```
python3 -m venv .venv
```
in case you don’t have the venv module, install it
```
sudo apt update
sudo apt install python3-venv
```

4. Activate the virtual environment
```
source .venv/bin/activate
```

5. Install the necessary requirements from the requirements.txt
```
pip install -r requirements.txt
```

## Inventory

### 01. Example_1_Take_Snapshot
Connect to your Camera & record a Measurement

### 02. Example_2_Load_Measurement
Load, Access & Analyze a recorded Measurement

### 03. Example_3_Reprocess
Load & Reprocess a Measurement

### 04. Example_4_Exporters
Convert/Export to different File Formats

### 05. Example_5_Record_Video
Record a video using the Worker