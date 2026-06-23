# OT Plot Packaging

This project can be packaged as a Windows desktop app with PyInstaller.

## 1. Prepare a Python environment

Install the runtime and packaging dependencies:

```powershell
python -m pip install -r requirements-packaging.txt
```

If `python` on your machine points to the Windows Store stub, use the full path to the Python executable in your conda environment instead.

## 2. Build the app

Recommended: build an `onedir` package first because it is usually more stable for scientific Python stacks.

```powershell
powershell -ExecutionPolicy Bypass -File .\build_windows.ps1 -PythonExe "C:\Users\shanghaitech\.conda\envs\pylake\python.exe"
```

Optional: build a single-file executable.

```powershell
powershell -ExecutionPolicy Bypass -File .\build_windows.ps1 -PythonExe "C:\Users\shanghaitech\.conda\envs\pylake\python.exe" -OneFile
```

## 3. Distribute to other users

- `onedir`: send the whole folder inside `dist\OTPlotViewer\`
- `onefile`: send the generated `.exe`
- users do not need your original network path anymore; they only need access to their own `.h5` data folders

## Notes

- The app now starts with a blank input folder instead of a lab-specific default path.
- If the save folder is left blank, exports fall back to the selected input folder.
- `Scan` mode is still a placeholder in the current UI.