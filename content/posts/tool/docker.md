---
title: "Docker使用"
date: 2022-01-19T20:00:28+08:00
description: "docler简单使用教程"
tags: ["dokcer"]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: tool
comment : true
---

## Docker下载

```sh
# archlinux
sudo pacman -Syu docker
# 将用户lv追加进docker用户组
# 将当前用户添加进docker用户组
sudo gpasswd -a ${USER} docker
```

## Docker运行

```sh
# 修改docker默认镜像安装路径(没有则新建)
vim /etc/docker/daemon.json
# 修改文件中的路径
{
    "registry-mirrors":
        [
            "https://registry.cn-hangzhou.aliyuncs.com",
            "https://hub-mirror.c.163.com"

        ]
} 
# 重新加载配置文件
systemctl daemon-reload
# 启动docker服务
systemctl start/stop docker.service
```

## Docker基础使用

```sh
# 下载镜像
docker pull archlinux

# 运行archlinux
 docker run -it archlinux 
# 停止容器
docker stop<容器ID或容器名>
# 删除镜像之前需要先删除对应的容器
# 查看容器
docker ps -a
# 删除容器
docker rm 容器id
# 查看docker image
docker images
# 删除image
docker rmi 镜像id
```

## Docker中不能使用systemctl问题

```sh
# 执行命令 
# test 是自己起的名字
# archlinux 是镜像名字
docker run --privileged -id --name test archlinux /usr/sbin/init

# 运行刚刚的容器id
docker exec -it b8a0ae8742e2 bash
```
