# OTPlotViewer

Custom Python software for visualizing and exporting single-molecule optical tweezers data from Lumicks C-Trap H5 files.

This archived version focuses on kymograph and force-distance analysis. It provides:

- RGB kymograph visualization with adjustable channel ranges and pseudocolors.
- Interactive box selection on kymographs.
- Photon count versus time for selected kymograph regions.
- Photon count versus position for selected kymograph regions.
- Force, distance, and force-distance plotting.
- PNG and Excel export.
- Windows packaging with PyInstaller.

## Requirements

The software was developed and tested with Python and the packages listed in `requirements.txt`, including:

- `lumicks.pylake`
- `numpy`
- `pandas`
- `matplotlib`
- `h5py`
- `openpyxl`

In this version, `lumicks.pylake` is used through `lumicks.pylake.File` to open C-Trap H5 files and access kymograph objects. The code uses Pylake kymograph methods/properties including `file.kymos`, `kymo.get_image("red"/"green"/"blue")`, `kymo.line_timestamp_ranges()`, `kymo.pixelsize_um`, `kymo.line_time_seconds`, and `kymo.pixel_time_seconds`. Force and distance time-series datasets are read directly from the HDF5 file with `h5py`.

## Run From Source

```powershell
python kymograph_force_distance_ui.py
```

## Build A Windows Distribution

Install packaging dependencies first:

```powershell
python -m pip install -r requirements-packaging.txt
```

Then build the folder distribution:

```powershell
powershell -ExecutionPolicy Bypass -File .\build_windows.ps1 -PythonExe "C:\Path\To\python.exe"
```

The folder distribution is recommended for sharing because it is more reliable than a single-file executable for scientific Python applications with native dependencies.

## Suggested Citation Text

Kymographs were processed and visualized using custom Python software (`OTPlotViewer`, GitHub URL). The software uses `lumicks.pylake.File` to access C-Trap kymograph objects and metadata, while force and distance time series are read from HDF5 datasets using `h5py`; downstream image processing, plotting, and data export are performed with NumPy, Matplotlib, Pandas, and OpenPyXL.

Replace `GitHub URL` with the final repository link after upload.

## Notes

This repository contains the source code and packaging files. Large packaged Windows distributions should be attached through GitHub Releases rather than committed directly to the repository.
