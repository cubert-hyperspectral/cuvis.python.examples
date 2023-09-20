# Cuvis Python Examples

## Running the examples
To the the exampels running, first clone this git repository.

Then you can simply install the required dependencies using pip

```
pip install -r requirements.txt
```

Alternatively take a look on how to install the python wrapper manually [here](https://github.com/cubert-hyperspectral/cuvis.python).

Next, you need to install the Cuvis C SDK (see [here](https://cloud.cubert-gmbh.de/index.php/s/kKVtx0x2fmYqVgx)). For running the examples, you'd probably like to use sample data (provided [here](https://cloud.cubert-gmbh.de/index.php/s/3oECVGWpC1NpNqC))

## The examples

### 01_loadMeasurement
Load measurement from disk and print the value (count) for all available channels (wavelength) for one specific pixel.

### 02_reprocessMeasurement
Load measurement as well as references (dark, white, distance) from disk and reprocess the measurement to e.g. reflectance.

### 03_exportMeasurement
Load measurement from disk and save to different file formats.

### 04_changeDistance
Load measurement from disk and reprocess to a new distance.

### 05_recordSingleImages
Setup camera and record measurements via software trigger, aka "single shot mode" or "software mode".

### 05_recordSingleImages_async
Same as example 05_recordSingleImages but with asyncio.

### 06_recordVideo
Setup camera and record measurements via internal clock triggering, aka "video mode". In this example the worker is used to make use of multithreading (cuvis_worker_create).

### 06_recordVideo_async
Same as example 06_recordVideo but with asyncio.

### 07_recordVideoFromSessionFile
Setup a virtual camera based on a pre-recorded session file to simulate actual camera behaviour.