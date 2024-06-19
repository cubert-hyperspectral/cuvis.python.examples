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

# default images
loc_file = os.path.join(data_dir,
                        "set0_single",
                        "single_raw.cu3s")
loc_dark = os.path.join(data_dir,
                        "set0_single",
                        "single_dark.cu3s")
loc_white = os.path.join(data_dir,
                         "set0_single",
                         "single_white.cu3s")
loc_distance = os.path.join(data_dir,
                            "set0_single",
                            "single_distance.cu3s")

# default settings
loc_settings = os.path.join(data_dir, "settings")

# default output
loc_output = os.path.join(os.getcwd(), "EX02_reprocessed")


def run_example_reprocessMeasurement(
        userSettingsDir=loc_settings,
        measurementLoc=loc_file,
        darkLoc=loc_dark,
        whiteLoc=loc_white,
        distanceLoc=loc_distance,
        outDir=loc_output):
    print("loading user settings...")
    cuvis.init(userSettingsDir)
    cuvis.set_log_level("info")

    print("loading measurement file...")
    sessionM = cuvis.SessionFile(measurementLoc)
    mesu = sessionM[0]
    assert mesu._handle

    print("loading dark...")
    sessionDk = cuvis.SessionFile(darkLoc)
    dark = sessionDk[0]
    assert dark._handle

    print("loading white...")
    sessionWt = cuvis.SessionFile(whiteLoc)
    white = sessionWt[0]
    assert white._handle

    print("loading distance...")
    sessionDc = cuvis.SessionFile(distanceLoc)
    distance = sessionDc[0]
    assert distance._handle

    print("Data 1 {} t={}ms mode={}".format(mesu.name,
                                            mesu.integration_time,
                                            mesu.processing_mode.name,
                                            ))

    print("loading processing context...")
    processingContext = cuvis.ProcessingContext(sessionM)

    print("set references...")
    processingContext.set_reference(dark, cuvis.ReferenceType.Dark)
    processingContext.set_reference(white, cuvis.ReferenceType.White)
    processingContext.set_reference(distance, cuvis.ReferenceType.Distance)

    procArgs = cuvis.ProcessingArgs()
    saveArgs = cuvis.SaveArgs(allow_overwrite=True,
                                    allow_session_file=True,
                                    allow_info_file=False)

    modes = [cuvis.ProcessingMode.Raw,
             cuvis.ProcessingMode.DarkSubtract,
             cuvis.ProcessingMode.Reflectance,
             cuvis.ProcessingMode.SpectralRadiance
             ]

    for mode in modes:

        procArgs.processing_mode = mode

        if processingContext.is_capable(mesu, procArgs):
            print("processing to mode {}...".format(mode))
            processingContext.set_processing_args(procArgs)
            mesu = processingContext.apply(mesu)
            mesu.set_name(mode)
            saveArgs.export_dir = os.path.join(outDir, mode)
            exporter = cuvis.Export.CubeExporter(saveArgs)
            exporter.apply(mesu)

        else:
            print("Cannot process to {} mode!".format(mode))

    cuvis.shutdown()
    print("finished.")


if __name__ == "__main__":

    print("Example 02: Reprocess Measurement. Please provide:")

    userSettingsDir = input(
        "User settings directory (default: {}): ".format(loc_settings))
    if userSettingsDir.strip().lower() in ["", "default"]:
        userSettingsDir = loc_settings

    measurementLoc = input(
        "Measurement file (.cu3s) (default: {}): ".format(loc_file))
    if measurementLoc.strip().lower() in ["", "default"]:
        measurementLoc = loc_file

    darkLoc = input("Dark file (.cu3s) (default: {}): ".format(loc_dark))
    if darkLoc.strip().lower() in ["", "default"]:
        darkLoc = loc_dark

    whiteLoc = input("White file (.cu3s) (default: {}): ".format(loc_white))
    if whiteLoc.strip().lower() in ["", "default"]:
        whiteLoc = loc_white

    distanceLoc = input(
        "Distance file (.cu3s) (default: {}): ".format(loc_distance))
    if distanceLoc.strip().lower() in ["", "default"]:
        distanceLoc = loc_distance

    outDir = input(
        "Name of output directory (default: {}): ".format(loc_output))
    if outDir.strip().lower() in ["", "default"]:
        outDir = loc_output

    run_example_reprocessMeasurement(userSettingsDir,
                                     measurementLoc,
                                     darkLoc,
                                     whiteLoc,
                                     distanceLoc,
                                     outDir)
