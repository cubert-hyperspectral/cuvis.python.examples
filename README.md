![image](https://camo.githubusercontent.com/9fc396a08b84779ea0f78a4085e96bee6035fca702cd382f38cb661fa1ff1d0c/68747470733a2f2f7777772e7370656374726f6578706f2e636f6d2f77702d636f6e74656e742f75706c6f6164732f323031382f30372f637562657274323031382e706e67)


# cuvis.python.examples

## Running the examples
To get the exampels running, first set up a project directory with (probably) an own environment and clone this git repository there.

Then, you need to install the Cuvis C SDK (see [here](https://cloud.cubert-gmbh.de/index.php/s/62UdmciCPjxy1pm), as explained for the python wrapper [here](https://github.com/cubert-hyperspectral/cuvis.python).

Then you can simply install the required dependencies using pip in your local project environment.

```
pip install -r requirements.txt
```

Alternatively to pip, take a look on how to install the python wrapper manually [here](https://github.com/cubert-hyperspectral/cuvis.python).

For running some of the examples, you have to use sample data (provided [here](https://cloud.cubert-gmbh.de/index.php/s/3oECVGWpC1NpNqC)).

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
