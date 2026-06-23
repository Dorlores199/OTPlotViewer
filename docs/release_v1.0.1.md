# OTPlotViewer v1.0.1 Release Notes

## English

This release focuses on easier distribution and installation.

### What's New

- Added a small one-click Windows installer: `OTPlotViewer_Setup_1.0.1.exe`.
- The installer downloads the packaged OTPlotViewer application from this GitHub release, installs it into the current user's local application folder, and creates Desktop and Start Menu shortcuts.
- Improved installer download reliability with TLS 1.2, retry logic, and fallback download methods.
- Added bilingual English/Chinese installation instructions in `README.md`.
- Added installer build scripts under `installer/`.
- Updated Windows file version metadata to `1.0.1.0`.

### Recommended Installation

1. Download `OTPlotViewer_Setup_1.0.1.exe`.
2. Double-click the installer.
3. Allow it to download the application package from GitHub.
4. Launch OTPlotViewer from the Desktop shortcut or Start Menu.

### Portable Installation

If the installer cannot download files automatically, download all split archive files:

- `OTPlotViewer_v1.0.1_windows_folder_split.7z.001`
- `OTPlotViewer_v1.0.1_windows_folder_split.7z.002`
- `OTPlotViewer_v1.0.1_windows_folder_split.7z.003`
- `OTPlotViewer_v1.0.1_windows_folder_split.7z.004`

Keep all four files in the same folder, then extract `.001` with 7-Zip. After extraction, run `OTPlotViewer.exe` inside the `OTPlotViewer` folder.

## 中文

这个版本主要改进软件分发和安装方式。

### 更新内容

- 新增小体积 Windows 一键安装器：`OTPlotViewer_Setup_1.0.1.exe`。
- 安装器会自动从本 GitHub release 下载 OTPlotViewer 应用包，安装到当前用户的本地程序目录，并创建桌面和开始菜单快捷方式。
- 改进安装器下载稳定性，加入 TLS 1.2、自动重试和备用下载方式。
- 在 `README.md` 中加入中英文安装和使用说明。
- 在 `installer/` 目录中加入安装器构建脚本。
- Windows 文件版本号更新为 `1.0.1.0`。

### 推荐安装方式

1. 下载 `OTPlotViewer_Setup_1.0.1.exe`。
2. 双击运行安装器。
3. 等待安装器从 GitHub 下载应用包并完成安装。
4. 通过桌面快捷方式或开始菜单启动 OTPlotViewer。

### 便携版使用方式

如果一键安装器无法自动下载文件，可以手动下载所有分卷文件：

- `OTPlotViewer_v1.0.1_windows_folder_split.7z.001`
- `OTPlotViewer_v1.0.1_windows_folder_split.7z.002`
- `OTPlotViewer_v1.0.1_windows_folder_split.7z.003`
- `OTPlotViewer_v1.0.1_windows_folder_split.7z.004`

把四个文件放在同一个文件夹中，然后用 7-Zip 解压 `.001` 文件。解压后进入 `OTPlotViewer` 文件夹，双击运行 `OTPlotViewer.exe`。
