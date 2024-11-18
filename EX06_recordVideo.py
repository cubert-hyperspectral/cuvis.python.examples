import os
import platform
import sys
import time
from datetime import datetime, timedelta

import cuvis


# default directories and files
data_dir = None
lib_dir = None

if platform.system() == "Windows":
    lib_dir = os.getenv("CUVIS")
    data_dir = os.path.normpath(os.path.join(lib_dir, os.path.pardir, "sdk",
                                             "sample_data", "set_examples"))
elif platform.system() == "Linux":
    lib_dir = os.getenv("CUVIS_DATA")
    data_dir = os.path.normpath(
        os.path.join(lib_dir, "sample_data", "set_examples"))

# default factory
loc_factory = os.path.join(lib_dir, os.pardir,
                           "factory")
# default settings
loc_settings = os.path.join(data_dir, "settings")

# default output
loc_output = os.path.join(os.getcwd(), "EX06_video")

# parameters
loc_exptime = 100  # in ms
loc_autoexp = False
loc_fps = 2


def run_example_recordVideo(userSettingsDir=loc_settings,
                            factoryDir=loc_factory,
                            recDir=loc_output,
                            exposure=loc_exptime,
                            autoExp=loc_autoexp,
                            fps=loc_fps):
    print("loading user settings...")
    cuvis.init(userSettingsDir)
    cuvis.set_log_level("info")

    print("loading calibration (factory)...")
    calibration = cuvis.Calibration(factoryDir)

    print("loading acquisition context...")
    acquisitionContext = cuvis.AcquisitionContext(calibration)
    session_info = cuvis.SessionData("video", 0, 0)
    acquisitionContext.session_info = session_info

    print("prepare saving of measurements...")
    saveArgs = cuvis.SaveArgs(export_dir=recDir,
                              allow_overwrite=True,
                              allow_session_file=True,
                              fps=fps,
                              operation_mode=cuvis.OperationMode.Software)

    print("writing files to: {}".format(recDir))
    cubeExporter = cuvis.CubeExporter(saveArgs)

    print("prepare processing of measurements...")
    processingContext = cuvis.ProcessingContext(calibration)
    processingContext.processing_mode = cuvis.ProcessingMode.Raw

    print("Waiting for camera to come online...")

    while acquisitionContext.state == cuvis.HardwareState.Offline:
        print(".", end="")
        time.sleep(1)
    print("\n")

    print("Component details:")
    for i, comp in enumerate(acquisitionContext.components()):
        print("Component #{} {} is {}".format(i, comp.info.display_name,
                                              "online" if comp.online else "offline"))
        print(" -- info:        {}".format(comp.info.sensor_info))
        print(" -- use:         {}".format(comp.info.user_field))
        print(" -- pixelformat: {}".format(comp.info.pixel_format))

    print("initializing hardware...")
    acquisitionContext.integration_time = exposure
    acquisitionContext.operation_mode = cuvis.OperationMode.Internal
    acquisitionContext.fps = fps
    acquisitionContext.auto_exp = autoExp
    acquisitionContext.set_continuous(True)

    print("configuring worker...")
    workerSettings = cuvis.WorkerSettings()
    worker = cuvis.Worker(workerSettings)
    worker.set_acquisition_context(acquisitionContext)
    worker.set_processing_context(processingContext)
    worker.set_exporter(cubeExporter)
    worker.start_processing()

    print("recording...! (will stop after 2 minutes)")
    start = datetime.now()
    while (datetime.now() - start) < timedelta(minutes=2):

        while 1:
            if worker.has_next_result():
                break
            else:
                time.sleep(0.001)

        workerContainer = worker.get_next_result(1000)  # in ms
        if workerContainer.mesu.data is not None:
            print("current handle index: {}".format(
                workerContainer.mesu.session_info.sequence_number))

            print(workerContainer)

    print("acquisition stopped...")
    acquisitionContext.set_continuous(False)
    worker.stop_processing()
    cuvis.shutdown()
    print("finished.")


if __name__ == "__main__":
    print("Example 06: Record video file. Please provide:")

    userSettingsDir = input(
        "User settings directory (default: {}): ".format(loc_settings))
    if userSettingsDir.strip().lower() in ["", "default"]:
        userSettingsDir = loc_settings

    factoryDir = input("Factory directory (default: {}): ".format(loc_factory))
    if factoryDir.strip().lower() in ["", "default"]:
        factoryDir = loc_factory

    recDir = input(
        "Name of recording directory (default: {}): ".format(loc_output))
    if recDir.strip().lower() in ["", "default"]:
        recDir = loc_output

    exposure = input(
        "Exposure/Integration time in ms (default: {}): ".format(loc_exptime))
    if exposure.strip().lower() in ["", "default"]:
        exposure = loc_exptime
    exposure = int(exposure)

    autoExp = input(
        "Auto-exposure time [True/False] (default: {}): ".format(loc_autoexp))
    if autoExp.strip().lower() in ["", "default"]:
        autoExp = loc_autoexp
    autoExp = int(autoExp)

    fps = input(
        "Target frames per second (fps) (default: {}): ".format(loc_fps))
    if fps.strip().lower() in ["", "default"]:
        fps = loc_fps
    fps = int(fps)

    run_example_recordVideo(userSettingsDir, factoryDir, recDir, exposure,
                            autoExp, fps)

    while 1:
        sys.exit(0)
