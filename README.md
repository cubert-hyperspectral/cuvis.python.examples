![image](https://raw.githubusercontent.com/cubert-hyperspectral/cuvis.sdk/main/branding/logo/banner.png)

# cuvis.python.examples

## Running the examples
To get the exampels running, first set up a project directory with (probably) an own environment and clone this git repository there.

Then, you need to install the Cuvis C SDK (see [here](https://cloud.cubert-gmbh.de/s/qpxkyWkycrmBK9m), as explained for the python wrapper [here](https://github.com/cubert-hyperspectral/cuvis.python).

Then you can simply install the required dependencies using pip in your local project environment.

```
pip install -r requirements.txt
```

Alternatively to pip, take a look on how to install the python wrapper manually [here](https://github.com/cubert-hyperspectral/cuvis.python).

For running some of the examples, you have to use sample data (provided [here](https://cloud.cubert-gmbh.de/s/SrkSRja5FKGS2Tw)).

## Inventory

### 01_loadMeasurement
Load measurement from disk and print the value (count) for all available channels (wavelength) for one specific pixel.

### 02_reprocessMeasurement
Load measurement as well as references (dark, white, distance) from disk and reprocess the measurement to reflectance.

### 03_exportMeasurement
Load measurement from disk and save to different file formats.

### 04_changeDistance
Load measurement from disk and reprocess to a new given distance.

### 05_recordSingleImages
Setup camera and record measurements via looping software trigger, aka 
"single shot mode" or "software mode".

### 05_recordSingleImages_async
Same as example 05_recordSingleImages but with `asyncio`.

### 06_recordVideo
Setup camera and record measurements via internal clock triggering, aka "video mode". In this example the `cuvis.Worker` is used to make use of multithreading (`cuvis_worker_create`).

### 06_recordVideo_async
Same as example 06_recordVideo but with `asyncio`.

### 07_recordVideoFromSessionFile
Set up a virtual camera based on a pre-recorded session file to simulate actual camera behaviour.
