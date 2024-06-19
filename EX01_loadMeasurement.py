import os
import platform

import matplotlib.pyplot as plt
import numpy as np

import cuvis

### default directories and files
data_dir = None

if platform.system() == "Windows":
    lib_dir = os.getenv("CUVIS")
    data_dir = os.path.normpath(os.path.join(lib_dir, os.path.pardir, "sdk",
                                             "sample_data", "set_examples"))
elif platform.system() == "Linux":
    lib_dir = os.getenv("CUVIS_DATA")
    data_dir = os.path.normpath(
        os.path.join(lib_dir, "sample_data", "set_examples"))

# default image
loc_file = os.path.join(data_dir,
                        "set0_single",
                        "single.cu3s")
# default settings
loc_settings = os.path.join(data_dir, "settings")


def run_example_loadMeasurement(
        userSettingsDir=loc_settings,
        measurementLoc=loc_file):
    print("loading user settings...")
    cuvis.init(userSettingsDir)
    cuvis.set_log_level("info")

    print("loading session...")
    session = cuvis.SessionFile(measurementLoc)

    print("loading measurement file...")
    mesu = session[0]
    assert mesu._handle

    print("Data 1 {} t={}ms mode={}".format(mesu.name,
                                            mesu.integration_time,
                                            mesu.processing_mode.name,
                                            ))
    
    if isinstance(mesu.measurement_flags, cuvis.MeasurementFlags):
        print(f"Flags: {mesu.measurement_flags}")
        for v in cuvis.MeasurementFlags.supremum():
            print(f'{v}: {v in mesu.measurement_flags}')

    cube = mesu.data.get("cube", None)
    if cube is None:
        raise Exception("Cube not found")

    x = 120
    y = 200

    assert x < cube.width, "x index exceeds cube width!"
    assert y < cube.height, "y index exceeds cube height!"

    lambda_wl = []
    raw_counts = []
    for chn in np.arange(cube.channels):
        lambda_wl.append(cube.wavelength[chn])
        raw_counts.append(cube.array[x, y, chn])

    plt.plot(lambda_wl, raw_counts)
    plt.xlabel("lambda [nm]")
    plt.ylabel("raw counts [au]")
    plt.title("Spectrum of {} for x={}, y={}".format(mesu.name, x, y))
    plt.show()

    cuvis.shutdown()
    print("finished.")


if __name__ == "__main__":

    print("Example 01: Load Measurement. Please provide:")

    userSettingsDir = input(
        "User settings directory (default: {}): ".format(loc_settings))
    if userSettingsDir.strip().lower() in ["", "default"]:
        userSettingsDir = loc_settings

    measurementLoc = input(
        "Measurement file (.cu3s) (default: {}): ".format(loc_file))
    if measurementLoc.strip().lower() in ["", "default"]:
        measurementLoc = loc_file

    run_example_loadMeasurement(userSettingsDir, measurementLoc)
