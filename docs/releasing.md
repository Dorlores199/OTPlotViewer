# Release Workflow

OTPlotViewer uses GitHub Actions for CI and tag-based releases.

## Everyday Checks

Every push to `main` runs `.github/workflows/ci.yml`.

It checks:

- Python dependencies can be installed.
- `kymograph_force_distance_ui.py` compiles.
- PowerShell build and installer scripts parse correctly.

## Publishing A New Version

Use semantic tags such as `v1.0.3`.

Before creating a tag, update:

- `README.md`: download links and citation text.
- `CITATION.cff`: `version` and `date-released`.
- `version_info.txt`: Windows file/product version.
- `docs/release_vX.Y.Z.md`: release notes for the new tag.

Then run:

```powershell
git add README.md CITATION.cff version_info.txt docs/release_vX.Y.Z.md
git commit -m "Release vX.Y.Z"
git tag -a vX.Y.Z -m "OTPlotViewer vX.Y.Z"
git push origin main
git push origin vX.Y.Z
```

Pushing the tag starts `.github/workflows/release.yml`.

The release workflow:

- Verifies that release metadata matches the tag.
- Builds the Windows PyInstaller folder distribution.
- Creates a normal zip package.
- Creates the split 7-Zip portable package used by the installer.
- Builds `OTPlotViewer_Setup_X.Y.Z.exe`.
- Uploads all assets to the GitHub Release.

## Major Releases

For larger feature releases, use a new minor or major tag, for example:

- `v1.1.0` for a feature release.
- `v2.0.0` for a release with major workflow or file-format changes.

For small bug fixes, use a patch tag such as `v1.0.3`.

## 中文说明

每次推送到 `main` 后，GitHub 会自动运行 CI，检查 Python 源码和 PowerShell 脚本是否基本可用。

发布新版时，先更新：

- `README.md`：下载链接和论文引用文字。
- `CITATION.cff`：版本号和发布日期。
- `version_info.txt`：Windows 程序版本号。
- `docs/release_vX.Y.Z.md`：该版本的更新说明。

然后创建并推送 tag，例如 `v1.0.3`。GitHub Actions 会自动构建 Windows 可分发包、安装器，并创建 GitHub Release。
