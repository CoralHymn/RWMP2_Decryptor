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
- [installation-windows](#Installation-(Windows))
- [installation-linux](#Installation-(Linux))
- outdated！
- [server-deployment](https://github.com/CoralHymn/RWMP2_Decryptor/blob/masyer/Server-README_EN.md)

# Python Source Usage

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

# Installation (Windows)

Get the latest Windows versions from [Releases](https://github.com/CoralHymn/RWMP2_Decryptor/releases):
- [RWMP2_Decryptor_Windows_GUI.exe](https://github.com/CoralHymn/RWMP2_Decryptor/releases/download/Alpha_2.1.0/RWMP2_Decryptor_Windows_GUI.exe)
- [RWMP2_Decryptor_Windows_WebUI.exe](https://github.com/CoralHymn/RWMP2_Decryptor/releases/download/Alpha_2.1.0/RWMP2_Decryptor_Windows_WebUI.exe)  **(Recommended)** \
  Note❗ Versions before **2.1.0** only support Windows with outdated CLI interface - not recommended \
These are portable executables - just double-click to run

  ## Windows Guide
  
First change your .rwmod file extension to .zip before use
  
  **GUI**
  - Double-click the exe (may take a moment to load)
  - Click "Select ZIP File" to choose your mod file
  - Click "Process" and monitor progress. When complete, click "Download Result" to save
  ![wingui](http://hk.coralhymn.com/png/wingui.png)

  **WebUI**
  - Double-click the exe - a terminal will appear briefly before opening in your default browser
  - Drag & drop or click to upload your ZIP file (processed locally)
  - Click "Start", then wait for the download link to appear
  - Click the link to download (may take a moment)
  ![wingui](http://hk.coralhymn.com/png/winweb.png)
  

# Installation (Linux)

Works with most distros (contact me if issues occur) \
Get Linux versions from [Releases](https://github.com/CoralHymn/RWMP2_Decryptor/releases)\
These are (application/x-executable) binaries:
- [RWMP2_Decryptor_Linux_GUI.AppImage](https://github.com/CoralHymn/RWMP2_Decryptor/releases/download/Alpha_2.1.0/RWMP2_Decryptor_Linux_GUI.AppImage)
- [RWMP2_Decryptor_Linux_Web.AppImage](https://github.com/CoralHymn/RWMP2_Decryptor/releases/download/Alpha_2.1.0/RWMP2_Decryptor_Linux_Web.AppImage)(Recommended)\
After download, grant execute permissions:
```bash
chmod +x RWMP2_Decryptor_Linux*.AppImage  # Add executable permission
  ```

  ## Linux Guide
  
First change your .rwmod file extension to .zip before use
  
  **GUI**
  
  Run via terminal:
```bash
./RWMP2_Decryptor_Linux*.AppImage
  ```
  - Can also double-click (but ./ recommended)
  - Click "Select ZIP File" to choose your mod
  - Click "Process" and monitor progress. When complete, click "Download Result"

  **WebUI** 
  
  Run via terminal:
```bash
./RWMP2_Decryptor_Linux*.AppImage
  ```
  - Double-click works (but ./ recommended)
  - Terminal will appear briefly before browser launch
  - Drag & drop or click to upload ZIP
  - Click "Start", wait for download link
  - Click link to download
  - (Temporary files auto-cleaned)

 GUI may show error===Solution:
```bash
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, webgl, xcb.

  ```
Common PyQt5 Linux error indicating missing X11 display connection \
Ensure desktop environment is installed. If persists, install xcb libraries (Ubuntu/Debian):
```bash
sudo apt-get install libxcb-xinerama0 libxcb-xinerama0-dev
  ```
Other distros: Find equivalent xcb packages


#### About [ Android | iOS | macOS ]
  - These platforms can use the online web version. Developing mobile apps with Python is difficult and cumbersome.
  - More platform versions are under development. If you develop versions for other platforms, please add them to branches.

## ⚠⚠⚠️ Disclaimer

  - For educational/research purposes only. Users must ensure legal authorization for target files.
  - Prohibited for unauthorized decryption.
  - Misuse may lead to legal consequences. Developer assumes no liability for illegal usage.
  - Continued use constitutes acceptance of these terms.


使用的python库：
[PyWebIO](https://github.com/pywebio/PyWebIO)
