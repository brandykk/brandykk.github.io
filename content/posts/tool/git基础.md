---
title: "Git基础"
date: 2021-06-20T13:45:44+08:00
description: "git命令基础"
tags: [git]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: 开发
comment : true
---

## git命令

```zsh
# 全局设置提交代码的联系邮箱
git config --global user.email "mescal1993@hotmail.com"

# 全局设置提交代码的显示名称
git config --global user.name "lv"

# 解决每次提交代码都要输入帐号密码： 执行命令，然后在输入一次就好了
git config --global credential.helper store

#初始化本地新的git仓库
git init

#克隆github仓库
git clone 地址

#查看状态
git status

# .：代表添加所有文件
git add . 

# 提交到本地仓库
git commit -m 'update' 

# 推送到服务器
git push

# 从服务器拉取
git pull

# fatal: refusing to merge unrelated histories错误是两个仓库合并导致历史记录不一样导致的
git pull origin master --allow-unrelated-histories --rebase
```

## 配置gitee.io

1. 安装hugo	[中文文档](https://www.gohugo.org/)

```zsh
sudo pacman -Sy hugo
# 在代码根目录
# 创建新模板
hugo new ./content/posts/fire.md
# 启动服务
hugo server
# 打包 在项目根目录下打包，public目录中
hugo
```

### 2. 主题

[github](https://github.com/nodejh/hugo-theme-cactus-plus/blob/master/README_zh-cn.md)

3. [我的地址](https://brandykk.gitee.io/)
