# 服务器部署（2.1.0版本）


<div align="center">
  
### [🇺🇸 English](Server-README_EN.md) | [🇨🇳 简体中文](Server-README_ZH.md)

</div>

## 此部署已过时，为了您的服务器安全，本人不推荐使用
## 此部署已过时，为了您的服务器安全，本人不推荐使用
> 当然，除非您/真的/知道自己在做什么

您可以在[Releases](https://github.com/CoralHymn/RWMP2_Decryptor/releases)上获取python源码 

- [RWMP2_Decryptor_Server.py](https://github.com/CoralHymn/RWMP2_Decryptor/releases/download/Alpha_2.1.0/RWMP2_Decryptor_Server.py)

## 一、准备工作

服务器环境要求

- 一台 Linux 服务器（如 Ubuntu/CentOS）
- Python 3.6+
- 安装 pip
- 允许开放端口（该源码端口为8085）\
  如果您的服务器配置了面板服务，就可以不用敲命令了[跳过命令行](#二、面板部署步骤)

## 二、命令行部署步骤

#### 步骤 1：上传代码到服务器

你可以通过以下方式将代码上传到服务器：

- `scp` 命令：
  
  ```bash
  scp RWMP2_Decryptor_Server.py user@your_server_ip:/home/user/
  ```

- 使用 `git` 克隆项目（不推荐，因为有多余的代码）：
  
  ```bash
  git clone https://github.com/CoralHymn/RWMP2_Decryptor.git
  ```

#### 步骤 2：安装依赖（PyWebIO）

登录服务器，进入项目目录，创建虚拟环境（推荐）并安装依赖：

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装 PyWebIO
pip install pywebio
```

#### 步骤 3：运行应用

在服务器上运行脚本：

```bash
python RWMP2_Decryptor_Server.py
```

应用将在 `http://服务器IP:8085` 上运行。

#### 步骤 4：后台运行（使用 `nohup` 或 `screen`）

避免关闭终端后程序停止，使用后台运行：

##### 方法 1：使用 `nohup`

```bash
nohup python RWMP2_Decryptor_Server.py > app.log 2>&1 &
```

查看日志：

```bash
tail -f app.log
```

##### 方法 2：使用 `screen`

```bash
screen -S pywebio
python RWMP2_Decryptor_Server.py
# 按 Ctrl+A, 再按 D 退出 screen
```

恢复 screen：

```bash
screen -r pywebio
```

#### 步骤 5：配置防火墙和安全组

确保服务器防火墙开放了你使用的端口（如 8085）：

- **Ubuntu（ufw）**：
  
  ```bash
  sudo ufw allow 8085
  ```

- **CentOS（firewalld）**：
  
  ```bash
  sudo firewall-cmd --permanent --add-port=8085/tcp
  sudo firewall-cmd --reload
  ```

- **云服务器（如阿里云、腾讯云）**：在控制台安全组中添加入站规则，开放端口 8080。

#### 步骤 6：（可选）使用 Nginx 反向代理

如果你想通过域名访问（如 `http://yourdomain.com`），可以配置 Nginx：

1. 安装 Nginx：
   
   ```bash
   sudo apt install nginx  # Ubuntu
   ```

2. 配置 Nginx 反向代理（`/etc/nginx/sites-available/pywebio`）：
   
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;  # 或服务器IP
   
       location / {
           proxy_pass http://127.0.0.1:8085;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

3. 启用配置并重启 Nginx：
   
   ```bash
   sudo ln -s /etc/nginx/sites-available/pywebio /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## 二、面板部署步骤

（宝塔面板演示）

### 第一步：安装 Python 项目管理器

宝塔从 **v7.7+** 开始内置了「Python 项目」插件，但是默认没有下载。

1. 登录宝塔面板
2. 进入【网站】
3. 找到：
   - ✅ **Python 项目**

> ⚠️ 注意：确保你的服务器有足够内存（建议 1G 以上），否则编译可能失败。

---

### 第二步：上传你Py文件

#### 用宝塔【文件】功能上传

1. 进入【文件】→ 找到或新建一个目录，比如 `/www/wwwroot/pywebio_app`
2. 把 Python 脚本（如 `RWMP2_Decryptor_Server.py`）上传进去

---

### 第三步：创建并配置 Python 项目

1. 回到宝塔首页 → 【网站】→ 打开 **Python 项目**
2. 点击【添加项目】

填写以下信息：

| 字段       | 示例值                                | 说明                  |
| -------- | ---------------------------------- | ------------------- |
| 项目名称     | `随便填写`                             | 自定义名称               |
| Python环境 | Python 3.9                         | 根据你安装的版本选           |
| 启动方式     | `命令行启动`                            | 一般来说选择这个选项          |
| 项目路径     | `/www/wwwroot/pywebio_app`         | 你的代码所在目录            |
| 启动命令     | `python RWMP2_Decryptor_Server.py` | 主程序文件               |
| 环境变量     | `无`                                | 这个不用写               |
| 安装依赖包    | `路径/requirements.txt`              | 仓库里面的requirements文件 |

✅ 提交后，宝塔会自动：

- 创建虚拟环境
- 安装依赖
- 启动你的项目

---

### 第四步：放行端口

1. 宝塔左侧 → 【安全】→ 放行端口
2. 添加端口：`8085`
3. 保存

> ❗ 同时去云服务商控制台（如阿里云安全组、腾讯云防火墙）开放 `8085` 端口！

---

### 第五步：启动项目

在【Python 项目管】中：

- 找到你的项目 → 点击【启动】

- 查看日志确认是否成功运行

- 如果看到：
  
  ```
  Running on http://0.0.0.0:8085
  ```
  
  说明成功了！

注意，部分情况下会显示

```
（ModuleNotFoundError: No module named 'pywebio'，具体以网页为准）
```

不用担心，先去完成第六步
---

### 第六步：访问你的应用

打开浏览器，输入：

```
http://你的服务器IP:8085
```

你应该能看到py文件的页面！

---

### 第七步：（推荐）用 Nginx 反向代理，实现域名访问 + HTTPS

#### 1. 添加网站

- 宝塔【网站】→【添加站点】
- 域名填：`py.yourdomain.com`（记得 DNS 解析到服务器 IP）
- 根目录随便选（后续会被代理覆盖）

#### 2. 设置反向代理

- 进入该站点 →【反向代理】

- 目标 URL 填：`http://127.0.0.1:8085`

- 保存
  ✅ 完成后，你的应用就可以通过：
  
  ```
  http://py.yourdomain.com
  ```
  
  安全访问，无需端口号！

---

## ✅ 常见问题 & 解决方案

| 问题         | 解决方法                   |
| ---------- | ---------------------- |
| 访问显示“无法连接” | 检查宝塔【安全】和云服务商安全组是否开放端口 |
| 项目启动失败     | 查看【Python项目管理器】的日志，看报错 |
| 页面空白       | 检查 端口是否放行              |
| 修改代码后不生效   | 在宝塔中【停止】→【启动】项目        |
