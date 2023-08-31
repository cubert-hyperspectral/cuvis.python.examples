import os
import platform
import sys
import time
from datetime import datetime, timedelta

import cuvis

### default directories and files
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

# default image
loc_file = os.path.join(data_dir,
                        "set0_lab",
                        "x20p_calib_color.cu3s")
# default settings
loc_settings = os.path.join(data_dir, "settings")

# default output
loc_output = os.path.join(os.getcwd(), "EX07_video")

# parameters
loc_exptime = 100
loc_autoexp = False
loc_fps = 2


def run_example_recordVideoFromSessionFile(userSettingsDir=loc_settings,
                                           measurementLoc=loc_file,
                                           recDir=loc_output,
                                           exposure=loc_exptime,
                                           autoExp=loc_autoexp,
                                           fps=loc_fps):
    print("loading user settings...")
    settings = cuvis.General(userSettingsDir)
    settings.set_log_level("info")

    print("loading session file ...")
    session = cuvis.SessionFile(measurementLoc)

    print("loading acquisition context...")
    acquisitionContext = cuvis.AcquisitionContext(session, simulate=True)  #
    # using images from session file instead of camera
    session_info = cuvis.SessionData("video",0,0)
    acquisitionContext.session_info = session_info

    print("prepare saving of measurements...")
    saveArgs = cuvis.SaveArgs(export_dir=recDir,
                                    allow_overwrite=True,
                                    allow_session_file=True,
                                    fps=fps,
                                    operation_mode=cuvis.OperationMode.Internal)

    print("writing files to: {}".format(recDir))
    cubeExporter = cuvis.CubeExporter(saveArgs)

    print("prepare processing of measurements...")
    processingContext = cuvis.ProcessingContext(session)
    processingContext.processing_mode = cuvis.ProcessingMode.Raw

    print("Waiting for camera to come online...")

    while acquisitionContext.state == cuvis.HardwareState.Offline:
        print(".", end="")
        time.sleep(1)
    print("\n")

    print("Component details:")
    print("Component details:")
    for i, (info, is_online) in enumerate(acquisitionContext.components()):
        print("Component #{} {} is {}".format(i, info.display_name,
                                              "online" if is_online else "offline"))
        print(" -- info:        {}".format(info.sensor_info))
        print(" -- use:         {}".format(info.user_field))
        print(" -- pixelformat: {}".format(info.pixel_format))

    print("initializing simulated hardware...")
    acquisitionContext.integration_time = exposure
    acquisitionContext.operation_mode =cuvis.OperationMode.Internal
    acquisitionContext.fps = fps
    acquisitionContext.auto_exp = autoExp
    acquisitionContext.set_continuous(True)

    print("configuring worker...")
    workerSettings = cuvis.WorkerSettings(keep_out_of_sequence=False,
                                                poll_intervall=10,
                                                worker_count=0,
                                                hard_limit=10,
                                                soft_limit=10,
                                                can_drop=True)
    worker = cuvis.Worker(workerSettings)
    worker.set_acquisition_context(acquisitionContext)
    worker.set_processing_context(processingContext)
    worker.set_exporter(cubeExporter)

    print("recording...! (will stop after 2 minutes)")
    start = datetime.now()
    while (datetime.now() - start) < timedelta(minutes=2):

        while 1:
            if worker.has_next_result():
                break
            else:
                time.sleep(0.001)

        workerContainer = worker.get_next_result()
        if workerContainer.mesu.data is not None:
            print("current handle index: {}".format(
                workerContainer.mesu.session_info.sequence_number))
            if worker.get_queue_limits()["soft_limit"] == worker.get_queue_used():
                print("worker queue is full! Main() loop can not keep up!")
                break
            if acquisitionContext.queue_size == acquisitionContext.queue_used:
                print("acquisition queue is full! Worker can not keep up!")
                break

    print("acquisition stopped...")
    acquisitionContext.set_continuous(False)
    print("finished.")

    pass


if __name__ == "__main__":
    print("Example 07: Record video from session file. Please provide:")

    userSettingsDir = input(
        "User settings directory (default: {}): ".format(loc_settings))
    if userSettingsDir.strip().lower() in ["", "default"]:
        userSettingsDir = loc_settings

    factoryDir = input("Session file (default: {}): ".format(
        loc_file))
    if factoryDir.strip().lower() in ["", "default"]:
        factoryDir = loc_file

    recDir = input(
        "Name of recording directory (default: {}): ".format(loc_output))
    if recDir.strip().lower() in ["", "default"]:
        recDir = loc_output

    exposure = input(
        "Exposure/Integration time [ms] (default: {}): ".format(loc_exptime))
    if exposure.strip().lower() in ["", "default"]:
        exposure = loc_exptime
    exposure = int(exposure)

    autoExp = input(
        "Auto-exposure time [True/False] (default: {}): ".format(loc_autoexp))
    if autoExp.strip().lower() in ["", "default"]:
        autoExp = loc_autoexp

    fps = input(
        "Target frames per second (fps) (default: {}): ".format(loc_fps))
    if fps.strip().lower() in ["", "default"]:
        fps = loc_fps
    fps = int(fps)

    run_example_recordVideoFromSessionFile(userSettingsDir, factoryDir, recDir, exposure,
                            autoExp, fps)

    while 1:
        sys.exit(0)
