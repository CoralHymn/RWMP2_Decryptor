# RWMP2_Decryptor

<div align="center">

### [🇺🇸 English](README_EN.md) | [🇨🇳 简体中文](README.md)

</div>

<div align="center">

## [前往官网](https://coralhymn.com/) | [文档网页](https://docs.cc00.top/)

</div>

## 介绍

- RWMP2_Decryptor是“Rusted Warfare”游戏的MOD加密工具“RWMP2”的解锁工具
- 使用python制作，支持GUI与WebUI两个界面软件以及HTML静态页面
- 本软件使用了“Qwen3-235B-A22B”与“Qwen3-Coder”辅助编写

----

> 如果你觉得这个这个软件好用，请在Github上给我一颗星！ \
> 此软件支持 [ *Windows——Linux——服务器* ]
> 网页支持任何能够访问浏览器的设备

----

# 在线使用 (移动设备推荐)

我们提供了纯HTML版本，无需安装任何软件，直接在浏览器中使用：

[👉 点击这里在线使用](https://sg.coralhymn.com/py/RWMP2_Decryptor.html)

**优势：**

- 全平台兼容（Windows、Mac、Linux、手机浏览器）
- 无需安装，零配置
- 基于Pyodide技术，完全在浏览器中运行

> ⚠️ 已知问题：在某些移动端浏览器（如Via）上可能出现下载失败，请使用Chrome、Edge等主流浏览器。

# 💻 本地/服务器安装（PC设备推荐）

注意！releases已过时，最新版未构建，请使用源码构建

- [python](#python源码使用)
- [windows](#安装（windows）)
- [Linux](#安装（Linux）)
- [服务器](#服务器部署)

# python源码使用



> 如果您使用 macOS，您可以从 [Python 网站](https://www.python.org/downloads)_获取官方安装程序。您可以使用 Python 3.10 以上时任何版本，但避免使用 Alpha、Beta 和候选版本
> 
> 如果您使用的是 Linux，您将使用系统软件包管理器（Debian/Ubuntu/Mint 上的 `apt`，Fedora 上的 `dnf`，或 Arch 上的 `pacman`）安装 Python（Linux一般自带py环境）
> 
> 如果您使用的是 Windows，您可以从 [Python 网站](https://www.python.org/downloads) 获取官方安装程序。您可以使用 Python 3.9 到 3.13 的任何稳定版本。我们还建议避免使用 Alpha、Beta 和候选版本

此外您还需要下载git软件拉取源码

您可以输入以下指令查询您的python版本

```
python3 --version
```

在所有准备完成后，您就可以开始您的python源码使用了

首先使用 `git` 克隆项目：

```bash
git clone https://github.com/CoralHymn/RWMP2_Decryptor.git
```

进入项目目录

```
cd RWMP2_Decryptor
```

安装依赖(您可在此步骤前创建虚拟环境，但不同系统直接操作不同，因此我讲通用的方法)

```bash
# 安装 PyWebIO
pip install pywebio
```

> 如果您是Linux用户，linux自带的py库一般不含tkinter库，因此您需要额外输入
> 
> pip install tkinter

运行脚本

```bash
python run_gui.py
```

成功运行！



# 安装（windows）

您可以在[Releases](https://github.com/CoralHymn/RWMP2_Decryptor/releases)上获取Windows的两个最新版本（已过时，最新版未构建） 

- [RWMP2_Decryptor_Windows_GUI.exe](https://github.com/CoralHymn/RWMP2_Decryptor/releases/download/Alpha_2.1.0/RWMP2_Decryptor_Windows_GUI.exe)
- [RWMP2_Decryptor_Windows_WebUI.exe](https://github.com/CoralHymn/RWMP2_Decryptor/releases/download/Alpha_2.1.0/RWMP2_Decryptor_Windows_WebUI.exe) 

## win使用教程

在此之前需要先把您的rwmod文件后缀改成zip后缀再进行使用

  **GUI**

- 双击打开exe文件（可能需要一些时间，但不会太久）

- 点击“选择zip文件”按钮后，会弹出文件管理器，您可以选择您需要解密的mod文件

- 点击“开始处理”按钮，您可以在下方观看进度，当提示完成时你可以点击“下载处理结果”按钮保存您的文件
  ![wingui](http://hk.coralhymn.com/png/wingui.png)
  
  **WebUI**

- 双击打开exe文件，这时会弹出终端，不用担心，等待一会会自动跳转到默认浏览器打开web页面

- 您可以拖动或点击上传您的zip文件，等待上传完成（是在您本地上的）

- 点击“开始”按钮，等待一会，会弹出下载链接

- 点击下载链接文字就已经开始下载了，可能需要等待一会

- （此版本会自动清理临时文件，所以不用担心）
  ![wingui](http://hk.coralhymn.com/png/winweb.png)

# 安装（Linux）

大多数发行版都可以使用（如果无法使用请联系我） \
您可以在[Releases](https://github.com/CoralHymn/RWMP2_Decryptor/releases)上获取Linux的两个最新版本 （已过时，最新版未构建）\
他们是（application/x-executable）可执行文件

- [RWMP2_Decryptor_Linux_GUI.AppImage](https://github.com/CoralHymn/RWMP2_Decryptor/releases/download/Alpha_2.1.0/RWMP2_Decryptor_Linux_GUI.AppImage)

- [RWMP2_Decryptor_Linux_Web.AppImage](https://github.com/CoralHymn/RWMP2_Decryptor/releases/download/Alpha_2.1.0/RWMP2_Decryptor_Linux_Web.AppImage)（推荐）\
  在您下载完成后，您必须要添加执行权限给文件否则无法运行
  
  ```bash
  chmod +x RWMP2_Decryptor_Linux*.AppImage  # 添加可执行权限
  ```
  
  ## Linux使用教程

在此之前需要先把您的rwmod文件后缀改成zip后缀再进行使用

  **GUI**

  目录输入

```bash
./RWMP2_Decryptor_Linux*.AppImage
```

  -您也可以双击执行文件

- 点击“选择zip文件”按钮后，会弹出文件管理器，您可以选择您需要解密的mod文件

- 点击“开始处理”按钮，您可以在下方观看进度，当提示完成时你可以点击“下载处理结果”按钮保存您的文件
  
  **WebUI** 
  
  目录输入
  
  ```bash
  ./RWMP2_Decryptor_Linux*.AppImage
  ```
  
  -您也可以双击执行文件（但推荐使用./）

- 这时会弹出终端，不用担心，等待一会会自动跳转到默认浏览器打开web页面

- 您可以拖动或点击上传您的zip文件，等待上传完成（是在您本地上的）

- 点击“开始”按钮，等待一会，会弹出下载链接

- 点击下载链接文字就已经开始下载了，可能需要等待一会

- （此版本会自动清理临时文件，所以不用担心）
  
  GUI可能会有报错===解决方法
  
  ```bash
  qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
  This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
  ```

Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, webgl, xcb.

```
这个错误是 Linux 系统上运行 PyQt5 程序时非常常见的问题。错误信息 Could not load the Qt platform plugin "xcb" 表明这个 PyQt5 应用程序无法连接到系统的图形显示服务（通常是 X11）\
确保你的Linux包含了桌面环境 ，如果还是错误那就是因为缺少了 xcb 相关的系统库\
运行以下命令来安装它们（适用于 Ubuntu/Debian）：
```bash
sudo apt-get install libxcb-xinerama0 libxcb-xinerama0-dev
```

如果您其他发行版请寻找您发行版的 xcb 相关的系统库


#### 关于 [ 安卓 | ios | macOS ]

- 这些设备可前往在线网页使用，py开发移动端的软件有些难且麻烦
- 更多平台版本正在开发中，如果您开发了其他平台版本请添加到分支

## ⚠️ 使用声明

- 本软件仅限学习研究用途，使用者必须确保已获得目标文件的合法授权。
- 禁止用于任何未经授权的解密的行为。
- 滥用本工具可能导致严重法律后果，开发者不对任何非法使用行为承担责任。
- 继续使用即表示您已阅读、理解并同意上述条款。 

使用的python库：
[PyWebIO](https://github.com/pywebio/PyWebIO)
