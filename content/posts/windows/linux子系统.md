---
title: "Linux子系统"
date: 2022-06-13T09:50:21+08:00
description: "win11上linux子系统安装archlinux"
tags: [“windows”]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: "windows"
comment : true
---

## 在win11上安装archlinux子系统

> 需要先开启linux子系统和虚拟平台服务,[参考](https://zhuanlan.zhihu.com/p/417410431)

### 1. 下载linux内核升级包

[双击安装即可](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi)

### 2. 将`WSL2`设置为默认版本

```powershell
# 管理员输入命令
wsl --set-default-version 2
```

### 3. 安装LxRunOffline

> 默认会安装在C盘，用这个工具可以指定安装路径

[github下载](https://github.com/DDoSolitary/LxRunOffline/releases)解压，里面的exe不需要安装，可以将exe路径配置环境变量方便使用，或者在exe所在的文件夹下打开控制台使用命令

### 4. 下载ArchLinux

[下载tar.gz版本(清华源)](https://mirrors.tuna.tsinghua.edu.cn/archlinux/iso/latest/)，也可以在官网找

### 5. 安装到WSL

```powershell
# LxRunOffline i -n <自定义名称> -f <Arch镜像位置> -d <安装系统的位置> -r root.x86_64

LxRunOffline i -n archlinux -f D:\WSL\archlinux_img\archlinux-bootstrap-2021.10.01-x86_64.tar.gz  -d  D:\WSL\archlinux -r root.x86_64
```

### 6. 进入系统

```powershell
# wsl -d <名字>
wsl -d archlinux
```

如果此处报：**FATAL: kernel too old**

输入一下命令，进行转行

```powershell
# 命令格式：
# wsl --set-version <名称> 2
# 如：
wsl --set-version archlinux 2
```

### 7. 首次进入系统执行命令

```sh
pacman -Syy
pacman-key --init
pacman-key --populate
```

## 8. 移除linux

```cmd
# 查看已安装的系统
wsl -l -v
# 卸载
wsl --unregister 名字
```

## 9. 创建新用户

```zsh
useradd -m -G wheel -s /bin/bash <用户名>
# 将文件/etc/sudoers中的wheel ALL=(ALL) ALL那一行前面的注释去掉

# 查看当前用户id
id -u <用户名>

# 退出linux
lxrunoffline su -n <你的arch名字> -v <账户id>
```

## 10. 导入导出镜像

```zsh
# 导出
wsl --export Arch  F:\Arch.tar
#导入
wsl --import Arch d:\Arch F:\Arch.tar --version 2
```

## 11. 重启WSL

```
wsl --shutdown
```

## 12. 开启systemctl和默认用户

```zsh
vim /etc/wsl.conf
[boot]
systemd=true
[user]
default=用户名
```

## 13.mariadb开机自启

> wsl2启动mariadb时无法创建mysql文件夹，需要手动创建

```zsh
# 编写脚本 mariadb.local 文件
# mkdir /run/mysql & chown -R mysql:mysql /run/mysql & systemctl start mariadb.service

chmod +x ~/mariadb.local

# vim /usr/lib/systemd/system/mariadb-local.service

[Unit]
Description="mariadb databases start servece"

[Service]
Type=forking
ExecStart=/root/mariadb.local start
TimeoutSec=0
StandardInput=tty
RemainAfterExit=yes
SysVStartPriority=99

[Install]
WantedBy=multi-user.target

# systemctl enable mariadb-local.service
```

