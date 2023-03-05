---
title: "Linux基础命令"
date: 2021-10-08T17:24:15+08:00
description: "linux基础命令,基于manjaro发行版学习"
tags: ["linux"]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: linux
comment : true
---

```sh
# 查看内核信息
uname -a
# 查看端口号
-t (tcp) 仅显示tcp相关选项
-u (udp)仅显示udp相关选项
-n 拒绝显示别名，能显示数字的全部转化为数字
-l 仅列出在Listen(监听)的服务状态
-p 显示建立相关链接的程序名
netstat -tunlp | grep 端口号
# 查看当前所有tcp端口
netstat -ntlp
# 查看所有80端口使用情况
netstat -ntulp | grep 80
```

