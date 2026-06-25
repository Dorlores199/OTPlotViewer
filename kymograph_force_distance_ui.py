import os
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, ttk

import h5py
import lumicks.pylake as lk
import numpy as np
import pandas as pd

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector


BASE = ""
DEFAULT_FILES = []
DEFAULT_BROWSE_DIR = os.path.expanduser("~")

FORCE_DS = "Force LF/Force 2x"
FORCE_FALLBACK_DS = (FORCE_DS, "Force HF/Force 2x")
DIST_CHOICES = {
    "Distance/Distance 1": "Distance/Distance 1",
    "Force LF/Trap 1": "Force LF/Trap 1",
    "Force LF/Trap 2": "Force LF/Trap 2",
}
DIST1_DS = DIST_CHOICES["Distance/Distance 1"]
RGB_CHANNELS = ("red", "green", "blue")
CHANNEL_INDEX = {"red": 0, "green": 1, "blue": 2}
CHANNEL_LABELS = {"red": "Red", "green": "Green", "blue": "Blue"}
DEFAULT_ENABLED = {"red": True, "green": True, "blue": True}
DEFAULT_PSEUDOCOLORS = {"red": "#FF0000", "green": "#00FF00", "blue": "#0000FF"}
PANEL_EYE_OPEN = "\U0001F441"
PANEL_EYE_CLOSED = "\U0001F441\u0336"
FD_OVERLAY_COLORS = ("#1F77B4", "#FF7F0E", "#2CA02C", "#9467BD", "#8C564B", "#E377C2", "#7F7F7F", "#BCBD22", "#17BECF")
DATA_MODE_OPTIONS = (("kymograph", "kymograph_mode"), ("fd_curve", "fd_curve_mode"), ("scan", "scan_mode"))
DATA_MODE_LABEL_KEYS = {mode_key: label_key for mode_key, label_key in DATA_MODE_OPTIONS}
PANEL_SPECS = (
    ("kymo", "Kymograph", 3.8),
    ("force", "Force", 1.0),
    ("distance", "Distance", 1.0),
    ("photon", "Photon count", 1.0),
    ("photon_profile", "Photon profile", 0.8),
    ("fd", "Force-Distance", 1.0),
)
PANEL_SHARE_GROUPS = {
    "kymo": "time",
    "force": "time",
    "distance": "time",
    "photon": "time",
    "photon_profile": "photon_profile",
    "fd": "fd",
}
PANEL_DEFAULTS = {panel_key: {"show": True, "export_style": True} for panel_key, _panel_label, _weight in PANEL_SPECS}
FONT_CHOICES = (
    "Arial",
    "Calibri",
    "Cambria",
    "Times New Roman",
    "Helvetica",
    "DejaVu Sans",
)
RANGE_DEFAULTS = {
    "time_min": "",
    "time_max": "",
    "time_interval": "",
    "force_min": "",
    "force_max": "",
    "force_interval": "",
    "distance_min": "",
    "distance_max": "",
    "distance_interval": "",
    "image_y_min": "",
    "image_y_max": "",
    "image_y_interval": "",
}
STYLE_DEFAULTS = {
    "fontfamily": "Arial",
    "font_bold": False,
    "tick_fontsize": "10",
    "label_fontsize": "12",
    "title_fontsize": "15",
    "spine_width": "1.0",
    "tick_width": "1.0",
    "curve_width": "1.0",
    "force_color": "#1F77B4",
    "distance_color": "#FF7F0E",
    "fd_color": "#D62728",
    "photon_red_color": "#D62728",
    "photon_green_color": "#2CA02C",
    "photon_blue_color": "#1F77B4",
}
STYLE_COLOR_LABELS = {
    "force_color": "Force line",
    "distance_color": "Distance line",
    "fd_color": "Force-Distance line",
    "photon_red_color": "Photon red",
    "photon_green_color": "Photon green",
    "photon_blue_color": "Photon blue",
}
PREVIEW_CANVAS_SIZE = (11.0, 8.0)
PREVIEW_DPI = 120
PREVIEW_BACKGROUND = "#FFFFFF"
LANGUAGE_OPTIONS = (("English", "en"), ("\u7b80\u4f53\u4e2d\u6587", "zh"))
LANGUAGE_NAME_TO_CODE = {name: code for name, code in LANGUAGE_OPTIONS}
LANGUAGE_CODE_TO_NAME = {code: name for name, code in LANGUAGE_OPTIONS}
TRANSLATIONS = {
    "en": {
        "window_title": "Kymograph / Force / Distance Viewer", "language": "Language", "input_folder": "Input folder", "browse": "Browse...", "refresh": "Refresh", "open_folder": "Open folder", "file": "File", "distance_source": "Distance source", "panels": "Panels", "apply_section_to_all": "Apply section to all", "panel": "Panel", "show": "Show", "eye": "Eye", "ranges": "Ranges", "blank_auto": "Blank = auto", "range_drag_hint": "Drag a box to set ranges; double-click plot to reset", "time_range": "Time min/max (s)", "force_range": "Force min/max (pN)", "distance_range": "Distance min/max (um)", "image_y_range": "Image y min/max (um)", "save_folder_png": "Save folder (png)", "rgb_image": "RGB image", "reset_rgb": "Reset RGB", "style": "Style", "font": "Font", "bold_text": "Bold text", "tick_size": "Tick size", "label_size": "Label size", "title_size": "Title size", "axis_width": "Axis width", "tick_width": "Tick width", "curve_width": "Curve width", "force_line": "Force line", "distance_line": "Distance line", "fd_line": "FD line", "photon_red": "Photon red", "photon_green": "Photon green", "photon_blue": "Photon blue", "draw_current": "Draw current", "save_current_png": "Save current PNG", "save_all_png": "Save all to PNG", "export_current_excel": "Export current Excel", "export_all_excel": "Export all to Excel", "ready": "Ready", "apply_all": "Apply all", "pick": "Pick...", "to": "to", "step": "step", "apply_channel_to_all": "Apply channel to all", "min": "Min", "max": "Max", "gamma": "Gamma", "color": "Color", "kymo_panel": "Kymograph", "force_panel": "Force", "distance_panel": "Distance", "photon_panel": "Photon count", "photon_profile_panel": "Photon vs position", "fd_panel": "Force-Distance", "red_channel": "Red channel", "green_channel": "Green channel", "blue_channel": "Blue channel"
    },
    "zh": {
        "window_title": "\u004b\u0079\u006d\u006f\u0067\u0072\u0061\u0070\u0068 / Force / Distance \u67e5\u770b\u5668", "language": "\u8bed\u8a00", "input_folder": "\u8f93\u5165\u6587\u4ef6\u5939", "browse": "\u6d4f\u89c8...", "refresh": "\u5237\u65b0", "open_folder": "\u6253\u5f00\u6587\u4ef6\u5939", "file": "\u6587\u4ef6", "distance_source": "\u8ddd\u79bb\u6765\u6e90", "panels": "\u9762\u677f", "apply_section_to_all": "\u6574\u7ec4\u5e94\u7528\u5230\u5168\u90e8", "panel": "\u56fe\u5f62", "show": "\u663e\u793a", "eye": "\u773c\u775b", "ranges": "\u8303\u56f4", "blank_auto": "\u7559\u7a7a = \u81ea\u52a8", "range_drag_hint": "\u62d6\u62fd\u6846\u9009\u53ef\u8bbe\u7f6e\u8303\u56f4\uff1b\u53cc\u51fb\u56fe\u50cf\u53ef\u91cd\u7f6e", "time_range": "\u65f6\u95f4\u6700\u5c0f/\u6700\u5927 (s)", "force_range": "\u529b\u6700\u5c0f/\u6700\u5927 (pN)", "distance_range": "\u8ddd\u79bb\u6700\u5c0f/\u6700\u5927 (um)", "image_y_range": "\u56fe\u50cf y \u6700\u5c0f/\u6700\u5927 (um)", "save_folder_png": "\u4fdd\u5b58\u6587\u4ef6\u5939 (png)", "rgb_image": "RGB \u56fe\u50cf", "reset_rgb": "\u91cd\u7f6e RGB", "style": "\u6837\u5f0f", "font": "\u5b57\u4f53", "bold_text": "\u7c97\u4f53\u6587\u5b57", "tick_size": "\u523b\u5ea6\u5b57\u53f7", "label_size": "\u6807\u7b7e\u5b57\u53f7", "title_size": "\u6807\u9898\u5b57\u53f7", "axis_width": "\u5750\u6807\u8f74\u5bbd\u5ea6", "tick_width": "\u523b\u5ea6\u5bbd\u5ea6", "curve_width": "\u66f2\u7ebf\u5bbd\u5ea6", "force_line": "\u529b\u66f2\u7ebf\u989c\u8272", "distance_line": "\u8ddd\u79bb\u66f2\u7ebf\u989c\u8272", "fd_line": "FD \u66f2\u7ebf\u989c\u8272", "photon_red": "Photon \u7ea2\u8272", "photon_green": "Photon \u7eff\u8272", "photon_blue": "Photon \u84dd\u8272", "draw_current": "\u7ed8\u5236\u5f53\u524d", "save_current_png": "\u4fdd\u5b58\u5f53\u524d PNG", "save_all_png": "\u5168\u90e8\u4fdd\u5b58\u4e3a PNG", "export_current_excel": "\u5bfc\u51fa\u5f53\u524d Excel", "export_all_excel": "\u5168\u90e8\u5bfc\u51fa Excel", "ready": "\u5c31\u7eea", "apply_all": "\u5e94\u7528\u5230\u5168\u90e8", "pick": "\u9009\u62e9...", "to": "\u5230", "step": "\u95f4\u9694", "apply_channel_to_all": "\u6574\u901a\u9053\u5e94\u7528\u5230\u5168\u90e8", "min": "\u6700\u5c0f", "max": "\u6700\u5927", "gamma": "Gamma", "color": "\u989c\u8272", "kymo_panel": "Kymograph", "force_panel": "\u529b", "distance_panel": "\u8ddd\u79bb", "photon_panel": "Photon \u8ba1\u6570", "photon_profile_panel": "Photon-\u4f4d\u7f6e", "fd_panel": "\u529b-\u8ddd\u79bb", "red_channel": "\u7ea2\u8272\u901a\u9053", "green_channel": "\u7eff\u8272\u901a\u9053", "blue_channel": "\u84dd\u8272\u901a\u9053"
    },
}
TRANSLATIONS["en"].update({
    "data_type": "Data type",
    "kymograph_mode": "Kymograph",
    "fd_curve_mode": "FD Curve",
    "scan_mode": "Scan",
    "fd_overlay": "FD overlay",
    "enable_fd_overlay": "Enable FD overlay",
    "include_current_file": "Include current file",
    "overlay_files": "Overlay files",
    "select_all": "Select all",
    "clear": "Clear",
    "plot_size": "Plot size",
    "plot_width": "Width",
    "plot_height": "Height",
    "lock_aspect_ratio": "Lock aspect ratio",
    "scan_tools": "Scan tools",
    "scan_placeholder": "Scan processing tools will be added here.",
    "no_files_for_mode": "No files found for this category.",
    "select_input_folder_hint": "Select an input folder to get started.",
    "no_h5_files_found": "No H5 files were found in the selected folder.",
    "folder_not_found": "The selected folder does not exist.",
    "input_folder_not_set": "Choose an input folder first.",
    "kymograph_only_action": "This action is currently available only in Kymograph mode.",
    "scan_excel_placeholder": "Scan data export will be added when Scan analysis tools are implemented.",
})
TRANSLATIONS["zh"].update({
    "data_type": "\u6570\u636e\u7c7b\u578b",
    "kymograph_mode": "Kymograph",
    "fd_curve_mode": "FD Curve",
    "scan_mode": "Scan",
    "fd_overlay": "FD \u53e0\u52a0",
    "enable_fd_overlay": "\u542f\u7528 FD \u53e0\u52a0",
    "include_current_file": "\u5305\u542b\u5f53\u524d\u6587\u4ef6",
    "overlay_files": "\u53e0\u52a0\u6587\u4ef6",
    "select_all": "\u5168\u9009",
    "clear": "\u6e05\u7a7a",
    "plot_size": "\u4f5c\u56fe\u5c3a\u5bf8",
    "plot_width": "\u5bbd\u5ea6",
    "plot_height": "\u9ad8\u5ea6",
    "lock_aspect_ratio": "\u9501\u5b9a\u957f\u5bbd\u6bd4",
    "scan_tools": "Scan \u529f\u80fd",
    "scan_placeholder": "Scan \u6570\u636e\u7684\u5904\u7406\u529f\u80fd\u4f1a\u540e\u7eed\u52a0\u5165\u5728\u8fd9\u91cc\u3002",
    "no_files_for_mode": "\u5f53\u524d\u7c7b\u522b\u6ca1\u6709\u627e\u5230\u6587\u4ef6\u3002",
    "select_input_folder_hint": "\u8bf7\u5148\u9009\u62e9\u8f93\u5165\u6587\u4ef6\u5939\u3002",
    "no_h5_files_found": "\u6240\u9009\u6587\u4ef6\u5939\u4e2d\u6ca1\u6709\u627e\u5230 H5 \u6587\u4ef6\u3002",
    "folder_not_found": "\u6240\u9009\u6587\u4ef6\u5939\u4e0d\u5b58\u5728\u3002",
    "input_folder_not_set": "\u8bf7\u5148\u9009\u62e9\u8f93\u5165\u6587\u4ef6\u5939\u3002",
    "kymograph_only_action": "\u8fd9\u4e2a\u64cd\u4f5c\u76ee\u524d\u53ea\u5728 Kymograph \u6a21\u5f0f\u4e0b\u53ef\u7528\u3002",
    "scan_excel_placeholder": "Scan \u6570\u636e Excel \u5bfc\u51fa\u4f1a\u5728\u540e\u7eed\u52a0\u5165 Scan \u5206\u6790\u529f\u80fd\u540e\u63d0\u4f9b\u3002",
})
RGB_OVERRIDE_DEFAULTS = {
    color: {"enabled": None, "min": None, "max": None, "gamma": None, "pseudocolor": None} for color in RGB_CHANNELS
}


def list_h5_files(input_dir):
    try:
        return sorted([name for name in os.listdir(input_dir) if name.lower().endswith(".h5")])
    except Exception:
        return []


def classify_file_type(filename):
    lower_name = str(filename or "").lower()
    if "fd curve" in lower_name or "fd_curve" in lower_name or "fdcurve" in lower_name:
        return "fd_curve"
    if "scan" in lower_name:
        return "scan"
    if "kymograph" in lower_name:
        return "kymograph"
    return "kymograph"


def group_files_by_type(files):
    grouped = {mode_key: [] for mode_key, _label_key in DATA_MODE_OPTIONS}
    for filename in files:
        grouped.setdefault(classify_file_type(filename), []).append(filename)
    return grouped


def parse_optional_float(value):
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return float(text)
    except Exception:
        return None


def format_number(value, digits=2):
    if value is None:
        return ""
    if abs(value) >= 100:
        digits = 1
    if abs(value) >= 1000:
        digits = 0
    return f"{value:.{digits}f}"


def normalize_hex_color(value, fallback=None):
    text = str(value or "").strip()
    if text.startswith("#"):
        text = text[1:]
    if len(text) == 3:
        text = "".join(ch * 2 for ch in text)
    if len(text) != 6:
        return fallback
    try:
        int(text, 16)
    except Exception:
        return fallback
    return f"#{text.upper()}"


def hex_color_to_rgb(color_text):
    normalized = normalize_hex_color(color_text, "#FFFFFF")
    return np.array([int(normalized[idx:idx + 2], 16) for idx in (1, 3, 5)], dtype=np.float64) / 255.0


def _resolve_h5_dataset_path(handle, path_or_paths):
    candidates = (path_or_paths,) if isinstance(path_or_paths, str) else tuple(path_or_paths)
    for path in candidates:
        if path in handle:
            return path
    raise KeyError(f"Missing HDF5 dataset. Tried: {', '.join(candidates)}")


def _open_h5_signal(handle, path_or_paths):
    path = _resolve_h5_dataset_path(handle, path_or_paths)
    ds = handle[path]
    fields = ds.dtype.fields or {}
    if "Timestamp" in fields and "Value" in fields:
        timestamps = np.asarray(ds["Timestamp"], dtype=np.int64)
        values = np.asarray(ds["Value"], dtype=np.float64)
        if timestamps.size == 0:
            raise ValueError(f"HDF5 dataset is empty: {path}")
        return {
            "kind": "timeseries",
            "path": path,
            "timestamps": timestamps,
            "values": values,
        }

    if "Start time (ns)" in ds.attrs and "Sample rate (Hz)" in ds.attrs:
        n_points = int(ds.shape[0]) if ds.shape else 0
        if n_points <= 0:
            raise ValueError(f"HDF5 dataset is empty: {path}")
        start_ns = int(ds.attrs["Start time (ns)"])
        sample_rate = float(ds.attrs["Sample rate (Hz)"])
        stop_attr = ds.attrs.get("Stop time (ns)", None)
        stop_ns = int(stop_attr) if stop_attr is not None else int(start_ns + (n_points - 1) * 1e9 / sample_rate)
        return {
            "kind": "continuous",
            "path": path,
            "dataset": ds,
            "n_points": n_points,
            "start_ns": start_ns,
            "stop_ns": stop_ns,
            "sample_rate": sample_rate,
        }

    raise ValueError(f"Unsupported HDF5 signal format: {path}")


def _signal_start_ns(signal):
    if signal["kind"] == "timeseries":
        return int(signal["timestamps"][0])
    return int(signal["start_ns"])


def _signal_stop_ns(signal):
    if signal["kind"] == "timeseries":
        return int(signal["timestamps"][-1])
    return int(signal["stop_ns"])


def _choose_signal_timestamps(force_signal, dist_signal, max_points=12000):
    if force_signal["kind"] == "timeseries":
        return force_signal["timestamps"]
    if dist_signal["kind"] == "timeseries":
        return dist_signal["timestamps"]

    start_ns = max(_signal_start_ns(force_signal), _signal_start_ns(dist_signal))
    stop_ns = min(_signal_stop_ns(force_signal), _signal_stop_ns(dist_signal))
    if stop_ns <= start_ns:
        start_ns = min(_signal_start_ns(force_signal), _signal_start_ns(dist_signal))
        stop_ns = max(_signal_stop_ns(force_signal), _signal_stop_ns(dist_signal))
    n_points = max(2, min(max_points, force_signal["n_points"], dist_signal["n_points"]))
    return np.linspace(start_ns, stop_ns, n_points).astype(np.int64)


def _sample_signal_at_timestamps(signal, target_timestamps):
    target_timestamps = np.asarray(target_timestamps, dtype=np.int64)
    if signal["kind"] == "timeseries":
        source_timestamps = signal["timestamps"]
        values = signal["values"]
        if source_timestamps.shape == target_timestamps.shape and np.array_equal(source_timestamps, target_timestamps):
            return values
        t0 = int(source_timestamps[0])
        source_t = (source_timestamps - t0) / 1e9
        target_t = (target_timestamps - t0) / 1e9
        return np.interp(target_t, source_t, values)

    n_points = signal["n_points"]
    start_ns = signal["start_ns"]
    sample_rate = signal["sample_rate"]
    positions = (target_timestamps.astype(np.float64) - float(start_ns)) * sample_rate / 1e9
    positions = np.clip(positions, 0.0, float(n_points - 1))
    left = np.floor(positions).astype(np.int64)
    right = np.clip(left + 1, 0, n_points - 1)
    frac = positions - left

    needed = np.unique(np.concatenate([left, right]))
    samples = np.asarray(signal["dataset"][needed], dtype=np.float64)
    left_values = samples[np.searchsorted(needed, left)]
    right_values = samples[np.searchsorted(needed, right)]
    return left_values * (1.0 - frac) + right_values * frac


def h5_load_timeseries(h5_path, force_path, dist_path):
    with h5py.File(h5_path, "r") as handle:
        force_candidates = FORCE_FALLBACK_DS if force_path == FORCE_DS else force_path
        force_signal = _open_h5_signal(handle, force_candidates)
        dist_signal = _open_h5_signal(handle, dist_path)
        target_timestamps = _choose_signal_timestamps(force_signal, dist_signal)
        if target_timestamps.size == 0:
            raise ValueError("No timestamps available for force/distance alignment.")

        t0 = min(_signal_start_ns(force_signal), _signal_start_ns(dist_signal))
        t_force = (target_timestamps - t0) / 1e9
        force = _sample_signal_at_timestamps(force_signal, target_timestamps)
        dist_aligned = _sample_signal_at_timestamps(dist_signal, target_timestamps)

    return t0, t_force, force, dist_aligned


def load_kymo_data(h5_path, t0_ns):
    file_handle = lk.File(h5_path)
    if not file_handle.kymos:
        return None

    kymo = next(iter(file_handle.kymos.values()))
    line_ranges = kymo.line_timestamp_ranges()
    if not line_ranges:
        return None

    red = np.asarray(kymo.get_image("red"), dtype=np.float64)
    green = np.asarray(kymo.get_image("green"), dtype=np.float64)
    blue = np.asarray(kymo.get_image("blue"), dtype=np.float64)

    first_start, _ = line_ranges[0]
    _, last_stop = line_ranges[-1]
    x0 = (first_start - t0_ns) / 1e9
    x1 = (last_stop - t0_ns) / 1e9

    pixelsize_um = float(np.atleast_1d(kymo.pixelsize_um)[0]) if kymo.pixelsize_um is not None else 1.0
    y_size_um = float(red.shape[0] * pixelsize_um)

    return {
        "name": kymo.name,
        "red": red,
        "green": green,
        "blue": blue,
        "x0": x0,
        "x1": x1,
        "y0": 0.0,
        "y1": y_size_um,
        "pixelsize_um": pixelsize_um,
        "line_time_seconds": float(kymo.line_time_seconds),
        "pixel_time_seconds": float(kymo.pixel_time_seconds),
    }


def load_plot_data(h5_path, force_path, dist_path):
    t0_ns, t_force, force, dist = h5_load_timeseries(h5_path, force_path, dist_path)
    if dist_path == DIST1_DS:
        dist1 = dist
    else:
        _, _, _, dist1 = h5_load_timeseries(h5_path, force_path, DIST1_DS)
    kymo = load_kymo_data(h5_path, t0_ns)
    return {"t": t_force, "force": force, "dist": dist, "dist1": dist1, "kymo": kymo}


def build_rgb_image(kymo_data, rgb_settings):
    rows, cols = kymo_data["red"].shape
    rgb = np.zeros((rows, cols, 3), dtype=np.float64)

    for color in RGB_CHANNELS:
        channel = np.asarray(kymo_data[color], dtype=np.float64)
        settings = rgb_settings[color]
        if not settings["enabled"]:
            continue

        cmin = settings["min"]
        cmax = settings["max"]
        gamma = max(settings["gamma"], 0.05)
        if cmax <= cmin:
            cmax = cmin + 1.0

        normalized = np.clip((channel - cmin) / (cmax - cmin), 0.0, 1.0)
        rgb += (normalized ** (1.0 / gamma))[..., None] * hex_color_to_rgb(settings["pseudocolor"])

    return np.clip(rgb, 0.0, 1.0)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kymograph / Force / Distance Viewer")
        self.geometry("1700x1000")

        self.language_code = "en"
        self.language_display_var = tk.StringVar(value=LANGUAGE_CODE_TO_NAME[self.language_code])
        self.data_mode_var = tk.StringVar(value="kymograph")
        self.current_mode_key = self.data_mode_var.get()
        self.data_cache = {}
        self.all_files = list(DEFAULT_FILES)
        self.file_groups = group_files_by_type(self.all_files)
        self.mode_file_selection = {mode_key: "" for mode_key, _label_key in DATA_MODE_OPTIONS}
        self.file_list = list(self.file_groups.get(self.current_mode_key, []))
        self.plot_width_var = tk.StringVar(value="11")
        self.plot_height_var = tk.StringVar(value="8")
        self.plot_aspect_lock_var = tk.BooleanVar(value=True)
        self.range_vars = {}
        self.range_pairs = {}
        self.style_vars = {}
        self.rgb_vars = {}
        self.panel_vars = {}
        self.panel_eye_text_vars = {}
        self.style_color_previews = {}
        self.fd_overlay_enabled_var = None
        self.fd_overlay_include_current_var = None
        self.fd_overlay_listbox = None
        self.file_label = None
        self.plot_size_section = None
        self.dist_label = None
        self.save_label = None
        self.save_frame = None
        self.button_frame = None
        self.status_label = None
        self._suspend_redraw = False
        self._plot_size_syncing = False
        self._plot_aspect_ratio = 11.0 / 8.0
        self._section_vars = {}
        self._range_selectors = []
        self.status_var = tk.StringVar(value=self._t("select_input_folder_hint"))

        self.global_plot_size_defaults = {"width": "11", "height": "8", "lock_aspect": True}
        self.global_range_defaults = dict(RANGE_DEFAULTS)
        self.global_style_defaults = dict(STYLE_DEFAULTS)
        self.global_rgb_defaults = {color: dict(RGB_OVERRIDE_DEFAULTS[color]) for color in RGB_CHANNELS}
        self.global_panel_defaults = {panel_key: dict(PANEL_DEFAULTS[panel_key]) for panel_key, _panel_label, _weight in PANEL_SPECS}

        self._build_ui()
        self._refresh_file_list(keep_selection=False)
        self._reset_controls_for_selected_file()
        self._draw_current()

    def _t(self, key):
        return TRANSLATIONS.get(self.language_code, TRANSLATIONS["en"]).get(key, TRANSLATIONS["en"].get(key, key))

    def _get_dialog_dir(self, *candidates):
        for candidate in candidates:
            path = str(candidate or "").strip()
            if path and os.path.isdir(path):
                return path
        if os.path.isdir(DEFAULT_BROWSE_DIR):
            return DEFAULT_BROWSE_DIR
        cwd = os.getcwd()
        return cwd if os.path.isdir(cwd) else ""

    def _get_empty_state_message(self, mode_key):
        input_dir = self._get_input_dir()
        if not input_dir:
            return self._t("select_input_folder_hint")
        if not os.path.isdir(input_dir):
            return self._t("folder_not_found")
        if not self.all_files:
            return self._t("no_h5_files_found")
        return self._t("no_files_for_mode")

    def _panel_label(self, panel_key):
        return self._t(f"{panel_key}_panel")

    def _snapshot_ui_state(self):
        state = {
            "input_dir": self.input_dir_var.get() if hasattr(self, "input_dir_var") else "",
            "save_dir": self.save_dir_var.get() if hasattr(self, "save_dir_var") else "",
            "file": self.file_var.get() if hasattr(self, "file_var") else "",
            "data_mode": self._get_current_mode(),
            "distance_source": self.dist_var.get() if hasattr(self, "dist_var") else list(DIST_CHOICES.keys())[0],
            "ranges": {key: var.get() for key, var in self.range_vars.items()},
            "styles": {key: self._capture_var_value(var) for key, var in self.style_vars.items()},
            "panels": {panel_key: {field: bool(var.get()) for field, var in values.items()} for panel_key, values in self.panel_vars.items()},
            "sections": {key: value["expanded"] for key, value in self._section_vars.items()},
            "rgb": {},
            "fd_overlay": {
                "enabled": bool(self.fd_overlay_enabled_var.get()) if self.fd_overlay_enabled_var else False,
                "include_current": bool(self.fd_overlay_include_current_var.get()) if self.fd_overlay_include_current_var else True,
                "files": self._get_fd_overlay_selected_files() if self.fd_overlay_listbox else [],
            },
        }
        for color, values in self.rgb_vars.items():
            state["rgb"][color] = {"enabled": bool(values["enabled"].get()), "min": str(values["min"].get()), "max": str(values["max"].get()), "gamma": float(values["gamma"].get()), "pseudocolor": str(values["pseudocolor"].get())}
        return state

    def _restore_ui_state(self, state):
        self._suspend_redraw = True
        try:
            self.input_dir_var.set(state.get("input_dir", ""))
            self.save_dir_var.set(state.get("save_dir", ""))
            self.data_mode_var.set(state.get("data_mode", "kymograph"))
            self.current_mode_key = self._get_current_mode()
            self.dist_var.set(state.get("distance_source", list(DIST_CHOICES.keys())[0]))
            self._refresh_file_list(keep_selection=False)
            self._update_mode_visibility()
            selected_file = state.get("file", "")
            if selected_file in self.file_list:
                self.file_var.set(selected_file)
            for key, value in state.get("ranges", {}).items():
                if key in self.range_vars:
                    self.range_vars[key].set(value)
            for key, value in state.get("styles", {}).items():
                if key in self.style_vars:
                    self.style_vars[key].set(value)
            for panel_key, values in state.get("panels", {}).items():
                if panel_key in self.panel_vars:
                    for field, value in values.items():
                        if field in self.panel_vars[panel_key]:
                            self.panel_vars[panel_key][field].set(bool(value))
                    self._update_panel_eye_button(panel_key)
            for color, values in state.get("rgb", {}).items():
                if color in self.rgb_vars:
                    self.rgb_vars[color]["enabled"].set(bool(values.get("enabled", False)))
                    self.rgb_vars[color]["min"].set(str(values.get("min", "")))
                    self.rgb_vars[color]["max"].set(str(values.get("max", "")))
                    self.rgb_vars[color]["gamma"].set(float(values.get("gamma", 1.0)))
                    self.rgb_vars[color]["pseudocolor"].set(str(values.get("pseudocolor", DEFAULT_PSEUDOCOLORS[color])))
                    self._update_gamma_label(color)
                    self._update_rgb_color_preview(color)
            fd_state = state.get("fd_overlay", {})
            if self.fd_overlay_enabled_var is not None:
                self.fd_overlay_enabled_var.set(bool(fd_state.get("enabled", False)))
            if self.fd_overlay_include_current_var is not None:
                self.fd_overlay_include_current_var.set(bool(fd_state.get("include_current", True)))
            self._refresh_fd_overlay_file_list(keep_selection=False, selected_files=fd_state.get("files", []))

            for section_key, expanded in state.get("sections", {}).items():
                if section_key in self._section_vars:
                    self._section_vars[section_key]["expanded"] = bool(expanded)
                    self._section_vars[section_key]["refresh"]()
        finally:
            self._suspend_redraw = False

    def _rebuild_ui_for_language(self):
        state = self._snapshot_ui_state()
        if hasattr(self, "main_container"):
            self.main_container.destroy()
        self._section_vars = {}
        self.panel_eye_text_vars = {}
        self.style_color_previews = {}
        self._build_ui()
        self._restore_ui_state(state)
        self._draw_current()

    def _on_language_selected(self, _event=None):
        new_code = LANGUAGE_NAME_TO_CODE.get(self.language_display_var.get(), "en")
        if new_code == self.language_code:
            return
        self.language_code = new_code
        self._rebuild_ui_for_language()

    def _build_ui(self):
        self.title(self._t("window_title"))
        root = ttk.Frame(self, padding=10)
        root.pack(fill="both", expand=True)
        self.main_container = root

        left_outer = ttk.Frame(root)
        left_outer.pack(side="left", fill="y", padx=(0, 10))

        panel_bg = ttk.Style().lookup("TFrame", "background") or self.cget("background")
        self.left_canvas = tk.Canvas(left_outer, highlightthickness=0, borderwidth=0, width=460, background=panel_bg)
        left_scrollbar = ttk.Scrollbar(left_outer, orient="vertical", command=self.left_canvas.yview)
        self.left_canvas.configure(yscrollcommand=left_scrollbar.set)
        left_scrollbar.pack(side="right", fill="y")
        self.left_canvas.pack(side="left", fill="y", expand=True)

        left = ttk.Frame(self.left_canvas)
        left.grid_columnconfigure(0, weight=1)
        self.left_canvas_window = self.left_canvas.create_window((0, 0), window=left, anchor="nw")
        left.bind("<Configure>", self._on_left_panel_configure)
        self.left_canvas.bind("<Configure>", self._on_left_canvas_configure)
        self.bind_all("<MouseWheel>", self._on_left_mousewheel, add="+")
        self.bind_all("<Button-4>", self._on_left_mousewheel, add="+")
        self.bind_all("<Button-5>", self._on_left_mousewheel, add="+")

        right = ttk.Frame(root)
        right.pack(side="right", fill="both", expand=True)
        preview_width_px, preview_height_px = self._get_preview_canvas_pixel_size()
        self.preview_shell = tk.Frame(right, background=PREVIEW_BACKGROUND)
        self.preview_shell.pack(fill="both", expand=True)
        self.preview_host = tk.Frame(
            self.preview_shell,
            width=preview_width_px,
            height=preview_height_px,
            background=PREVIEW_BACKGROUND,
            highlightthickness=0,
            borderwidth=0,
        )
        self.preview_host.pack_propagate(False)
        self.preview_host.place(relx=0.5, rely=0.5, anchor="center", width=preview_width_px, height=preview_height_px)

        row = 0
        ttk.Label(left, text=self._t("language")).grid(row=row, column=0, sticky="w")
        row += 1
        language_combo = ttk.Combobox(left, textvariable=self.language_display_var, values=[name for name, _code in LANGUAGE_OPTIONS], state="readonly", width=18)
        language_combo.grid(row=row, column=0, pady=(0, 10), sticky="w")
        language_combo.bind("<<ComboboxSelected>>", self._on_language_selected)

        row += 1
        ttk.Label(left, text=self._t("input_folder")).grid(row=row, column=0, sticky="w")
        row += 1
        self.input_dir_var = tk.StringVar(value="")
        fr_input = ttk.Frame(left)
        fr_input.grid(row=row, column=0, sticky="we", pady=(0, 10))
        ttk.Entry(fr_input, textvariable=self.input_dir_var, width=38).pack(side="left")
        ttk.Button(fr_input, text=self._t("browse"), command=self._pick_input_dir).pack(side="left", padx=(8, 0))
        ttk.Button(fr_input, text=self._t("refresh"), command=self._refresh_and_draw).pack(side="left", padx=(8, 0))
        ttk.Button(fr_input, text=self._t("open_folder"), command=self._open_input_dir).pack(side="left", padx=(8, 0))

        row += 1
        mode_frame = ttk.LabelFrame(left, text=self._t("data_type"))
        mode_frame.grid(row=row, column=0, sticky="we", pady=(0, 10))
        for idx, (mode_key, label_key) in enumerate(DATA_MODE_OPTIONS):
            ttk.Radiobutton(mode_frame, text=self._t(label_key), variable=self.data_mode_var, value=mode_key, command=self._on_data_mode_changed).grid(row=0, column=idx, sticky="w", padx=(8 if idx == 0 else 0, 8), pady=4)

        row += 1
        self.file_label = ttk.Label(left, text=self._t("file"))
        self.file_label.grid(row=row, column=0, sticky="w")
        row += 1
        self.file_var = tk.StringVar(value=self.file_list[0] if self.file_list else "")
        self.file_combo = ttk.Combobox(left, textvariable=self.file_var, values=self.file_list, state="readonly", width=42)
        self.file_combo.grid(row=row, column=0, pady=(0, 10), sticky="we")
        self.file_combo.bind("<<ComboboxSelected>>", lambda _event: self._on_file_selected())

        row += 1
        self.dist_label = ttk.Label(left, text=self._t("distance_source"))
        self.dist_label.grid(row=row, column=0, sticky="w")
        row += 1
        self.dist_var = tk.StringVar(value="Distance/Distance 1")
        self.dist_combo = ttk.Combobox(
            left,
            textvariable=self.dist_var,
            values=list(DIST_CHOICES.keys()),
            state="readonly",
            width=42,
        )
        self.dist_combo.grid(row=row, column=0, pady=(0, 10), sticky="we")
        self.dist_combo.bind("<<ComboboxSelected>>", lambda _event: self._draw_current())

        row += 1
        overlay_body, row = self._add_collapsible_section(left, row, "fd_overlay", self._t("fd_overlay"), expanded=False)
        self.fd_overlay_enabled_var = tk.BooleanVar(value=False)
        self.fd_overlay_include_current_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(overlay_body, text=self._t("enable_fd_overlay"), variable=self.fd_overlay_enabled_var, command=self._draw_current).grid(row=0, column=0, sticky="w", padx=8, pady=(0, 4))
        ttk.Checkbutton(overlay_body, text=self._t("include_current_file"), variable=self.fd_overlay_include_current_var, command=self._draw_current).grid(row=1, column=0, sticky="w", padx=8, pady=(0, 6))
        ttk.Label(overlay_body, text=self._t("overlay_files")).grid(row=2, column=0, sticky="w", padx=8, pady=(0, 4))

        overlay_list_frame = ttk.Frame(overlay_body)
        overlay_list_frame.grid(row=3, column=0, sticky="we", padx=8, pady=(0, 6))
        overlay_list_frame.columnconfigure(0, weight=1)
        self.fd_overlay_listbox = tk.Listbox(overlay_list_frame, selectmode="extended", height=8, width=42, exportselection=False)
        self.fd_overlay_listbox.grid(row=0, column=0, sticky="we")
        overlay_scroll = ttk.Scrollbar(overlay_list_frame, orient="vertical", command=self.fd_overlay_listbox.yview)
        overlay_scroll.grid(row=0, column=1, sticky="ns")
        overlay_xscroll = ttk.Scrollbar(overlay_list_frame, orient="horizontal", command=self.fd_overlay_listbox.xview)
        overlay_xscroll.grid(row=1, column=0, sticky="we")
        self.fd_overlay_listbox.configure(yscrollcommand=overlay_scroll.set, xscrollcommand=overlay_xscroll.set)
        self.fd_overlay_listbox.bind("<<ListboxSelect>>", lambda _event: self._draw_current())

        overlay_btns = ttk.Frame(overlay_body)
        overlay_btns.grid(row=4, column=0, sticky="w", padx=8, pady=(0, 4))
        ttk.Button(overlay_btns, text=self._t("select_all"), command=self._select_all_fd_overlay_files).pack(side="left")
        ttk.Button(overlay_btns, text=self._t("clear"), command=self._clear_fd_overlay_files).pack(side="left", padx=(8, 0))
        self._refresh_fd_overlay_file_list(keep_selection=False)

        row += 1
        scan_body, row = self._add_collapsible_section(left, row, "scan_tools", self._t("scan_tools"), expanded=True)
        ttk.Label(scan_body, text=self._t("scan_placeholder"), wraplength=360, justify="left").grid(row=0, column=0, sticky="w", padx=8, pady=(0, 4))

        row += 1
        panel_body, row = self._add_collapsible_section(left, row, "panels", self._t("panels"), expanded=True)
        panel_body.columnconfigure(1, weight=1)
        panel_body.columnconfigure(2, weight=1)
        panel_toolbar = ttk.Frame(panel_body)
        panel_toolbar.grid(row=0, column=0, columnspan=4, sticky="we", pady=(0, 6))
        ttk.Button(panel_toolbar, text=self._t("apply_section_to_all"), command=self._apply_all_panels_to_all).pack(side="right")
        ttk.Label(panel_body, text=self._t("panel")).grid(row=1, column=0, sticky="w", padx=8, pady=(0, 4))
        ttk.Label(panel_body, text=self._t("show")).grid(row=1, column=1, sticky="w", padx=8, pady=(0, 4))
        ttk.Label(panel_body, text=self._t("eye")).grid(row=1, column=2, sticky="w", padx=8, pady=(0, 4))

        for panel_row, (panel_key, _panel_label, _weight) in enumerate(PANEL_SPECS, start=2):
            show_var = tk.BooleanVar(value=True)
            export_style_var = tk.BooleanVar(value=True)
            eye_text_var = tk.StringVar()
            self.panel_vars[panel_key] = {"show": show_var, "export_style": export_style_var}
            self.panel_eye_text_vars[panel_key] = eye_text_var
            self._update_panel_eye_button(panel_key)

            ttk.Label(panel_body, text=self._panel_label(panel_key)).grid(row=panel_row, column=0, sticky="w", padx=8, pady=(0, 4))
            ttk.Checkbutton(panel_body, variable=show_var, command=self._draw_current).grid(row=panel_row, column=1, sticky="w", padx=8, pady=(0, 4))
            ttk.Button(panel_body, textvariable=eye_text_var, width=4, command=lambda k=panel_key: self._toggle_panel_export_style(k)).grid(row=panel_row, column=2, sticky="w", padx=8, pady=(0, 4))
            ttk.Button(panel_body, text=self._t("apply_all"), command=lambda k=panel_key: self._apply_panel_field_to_all(k)).grid(row=panel_row, column=3, sticky="e", padx=(8, 8), pady=(0, 4))

        row += 1
        ranges_body, row = self._add_collapsible_section(left, row, "ranges", self._t("ranges"), expanded=False)
        ranges_toolbar = ttk.Frame(ranges_body)
        ranges_toolbar.grid(row=0, column=0, sticky="we", pady=(0, 8))
        ttk.Label(ranges_toolbar, text=self._t("blank_auto")).pack(side="left")
        ttk.Label(ranges_toolbar, text=self._t("range_drag_hint")).pack(side="left", padx=(10, 0))
        ttk.Button(ranges_toolbar, text=self._t("apply_section_to_all"), command=self._apply_all_ranges_to_all).pack(side="right")

        self.time_min = tk.StringVar(value="")
        self.time_max = tk.StringVar(value="")
        self.time_interval = tk.StringVar(value="")
        self.force_min = tk.StringVar(value="")
        self.force_max = tk.StringVar(value="")
        self.force_interval = tk.StringVar(value="")
        self.dist_min = tk.StringVar(value="")
        self.dist_max = tk.StringVar(value="")
        self.dist_interval = tk.StringVar(value="")
        self.img_y_min = tk.StringVar(value="")
        self.img_y_max = tk.StringVar(value="")
        self.img_y_interval = tk.StringVar(value="")

        self.range_vars = {
            "time_min": self.time_min,
            "time_max": self.time_max,
            "time_interval": self.time_interval,
            "force_min": self.force_min,
            "force_max": self.force_max,
            "force_interval": self.force_interval,
            "distance_min": self.dist_min,
            "distance_max": self.dist_max,
            "distance_interval": self.dist_interval,
            "image_y_min": self.img_y_min,
            "image_y_max": self.img_y_max,
            "image_y_interval": self.img_y_interval,
        }
        self.range_pairs = {
            "time": (self.time_min, self.time_max, self.time_interval),
            "force": (self.force_min, self.force_max, self.force_interval),
            "distance": (self.dist_min, self.dist_max, self.dist_interval),
            "image_y": (self.img_y_min, self.img_y_max, self.img_y_interval),
        }

        inner_row = 1
        inner_row = self._add_range_row(ranges_body, inner_row, self._t("time_range"), self.time_min, self.time_max, self.time_interval, lambda: self._apply_range_pair_to_all("time"))
        inner_row = self._add_range_row(ranges_body, inner_row, self._t("force_range"), self.force_min, self.force_max, self.force_interval, lambda: self._apply_range_pair_to_all("force"))
        inner_row = self._add_range_row(ranges_body, inner_row, self._t("distance_range"), self.dist_min, self.dist_max, self.dist_interval, lambda: self._apply_range_pair_to_all("distance"))
        self._add_range_row(ranges_body, inner_row, self._t("image_y_range"), self.img_y_min, self.img_y_max, self.img_y_interval, lambda: self._apply_range_pair_to_all("image_y"))


        rgb_body, row = self._add_collapsible_section(left, row, "rgb_image", self._t("rgb_image"), expanded=False)
        rgb_toolbar = ttk.Frame(rgb_body)
        rgb_toolbar.grid(row=0, column=0, sticky="we", pady=(0, 8))
        ttk.Button(rgb_toolbar, text=self._t("reset_rgb"), command=self._reset_rgb_for_current_file).pack(side="left")
        ttk.Button(rgb_toolbar, text=self._t("apply_section_to_all"), command=self._apply_all_rgb_to_all).pack(side="right")
        current_row = 1
        for color in RGB_CHANNELS:
            current_row = self._build_rgb_controls(rgb_body, current_row, color)

        style_body, row = self._add_collapsible_section(left, row, "style", self._t("style"), expanded=False)
        style_body.columnconfigure(1, weight=1)
        style_body.columnconfigure(3, weight=1)

        style_toolbar = ttk.Frame(style_body)
        style_toolbar.grid(row=0, column=0, columnspan=5, sticky="we", pady=(0, 8))
        ttk.Button(style_toolbar, text=self._t("apply_section_to_all"), command=self._apply_all_style_to_all).pack(side="right")

        self.font_family_var = tk.StringVar(value=STYLE_DEFAULTS["fontfamily"])
        self.font_bold_var = tk.BooleanVar(value=bool(STYLE_DEFAULTS["font_bold"]))
        self.tick_fontsize_var = tk.StringVar(value=STYLE_DEFAULTS["tick_fontsize"])
        self.label_fontsize_var = tk.StringVar(value=STYLE_DEFAULTS["label_fontsize"])
        self.title_fontsize_var = tk.StringVar(value=STYLE_DEFAULTS["title_fontsize"])
        self.spine_width_var = tk.StringVar(value=STYLE_DEFAULTS["spine_width"])
        self.tick_width_var = tk.StringVar(value=STYLE_DEFAULTS["tick_width"])
        self.curve_width_var = tk.StringVar(value=STYLE_DEFAULTS["curve_width"])
        self.force_color_var = tk.StringVar(value=STYLE_DEFAULTS["force_color"])
        self.distance_color_var = tk.StringVar(value=STYLE_DEFAULTS["distance_color"])
        self.fd_color_var = tk.StringVar(value=STYLE_DEFAULTS["fd_color"])
        self.photon_red_color_var = tk.StringVar(value=STYLE_DEFAULTS["photon_red_color"])
        self.photon_green_color_var = tk.StringVar(value=STYLE_DEFAULTS["photon_green_color"])
        self.photon_blue_color_var = tk.StringVar(value=STYLE_DEFAULTS["photon_blue_color"])

        self.style_vars = {
            "fontfamily": self.font_family_var,
            "font_bold": self.font_bold_var,
            "tick_fontsize": self.tick_fontsize_var,
            "label_fontsize": self.label_fontsize_var,
            "title_fontsize": self.title_fontsize_var,
            "spine_width": self.spine_width_var,
            "tick_width": self.tick_width_var,
            "curve_width": self.curve_width_var,
            "force_color": self.force_color_var,
            "distance_color": self.distance_color_var,
            "fd_color": self.fd_color_var,
            "photon_red_color": self.photon_red_color_var,
            "photon_green_color": self.photon_green_color_var,
            "photon_blue_color": self.photon_blue_color_var,
        }

        ttk.Label(style_body, text=self._t("font")).grid(row=1, column=0, sticky="w", padx=8, pady=(0, 4))
        font_combo = ttk.Combobox(style_body, textvariable=self.font_family_var, values=FONT_CHOICES, state="readonly", width=18)
        font_combo.grid(row=1, column=1, columnspan=3, sticky="we", padx=(0, 8), pady=(0, 4))
        font_combo.bind("<<ComboboxSelected>>", lambda _event: self._draw_current())
        ttk.Button(style_body, text=self._t("apply_all"), command=lambda: self._apply_style_field_to_all("fontfamily")).grid(row=1, column=4, padx=(0, 8), pady=(0, 4))

        self._add_style_toggle_row(style_body, 2, self._t("bold_text"), self.font_bold_var, "font_bold")
        self._add_style_entry_row(style_body, 3, self._t("tick_size"), self.tick_fontsize_var, "tick_fontsize")
        self._add_style_entry_row(style_body, 4, self._t("label_size"), self.label_fontsize_var, "label_fontsize")
        self._add_style_entry_row(style_body, 5, self._t("title_size"), self.title_fontsize_var, "title_fontsize")
        self._add_style_entry_row(style_body, 6, self._t("axis_width"), self.spine_width_var, "spine_width")
        self._add_style_entry_row(style_body, 7, self._t("tick_width"), self.tick_width_var, "tick_width")
        self._add_style_entry_row(style_body, 8, self._t("curve_width"), self.curve_width_var, "curve_width")
        self._add_style_color_row(style_body, 9, self._t("force_line"), self.force_color_var, "force_color", STYLE_DEFAULTS["force_color"])
        self._add_style_color_row(style_body, 10, self._t("distance_line"), self.distance_color_var, "distance_color", STYLE_DEFAULTS["distance_color"])
        self._add_style_color_row(style_body, 11, self._t("fd_line"), self.fd_color_var, "fd_color", STYLE_DEFAULTS["fd_color"])
        self._add_style_color_row(style_body, 12, self._t("photon_red"), self.photon_red_color_var, "photon_red_color", STYLE_DEFAULTS["photon_red_color"])
        self._add_style_color_row(style_body, 13, self._t("photon_green"), self.photon_green_color_var, "photon_green_color", STYLE_DEFAULTS["photon_green_color"])
        self._add_style_color_row(style_body, 14, self._t("photon_blue"), self.photon_blue_color_var, "photon_blue_color", STYLE_DEFAULTS["photon_blue_color"])

        plot_size_body, row = self._add_collapsible_section(left, row, "plot_size", self._t("plot_size"), expanded=False)
        self.plot_size_section = plot_size_body
        plot_size_body.columnconfigure(1, weight=1)
        plot_size_toolbar = ttk.Frame(plot_size_body)
        plot_size_toolbar.grid(row=0, column=0, columnspan=2, sticky="we", pady=(0, 8))
        ttk.Button(plot_size_toolbar, text=self._t("apply_section_to_all"), command=self._apply_plot_size_to_all).pack(side="right")
        ttk.Label(plot_size_body, text=self._t("plot_width")).grid(row=1, column=0, sticky="w", padx=8, pady=(0, 4))
        plot_width_entry = ttk.Entry(plot_size_body, textvariable=self.plot_width_var, width=10)
        plot_width_entry.grid(row=1, column=1, sticky="w", pady=(0, 4))
        ttk.Label(plot_size_body, text=self._t("plot_height")).grid(row=2, column=0, sticky="w", padx=8, pady=(0, 4))
        plot_height_entry = ttk.Entry(plot_size_body, textvariable=self.plot_height_var, width=10)
        plot_height_entry.grid(row=2, column=1, sticky="w", pady=(0, 4))
        ttk.Checkbutton(
            plot_size_body,
            text=self._t("lock_aspect_ratio"),
            variable=self.plot_aspect_lock_var,
            command=self._on_plot_aspect_toggle,
        ).grid(row=3, column=0, columnspan=2, sticky="w", padx=8, pady=(4, 0))
        self._bind_plot_size_entry(plot_width_entry, "width")
        self._bind_plot_size_entry(plot_height_entry, "height")

        self.save_label = ttk.Label(left, text=self._t("save_folder_png"))
        self.save_label.grid(row=row, column=0, sticky="w")
        row += 1
        self.save_dir_var = tk.StringVar(value="")
        fr_save = ttk.Frame(left)
        self.save_frame = fr_save
        fr_save.grid(row=row, column=0, sticky="we", pady=(0, 10))
        ttk.Entry(fr_save, textvariable=self.save_dir_var, width=38).pack(side="left")
        ttk.Button(fr_save, text=self._t("browse"), command=self._pick_save_dir).pack(side="left", padx=(8, 0))
        ttk.Button(fr_save, text=self._t("open_folder"), command=self._open_save_dir).pack(side="left", padx=(8, 0))

        row += 1
        btn_frame = ttk.Frame(left)
        self.button_frame = btn_frame
        btn_frame.grid(row=row, column=0, sticky="w")
        ttk.Button(btn_frame, text=self._t("draw_current"), command=self._draw_current).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(btn_frame, text=self._t("save_current_png"), command=self._save_current).grid(row=0, column=1)
        ttk.Button(btn_frame, text=self._t("save_all_png"), command=self._save_all).grid(row=1, column=0, columnspan=2, sticky="we", pady=(8, 0))
        ttk.Button(btn_frame, text=self._t("export_current_excel"), command=self._export_current_excel).grid(row=2, column=0, columnspan=2, sticky="we", pady=(8, 0))
        ttk.Button(btn_frame, text=self._t("export_all_excel"), command=self._export_all_excel).grid(row=3, column=0, columnspan=2, sticky="we", pady=(8, 0))

        row += 1
        self.status_var.set(self._t("select_input_folder_hint"))
        self.status_label = ttk.Label(left, textvariable=self.status_var, wraplength=360, justify="left")
        self.status_label.grid(row=row, column=0, sticky="we", pady=(8, 8))

        self.fig = Figure(figsize=self._get_preview_display_figure_size(), dpi=PREVIEW_DPI)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.preview_host)
        self.canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")
        self._update_preview_widget_geometry()
        self.canvas.mpl_connect("button_press_event", self._on_plot_button_press)
        self._update_mode_visibility()
        self.after_idle(self._on_left_panel_configure)

    def _on_left_panel_configure(self, _event=None):
        if hasattr(self, "left_canvas"):
            self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all"))

    def _on_left_canvas_configure(self, event):
        if hasattr(self, "left_canvas") and hasattr(self, "left_canvas_window"):
            self.left_canvas.itemconfigure(self.left_canvas_window, width=event.width)
            self._on_left_panel_configure()

    def _pointer_inside_left_canvas(self):
        if not hasattr(self, "left_canvas"):
            return False
        x_root = self.winfo_pointerx()
        y_root = self.winfo_pointery()
        left = self.left_canvas.winfo_rootx()
        top = self.left_canvas.winfo_rooty()
        right = left + self.left_canvas.winfo_width()
        bottom = top + self.left_canvas.winfo_height()
        return left <= x_root < right and top <= y_root < bottom

    def _on_left_mousewheel(self, event):
        if not self._pointer_inside_left_canvas():
            return

        if hasattr(event, "delta") and event.delta:
            steps = -int(event.delta / 120) if abs(event.delta) >= 120 else (-1 if event.delta > 0 else 1)
            self.left_canvas.yview_scroll(steps, "units")
        elif getattr(event, "num", None) == 4:
            self.left_canvas.yview_scroll(-1, "units")
        elif getattr(event, "num", None) == 5:
            self.left_canvas.yview_scroll(1, "units")

    def _add_collapsible_section(self, parent, row_idx, section_key, title, expanded=False):
        container = ttk.Frame(parent)
        container.grid(row=row_idx, column=0, sticky="we", pady=(0, 10))
        container.columnconfigure(0, weight=1)

        text_var = tk.StringVar()
        body = ttk.Frame(container)
        state = {"expanded": expanded, "container": container, "body": body}

        def refresh():
            prefix = "[-]" if state["expanded"] else "[+]"
            text_var.set(f"{prefix} {title}")
            if state["expanded"]:
                body.pack(fill="x", padx=8, pady=(6, 0))
            else:
                body.pack_forget()
            self.after_idle(self._on_left_panel_configure)
        state["refresh"] = refresh

        def toggle():
            state["expanded"] = not state["expanded"]
            refresh()

        ttk.Button(container, textvariable=text_var, command=toggle).pack(fill="x")
        refresh()
        self._section_vars[section_key] = state
        return body, row_idx + 1

    def _add_range_row(self, parent, row_idx, label, vmin_var, vmax_var, interval_var, apply_command):
        ttk.Label(parent, text=label).grid(row=row_idx, column=0, sticky="w")
        frame = ttk.Frame(parent)
        frame.grid(row=row_idx + 1, column=0, sticky="w", pady=(2, 10))
        entry_min = ttk.Entry(frame, textvariable=vmin_var, width=10)
        entry_min.pack(side="left")
        ttk.Label(frame, text=self._t("to")).pack(side="left", padx=5)
        entry_max = ttk.Entry(frame, textvariable=vmax_var, width=10)
        entry_max.pack(side="left")
        ttk.Label(frame, text=self._t("step")).pack(side="left", padx=(8, 5))
        entry_interval = ttk.Entry(frame, textvariable=interval_var, width=8)
        entry_interval.pack(side="left")
        ttk.Button(frame, text=self._t("apply_all"), command=apply_command).pack(side="left", padx=(8, 0))
        self._bind_redraw_entry(entry_min)
        self._bind_redraw_entry(entry_max)
        self._bind_redraw_entry(entry_interval)
        return row_idx + 2

    def _add_style_entry_row(self, parent, row_idx, label, var, key):
        ttk.Label(parent, text=label).grid(row=row_idx, column=0, sticky="w", padx=8, pady=(0, 4))
        entry = ttk.Entry(parent, textvariable=var, width=12)
        entry.grid(row=row_idx, column=1, sticky="w", padx=(0, 8), pady=(0, 4))
        ttk.Button(parent, text=self._t("apply_all"), command=lambda k=key: self._apply_style_field_to_all(k)).grid(row=row_idx, column=4, padx=(0, 8), pady=(0, 4))
        self._bind_redraw_entry(entry)

    def _add_style_toggle_row(self, parent, row_idx, label, var, key):
        ttk.Label(parent, text=label).grid(row=row_idx, column=0, sticky="w", padx=8, pady=(0, 4))
        ttk.Checkbutton(parent, variable=var, command=self._draw_current).grid(row=row_idx, column=1, sticky="w", padx=(0, 8), pady=(0, 4))
        ttk.Button(parent, text=self._t("apply_all"), command=lambda k=key: self._apply_style_field_to_all(k)).grid(row=row_idx, column=4, padx=(0, 8), pady=(0, 4))

    def _add_style_color_row(self, parent, row_idx, label, var, key, fallback_color):
        ttk.Label(parent, text=label).grid(row=row_idx, column=0, sticky="w", padx=8, pady=(0, 4))
        entry = ttk.Entry(parent, textvariable=var, width=12)
        entry.grid(row=row_idx, column=1, sticky="w", padx=(0, 8), pady=(0, 4))
        ttk.Button(parent, text=self._t("pick"), command=lambda k=key: self._pick_style_color(k)).grid(row=row_idx, column=2, sticky="w", padx=(0, 8), pady=(0, 4))
        preview = tk.Label(parent, width=3, relief="solid", bd=1, bg=normalize_hex_color(var.get(), fallback_color))
        preview.grid(row=row_idx, column=3, sticky="w", pady=(0, 4))
        ttk.Button(parent, text=self._t("apply_all"), command=lambda k=key: self._apply_style_field_to_all(k)).grid(row=row_idx, column=4, padx=(0, 8), pady=(0, 4))
        self.style_color_previews[key] = preview
        var.trace_add("write", lambda *_args, k=key, fb=fallback_color: self._update_style_color_preview(k, fb))
        self._update_style_color_preview(key, fallback_color)
        self._bind_redraw_entry(entry)

    def _pick_style_color(self, key):
        initial = normalize_hex_color(self.style_vars[key].get(), STYLE_DEFAULTS[key])
        _rgb, color_text = colorchooser.askcolor(color=initial, title=f"Choose {STYLE_COLOR_LABELS[key]}")
        if color_text:
            self.style_vars[key].set(color_text.upper())
            self._draw_current()

    def _update_style_color_preview(self, key, fallback_color=None):
        preview = self.style_color_previews.get(key)
        if preview is None:
            return
        if fallback_color is None:
            fallback_color = STYLE_DEFAULTS[key]
        color_text = normalize_hex_color(self.style_vars[key].get(), fallback_color)
        preview.configure(bg=color_text)

    def _build_rgb_controls(self, parent, row_idx, color):
        section = ttk.LabelFrame(parent, text=self._t(f"{color}_channel"))
        section.grid(row=row_idx, column=0, sticky="we", padx=8, pady=(0, 8))

        enabled_var = tk.BooleanVar(value=DEFAULT_ENABLED[color])
        min_var = tk.StringVar(value="0")
        max_var = tk.StringVar(value="1")
        gamma_var = tk.DoubleVar(value=1.0)
        gamma_label_var = tk.StringVar(value="1.00")
        pseudocolor_var = tk.StringVar(value=DEFAULT_PSEUDOCOLORS[color])

        self.rgb_vars[color] = {
            "enabled": enabled_var,
            "min": min_var,
            "max": max_var,
            "gamma": gamma_var,
            "gamma_label": gamma_label_var,
            "pseudocolor": pseudocolor_var,
        }

        toolbar = ttk.Frame(section)
        toolbar.grid(row=0, column=0, columnspan=5, sticky="we", padx=8, pady=(4, 4))
        ttk.Button(toolbar, text=self._t("apply_channel_to_all"), command=lambda c=color: self._apply_rgb_channel_to_all(c)).pack(side="right")

        ttk.Checkbutton(section, text=self._t("show"), variable=enabled_var, command=self._draw_current).grid(row=1, column=0, sticky="w", padx=8, pady=(0, 4))
        ttk.Button(section, text=self._t("apply_all"), command=lambda c=color: self._apply_rgb_detail_to_all(c, ("enabled",))).grid(row=1, column=4, sticky="e", padx=(0, 8), pady=(0, 4))

        ttk.Label(section, text=self._t("min")).grid(row=2, column=0, sticky="w", padx=8)
        min_entry = ttk.Entry(section, textvariable=min_var, width=10)
        min_entry.grid(row=2, column=1, sticky="w", padx=(0, 8))
        ttk.Label(section, text=self._t("max")).grid(row=2, column=2, sticky="w")
        max_entry = ttk.Entry(section, textvariable=max_var, width=10)
        max_entry.grid(row=2, column=3, sticky="w", padx=(0, 8))
        ttk.Button(section, text=self._t("apply_all"), command=lambda c=color: self._apply_rgb_detail_to_all(c, ("min", "max"))).grid(row=2, column=4, sticky="e", padx=(0, 8))

        ttk.Label(section, text=self._t("gamma")).grid(row=3, column=0, sticky="w", padx=8, pady=(2, 6))
        gamma_scale = ttk.Scale(section, from_=0.2, to=3.0, variable=gamma_var, orient="horizontal", command=self._on_gamma_changed)
        gamma_scale.grid(row=3, column=1, columnspan=2, sticky="we", padx=(0, 8), pady=(2, 6))
        ttk.Label(section, textvariable=gamma_label_var, width=6).grid(row=3, column=3, sticky="w", pady=(2, 6))
        ttk.Button(section, text=self._t("apply_all"), command=lambda c=color: self._apply_rgb_detail_to_all(c, ("gamma",))).grid(row=3, column=4, sticky="e", padx=(0, 8), pady=(2, 6))

        ttk.Label(section, text=self._t("color")).grid(row=4, column=0, sticky="w", padx=8, pady=(0, 6))
        color_entry = ttk.Entry(section, textvariable=pseudocolor_var, width=10)
        color_entry.grid(row=4, column=1, sticky="w", padx=(0, 8), pady=(0, 6))
        ttk.Button(section, text=self._t("pick"), command=lambda c=color: self._pick_rgb_pseudocolor(c)).grid(row=4, column=2, sticky="w", padx=(0, 8), pady=(0, 6))
        color_preview = tk.Label(section, width=3, relief="solid", bd=1, bg=DEFAULT_PSEUDOCOLORS[color])
        color_preview.grid(row=4, column=3, sticky="w", pady=(0, 6))
        ttk.Button(section, text=self._t("apply_all"), command=lambda c=color: self._apply_rgb_detail_to_all(c, ("pseudocolor",))).grid(row=4, column=4, sticky="e", padx=(0, 8), pady=(0, 6))
        self.rgb_vars[color]["color_preview"] = color_preview
        section.columnconfigure(1, weight=1)
        section.columnconfigure(2, weight=1)

        gamma_var.trace_add("write", lambda *_args, c=color: self._update_gamma_label(c))
        pseudocolor_var.trace_add("write", lambda *_args, c=color: self._update_rgb_color_preview(c))
        self._update_gamma_label(color)
        self._update_rgb_color_preview(color)
        self._bind_redraw_entry(min_entry)
        self._bind_redraw_entry(max_entry)
        self._bind_redraw_entry(color_entry)
        return row_idx + 1

    def _bind_redraw_entry(self, widget):
        widget.bind("<Return>", lambda _event: self._draw_current())
        widget.bind("<FocusOut>", lambda _event: self._draw_current())

    def _bind_plot_size_entry(self, widget, dimension):
        widget.bind("<Return>", lambda _event, dim=dimension: self._on_plot_size_changed(dim))
        widget.bind("<FocusOut>", lambda _event, dim=dimension: self._on_plot_size_changed(dim))

    def _format_plot_size_value(self, value):
        text = f"{float(value):.3f}".rstrip("0").rstrip(".")
        return text or "0"

    def _update_plot_aspect_ratio_from_vars(self):
        width = parse_optional_float(self.plot_width_var.get())
        height = parse_optional_float(self.plot_height_var.get())
        if width is None or height is None or width <= 0 or height <= 0:
            return
        self._plot_aspect_ratio = float(width) / float(height)

    def _apply_plot_aspect_ratio(self, changed_dimension):
        if self._plot_size_syncing or not bool(self.plot_aspect_lock_var.get()):
            self._update_plot_aspect_ratio_from_vars()
            return

        width = parse_optional_float(self.plot_width_var.get())
        height = parse_optional_float(self.plot_height_var.get())
        ratio = self._plot_aspect_ratio if self._plot_aspect_ratio > 0 else (11.0 / 8.0)

        if changed_dimension == "width" and width is not None and width > 0:
            new_height = width / ratio
            self._plot_size_syncing = True
            try:
                self.plot_height_var.set(self._format_plot_size_value(new_height))
            finally:
                self._plot_size_syncing = False
            height = new_height
        elif changed_dimension == "height" and height is not None and height > 0:
            new_width = height * ratio
            self._plot_size_syncing = True
            try:
                self.plot_width_var.set(self._format_plot_size_value(new_width))
            finally:
                self._plot_size_syncing = False
            width = new_width

        if width is not None and height is not None and width > 0 and height > 0:
            self._plot_aspect_ratio = float(width) / float(height)

    def _on_plot_size_changed(self, changed_dimension):
        self._apply_plot_aspect_ratio(changed_dimension)
        if not self._suspend_redraw:
            self._draw_current()

    def _on_plot_aspect_toggle(self):
        if bool(self.plot_aspect_lock_var.get()):
            self._update_plot_aspect_ratio_from_vars()
        if not self._suspend_redraw:
            self._draw_current()

    def _update_gamma_label(self, color):
        value = self.rgb_vars[color]["gamma"].get()
        self.rgb_vars[color]["gamma_label"].set(f"{value:.2f}")

    def _update_rgb_color_preview(self, color):
        preview = self.rgb_vars[color].get("color_preview")
        if preview is None:
            return
        color_text = normalize_hex_color(self.rgb_vars[color]["pseudocolor"].get(), DEFAULT_PSEUDOCOLORS[color])
        preview.configure(bg=color_text)

    def _on_gamma_changed(self, _value):
        if not self._suspend_redraw:
            self._draw_current()

    def _pick_rgb_pseudocolor(self, color):
        initial = normalize_hex_color(self.rgb_vars[color]["pseudocolor"].get(), DEFAULT_PSEUDOCOLORS[color])
        _rgb, color_text = colorchooser.askcolor(color=initial, title=f"Choose {CHANNEL_LABELS[color]} pseudocolor")
        if color_text:
            self.rgb_vars[color]["pseudocolor"].set(color_text.upper())
            self._draw_current()

    def _capture_var_value(self, var):
        if isinstance(var, tk.BooleanVar):
            return bool(var.get())
        return str(var.get())

    def _set_status(self, text):
        self.status_var.set(str(text))
        self.update_idletasks()

    def _get_current_mode(self):
        mode = self.data_mode_var.get() if self.data_mode_var is not None else "kymograph"
        return mode if mode in DATA_MODE_LABEL_KEYS else "kymograph"

    def _set_widget_visible(self, widget, visible):
        if widget is None:
            return
        if visible:
            widget.grid()
        else:
            widget.grid_remove()

    def _set_section_visible(self, section_key, visible):
        section_state = self._section_vars.get(section_key)
        if not section_state:
            return
        self._set_widget_visible(section_state.get("container"), visible)

    def _update_file_label(self):
        if self.file_label is None:
            return
        mode_key = self._get_current_mode()
        self.file_label.configure(text=f"{self._t('file')} ({self._t(DATA_MODE_LABEL_KEYS[mode_key])})")

    def _update_mode_visibility(self):
        mode_key = self._get_current_mode()
        show_kymo = mode_key == "kymograph"
        show_fd = mode_key == "fd_curve"
        show_scan = mode_key == "scan"

        self._update_file_label()
        self._set_widget_visible(self.dist_label, show_kymo)
        self._set_widget_visible(self.dist_combo, show_kymo)
        self._set_section_visible("fd_overlay", show_fd)
        self._set_section_visible("scan_tools", show_scan)
        for section_key in ("panels", "ranges", "rgb_image", "style"):
            self._set_section_visible(section_key, show_kymo)
        self._set_section_visible("plot_size", True)
        self._set_widget_visible(self.save_label, True)
        self._set_widget_visible(self.save_frame, True)
        self._set_widget_visible(self.button_frame, True)
        self.after_idle(self._on_left_panel_configure)

    def _on_data_mode_changed(self):
        if hasattr(self, "file_var"):
            self.mode_file_selection[self.current_mode_key] = self.file_var.get().strip()
        self.current_mode_key = self._get_current_mode()
        self._refresh_file_list(keep_selection=True)
        self._update_mode_visibility()
        self._draw_current()

    def _get_preview_figure_size(self):
        return PREVIEW_CANVAS_SIZE

    def _get_preview_canvas_pixel_size(self):
        width, height = self._get_preview_figure_size()
        return max(int(round(width * PREVIEW_DPI)), 1), max(int(round(height * PREVIEW_DPI)), 1)

    def _get_preview_display_figure_size(self):
        width, height = self._get_plot_figure_size()
        max_width, max_height = self._get_preview_figure_size()
        scale = min(max_width / width, max_height / height, 1.0)
        return max(width * scale, 1.0), max(height * scale, 1.0)

    def _get_preview_display_pixel_size(self):
        width, height = self._get_preview_display_figure_size()
        return max(int(round(width * PREVIEW_DPI)), 1), max(int(round(height * PREVIEW_DPI)), 1)

    def _get_plot_figure_size(self):
        width = parse_optional_float(self.plot_width_var.get()) or 11.0
        height = parse_optional_float(self.plot_height_var.get()) or 8.0
        return max(float(width), 4.0), max(float(height), 3.0)

    def _get_kymograph_image_aspect(self, kymo_data):
        if not kymo_data:
            return "auto"
        rows, cols = np.asarray(kymo_data["red"]).shape
        if rows <= 0 or cols <= 0:
            return "auto"
        x_span = abs(float(kymo_data["x1"]) - float(kymo_data["x0"]))
        y_span = abs(float(kymo_data["y1"]) - float(kymo_data["y0"]))
        if x_span <= 0 or y_span <= 0:
            return "auto"
        return max((y_span * cols) / (x_span * rows), 1e-6)

    def _get_kymograph_display_aspect(self, kymo_data, fill_panel=False):
        if fill_panel:
            return "auto"
        return self._get_kymograph_image_aspect(kymo_data)

    def _apply_current_figure_size(self):
        if not hasattr(self, "fig"):
            return
        width, height = self._get_preview_display_figure_size()
        self.fig.set_size_inches(width, height, forward=False)
        self._update_preview_widget_geometry()

    def _update_preview_widget_geometry(self):
        if not hasattr(self, "canvas"):
            return
        width_px, height_px = self._get_preview_display_pixel_size()
        self.canvas.get_tk_widget().place_configure(width=width_px, height=height_px)

    def _build_message_figure(self, title, message):
        fig = Figure(figsize=self._get_plot_figure_size(), dpi=120)
        ax = fig.add_subplot(111)
        ax.axis("off")
        if title:
            ax.set_title(str(title))
        ax.text(0.5, 0.5, str(message), ha="center", va="center", transform=ax.transAxes)
        fig.subplots_adjust(top=0.92, bottom=0.08, left=0.08, right=0.98)
        return fig

    def _render_placeholder(self, message, title=None):
        self._apply_current_figure_size()
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis("off")
        if title:
            ax.set_title(str(title))
        ax.text(0.5, 0.5, str(message), ha="center", va="center", transform=ax.transAxes)
        self.fig.subplots_adjust(top=0.92, bottom=0.08, left=0.08, right=0.98)
        self._range_selectors = []
        self.canvas.draw_idle()

    def _ensure_kymograph_mode(self, action_title):
        if self._get_current_mode() == "kymograph":
            return True
        messagebox.showinfo(action_title, self._t("kymograph_only_action"))
        return False

    def _get_fd_overlay_selected_files(self):
        if self.fd_overlay_listbox is None:
            return []
        return [self.fd_overlay_listbox.get(idx) for idx in self.fd_overlay_listbox.curselection()]

    def _refresh_fd_overlay_file_list(self, keep_selection=True, selected_files=None):
        if self.fd_overlay_listbox is None:
            return
        if selected_files is None and keep_selection:
            selected_files = self._get_fd_overlay_selected_files()
        selected = set(selected_files or [])
        source_files = list(self.file_groups.get("fd_curve", [])) if hasattr(self, "file_groups") else []
        self.fd_overlay_listbox.delete(0, tk.END)
        for filename in source_files:
            self.fd_overlay_listbox.insert(tk.END, filename)
        for idx, filename in enumerate(source_files):
            if filename in selected:
                self.fd_overlay_listbox.selection_set(idx)

    def _select_all_fd_overlay_files(self):
        if self.fd_overlay_listbox is None:
            return
        self.fd_overlay_listbox.selection_set(0, tk.END)
        self._draw_current()

    def _clear_fd_overlay_files(self):
        if self.fd_overlay_listbox is None:
            return
        self.fd_overlay_listbox.selection_clear(0, tk.END)
        self._draw_current()

    def _get_data_for_filename(self, filename):
        filename = (filename or "").strip()
        if not filename:
            raise FileNotFoundError("No H5 file selected.")
        h5_path = os.path.join(self._get_input_dir(), filename)
        dist_ds = DIST_CHOICES[self.dist_var.get()]
        cache_key = (h5_path, dist_ds)
        if cache_key not in self.data_cache:
            self.data_cache[cache_key] = load_plot_data(h5_path, FORCE_DS, dist_ds)
        return self.data_cache[cache_key]

    def _get_fd_overlay_file_order(self):
        current_file = (self.file_var.get() or "").strip()
        selected_files = self._get_fd_overlay_selected_files()
        if not bool(self.fd_overlay_enabled_var.get() if self.fd_overlay_enabled_var else False):
            return [current_file] if current_file else []

        ordered_files = []
        if bool(self.fd_overlay_include_current_var.get() if self.fd_overlay_include_current_var else True) and current_file:
            ordered_files.append(current_file)
        for filename in selected_files:
            if filename and filename not in ordered_files:
                ordered_files.append(filename)
        if not ordered_files and current_file:
            ordered_files.append(current_file)
        return ordered_files

    def _get_fd_overlay_curves(self, current_data):
        current_file = (self.file_var.get() or "").strip()
        curves = []
        errors = []
        for filename in self._get_fd_overlay_file_order():
            try:
                data = current_data if filename == current_file else self._get_data_for_filename(filename)
                curves.append({
                    "label": filename.replace(".h5", ""),
                    "distance": np.asarray(data["dist1"], dtype=np.float64),
                    "force": np.asarray(data["force"], dtype=np.float64),
                    "is_current": filename == current_file,
                })
            except Exception as exc:
                errors.append(f"{filename}: {exc}")

        if errors:
            self._set_status("FD overlay skipped some files: " + " | ".join(errors[:2]))
        return curves

    def _build_fd_overlay_sheet_data(self, selected_fn, data):
        curves = self._get_fd_overlay_curves(data)
        if not curves:
            curves = [{
                "label": selected_fn.replace(".h5", ""),
                "distance": np.asarray(data["dist1"], dtype=np.float64),
                "force": np.asarray(data["force"], dtype=np.float64),
                "is_current": True,
            }]
        columns = {}
        for curve in curves:
            safe_label = curve["label"].replace(" ", "_")
            columns[f"{safe_label}_distance_um"] = pd.Series(np.asarray(curve["distance"], dtype=np.float64))
            columns[f"{safe_label}_force2x_pN"] = pd.Series(np.asarray(curve["force"], dtype=np.float64))
        return {"FD_Overlay": pd.DataFrame(columns)}

    def _build_scan_summary_sheet(self, filenames):
        return {"Scan_Summary": pd.DataFrame({"file": list(filenames), "note": [self._t("scan_excel_placeholder")] * len(list(filenames))})}

    def _save_current_fd_curve(self):
        save_dir = self._resolve_save_dir(default_to_base=False)
        if not save_dir:
            return
        selected_fn = self.file_var.get().strip()
        try:
            idx = self.file_list.index(selected_fn) + 1
        except ValueError:
            idx = 0
        out_name = f"{idx:02d}_{selected_fn.replace('.h5', '')}_fd_curve_overlay.png"
        out_path = os.path.join(save_dir, out_name)
        data = self._get_current_data()
        fig = self._build_export_figure(["fd"], data, selected_fn, panel_export_style_override={"fd": True})
        fig.savefig(out_path)
        self._set_status(f"Saved PNG: {out_path}")
    def _save_all_fd_curve(self):
        save_dir = self._resolve_save_dir(default_to_base=True)
        if not save_dir:
            return
        files = list(self.file_list)
        if not files:
            messagebox.showwarning("Save all", "No H5 files available in the current input folder.")
            return
        selected_before = self.file_var.get().strip()
        saved = 0
        errors = []
        for idx, filename in enumerate(files, start=1):
            try:
                self.file_var.set(filename)
                data = self._get_current_data()
                fig = self._build_export_figure(["fd"], data, filename, panel_export_style_override={"fd": True})
                out_name = f"{idx:02d}_{filename.replace('.h5', '')}_fd_curve_overlay.png"
                fig.savefig(os.path.join(save_dir, out_name))
                saved += 1
            except Exception as exc:
                errors.append((filename, str(exc)))
        if selected_before:
            self.file_var.set(selected_before)
            self._draw_current()
        if errors:
            first_name, first_err = errors[0]
            self._set_status(f"Saved {saved} FD PNG(s) to {save_dir}. Errors: {len(errors)} (first: {first_name}: {first_err})")
        else:
            self._set_status(f"Saved {saved} FD PNG(s) to {save_dir}")

    def _save_current_scan_png(self):
        save_dir = self._resolve_save_dir(default_to_base=False)
        if not save_dir:
            return
        selected_fn = self.file_var.get().strip()
        out_name = f"{selected_fn.replace('.h5', '')}_scan_view.png"
        out_path = os.path.join(save_dir, out_name)
        fig = self._build_message_figure(selected_fn, self._t("scan_placeholder"))
        fig.savefig(out_path)
        self._set_status(f"Saved PNG: {out_path}")
    def _save_all_scan_png(self):
        save_dir = self._resolve_save_dir(default_to_base=True)
        if not save_dir:
            return
        files = list(self.file_list)
        if not files:
            messagebox.showwarning("Save all", "No H5 files available in the current input folder.")
            return
        saved = 0
        for idx, filename in enumerate(files, start=1):
            fig = self._build_message_figure(filename, self._t("scan_placeholder"))
            out_name = f"{idx:02d}_{filename.replace('.h5', '')}_scan_view.png"
            fig.savefig(os.path.join(save_dir, out_name))
            saved += 1
        self._set_status(f"Saved {saved} Scan PNG(s) to {save_dir}")

    def _apply_range_pair_to_all(self, prefix):
        min_var, max_var, interval_var = self.range_pairs[prefix]
        self.global_range_defaults[f"{prefix}_min"] = str(min_var.get())
        self.global_range_defaults[f"{prefix}_max"] = str(max_var.get())
        self.global_range_defaults[f"{prefix}_interval"] = str(interval_var.get())

    def _apply_all_ranges_to_all(self):
        for prefix in self.range_pairs:
            self._apply_range_pair_to_all(prefix)

    def _reset_range_controls(self):
        for key, var in self.range_vars.items():
            var.set(self.global_range_defaults[key])

    def _apply_style_field_to_all(self, key):
        self.global_style_defaults[key] = self._capture_var_value(self.style_vars[key])

    def _apply_all_style_to_all(self):
        for key in self.style_vars:
            self._apply_style_field_to_all(key)

    def _reset_style_controls(self):
        for key, var in self.style_vars.items():
            var.set(self.global_style_defaults[key])

    def _apply_rgb_detail_to_all(self, color, fields):
        for field in fields:
            if field == "enabled":
                self.global_rgb_defaults[color][field] = bool(self.rgb_vars[color][field].get())
            elif field == "gamma":
                self.global_rgb_defaults[color][field] = float(self.rgb_vars[color][field].get())
            elif field == "pseudocolor":
                self.global_rgb_defaults[color][field] = normalize_hex_color(self.rgb_vars[color][field].get(), DEFAULT_PSEUDOCOLORS[color])
            else:
                self.global_rgb_defaults[color][field] = str(self.rgb_vars[color][field].get())

    def _apply_rgb_channel_to_all(self, color):
        self._apply_rgb_detail_to_all(color, ("enabled", "min", "max", "gamma", "pseudocolor"))

    def _apply_all_rgb_to_all(self):
        for color in RGB_CHANNELS:
            self._apply_rgb_channel_to_all(color)

    def _get_rgb_file_defaults(self, data, color):
        if not data or not data.get("kymo"):
            return {"enabled": False, "min": "0", "max": "1.00", "gamma": 1.0, "pseudocolor": DEFAULT_PSEUDOCOLORS[color]}

        channel = np.asarray(data["kymo"][color], dtype=np.float64)
        vmax = float(np.max(channel)) if channel.size else 1.0
        return {
            "enabled": bool(DEFAULT_ENABLED[color] and vmax > 0),
            "min": "0",
            "max": format_number(max(vmax, 1.0), digits=2),
            "gamma": 1.0,
            "pseudocolor": DEFAULT_PSEUDOCOLORS[color],
        }

    def _reset_rgb_controls_from_data(self, data):
        for color in RGB_CHANNELS:
            defaults = self._get_rgb_file_defaults(data, color)
            overrides = self.global_rgb_defaults[color]

            enabled_value = defaults["enabled"] if overrides["enabled"] is None else overrides["enabled"]
            min_value = defaults["min"] if overrides["min"] is None else overrides["min"]
            max_value = defaults["max"] if overrides["max"] is None else overrides["max"]
            gamma_value = defaults["gamma"] if overrides["gamma"] is None else overrides["gamma"]
            pseudocolor_value = defaults["pseudocolor"] if overrides["pseudocolor"] is None else overrides["pseudocolor"]

            self.rgb_vars[color]["enabled"].set(bool(enabled_value))
            self.rgb_vars[color]["min"].set(str(min_value))
            self.rgb_vars[color]["max"].set(str(max_value))
            self.rgb_vars[color]["gamma"].set(float(gamma_value))
            self.rgb_vars[color]["pseudocolor"].set(str(pseudocolor_value))
            self._update_gamma_label(color)
            self._update_rgb_color_preview(color)

    def _toggle_panel_export_style(self, panel_key):
        current = bool(self.panel_vars[panel_key]["export_style"].get())
        self.panel_vars[panel_key]["export_style"].set(not current)
        self._update_panel_eye_button(panel_key)
        self._draw_current()

    def _update_panel_eye_button(self, panel_key):
        if panel_key not in self.panel_eye_text_vars:
            return
        is_open = bool(self.panel_vars[panel_key]["export_style"].get())
        self.panel_eye_text_vars[panel_key].set(PANEL_EYE_OPEN if is_open else PANEL_EYE_CLOSED)

    def _apply_panel_field_to_all(self, panel_key):
        self.global_panel_defaults[panel_key]["show"] = bool(self.panel_vars[panel_key]["show"].get())
        self.global_panel_defaults[panel_key]["export_style"] = bool(self.panel_vars[panel_key]["export_style"].get())

    def _apply_all_panels_to_all(self):
        for panel_key, _panel_label, _weight in PANEL_SPECS:
            self._apply_panel_field_to_all(panel_key)

    def _reset_panel_controls(self):
        for panel_key, _panel_label, _weight in PANEL_SPECS:
            defaults = self.global_panel_defaults[panel_key]
            self.panel_vars[panel_key]["show"].set(bool(defaults["show"]))
            self.panel_vars[panel_key]["export_style"].set(bool(defaults.get("export_style", True)))
            self._update_panel_eye_button(panel_key)

    def _apply_plot_size_to_all(self):
        self.global_plot_size_defaults["width"] = str(self.plot_width_var.get())
        self.global_plot_size_defaults["height"] = str(self.plot_height_var.get())
        self.global_plot_size_defaults["lock_aspect"] = bool(self.plot_aspect_lock_var.get())
        self._update_plot_aspect_ratio_from_vars()

    def _reset_plot_size_controls(self):
        self._plot_size_syncing = True
        try:
            self.plot_width_var.set(str(self.global_plot_size_defaults["width"]))
            self.plot_height_var.set(str(self.global_plot_size_defaults["height"]))
            self.plot_aspect_lock_var.set(bool(self.global_plot_size_defaults.get("lock_aspect", True)))
        finally:
            self._plot_size_syncing = False
        self._update_plot_aspect_ratio_from_vars()

    def _reset_controls_for_selected_file(self):
        self._suspend_redraw = True
        try:
            self._reset_plot_size_controls()
            self._reset_panel_controls()
            self._reset_range_controls()
            self._reset_style_controls()
            data = None
            try:
                data = self._get_current_data()
            except Exception:
                data = None
            self._reset_rgb_controls_from_data(data)
        finally:
            self._suspend_redraw = False

    def _get_input_dir(self):
        return (self.input_dir_var.get() or "").strip()

    def _pick_input_dir(self):
        chosen = filedialog.askdirectory(
            initialdir=self._get_dialog_dir(self._get_input_dir(), self.save_dir_var.get()),
            title="Select input folder",
        )
        if chosen:
            self.input_dir_var.set(chosen)
            if not (self.save_dir_var.get() or "").strip():
                self.save_dir_var.set(chosen)
            self._refresh_and_draw()

    def _open_input_dir(self):
        input_dir = self._get_input_dir()
        if not input_dir:
            messagebox.showwarning("Open folder", self._t("input_folder_not_set"))
            return
        if not os.path.isdir(input_dir):
            messagebox.showwarning("Open folder", self._t("folder_not_found"))
            return
        try:
            os.startfile(input_dir)
        except Exception as exc:
            messagebox.showerror("Open folder", str(exc))

    def _pick_save_dir(self):
        chosen = filedialog.askdirectory(
            initialdir=self._get_dialog_dir(self.save_dir_var.get(), self._get_input_dir()),
            title="Select save folder",
        )
        if chosen:
            self.save_dir_var.set(chosen)

    def _open_save_dir(self):
        save_dir = (self.save_dir_var.get() or "").strip() or self._get_input_dir()
        if not save_dir:
            messagebox.showwarning("Open folder", self._t("input_folder_not_set"))
            return
        try:
            os.makedirs(save_dir, exist_ok=True)
            os.startfile(save_dir)
        except Exception as exc:
            messagebox.showerror("Open folder", str(exc))

    def _refresh_file_list(self, keep_selection=True):
        current = self.file_var.get().strip() if hasattr(self, "file_var") else ""
        files = list_h5_files(self._get_input_dir())

        self.all_files = files
        self.file_groups = group_files_by_type(files)
        mode_key = self._get_current_mode()
        mode_files = list(self.file_groups.get(mode_key, []))

        self.file_list = mode_files
        self.file_combo["values"] = mode_files
        self._refresh_fd_overlay_file_list(keep_selection=keep_selection)
        self._update_file_label()

        preferred = current
        if keep_selection and current:
            self.mode_file_selection[self.current_mode_key] = current
        if preferred not in mode_files:
            preferred = self.mode_file_selection.get(mode_key, "")

        if preferred in mode_files:
            self.file_var.set(preferred)
        elif mode_files:
            self.file_var.set(mode_files[0])
        else:
            self.file_var.set("")

    def _refresh_and_draw(self):
        self._refresh_file_list(keep_selection=True)
        self._reset_controls_for_selected_file()
        self._draw_current()

    def _on_file_selected(self):
        self._reset_controls_for_selected_file()
        self._draw_current()

    def _get_current_path(self):
        filename = self.file_var.get().strip()
        if not filename:
            raise FileNotFoundError("No H5 file selected.")
        return os.path.join(self._get_input_dir(), filename)

    def _get_current_data(self):
        filename = self.file_var.get().strip()
        return self._get_data_for_filename(filename)

    def _reset_rgb_for_current_file(self):
        try:
            data = self._get_current_data()
            self._suspend_redraw = True
            self._reset_rgb_controls_from_data(data)
        except Exception as exc:
            messagebox.showerror("RGB", str(exc))
        finally:
            self._suspend_redraw = False
        self._draw_current()

    def _get_rgb_settings(self, data):
        kymo = data.get("kymo")
        if not kymo:
            return None

        settings = {}
        for color in RGB_CHANNELS:
            channel = np.asarray(kymo[color], dtype=np.float64)
            channel_max = float(np.max(channel)) if channel.size else 1.0
            fallback_max = max(channel_max, 1.0)

            cmin = parse_optional_float(self.rgb_vars[color]["min"].get())
            cmax = parse_optional_float(self.rgb_vars[color]["max"].get())
            gamma = self.rgb_vars[color]["gamma"].get()

            if cmin is None:
                cmin = 0.0
            if cmax is None:
                cmax = fallback_max
            if cmax <= cmin:
                cmax = cmin + 1.0

            settings[color] = {
                "enabled": bool(self.rgb_vars[color]["enabled"].get()),
                "min": cmin,
                "max": cmax,
                "gamma": max(float(gamma), 0.05),
                "pseudocolor": normalize_hex_color(self.rgb_vars[color]["pseudocolor"].get(), DEFAULT_PSEUDOCOLORS[color]),
            }
        return settings

    def _get_plot_limits(self):
        return {
            "tmin": parse_optional_float(self.time_min.get()),
            "tmax": parse_optional_float(self.time_max.get()),
            "tstep": parse_optional_float(self.time_interval.get()),
            "fmin": parse_optional_float(self.force_min.get()),
            "fmax": parse_optional_float(self.force_max.get()),
            "fstep": parse_optional_float(self.force_interval.get()),
            "dmin": parse_optional_float(self.dist_min.get()),
            "dmax": parse_optional_float(self.dist_max.get()),
            "dstep": parse_optional_float(self.dist_interval.get()),
            "iymin": parse_optional_float(self.img_y_min.get()),
            "iymax": parse_optional_float(self.img_y_max.get()),
            "iystep": parse_optional_float(self.img_y_interval.get()),
        }

    def _build_axis_ticks(self, vmin, vmax, interval):
        if vmin is None or vmax is None or interval is None:
            return None
        interval = float(interval)
        if interval <= 0:
            return None

        low, high = sorted((float(vmin), float(vmax)))
        span = high - low
        if span <= 0:
            return None
        if span / interval > 500:
            return None

        eps = max(abs(interval) * 1e-9, span * 1e-9, 1e-12)
        ticks = np.arange(low, high + eps, interval, dtype=np.float64)
        if ticks.size == 0:
            ticks = np.array([low, high], dtype=np.float64)
        elif abs(ticks[0] - low) > eps:
            ticks = np.insert(ticks, 0, low)

        if abs(ticks[-1] - high) > eps:
            ticks = np.append(ticks, high)
        return ticks

    def _apply_axis_interval(self, ax, axis, vmin, vmax, interval):
        ticks = self._build_axis_ticks(vmin, vmax, interval)
        if ticks is None:
            return
        if axis == "x":
            ax.set_xticks(ticks)
        else:
            ax.set_yticks(ticks)

    def _get_enabled_photon_channels(self, rgb_settings=None):
        if rgb_settings is None:
            return [color for color in RGB_CHANNELS if bool(self.rgb_vars[color]["enabled"].get())]
        return [color for color in RGB_CHANNELS if bool(rgb_settings[color]["enabled"])]

    def _clone_rgb_settings(self, rgb_settings):
        if rgb_settings is None:
            return None
        return {color: dict(rgb_settings[color]) for color in RGB_CHANNELS}

    def _build_png_export_variants(self, data, title):
        rgb_settings = self._get_rgb_settings(data)
        enabled_channels = self._get_enabled_photon_channels(rgb_settings)
        if not rgb_settings or not enabled_channels:
            return [{
                "name_suffix": "",
                "title": title,
                "rgb_settings": rgb_settings,
                "photon_channels": enabled_channels,
            }]

        variants = []
        for color in enabled_channels:
            single_settings = self._clone_rgb_settings(rgb_settings)
            for other_color in RGB_CHANNELS:
                single_settings[other_color]["enabled"] = (other_color == color)
            variants.append({
                "name_suffix": f"_rgb_{color}",
                "title": f"{title} [{CHANNEL_LABELS[color]}]",
                "rgb_settings": single_settings,
                "photon_channels": [color],
            })

        if len(enabled_channels) > 1:
            variants.append({
                "name_suffix": "_rgb_merge",
                "title": f"{title} [RGB merge]",
                "rgb_settings": self._clone_rgb_settings(rgb_settings),
                "photon_channels": list(enabled_channels),
            })

        return variants

    def _get_photon_trace(self, data, limits, enabled_channels=None):
        kymo = data.get("kymo") if data else None
        if not kymo:
            return np.array([], dtype=np.float64), {}

        if enabled_channels is None:
            enabled_channels = self._get_enabled_photon_channels()
        if not enabled_channels:
            return np.array([], dtype=np.float64), {}

        first_channel = np.asarray(kymo[enabled_channels[0]], dtype=np.float64)
        if first_channel.ndim != 2 or first_channel.size == 0:
            return np.array([], dtype=np.float64), {}

        rows, cols = first_channel.shape
        if rows == 0 or cols == 0:
            return np.array([], dtype=np.float64), {}

        y0 = float(kymo["y0"])
        y1 = float(kymo["y1"])
        dy = (y1 - y0) / rows if rows else 1.0
        y_centers = y0 + (np.arange(rows, dtype=np.float64) + 0.5) * dy

        iymin = limits["iymin"]
        iymax = limits["iymax"]
        if iymin is None or iymax is None:
            row_mask = np.ones(rows, dtype=bool)
        else:
            low, high = sorted((float(iymin), float(iymax)))
            row_mask = (y_centers >= low) & (y_centers <= high)
            if not np.any(row_mask):
                mid = 0.5 * (low + high)
                row_mask[np.argmin(np.abs(y_centers - mid))] = True

        x0 = float(kymo["x0"])
        x1 = float(kymo["x1"])
        dx = (x1 - x0) / cols if cols else 0.0
        time_s = x0 + (np.arange(cols, dtype=np.float64) + 0.5) * dx

        tmin = limits["tmin"]
        tmax = limits["tmax"]
        if tmin is not None and tmax is not None and tmax > tmin:
            time_mask = (time_s >= tmin) & (time_s <= tmax)
            time_s = time_s[time_mask]
        else:
            time_mask = slice(None)

        traces = {}
        for color in enabled_channels:
            channel = np.asarray(kymo[color], dtype=np.float64)
            photon = np.sum(channel[row_mask, :], axis=0)
            photon = photon[time_mask]
            traces[color] = photon

        return time_s, traces

    def _get_photon_profile(self, data, limits, enabled_channels=None):
        kymo = data.get("kymo") if data else None
        if not kymo:
            return np.array([], dtype=np.float64), {}

        if enabled_channels is None:
            enabled_channels = self._get_enabled_photon_channels()
        if not enabled_channels:
            return np.array([], dtype=np.float64), {}

        first_channel = np.asarray(kymo[enabled_channels[0]], dtype=np.float64)
        if first_channel.ndim != 2 or first_channel.size == 0:
            return np.array([], dtype=np.float64), {}

        rows, cols = first_channel.shape
        if rows == 0 or cols == 0:
            return np.array([], dtype=np.float64), {}

        y0 = float(kymo["y0"])
        y1 = float(kymo["y1"])
        dy = (y1 - y0) / rows if rows else 1.0
        y_centers = y0 + (np.arange(rows, dtype=np.float64) + 0.5) * dy

        iymin = limits["iymin"]
        iymax = limits["iymax"]
        if iymin is None or iymax is None:
            row_mask = np.ones(rows, dtype=bool)
        else:
            low, high = sorted((float(iymin), float(iymax)))
            row_mask = (y_centers >= low) & (y_centers <= high)
            if not np.any(row_mask):
                mid = 0.5 * (low + high)
                row_mask[np.argmin(np.abs(y_centers - mid))] = True

        x0 = float(kymo["x0"])
        x1 = float(kymo["x1"])
        dx = (x1 - x0) / cols if cols else 0.0
        time_s = x0 + (np.arange(cols, dtype=np.float64) + 0.5) * dx

        tmin = limits["tmin"]
        tmax = limits["tmax"]
        if tmin is not None and tmax is not None and tmax > tmin:
            time_mask = (time_s >= tmin) & (time_s <= tmax)
            if not np.any(time_mask):
                mid = 0.5 * (float(tmin) + float(tmax))
                time_mask[np.argmin(np.abs(time_s - mid))] = True
        else:
            time_mask = np.ones(cols, dtype=bool)

        profile_positions = y_centers[row_mask]
        profiles = {}
        for color in enabled_channels:
            channel = np.asarray(kymo[color], dtype=np.float64)
            profiles[color] = np.sum(channel[row_mask, :][:, time_mask], axis=1)

        return profile_positions, profiles

    def _format_range_value(self, value):

        return format_number(float(value), digits=3)

    def _set_range_pair(self, min_var, max_var, value0, value1):
        low, high = sorted((float(value0), float(value1)))
        min_var.set(self._format_range_value(low))
        max_var.set(self._format_range_value(high))

    def _apply_box_selection_to_ranges(self, axis_key, x0, x1, y0, y1):
        self._suspend_redraw = True
        try:
            if axis_key in ("kymo", "force", "distance", "photon"):
                self._set_range_pair(self.time_min, self.time_max, x0, x1)

            if axis_key == "kymo":
                self._set_range_pair(self.img_y_min, self.img_y_max, y0, y1)
            elif axis_key == "force":
                self._set_range_pair(self.force_min, self.force_max, y0, y1)
            elif axis_key == "distance":
                self._set_range_pair(self.dist_min, self.dist_max, y0, y1)
            elif axis_key == "fd":
                self._set_range_pair(self.dist_min, self.dist_max, x0, x1)
                self._set_range_pair(self.force_min, self.force_max, y0, y1)
        finally:
            self._suspend_redraw = False

        self._draw_current()

    def _on_axis_box_selected(self, axis_key, eclick, erelease):
        if eclick.xdata is None or eclick.ydata is None or erelease.xdata is None or erelease.ydata is None:
            return

        x0 = float(eclick.xdata)
        x1 = float(erelease.xdata)
        y0 = float(eclick.ydata)
        y1 = float(erelease.ydata)

        if abs(x1 - x0) < 1e-12 and abs(y1 - y0) < 1e-12:
            return

        self._apply_box_selection_to_ranges(axis_key, x0, x1, y0, y1)

    def _enable_range_selectors(self, axes):
        self._range_selectors = []
        for axis_key, ax in axes.items():
            selector = RectangleSelector(
                ax,
                lambda eclick, erelease, key=axis_key: self._on_axis_box_selected(key, eclick, erelease),
                button=[1],
                minspanx=0.0,
                minspany=0.0,
                spancoords="data",
                useblit=False,
                interactive=False,
            )
            self._range_selectors.append(selector)

    def _on_plot_button_press(self, event):
        if not getattr(event, "dblclick", False):
            return
        if event.inaxes is None:
            return

        self._suspend_redraw = True
        try:
            self._reset_range_controls()
        finally:
            self._suspend_redraw = False

        self._draw_current()

    def _get_style_settings(self):
        return {
            "fontfamily": (self.font_family_var.get() or STYLE_DEFAULTS["fontfamily"]).strip() or STYLE_DEFAULTS["fontfamily"],
            "fontweight": "bold" if bool(self.font_bold_var.get()) else "normal",
            "tick_fontsize": parse_optional_float(self.tick_fontsize_var.get()) or 10.0,
            "label_fontsize": parse_optional_float(self.label_fontsize_var.get()) or 12.0,
            "title_fontsize": parse_optional_float(self.title_fontsize_var.get()) or 15.0,
            "spine_width": parse_optional_float(self.spine_width_var.get()) or 1.0,
            "tick_width": parse_optional_float(self.tick_width_var.get()) or 1.0,
            "curve_width": parse_optional_float(self.curve_width_var.get()) or 1.0,
            "force_color": normalize_hex_color(self.force_color_var.get(), STYLE_DEFAULTS["force_color"]),
            "distance_color": normalize_hex_color(self.distance_color_var.get(), STYLE_DEFAULTS["distance_color"]),
            "fd_color": normalize_hex_color(self.fd_color_var.get(), STYLE_DEFAULTS["fd_color"]),
            "photon_red_color": normalize_hex_color(self.photon_red_color_var.get(), STYLE_DEFAULTS["photon_red_color"]),
            "photon_green_color": normalize_hex_color(self.photon_green_color_var.get(), STYLE_DEFAULTS["photon_green_color"]),
            "photon_blue_color": normalize_hex_color(self.photon_blue_color_var.get(), STYLE_DEFAULTS["photon_blue_color"]),
        }

    def _apply_axis_style(self, ax, style, show_xlabels=True):
        ax.tick_params(axis="both", width=style["tick_width"], labelsize=style["tick_fontsize"])
        if not show_xlabels:
            ax.tick_params(axis="x", which="both", labelbottom=False)
        for spine in ax.spines.values():
            spine.set_linewidth(style["spine_width"])
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontfamily(style["fontfamily"])
            label.set_fontsize(style["tick_fontsize"])
            label.set_fontweight(style["fontweight"])

    def _apply_export_panel_style(self, ax, show_meta):
        if show_meta:
            return
        legend = ax.get_legend()
        if legend is not None:
            legend.remove()
        ax.set_title("")
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.grid(False)
        ax.tick_params(axis="both", which="both", bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
        for spine in ax.spines.values():
            spine.set_visible(False)

    def _get_panel_keys(self, mode):
        return [panel_key for panel_key, _panel_label, _weight in PANEL_SPECS if self.panel_vars[panel_key]["show"].get()]

    def _get_panel_export_style_flags(self):
        return {panel_key: bool(self.panel_vars[panel_key]["export_style"].get()) for panel_key, _panel_label, _weight in PANEL_SPECS}

    def _create_panel_axes(self, fig, panel_keys):
        fig.clear()
        if not panel_keys:
            return {}

        height_lookup = {panel_key: weight for panel_key, _panel_label, weight in PANEL_SPECS}
        grid = fig.add_gridspec(len(panel_keys), 1, height_ratios=[height_lookup[panel_key] for panel_key in panel_keys])

        axes = {}
        shared_axes = {}
        for idx, panel_key in enumerate(panel_keys):
            group = PANEL_SHARE_GROUPS[panel_key]
            share_ax = shared_axes.get(group)
            if share_ax is None:
                ax = fig.add_subplot(grid[idx, 0])
                shared_axes[group] = ax
            else:
                ax = fig.add_subplot(grid[idx, 0], sharex=share_ax)
            axes[panel_key] = ax
        return axes

    def _render_plot(
        self,
        fig,
        axes,
        data,
        title,
        rgb_settings_override=None,
        photon_channels_override=None,
        panel_export_style_override=None,
        fill_kymograph_panel=False,
    ):
        limits = self._get_plot_limits()
        rgb_settings = rgb_settings_override if rgb_settings_override is not None else self._get_rgb_settings(data)
        style = self._get_style_settings()
        panel_export_style = panel_export_style_override if panel_export_style_override is not None else self._get_panel_export_style_flags()
        panel_keys = list(axes.keys())

        if not panel_keys:
            ax = fig.add_subplot(111)
            ax.axis("off")
            ax.text(0.5, 0.5, "No panels selected", ha="center", va="center", transform=ax.transAxes)
            fig.subplots_adjust(top=0.95, bottom=0.07, left=0.09, right=0.98)
            return

        t = data["t"]
        force = data["force"]
        dist = data["dist"]
        dist1 = data["dist1"]
        enabled_photon_channels = photon_channels_override
        if enabled_photon_channels is None:
            enabled_photon_channels = self._get_enabled_photon_channels(rgb_settings)
        photon_t, photon_traces = self._get_photon_trace(data, limits, enabled_photon_channels)
        photon_y, photon_profiles = self._get_photon_profile(data, limits, enabled_photon_channels)
        kymo = data["kymo"]
        top_ax = axes[panel_keys[0]]
        last_panel_by_group = {}
        for panel_key in panel_keys:
            last_panel_by_group[PANEL_SHARE_GROUPS[panel_key]] = panel_key

        if "kymo" in axes:
            ax_img = axes["kymo"]
            ax_img.cla()
            if kymo and rgb_settings:
                rgb_image = build_rgb_image(kymo, rgb_settings)
                ax_img.imshow(
                    rgb_image,
                    aspect=self._get_kymograph_display_aspect(kymo, fill_panel=fill_kymograph_panel),
                    origin="upper",
                    extent=[kymo["x0"], kymo["x1"], kymo["y1"], kymo["y0"]],
                    interpolation="nearest",
                )
            else:
                ax_img.text(0.5, 0.5, "No kymograph image", ha="center", va="center", transform=ax_img.transAxes)
            ax_img.set_ylabel("position (um)", fontfamily=style["fontfamily"], fontsize=style["label_fontsize"], fontweight=style["fontweight"])
            if last_panel_by_group["time"] == "kymo":
                ax_img.set_xlabel("time (s)", fontfamily=style["fontfamily"], fontsize=style["label_fontsize"], fontweight=style["fontweight"], labelpad=2)
            self._apply_axis_style(ax_img, style, show_xlabels=(last_panel_by_group["time"] == "kymo"))
            if last_panel_by_group["time"] != "kymo":
                ax_img.tick_params(axis="x", which="both", bottom=False)
            else:
                ax_img.tick_params(axis="x", pad=1)

        if "force" in axes:
            ax_force = axes["force"]
            ax_force.cla()
            ax_force.plot(t, force, color=style["force_color"], linewidth=style["curve_width"])
            ax_force.set_ylabel("force2x (pN)", fontfamily=style["fontfamily"], fontsize=style["label_fontsize"], fontweight=style["fontweight"])
            if last_panel_by_group["time"] == "force":
                ax_force.set_xlabel("time (s)", fontfamily=style["fontfamily"], fontsize=style["label_fontsize"], fontweight=style["fontweight"], labelpad=2)
            ax_force.grid(True, alpha=0.25)
            self._apply_axis_style(ax_force, style, show_xlabels=(last_panel_by_group["time"] == "force"))
            if last_panel_by_group["time"] == "force":
                ax_force.tick_params(axis="x", pad=1)

        if "distance" in axes:
            ax_dist = axes["distance"]
            ax_dist.cla()
            ax_dist.plot(t, dist, color=style["distance_color"], linewidth=style["curve_width"])
            ax_dist.set_ylabel("distance (um)", fontfamily=style["fontfamily"], fontsize=style["label_fontsize"], fontweight=style["fontweight"])
            if last_panel_by_group["time"] == "distance":
                ax_dist.set_xlabel("time (s)", fontfamily=style["fontfamily"], fontsize=style["label_fontsize"], fontweight=style["fontweight"], labelpad=2)
            ax_dist.grid(True, alpha=0.25)
            self._apply_axis_style(ax_dist, style, show_xlabels=(last_panel_by_group["time"] == "distance"))
            if last_panel_by_group["time"] == "distance":
                ax_dist.tick_params(axis="x", pad=1)

        if "photon" in axes:
            ax_photon = axes["photon"]
            ax_photon.cla()
            if photon_t.size and photon_traces:
                line_colors = {"red": style["photon_red_color"], "green": style["photon_green_color"], "blue": style["photon_blue_color"]}
                for color in enabled_photon_channels:
                    if color in photon_traces:
                        ax_photon.plot(
                            photon_t,
                            photon_traces[color],
                            color=line_colors[color],
                            linewidth=style["curve_width"],
                            label=CHANNEL_LABELS[color],
                        )
                if len(photon_traces) > 1:
                    ax_photon.legend(loc="upper right", prop={"family": style["fontfamily"], "size": max(style["tick_fontsize"] - 1, 7), "weight": style["fontweight"]})
            else:
                ax_photon.text(0.5, 0.5, "No photon trace", ha="center", va="center", transform=ax_photon.transAxes)
            ax_photon.set_ylabel("photon count", fontfamily=style["fontfamily"], fontsize=style["label_fontsize"], fontweight=style["fontweight"])
            if last_panel_by_group["time"] == "photon":
                ax_photon.set_xlabel("time (s)", fontfamily=style["fontfamily"], fontsize=style["label_fontsize"], fontweight=style["fontweight"], labelpad=2)
            ax_photon.grid(True, alpha=0.25)
            self._apply_axis_style(ax_photon, style, show_xlabels=(last_panel_by_group["time"] == "photon"))
            if last_panel_by_group["time"] == "photon":
                ax_photon.tick_params(axis="x", pad=1)

        if "photon_profile" in axes:
            ax_photon_profile = axes["photon_profile"]
            ax_photon_profile.cla()
            if photon_y.size and photon_profiles:
                line_colors = {"red": style["photon_red_color"], "green": style["photon_green_color"], "blue": style["photon_blue_color"]}
                for color in enabled_photon_channels:
                    if color in photon_profiles:
                        ax_photon_profile.plot(
                            photon_y,
                            photon_profiles[color],
                            color=line_colors[color],
                            linewidth=style["curve_width"],
                            label=CHANNEL_LABELS[color],
                        )
                if len(photon_profiles) > 1:
                    ax_photon_profile.legend(loc="upper right", prop={"family": style["fontfamily"], "size": max(style["tick_fontsize"] - 1, 7), "weight": style["fontweight"]})
            else:
                ax_photon_profile.text(0.5, 0.5, "No photon profile", ha="center", va="center", transform=ax_photon_profile.transAxes)
            ax_photon_profile.set_ylabel("photon count", fontfamily=style["fontfamily"], fontsize=style["label_fontsize"], fontweight=style["fontweight"])
            ax_photon_profile.set_xlabel("position (um)", fontfamily=style["fontfamily"], fontsize=style["label_fontsize"], fontweight=style["fontweight"], labelpad=2)
            ax_photon_profile.grid(True, alpha=0.25)
            self._apply_axis_style(ax_photon_profile, style, show_xlabels=True)
            ax_photon_profile.tick_params(axis="x", pad=1)

        if "fd" in axes:
            ax_fd = axes["fd"]
            ax_fd.cla()
            fd_curves = self._get_fd_overlay_curves(data)
            if not fd_curves:
                fd_curves = [{"label": title.replace(".h5", ""), "distance": dist1, "force": force, "is_current": True}]

            if len(fd_curves) == 1:
                curve = fd_curves[0]
                ax_fd.plot(curve["distance"], curve["force"], color=style["fd_color"], linewidth=style["curve_width"])
            else:
                overlay_color_idx = 0
                for curve in fd_curves:
                    if curve["is_current"]:
                        color = style["fd_color"]
                        line_width = style["curve_width"] * 1.35
                        zorder = 4
                    else:
                        color = FD_OVERLAY_COLORS[overlay_color_idx % len(FD_OVERLAY_COLORS)]
                        overlay_color_idx += 1
                        line_width = style["curve_width"]
                        zorder = 3
                    ax_fd.plot(curve["distance"], curve["force"], color=color, linewidth=line_width, label=curve["label"], alpha=0.95, zorder=zorder)
                ax_fd.legend(loc="best", prop={"family": style["fontfamily"], "size": max(style["tick_fontsize"] - 1, 7), "weight": style["fontweight"]})

            ax_fd.set_xlabel("Distance 1 LF (um)", fontfamily=style["fontfamily"], fontsize=style["label_fontsize"], fontweight=style["fontweight"])
            ax_fd.set_ylabel("Force 2x LF (pN)", fontfamily=style["fontfamily"], fontsize=style["label_fontsize"], fontweight=style["fontweight"])
            ax_fd.grid(True, alpha=0.25)
            self._apply_axis_style(ax_fd, style, show_xlabels=True)

        top_ax.set_title(title, fontfamily=style["fontfamily"], fontsize=style["title_fontsize"], fontweight=style["fontweight"])

        tmin = limits["tmin"]
        tmax = limits["tmax"]
        tstep = limits["tstep"]
        fmin = limits["fmin"]
        fmax = limits["fmax"]
        fstep = limits["fstep"]
        dmin = limits["dmin"]
        dmax = limits["dmax"]
        dstep = limits["dstep"]
        iymin = limits["iymin"]
        iymax = limits["iymax"]
        iystep = limits["iystep"]

        time_bottom_panel = last_panel_by_group.get("time")
        if time_bottom_panel and tmin is not None and tmax is not None and tmax > tmin:
            axes[time_bottom_panel].set_xlim(tmin, tmax)
            self._apply_axis_interval(axes[time_bottom_panel], "x", tmin, tmax, tstep)
        if "force" in axes and fmin is not None and fmax is not None and fmax > fmin:
            axes["force"].set_ylim(fmin, fmax)
            self._apply_axis_interval(axes["force"], "y", fmin, fmax, fstep)
        if "distance" in axes and dmin is not None and dmax is not None and dmax > dmin:
            axes["distance"].set_ylim(dmin, dmax)
            self._apply_axis_interval(axes["distance"], "y", dmin, dmax, dstep)
        if "kymo" in axes and iymin is not None and iymax is not None and iymax > iymin:
            axes["kymo"].set_ylim(iymax, iymin)
            self._apply_axis_interval(axes["kymo"], "y", iymin, iymax, iystep)
        if "fd" in axes and dmin is not None and dmax is not None and dmax > dmin:
            axes["fd"].set_xlim(dmin, dmax)
            self._apply_axis_interval(axes["fd"], "x", dmin, dmax, dstep)
        if "fd" in axes and fmin is not None and fmax is not None and fmax > fmin:
            axes["fd"].set_ylim(fmin, fmax)
            self._apply_axis_interval(axes["fd"], "y", fmin, fmax, fstep)

        for panel_key, ax in axes.items():
            self._apply_export_panel_style(ax, bool(panel_export_style.get(panel_key, True)))

        hspace = 0.32 if ("fd" in axes and any(key in axes for key in ("kymo", "force", "distance", "photon", "photon_profile"))) else 0.08
        fig.subplots_adjust(top=0.95, bottom=0.07, left=0.09, right=0.98, hspace=hspace)

    def _build_export_figure(self, panel_keys, data, title, rgb_settings_override=None, photon_channels_override=None, panel_export_style_override=None):

        fig = Figure(figsize=self._get_plot_figure_size(), dpi=120)
        axes = self._create_panel_axes(fig, panel_keys)
        self._render_plot(
            fig,
            axes,
            data,
            title,
            rgb_settings_override=rgb_settings_override,
            photon_channels_override=photon_channels_override,
            panel_export_style_override=panel_export_style_override,
            fill_kymograph_panel=True,
        )
        return fig

    def _ensure_export_panels_selected(self):
        if self._get_panel_keys("save"):
            return True
        messagebox.showwarning("Save PNG", "Select at least one panel in Panels -> Save PNG before exporting.")
        return False

    def _resolve_save_dir(self, default_to_base=False):
        save_dir = (self.save_dir_var.get() or "").strip()
        if not save_dir:
            save_dir = self._get_input_dir()
        if not save_dir and not default_to_base:
            self._pick_save_dir()
            save_dir = (self.save_dir_var.get() or "").strip() or self._get_input_dir()
        if not save_dir:
            messagebox.showwarning("Save folder", self._t("input_folder_not_set"))
            return None
        os.makedirs(save_dir, exist_ok=True)
        return save_dir

    def _build_curve_sheet_data(self, filename, data, include_filename):
        time_s = np.asarray(data["t"], dtype=np.float64)
        force_pn = np.asarray(data["force"], dtype=np.float64)
        distance_um = np.asarray(data["dist"], dtype=np.float64)
        distance1_um = np.asarray(data["dist1"], dtype=np.float64)
        limits = self._get_plot_limits()
        photon_time_s, photon_traces = self._get_photon_trace(data, limits)
        photon_pos_um, photon_profiles = self._get_photon_profile(data, limits)

        photon_sheet = {"time_s": photon_time_s}
        for color in self._get_enabled_photon_channels():
            if color in photon_traces:
                photon_sheet[f"photon_count_{color}"] = photon_traces[color]

        photon_profile_sheet = {"position_um": photon_pos_um}
        for color in self._get_enabled_photon_channels():
            if color in photon_profiles:
                photon_profile_sheet[f"photon_count_{color}"] = photon_profiles[color]

        sheets = {
            "Force_vs_Time": pd.DataFrame({"time_s": time_s, "force2x_pN": force_pn}),
            "Distance_vs_Time": pd.DataFrame({"time_s": time_s, "distance_um": distance_um}),
            "FD_Curve": pd.DataFrame({"distance1_um": distance1_um, "force2x_pN": force_pn}),
            "PhotonCount_vs_Time": pd.DataFrame(photon_sheet),
            "PhotonCount_vs_Position": pd.DataFrame(photon_profile_sheet),
        }

        if include_filename:
            for df in sheets.values():
                df.insert(0, "file", filename)
        return sheets

    def _write_curve_workbook(self, out_path, sheet_frames):
        with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
            for sheet_name, frame in sheet_frames.items():
                frame.to_excel(writer, sheet_name=sheet_name, index=False)

    def _draw_current(self):
        if self._suspend_redraw:
            return
        try:
            mode_key = self._get_current_mode()
            selected_file = self.file_var.get().strip() if hasattr(self, "file_var") else ""
            if not selected_file:
                self._render_placeholder(self._get_empty_state_message(mode_key), title=self._t(DATA_MODE_LABEL_KEYS[mode_key]))
                return

            if mode_key == "scan":
                self._render_placeholder(self._t("scan_placeholder"), title=selected_file)
                return

            self._apply_current_figure_size()
            data = self._get_current_data()
            panel_keys = ["fd"] if mode_key == "fd_curve" else self._get_panel_keys("show")
            axes = self._create_panel_axes(self.fig, panel_keys)
            self._render_plot(
                self.fig,
                axes,
                data,
                os.path.basename(self._get_current_path()),
                fill_kymograph_panel=True,
            )
            if mode_key == "kymograph":
                self._enable_range_selectors(axes)
            else:
                self._range_selectors = []
            self.canvas.draw_idle()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _save_current(self):
        mode_key = self._get_current_mode()
        if mode_key == "fd_curve":
            return self._save_current_fd_curve()
        if mode_key == "scan":
            return self._save_current_scan_png()
        if not self._ensure_kymograph_mode("Save current PNG"):
            return
        try:
            if not self._ensure_export_panels_selected():
                return

            save_dir = self._resolve_save_dir(default_to_base=False)
            if not save_dir:
                return

            selected_fn = self.file_var.get().strip()
            data = self._get_current_data()

            try:
                idx = self.file_list.index(selected_fn) + 1
            except ValueError:
                idx = 0

            save_panels = self._get_panel_keys("save")
            panel_export_style = self._get_panel_export_style_flags()
            saved_paths = []
            for variant in self._build_png_export_variants(data, selected_fn):
                fig = self._build_export_figure(
                    save_panels,
                    data,
                    variant["title"],
                    rgb_settings_override=variant["rgb_settings"],
                    photon_channels_override=variant["photon_channels"],
                    panel_export_style_override=panel_export_style,
                )
                out_name = f"{idx:02d}_{selected_fn.replace('.h5', '')}_kymo_force_distance{variant['name_suffix']}.png"
                out_path = os.path.join(save_dir, out_name)
                fig.savefig(out_path)
                saved_paths.append(out_path)
            self._set_status(f"Saved {len(saved_paths)} PNG file(s) to {save_dir}")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _save_all(self):
        mode_key = self._get_current_mode()
        if mode_key == "fd_curve":
            return self._save_all_fd_curve()
        if mode_key == "scan":
            return self._save_all_scan_png()
        if not self._ensure_kymograph_mode("Save all PNG"):
            return
        if not self._ensure_export_panels_selected():
            return

        save_dir = self._resolve_save_dir(default_to_base=True)
        if not save_dir:
            return

        files = list(self.file_list)
        if not files:
            messagebox.showwarning("Save all", "No H5 files available in the current input folder.")
            return

        selected_before = self.file_var.get().strip()
        save_panels = self._get_panel_keys("save")
        panel_export_style = self._get_panel_export_style_flags()
        saved = 0
        errors = []

        for idx, filename in enumerate(files, start=1):
            try:
                self.file_var.set(filename)
                data = self._get_current_data()
                for variant in self._build_png_export_variants(data, filename):
                    fig = self._build_export_figure(
                        save_panels,
                        data,
                        variant["title"],
                        rgb_settings_override=variant["rgb_settings"],
                        photon_channels_override=variant["photon_channels"],
                        panel_export_style_override=panel_export_style,
                    )

                    out_name = f"{idx:02d}_{filename.replace('.h5', '')}_kymo_force_distance{variant['name_suffix']}.png"
                    out_path = os.path.join(save_dir, out_name)
                    fig.savefig(out_path)
                    saved += 1
            except Exception as exc:
                errors.append((filename, str(exc)))

        if selected_before:
            self.file_var.set(selected_before)
            self._draw_current()

        if errors:
            first_name, first_err = errors[0]
            self._set_status(f"Saved {saved} PNG(s) for {len(files)} file(s) to {save_dir}. Errors: {len(errors)} (first: {first_name}: {first_err})")
        else:
            self._set_status(f"Saved {saved} PNG(s) for {len(files)} file(s) to {save_dir}")

    def _export_current_excel(self):
        mode_key = self._get_current_mode()
        if mode_key == "fd_curve":
            try:
                save_dir = self._resolve_save_dir(default_to_base=False)
                if not save_dir:
                    return
                selected_fn = self.file_var.get().strip()
                data = self._get_current_data()
                out_path = os.path.join(save_dir, f"{selected_fn.replace('.h5', '')}_fd_overlay.xlsx")
                self._write_curve_workbook(out_path, self._build_fd_overlay_sheet_data(selected_fn, data))
                self._set_status(f"Exported Excel: {out_path}")
            except Exception as exc:
                messagebox.showerror("Error", str(exc))
            return
        if mode_key == "scan":
            try:
                save_dir = self._resolve_save_dir(default_to_base=False)
                if not save_dir:
                    return
                selected_fn = self.file_var.get().strip()
                out_path = os.path.join(save_dir, f"{selected_fn.replace('.h5', '')}_scan_summary.xlsx")
                self._write_curve_workbook(out_path, self._build_scan_summary_sheet([selected_fn]))
                self._set_status(f"Exported Excel: {out_path}")
            except Exception as exc:
                messagebox.showerror("Error", str(exc))
            return
        if not self._ensure_kymograph_mode("Export current Excel"):
            return
        try:
            save_dir = self._resolve_save_dir(default_to_base=False)
            if not save_dir:
                return

            selected_fn = self.file_var.get().strip()
            data = self._get_current_data()

            try:
                idx = self.file_list.index(selected_fn) + 1
            except ValueError:
                idx = 0

            sheet_frames = self._build_curve_sheet_data(selected_fn, data, include_filename=False)
            out_name = f"{idx:02d}_{selected_fn.replace('.h5', '')}_curves.xlsx"
            out_path = os.path.join(save_dir, out_name)
            self._write_curve_workbook(out_path, sheet_frames)
            self._set_status(f"Exported Excel: {out_path}")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _export_all_excel(self):
        mode_key = self._get_current_mode()
        if mode_key == "fd_curve":
            try:
                save_dir = self._resolve_save_dir(default_to_base=True)
                if not save_dir:
                    return
                files = list(self.file_list)
                if not files:
                    messagebox.showwarning("Export all", "No H5 files available in the current input folder.")
                    return
                grouped = []
                errors = []
                selected_before = self.file_var.get().strip()
                for filename in files:
                    try:
                        self.file_var.set(filename)
                        data = self._get_current_data()
                        frame = self._build_curve_sheet_data(filename, data, include_filename=True)["FD_Curve"]
                        grouped.append(frame)
                    except Exception as exc:
                        errors.append((filename, str(exc)))
                if selected_before:
                    self.file_var.set(selected_before)
                    self._draw_current()
                out_path = os.path.join(save_dir, "all_fd_curves.xlsx")
                merged = pd.concat(grouped, ignore_index=True) if grouped else pd.DataFrame()
                self._write_curve_workbook(out_path, {"FD_Curve": merged})
                if errors:
                    first_name, first_err = errors[0]
                    self._set_status(f"Exported FD Excel to {out_path}. Errors: {len(errors)} (first: {first_name}: {first_err})")
                else:
                    self._set_status(f"Exported FD Excel to {out_path}")
            except Exception as exc:
                messagebox.showerror("Error", str(exc))
            return
        if mode_key == "scan":
            try:
                save_dir = self._resolve_save_dir(default_to_base=True)
                if not save_dir:
                    return
                files = list(self.file_list)
                if not files:
                    messagebox.showwarning("Export all", "No H5 files available in the current input folder.")
                    return
                out_path = os.path.join(save_dir, "all_scan_summary.xlsx")
                self._write_curve_workbook(out_path, self._build_scan_summary_sheet(files))
                self._set_status(f"Exported Excel: {out_path}")
            except Exception as exc:
                messagebox.showerror("Error", str(exc))
            return
        if not self._ensure_kymograph_mode("Export all Excel"):
            return
        try:
            save_dir = self._resolve_save_dir(default_to_base=True)
            if not save_dir:
                return

            files = list(self.file_list)
            if not files:
                messagebox.showwarning("Export all", "No H5 files available in the current input folder.")
                return

            selected_before = self.file_var.get().strip()
            grouped_frames = {
                "Force_vs_Time": [],
                "Distance_vs_Time": [],
                "FD_Curve": [],
                "PhotonCount_vs_Time": [],
                "PhotonCount_vs_Position": [],
            }
            errors = []

            for filename in files:
                try:
                    self.file_var.set(filename)
                    data = self._get_current_data()
                    sheet_frames = self._build_curve_sheet_data(filename, data, include_filename=True)
                    for sheet_name, frame in sheet_frames.items():
                        grouped_frames[sheet_name].append(frame)
                except Exception as exc:
                    errors.append((filename, str(exc)))

            if selected_before:
                self.file_var.set(selected_before)
                self._draw_current()

            merged_frames = {}
            for sheet_name, frames in grouped_frames.items():
                if frames:
                    merged_frames[sheet_name] = pd.concat(frames, ignore_index=True)
                else:
                    merged_frames[sheet_name] = pd.DataFrame()

            out_path = os.path.join(save_dir, "all_traces_curves.xlsx")
            self._write_curve_workbook(out_path, merged_frames)

            if errors:
                first_name, first_err = errors[0]
                self._set_status(f"Exported all curves to {out_path}. Errors: {len(errors)} (first: {first_name}: {first_err})")
            else:
                self._set_status(f"Exported all curves to {out_path}")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

if __name__ == "__main__":

    app = App()
    app.mainloop()





