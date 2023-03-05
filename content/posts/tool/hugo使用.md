---
title: "Hugo使用"
date: 2021-06-18T20:48:28+08:00
description: "记录hugo博客使用方法"
tags: [hugo]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: tool 
comment : true
---

## 安装hugo

```zsh
#arch
sudo pacman -Sy hugo
```

## 初始化博客

```zsh
# 例如初始化site博客
hugo new site /path/to/site
```

## 创建文章

```zsh
# 在博客根目录执行
cd /path/to/site
# 初始化md文件
hugo new about.md
# 初始化md文件并放在post文件夹下
hugo new post/first.md
```

## 主题

```zsh
# 主题都在themes目录下
cd themes
# 下载主题
git clone ....
```

## 运行测试

```zsh
hugo server
# 然后在浏览器中打开输出的地址
```

## 部署

```zsh
# 执行命令
hugo
# 生成public文件夹，文件夹中的便是最终可以部署的文件
```

