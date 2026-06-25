# OTPlotViewer v1.0.2 Release Notes

## English

This is a compatibility bug-fix release for C-Trap kymograph files that do not contain the low-frequency force channel.

### What's Fixed

- Fixed kymograph files that failed with `Unable to synchronously open object (component not found)` when `Force LF/Force 2x` was absent.
- OTPlotViewer now automatically falls back to `Force HF/Force 2x` when `Force LF/Force 2x` is not available.
- Continuous high-frequency force data are sampled onto the distance/kymograph time axis for plotting, FD curves, and export.
- Verified with `20260616-131504 Kymograph 18.h5` from the `260616 30nt gap anneal ORCR first batch` dataset.

### Recommended Installation

1. Download `OTPlotViewer_Setup_1.0.2.exe`.
2. Double-click the installer.
3. Allow it to download the application package from GitHub.
4. Launch OTPlotViewer from the Desktop shortcut or Start Menu.

### Portable Installation

If the installer cannot download files automatically, download all split archive files:

- `OTPlotViewer_v1.0.2_windows_folder_split.7z.001`
- `OTPlotViewer_v1.0.2_windows_folder_split.7z.002`
- `OTPlotViewer_v1.0.2_windows_folder_split.7z.003`
- `OTPlotViewer_v1.0.2_windows_folder_split.7z.004`

Keep all four files in the same folder, then extract `.001` with 7-Zip. After extraction, run `OTPlotViewer.exe` inside the `OTPlotViewer` folder.

## 中文

这是一个兼容性修复版本，主要解决部分 C-Trap kymograph 文件没有低频 force 通道时无法打开的问题。

### 修复内容

- 修复部分 kymograph 文件因为缺少 `Force LF/Force 2x` 而弹出 `Unable to synchronously open object (component not found)` 的问题。
- 当文件里没有 `Force LF/Force 2x` 时，OTPlotViewer 会自动改用 `Force HF/Force 2x`。
- 高频连续 force 数据会自动采样到 distance/kymograph 的时间轴上，用于绘图、FD 曲线和数据导出。
- 已使用 `260616 30nt gap anneal ORCR first batch` 数据集中的 `20260616-131504 Kymograph 18.h5` 验证。

### 推荐安装方式

1. 下载 `OTPlotViewer_Setup_1.0.2.exe`。
2. 双击运行安装器。
3. 等待安装器从 GitHub 下载应用包并完成安装。
4. 通过桌面快捷方式或开始菜单启动 OTPlotViewer。

### 便携版使用方式

如果一键安装器无法自动下载文件，可以手动下载所有分卷文件：

- `OTPlotViewer_v1.0.2_windows_folder_split.7z.001`
- `OTPlotViewer_v1.0.2_windows_folder_split.7z.002`
- `OTPlotViewer_v1.0.2_windows_folder_split.7z.003`
- `OTPlotViewer_v1.0.2_windows_folder_split.7z.004`

把四个文件放在同一个文件夹中，然后用 7-Zip 解压 `.001` 文件。解压后进入 `OTPlotViewer` 文件夹，双击运行 `OTPlotViewer.exe`。
