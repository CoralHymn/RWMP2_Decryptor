# RWMP2_Decryptor

<div align="center">
  
### [🇺🇸 English](README_EN.md) | [🇨🇳 简体中文](README.md)

</div>

<div align="center">
  
## https://coralhymn.com/ | [Documentation Website](https://docs.cc00.top/)

</div>

## Introduction
  - RWMP2_Decryptor is an unlocking tool for the "RWMP2" MOD encryption utility used in the game "Rusted Warfare"
  - Developed using Python, available in both GUI and WebUI versions, as well as a pure HTML static page
  - This software was created with assistance from "Qwen3-235B-A22B" and "Qwen3-Coder" AI models

----

> If you find this tool useful, please give me a star on Github! \
> Supported platforms: [ *Windows——Linux——Servers* ] \
> The web version supports any device with a browser

----

# Online Usage (Recommended for Mobile Devices)

We provide a pure HTML version that requires no installation—just use it directly in your browser:

[👉 Click here to use online](https://sg.coralhymn.com/py/RWMP2_Decryptor.html)

**Advantages:**

- Full platform compatibility (Windows, Mac, Linux, mobile browsers)
- No installation or configuration required
- Runs entirely in the browser using Pyodide technology

> ⚠️ Known issue: Download may fail on certain mobile browsers (e.g., Via). Please use Chrome, Edge, or other mainstream browsers.

# 💻 Local/Server Installation (Recommended for PC)

> ⚠️ Note: Releases are outdated. The latest version has not been built yet—please build from source code.

- [python-source](#Python-Source-Usage)
- [installation-windows](#Windows-Guide)
- [installation-linux](#Linux-Guide)
- outdated！
- [server-deployment](https://github.com/CoralHymn/RWMP2_Decryptor/blob/masyer/Server-README_EN.md)

## Python Source Usage

> If you're on macOS, you can get the official installer from the [Python website](https://www.python.org/downloads). You may use any stable version of Python 3.10 or above, but avoid Alpha, Beta, and Release Candidate versions.
>
> On Linux, use your system package manager (`apt` on Debian/Ubuntu/Mint, `dnf` on Fedora, or `pacman` on Arch) to install Python (most Linux distributions come with Python pre-installed).
>
> On Windows, download the official installer from the [Python website](https://www.python.org/downloads). Any stable version between Python 3.9 and 3.13 is supported. Avoid Alpha, Beta, and Release Candidate versions.

You will also need Git to clone the source code.

Check your Python version with:
```bash
python --version
```

Clone the repository:
```bash
git clone https://github.com/CoralHymn/RWMP2_Decryptor.git
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the GUI version:
```bash
python RWMP2_Decryptor.py
```

Run the WebUI version:
```bash
python RWMP2_Decryptor_Web.py
```

## Windows Guide

Get the latest Windows versions from [Releases](https://github.com/CoralHymn/RWMP2_Decryptor/releases):
- [RWMP2_Decryptor_Windows.exe](https://github.com/CoralHymn/RWMP2_Decryptor/releases/download/Alpha_2.2.0/RWMP2_Decryptor_windows.exe)

These are portable executables - just double-click to run
  
  - Double-click the exe (may take a moment to load)
  - A window will appear, letting you choose your preferred interface.
  - Click "选择文件" to choose your mod file
  - Click "开始处理" (Start Processing), and you can monitor the progress below. When it’s done, click "下载处理结果" (Download Processed Result)​ to save your file.
  
  ![wingui](http://hk.coralhymn.com/png/wingui.png)
  ![wingui](http://hk.coralhymn.com/png/winweb.png)
  

## Linux Guide

Works with most distros (contact me if issues occur) \
Get Linux versions from [Releases](https://github.com/CoralHymn/RWMP2_Decryptor/releases)\
These are (application/x-executable) binaries:
- [RWMP2_Decryptor_Linux.AppImage](https://github.com/CoralHymn/RWMP2_Decryptor/releases/download/Alpha_2.2.0/RWMP2_Decryptor_Linux.AppImage)

After download, grant execute permissions:

```bash
chmod +x RWMP2_Decryptor_Linux.AppImage  # Add executable permission
  ```


  Run via terminal:
```bash
./RWMP2_Decryptor_Linux*.AppImage
  ```
  - Can also double-click (but ./ recommended)
  - A window will appear, letting you choose your preferred interface.
  - Click "选择文件" to choose your mod file
  - Click "开始处理" (Start Processing), and you can monitor the progress below. When it’s done, click "下载处理结果" (Download Processed Result)​ to save your file.



#### About [ Android | iOS | macOS ]
  - These platforms can use the online web version. Developing mobile apps with Python is difficult and cumbersome.
  - More platform versions are under development. If you develop versions for other platforms, please add them to branches.

## ⚠️ Disclaimer

  - For educational/research purposes only. Users must ensure legal authorization for target files.
  - Prohibited for unauthorized decryption.
  - Misuse may lead to legal consequences. Developer assumes no liability for illegal usage.
  - Continued use constitutes acceptance of these terms.


Python Libraries Used:
[PyWebIO](https://github.com/pywebio/PyWebIO)
