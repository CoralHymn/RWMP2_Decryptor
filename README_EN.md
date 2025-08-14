# RWMP2_Decryptor

<div align="center">
  
### README_EN.md | README.md

</div>

<div align="center">
  
## https://coralhymn.com/

</div>

## Introduction
  - RWMP2_Decryptor is an unlocking tool for the "RWMP2" MOD encryption utility used in the game "Rusted Warfare"
  - Developed using Python, available in both GUI and WebUI versions
  - This software was created with assistance from "Qwen3-235B-A22B" and "Qwen3-Coder" AI models

----

> If you find this tool useful, please give me a star on Github! \
> Supported platforms: [ *Windows——Linux——Servers* ]

----

## Online version available for cross-platform use (can be deployed on your server)
  https://rw.coralhymn.com/
  Known issue: Download may fail on "via" browser - please use Edge or Chrome
  
- #installation-windows
- #installation-linux
- #server-deployment
  
# Installation (Windows)

Get the latest Windows versions from https://github.com/CoralHymn/RWMP2_Decryptor/releases:
- https://github.com/CoralHymn/RWMP2_Decryptor/releases/download/Alpha_2.1.0/RWMP2_Decryptor_Windows_GUI.exe
- https://github.com/CoralHymn/RWMP2_Decryptor/releases/download/Alpha_2.1.0/RWMP2_Decryptor_Windows_WebUI.exe **(Recommended)** \
  Note❗ Versions before **2.1.0** only support Windows with outdated CLI interface - not recommended \
These are portable executables - just double-click to run

  ## Windows Guide
  
First change your .rwmod file extension to .zip before use
  
  **GUI**
  - Double-click the exe (may take a moment to load)
  - Click "Select ZIP File" to choose your mod file
  - Click "Process" and monitor progress. When complete, click "Download Result" to save
  

  **WebUI**
  - Double-click the exe - a terminal will appear briefly before opening in your default browser
  - Drag & drop or click to upload your ZIP file (processed locally)
  - Click "Start", then wait for the download link to appear
  - Click the link to download (may take a moment)
  - (Temporary files are auto-cleaned)
  

# Installation (Linux)

Works with most distros (contact me if issues occur) \
Get Linux versions from https://github.com/CoralHymn/RWMP2_Decryptor/releases \
These are (application/x-executable) binaries:
- https://github.com/CoralHymn/RWMP2_Decryptor/releases/download/Alpha_2.1.0/RWMP2_Decryptor_Linux_GUI.bin
- https://github.com/CoralHymn/RWMP2_Decryptor/releases/download/Alpha_2.1.0/RWMP2_Decryptor_Linux_Web.bin (Recommended)\
After download, grant execute permissions:
```bash
chmod +x RWMP2_Decryptor_Linux*.bin  # Add executable permission
  ```

  ## Linux Guide
  
First change your .rwmod file extension to .zip before use
  
  **GUI**
  
  Run via terminal:
```bash
./RWMP2_Decryptor_Linux*.bin
  ```
  - Can also double-click (but ./ recommended)
  - Click "Select ZIP File" to choose your mod
  - Click "Process" and monitor progress. When complete, click "Download Result"

  **WebUI** 
  
  Run via terminal:
```bash
./RWMP2_Decryptor_Linux*.bin
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

# Server Deployment

Get Python source from https://github.com/CoralHymn/RWMP2_Decryptor/releases:
- https://github.com/CoralHymn/RWMP2_Decryptor/releases/download/Alpha_2.1.0/RWMP2_Decryptor_Server.py

## Prerequisites

Server requirements:
- Linux server (Ubuntu/CentOS)
- Python 3.6+
- pip installed
- Open port (default 8085) \
If using control panel, skip to ##二、面板部署步骤

## Command Line Deployment
#### Step 1: Upload Code
Upload methods:
- `scp`:
  ```bash
  scp RWMP2_Decryptor_Server.py user@your_server_ip:/home/user/
  ```
- `git` (not recommended - extra files):
  ```bash
  git clone https://github.com/CoralHymn/RWMP2_Decryptor.git
  ```

#### Step 2: Install Dependencies (PyWebIO)
Create venv and install requirements:
```bash
# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate

# Install PyWebIO
pip install pywebio
```
#### Step 3: Run App
Execute:
```bash
python RWMP2_Decryptor_Server.py
```
Access at `http://server_ip:8085`.

#### Step 4: Background Run (nohup/screen)

Persistent operation:
##### Method 1: nohup
```bash
nohup python RWMP2_Decryptor_Server.py > app.log 2>&1 &
```
View logs:
```bash
tail -f app.log
```
##### Method 2: screen
```bash
screen -S pywebio
python RWMP2_Decryptor_Server.py
# Ctrl+A then D to detach
```
Resume:
```bash
screen -r pywebio
```

#### Step 5: Firewall Config
Open port (8085):

- **Ubuntu (ufw)**:
  ```bash
  sudo ufw allow 8085
  ```
- **CentOS (firewalld)**:
  ```bash
  sudo firewall-cmd --permanent --add-port=8085/tcp
  sudo firewall-cmd --reload
  ```
- **Cloud (Aliyun/Tencent)**: Add inbound rule for port 8080.

#### Step 6: (Optional) Nginx Reverse Proxy

For domain access (`http://yourdomain.com`):

1. Install Nginx:
   ```bash
   sudo apt install nginx  # Ubuntu
   ```
2. Config (`/etc/nginx/sites-available/pywebio`):
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://127.0.0.1:8085;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```
3. Enable & restart:
   ```bash
   sudo ln -s /etc/nginx/sites-available/pywebio /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## Panel Deployment (Baota Demo)
### Step 1: Install Python Manager

Baota v7.7+ includes Python project plugin (may need download):

1. Login to Baota
2. Go to 【Website】
3. Find:
   - ✅ **Python Project**

> ⚠ Requires 1GB+ RAM for compilation.

---

### Step 2: Upload Py File

#### Baota File Manager
1. 【Files】→ Create dir like `/www/wwwroot/pywebio_app`
2. Upload `RWMP2_Decryptor_Server.py`

---

### Step 3: Create Python Project

1. Baota homepage → 【Website】→ **Python Project**
2. 【Add Project】

Configure:

| Field | Example | Notes |
|------|--------|------|
| Name | `Any name` | Custom |
| Path | `/www/wwwroot/pywebio_app` | Code directory |
| Python | 3.9 | Your version |
| Entry | `RWMP2_Decryptor_Server.py` | Main file |
| Port | `8085` | App port |

✅ Baota will auto:
- Create venv
- Install deps
- Start project

---

### Step 4: Open Port

1. Baota left menu → 【Security】→ Open port
2. Add: `8085`
3. Save

> ❗ Also open in cloud provider console (Aliyun SG/Tencent FW)!

---

### Step 5: Start Project

In 【Python Project】:
- Find project → 【Start】
- Check logs for success
- 
If shows:
```
Running on http://0.0.0.0:8085
```
Success!

---

### Step 6: Access

Browser:
```
http://your_server_ip:8085
```

Should see the app!

---

### Step 7: (Recommended) Nginx Proxy for HTTPS Domain

#### 1. Add Site
- Baota 【Website】→【Add】
- Domain: `py.yourdomain.com` (DNS to server IP)
- Root: Any (will be overridden)

#### 2. Set Proxy
- Site →【Reverse Proxy】
- Target: `http://127.0.0.1:8085`
- Save
✅ Now accessible via:
```
http://py.yourdomain.com
```
No port needed!

---

## ✅ FAQs & Solutions

| Issue | Fix |
|------|----------|
| "Connection failed" | Check Baota 【Security】and cloud SG for open port |
| Startup fail | Check 【Python Project】logs |
| Blank page | Verify port access |
| Code changes not applying | 【Stop】→【Start】project |



#### About [ Android | iOS | macOS ]
  - More platform versions in development. Feel free to contribute branches.

## ⚠⚠⚠️ Disclaimer

  - For educational/research purposes only. Users must ensure legal authorization for target files.
  - Prohibited for unauthorized decryption.
  - Misuse may lead to legal consequences. Developer assumes no liability for illegal usage.
  - Continued use constitutes acceptance of these terms.
