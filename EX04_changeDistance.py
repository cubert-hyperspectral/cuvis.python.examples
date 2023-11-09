import os
import platform

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

loc_distance = int(1000)

# default output
loc_output = os.path.join(os.getcwd(), "EX04_distance_changed")


def run_example_changeDistance(userSettingsDir=loc_settings,
                               measurementLoc=loc_file,
                               distance=loc_distance,
                               exportDir=loc_output):
    print("loading user settings...")
    settings = cuvis.General(userSettingsDir)
    settings.set_log_level("info")

    print("loading session file...")
    session = cuvis.SessionFile(measurementLoc)
    mesu = session[0]
    assert mesu._handle

    print("Data 1 {} t={}ms mode={}".format(mesu.name,
                                            mesu.integration_time,
                                            mesu.processing_mode.name,
                                            ))

    print("loading calibration and processing context (factory)...")
    processingContext = cuvis.ProcessingContext(session)

    print("setting distance...")
    processingContext.calc_distance(distance)

    processingContext.processing_mode = cuvis.ProcessingMode.Raw

    saveArgs = cuvis.SaveArgs(export_dir=exportDir, allow_overwrite=True)

    assert processingContext.is_capable(mesu,
                                       processingContext.get_processing_args())

    print("changing distance...")
    print("original distance...")
    print(mesu.distance)
    processingContext.apply(mesu)
    print("new distance...")
    print(mesu.distance)
    print("saving...")
    mesu.save(saveArgs)
    print("finished.")

    pass


if __name__ == "__main__":

    print("Example 04: Change distance. Please provide:")

    userSettingsDir = input(
        "User settings directory (default: {}): ".format(loc_settings))
    if userSettingsDir.strip().lower() in ["", "default"]:
        userSettingsDir = loc_settings

    measurementLoc = input(
        "Measurement file (.cu3) (default: {}): ".format(loc_file))
    if measurementLoc.strip().lower() in ["", "default"]:
        measurementLoc = loc_file

    distance = input("New distance in mm (default: {}): ".format(loc_distance))
    if distance.strip().lower() in ["", "default"]:
        distance = loc_distance
    distance = int(distance)

    exportDir = input(
        "Name of export directory (default: {}): ".format(loc_output))
    if exportDir.strip().lower() in ["", "default"]:
        exportDir = loc_output

    run_example_changeDistance(userSettingsDir, measurementLoc,
                               distance, exportDir)
