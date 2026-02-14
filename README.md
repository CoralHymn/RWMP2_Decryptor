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


- [python](#python源码使用)
- [windows](#win使用教程)
- [Linux](#Linux使用教程)
- 过时的！
- [服务器](https://github.com/CoralHymn/RWMP2_Decryptor/blob/masyer/Server-README_ZH.md)

## python源码使用



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

> 如果您是Linux用户，linux自带的py库一般不含tkinter库，因此您需要额外输入(根据您的发行版使用)
> install python3-tkinter

运行脚本

```bash
python run_gui.py
```

成功运行！



## win使用教程

您可以在[Releases](https://github.com/CoralHymn/RWMP2_Decryptor/releases)上获取Windows的最新版本

- [RWMP2_Decryptor_Windows.exe](https://github.com/CoralHymn/RWMP2_Decryptor/releases/download/Alpha_2.2.0/RWMP2_Decryptor_windows.exe)


- 双击打开exe文件（可能需要一些时间，但不会太久）
- 此时会弹出一个窗口，让您选择，您可以根据您的喜好随意选择
- 点击“选择文件”按钮后，会弹出文件管理器，您可以选择您需要解密的mod文件

- 点击“开始处理”按钮，您可以在下方观看进度，当提示完成时你可以点击“下载处理结果”按钮保存您的文件
  ![wingui](http://hk.coralhymn.com/png/wingui.png)
  ![wingui](http://hk.coralhymn.com/png/winweb.png)

## Linux使用教程

大多数发行版都可以使用（如果无法使用请联系我） \
您可以在[Releases](https://github.com/CoralHymn/RWMP2_Decryptor/releases)上获取Linux的最新版本\
他们是（application/x-executable）可执行文件

- [RWMP2_Decryptor_Linux.AppImage](https://github.com/CoralHymn/RWMP2_Decryptor/releases/download/Alpha_2.2.0/RWMP2_Decryptor_Linux.AppImage)

  在您下载完成后，您必须要添加执行权限给文件否则无法运行
  
  ```bash
  chmod +x RWMP2_Decryptor_Linux.AppImage  # 添加可执行权限
  ```

  目录输入

```bash
./RWMP2_Decryptor_Linux.AppImage
```

  -您也可以双击执行文件

- 点击“选择zip文件”按钮后，会弹出文件管理器，您可以选择您需要解密的mod文件
- 此时会弹出一个窗口，让您选择，您可以根据您的喜好随意选择
- 点击“开始处理”按钮，您可以在下方观看进度，当提示完成时你可以点击“下载处理结果”按钮保存您的文件
  
 

### 关于 [ 安卓 | ios | macOS ]

- 这些设备可前往在线网页使用，py开发移动端的软件有些难且麻烦
- 更多平台版本正在开发中，如果您开发了其他平台版本请添加到分支

## ⚠️ 使用声明

- 本软件仅限学习研究用途，使用者必须确保已获得目标文件的合法授权。
- 禁止用于任何未经授权的解密的行为。
- 滥用本工具可能导致严重法律后果，开发者不对任何非法使用行为承担责任。
- 继续使用即表示您已阅读、理解并同意上述条款。 

使用的python库：
[PyWebIO](https://github.com/pywebio/PyWebIO)
