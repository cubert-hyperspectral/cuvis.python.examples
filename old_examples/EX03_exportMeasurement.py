import os
import platform
from pathlib import Path

import cuvis


def run_example_exportMeasurement(userSettingsDir,
                                  measurementLoc,
                                  pluginLoc,
                                  exportDir):
    print("loading user settings...")
    cuvis.init(userSettingsDir)
    cuvis.set_log_level("info")

    print("loading session file...")
    session = cuvis.SessionFile(measurementLoc)
    mesu = session[0]
    assert mesu._handle

    assert mesu.processing_mode != cuvis.ProcessingMode.Preview, "Wrong processing mode: {}".format(
        mesu.processing_mode.name)

    print("Export to Envi...")
    envi_settings = cuvis.EnviExportSettings(
        export_dir=os.path.join(exportDir, "envi"))
    enviExporter = cuvis.EnviExporter(envi_settings)
    enviExporter.apply(mesu)

    print("Export to Multi-Channel Tiff...")
    multi_tiff_settings = cuvis.TiffExportSettings(
        export_dir=os.path.join(exportDir, "multi"), format=cuvis.TiffFormat.MultiChannel)
    multiTiffExporter = cuvis.TiffExporter(multi_tiff_settings)
    multiTiffExporter.apply(mesu)

    print("Export to separate Tiffs...")
    single_tiff_settings = cuvis.TiffExportSettings(
        export_dir=os.path.join(exportDir, "single"), format=cuvis.TiffFormat.Single)
    singleTiffExporter = cuvis.TiffExporter(single_tiff_settings)
    singleTiffExporter.apply(mesu)

    print("Export View to file...")

    print("load plugin...")
    with open(pluginLoc) as f:
        userpluginCai = f.readlines()
    userpluginCai = "".join(userpluginCai)

    view_export_settings = cuvis.ViewExportSettings(
        export_dir=os.path.join(exportDir, "view"), userplugin=userpluginCai)
    # also view_export_settings = cuvis.ViewExportSettings(ExportDir=os.path.join(exportDir, "view"),
    # Userplugin=pluginLoc) works!
    viewExporter = cuvis.ViewExporter(view_export_settings)
    viewExporter.apply(mesu)

    cuvis.shutdown()
    print("finished.")


if __name__ == "__main__":

    if platform.system() == "Windows":
        lib_dir = Path(os.getenv("CUVIS"))
        data_dir = lib_dir.parent / "sdk" / \
            "sample_data" / "set_examples"
        plugin_dir = lib_dir.parent / "user" / "plugin"

    elif platform.system() == "Linux":
        lib_dir = Path(os.getenv("CUVIS_DATA"))
        data_dir = lib_dir / \
            "sample_data" / "set_examples"
        plugin_dir = lib_dir / "user" / "plugin"

    # default images
    loc_file = data_dir / "set0_single" / "single.cu3s"
    loc_plugin = plugin_dir / "ref" / "cai.xml"

    # default settings
    loc_settings = data_dir / "settings"

    # default output
    loc_output = Path(os.getcwd()) / "EX03_export"

    print("Example 03: Export Measurement. Please provide:")

    userSettingsDir = input(
        "User settings directory (default: {}): ".format(loc_settings))
    if userSettingsDir.strip().lower() in ["", "default"]:
        userSettingsDir = loc_settings

    measurementLoc = input(
        "Measurement file (.cu3) (default: {}): ".format(loc_file))
    if measurementLoc.strip().lower() in ["", "default"]:
        measurementLoc = loc_file

    pluginLoc = input(
        "User plugin file (.xml) (default: {}): ".format(loc_plugin))
    if pluginLoc.strip().lower() in ["", "default"]:
        pluginLoc = loc_plugin

    exportDir = input(
        "Name of export directory (default: {}): ".format(loc_output))
    if exportDir.strip().lower() in ["", "default"]:
        exportDir = loc_output

    run_example_exportMeasurement(str(userSettingsDir), str(measurementLoc), str(pluginLoc),
                                  str(exportDir))
