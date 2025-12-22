import os
import platform
from pathlib import Path
import time

import cuvis
import tifffile

def run_example_pansharpening(userSettingsDir,
                              measurementLoc,
                              panToCube,
                              panScale,
                              exportDir):
    
    print("loading user settings...")
    cuvis.init(userSettingsDir)
    cuvis.set_log_level("info")

    print("loading session file...")
    session = cuvis.SessionFile(measurementLoc)
    mesu = session[0]
    assert mesu._handle

    if 'pan' not in mesu.data.keys():
        raise ValueError('The measurement does not contain a Pan Image.')

    # settings pansharpening
    '''
    cuvis.PansharpeningAlgorithm:
    Defines, which algorithm is used to calculate the pansharpened image. Available options are:
    - Noop:
        "dummy" algorithm, only applies scaling.
    - CubertMacroPixel:
        Generates intensity scaling values for the spectral data from the panimage. Can operate without
        reference measurements.
    - CubertPanRatio:
        Preferred algorithm for reflectance measurements. The measurement's and white calibration's panimages
        are used to generate the panratio (or „panchromatic reflectance“ image). The panratio is then applied
        to the hyperspectral cube to scale the intensity of the spectra without changing their shape. 
    - AlphaBlendOverlay:
        Technically not a pan-sharpening algorithm. Quick workaround to display correlation results on top of
        the pan image using an opacity value selected by the user.
    '''
    panAlgo = cuvis.PanSharpeningAlgorithm.CubertPanRatio # algorithm for pansharpening

    '''
    cuvis.PanSharpeningInterpolationType:
    This setting controls which conventional algorithm is utilized for upscaling the hyperspectral data cube.
    Available options are: Nearest Neighbor, Linear, Cubic and Lanczos
    '''
    panInterp = cuvis.PanSharpeningInterpolationType.Cubic # interpolation method
    
    multi_tiff_settings = cuvis.TiffExportSettings(
        export_dir = str(exportDir),
        format = cuvis.TiffFormat.MultiChannel,
        pan_sharpening_algorithm = panAlgo,
        pan_sharpening_interpolation_type = panInterp, 
        pan_scale = panScale,
        add_pan = panToCube 
        )

    print("size before pansharpening: ", mesu.cube.width, "x", mesu.cube.height, "x", mesu.cube.channels)
    print("Pansharpening and tiff export in progress...")

    multiTiffExporter = cuvis.TiffExporter(multi_tiff_settings)
    multiTiffExporter.apply(mesu) 

    time.sleep(5)

    exportPath= Path(exportDir) / "x20p_flight_data_0000_raw.tiff"
    pansharpened_mesu = tifffile.imread(str(exportPath))
    
    print("size after pansharpening: ", pansharpened_mesu.shape[0], "x", pansharpened_mesu.shape[1], "x", pansharpened_mesu.shape[2] )
    print("algorithm used:", str(panAlgo).split('.')[-1])
    print("Interpolation method used:", str(panInterp).split('.')[-1])
    print("Pansharpening amount:", panScale)
    print("Panimage saved as 0th channel:", panToCube)

    cuvis.shutdown()
    print("finished.")


if __name__ == "__main__":
     
    if platform.system() == "Windows":
        data_dir = Path(os.getenv("CUVIS")).parent / "sdk" / \
            "sample_data" / "set_examples"

    elif platform.system() == "Linux":
        data_dir = Path(os.getenv("CUVIS_DATA")) / \
            "sample_data" / "set_examples"
        
    loc_file = data_dir / "set2_x20p_flight_data" / "x20p_flight_data.cu3s"
    loc_settings = data_dir / "settings"

    pan_to_cube = True
    pan_size = 1

    loc_output = Path(os.getcwd()) / "EX08_pansharpened_measurement"

    print("Example 08: Pansharpen X20 Plus measurement. Please provide:")

    userSettingsDir = input(
        "User settings directory (default: {}): ".format(loc_settings))
    if userSettingsDir.strip().lower() in ["", "default"]:
        userSettingsDir = loc_settings

    measurementLoc = input(
        "Measurement file (.cu3s) (default: {}): ".format(loc_file))
    if measurementLoc.strip().lower() in ["", "default"]:
        measurementLoc = loc_file

    panToCube = input(
        "Save panimage as 0th channel - True/False? (default: {}): ".format(pan_to_cube))
    if panToCube.lower() in ["", "default"]:
        panToCube = pan_to_cube  # use the default boolean value
    elif panToCube.lower() == "true":
        panToCube = True
    elif panToCube.lower() == "false":
        panToCube = False
    else:
        raise ValueError("Invalid input. Please enter True or False.")
    
    panScale = input(
        "Define the amount of pansharpening between 0 and 1 in respect to the size of the panimage (default: {}): ".format(pan_size))
    if panScale.strip().lower() in ["", "default"]:
        panScale = pan_size

    exportDir = input(
        "Name of export directory (default: {}): ".format(loc_output))
    if exportDir.strip().lower() in ["", "default"]:
        exportDir = loc_output

    
    run_example_pansharpening(str(userSettingsDir), str(measurementLoc), panToCube, panScale, exportDir)