 
## CMD命令汇总

下面是 **Windows CMD（命令提示符）中最常用的命令汇总**，共 30 个，包含说明和典型代码示例，适合日常开发、系统操作、文件管理、网络诊断等场景。

* * *

### 一、文件与目录操作（最常用）

| 命令 | 说明 | 示例 |
| --- | --- | --- |
| `dir` | 显示当前目录下的文件和子目录 | `dir /w` 宽格式显示 |
| `cd` / `chdir` | 切换目录 | `cd C:\Users\user\Desktop` |
| `md` / `mkdir` | 创建新目录 | `mkdir myfolder` |
| `del` | 删除文件 | `del test.txt` |
| `rd` / `rmdir` | 删除目录 | `rmdir /s myfolder`（含子项） |
| `copy` | 复制文件 | `copy a.txt d:\backup\a.txt` |
| `xcopy` | 高级复制（支持目录） | `xcopy mydir d:\backup /E /I` |
| `move` | 移动/重命名文件或目录 | `move a.txt d:\backup\` |
| `type` | 显示文件内容 | `type readme.txt` |
| `cls` | 清屏 | `cls` |

* * *

### 二、系统管理命令

| 命令 | 说明 | 示例 |
| --- | --- | --- |
| `tasklist` | 显示当前运行的进程列表 | `tasklist` |
| `taskkill` | 终止进程 | `taskkill /IM notepad.exe /F` |
| `systeminfo` | 显示系统信息 | `systeminfo` |
| `hostname` | 显示计算机名 | `hostname` |
| `set` | 查看/设置环境变量 | `set JAVA_HOME=C:\Java` |
| `echo` | 输出文本或变量 | `echo Hello World`，`echo %PATH%` |
| `pause` | 暂停脚本执行，按任意键继续 | `pause` |
| `exit` | 退出命令行或脚本 | `exit` |

* * *

### 三、磁盘与文件系统工具

| 命令 | 说明 | 示例 |
| --- | --- | --- |
| `chkdsk` | 检查磁盘错误 | `chkdsk C:` |
| `diskpart` | 启动磁盘分区工具 | `diskpart`（进入交互模式） |
| `format` | 格式化磁盘 | `format E: /FS:NTFS` |
| `label` | 查看或更改磁盘标签 | `label E:` |

* * *

### 四、网络命令（排障必备）

| 命令 | 说明 | 示例 |
| --- | --- | --- |
| `ipconfig` | 显示本机 IP 配置 | `ipconfig /all` |
| `ping` | 测试网络连接 | `ping www.baidu.com` |
| `tracert` | 路由跟踪 | `tracert www.google.com` |
| `netstat` | 查看端口/连接 | `netstat -an` |
| `nslookup` | DNS 查询 | `nslookup www.baidu.com` |
| `netsh` | 网络配置工具 | `netsh wlan show profiles` |
| `ftp` | FTP 客户端 | `ftp ftp.example.com` |

* * *

### 五、用户与权限

| 命令 | 说明 | 示例 |
| --- | --- | --- |
| `net user` | 用户管理 | `net user` 查看用户；`net user user1 /add` 添加用户 |
| `runas` | 以其他用户身份运行程序 | `runas /user:Administrator cmd` |
| `whoami` | 显示当前登录用户 | `whoami` |
| `attrib` | 修改文件属性 | `attrib +r file.txt`（设为只读） |

* * *

### 六、实用脚本技巧（批处理常用）

#### 输出变量

```cmd
set name=Tom
echo Hello, %name%
```

#### 简单循环

```cmd
for %%f in (*.txt) do echo %%f
```

#### 条件判断

```cmd
if exist "data.txt" (
echo File exists
) else (
echo File not found
)
```

* * *

### 附加建议

#### 推荐使用 `help` 或 `/？` 获取命令帮助：

```cmd
help xcopy
xcopy /?
```

#### 用于日志排查的命令示例：

```cmd
type error.log | find "ERROR"
findstr /i "exception" *.log
```

* * *

### CMD vs PowerShell

虽然 CMD 是经典的 Windows Shell，但在日常开发中，**推荐使用 PowerShell（功能更强）**。比如：

| 功能 | CMD 示例 | PowerShell 示例 |
| --- | --- | --- |
| 获取进程 | `tasklist` | `Get-Process` |
| 获取服务 | `sc query` | `Get-Service` |
| 网络信息 | `ipconfig` | `Get-NetIPAddress` |

* * *

## 实战示例

### Windows CMD 批处理（.bat）自动化脚本

下面是适用于 **Windows CMD 批处理（.bat）自动化脚本**的多套通用模板，涵盖：

1.  项目环境初始化脚本
2.  日志清理/备份自动化脚本
3.  一键部署/启动服务脚本
4.  异常日志扫描脚本
5.  定时任务设置方式（配合计划任务）

* * *

### 1\. 项目环境初始化（示例：拷贝配置、设置环境变量）

**init\_project.bat**

```bat
@echo off
echo [INFO] 初始化项目环境...
REM 创建项目目录
mkdir logs
mkdir output
REM 拷贝模板配置文件
copy config\template.conf config\app.conf
REM 设置环境变量（当前窗口有效）
set PYTHONPATH=%CD%\src
echo 当前 PYTHONPATH 设置为：%PYTHONPATH%
pause
```

* * *

### 2\. 自动清理日志或备份日志

**cleanup\_logs.bat**

```bat
@echo off
echo [INFO] 清理 7 天前的日志文件...
forfiles /p "logs" /s /m *.log /d -7 /c "cmd /c del @file"
echo [INFO] 备份日志...
xcopy logs backup_logs /E /Y
pause
```

> `forfiles` 是非常强大的 CMD 工具，可按日期批量删除或操作文件。

* * *

### 3\. 一键部署 / 启动服务

**deploy.bat**

```bat
@echo off
echo [INFO] 开始部署服务...
REM 拉取最新代码
cd /d D:\MyProject
git pull
REM 激活 Python 虚拟环境并运行服务
call venv\Scripts\activate.bat
python app.py
pause
```

* * *

### 4\. 自动扫描异常日志

**scan\_logs.bat**

```bat
@echo off
echo [INFO] 开始扫描日志中的异常...
REM 支持大小写敏感搜索“error”或“exception”
findstr /i "error exception failed" logs\*.log > found_errors.txt
if %errorlevel% equ 0 (
echo [FOUND] 异常日志内容已保存至 found_errors.txt
) else (
echo [OK] 暂未发现异常信息
)
pause
```

* * *

### 5\. 设置定时任务（每日自动执行某脚本）

在 CMD 中执行以下命令：

```cmd
schtasks /create /tn "LogScanTask" /tr "D:\scripts\scan_logs.bat" /sc daily /st 09:00
```

-   `/tn`: 任务名称
-   `/tr`: 脚本路径
-   `/sc`: 计划类型（daily）
-   `/st`: 启动时间（09:00）

* * *

### 附加技巧

#### 获取当前时间并写入日志

```bat
echo [%date% %time%] 服务启动 >> logs\run.log
```

#### 自动重启脚本（常用于守护）

```bat
:loop
python app.py
echo [WARN] 程序退出，5 秒后重启...
timeout /t 5
goto loop
```

* * *

### 常见目录结构建议

```mipsasm
D:\MyProject\
├── run.bat
├── init_project.bat
├── logs\
├── config\
├── backup_logs\
└── venv\
```

* * *
 
