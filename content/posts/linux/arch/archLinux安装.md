---
title: "ArchLinux安装记录"
date: 2021-06-18T21:14:52+08:00
description: "ArchLinux个人安装记录"
tags: ["arch"]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: linux
comment : true
---

> 更新于2023年3月5日；适用于Arch和win11双系统，btrfs文件系统，kde桌面

[参考](https://blog.csdn.net/kimux/article/details/128700223)

## 准备工作

- **先安装win10,然后再安装linux,关闭主板设置中的 `Secure Boot`,关闭win10的`快速启动`**

- 制作镜像：推荐[ventoy](https://www.ventoy.net/cn/)
- 确保是否为 `UEFI` 模式

```zsh
# 若输出了一堆东西，即` efi `变量，则说明已在 `UEFI `模式。否则请确认你的启动方式是否为 `UEFI`。
ls /sys/firmware/efi/efivars
```

---

## 分区(Btrfs)

[`Btrfs`](https://wiki.archlinux.org/title/Btrfs)文件系统不需要单独区分每个盘的大小，只需要单独分出一个盘即可。

- 单系统需要先将磁盘转为`gpt`格式，双系统的话，在win11上已经转过了，<font color='red'>`/dev/nvme0n1p6`</font>是安装磁盘，根据实际情况改成自己的磁盘

```zsh
# 或者执行命令
lsblk                       #显示分区情况
parted /dev/sdx             #执行parted，进行磁盘类型变更
(parted)mktable             #输入mktable
New disk label type? gpt    #输入gpt 将磁盘类型转换为gpt 如磁盘有数据会警告，输入yes即可
quit                        #最后quit退出parted命令行交互

# 格式化磁盘
mkfs.btrfs -f /dev/nvme0n1p6

# 如果是单个磁盘，不需要要保留磁盘数据则执行以下命令可以直接选择将磁盘转为`gpt`
cfdisk -z /dev/nvme0n1p6
```

- 挂载分区

```zsh
mount /dev/nvme0n1p6 /mnt
```

- 创建子卷

```zsh
# 根据需要在/mnt中创建子卷
btrfs su cr /mnt/@                    # 挂载到 root，必需
btrfs su cr /mnt/@boot                # boot 子卷, 可选
btrfs su cr /mnt/@home                # home ，可选
btrfs su cr /mnt/@var                 # var,  可选
btrfs su cr /mnt/@opt                 # opt,  可选
btrfs su cr /mnt/@snapshot            # 快照文件, 可选
btrfs su cr /mnt/@swap                # swapfile ，可选

#检查创建好的子卷
btrfs su li /mnt

#创建16G的交换文件 大小根据需要更改
btrfs filesystem mkswapfile -s 16g /mnt/@swap/swapfile
```

- 挂载子卷

```zsh
# 先卸载上面创建子卷时的挂载目录，否则会失败
umount /mnt

# 挂载根目录子卷 (这是SSD硬盘的参数，如果是机械硬盘，有些参数不太合适，请自行查询挂载参数）
mount -t btrfs -o defaults,compress-force=zstd:5,space_cache=v2,autodefrag,discard=async,subvol=@ /dev/nvme0n1p6 /mnt

# 创建其他子卷挂载目录 最好和上面的子卷保持一致
mkdir -pv /mnt/{boot,home,var,opt,.snapshot,.swap}

# 挂载创建好的目录
mount -t btrfs -o subvol=@boot /dev/nvme0n1p6 /mnt/boot
mount -t btrfs -o subvol=@home /dev/nvme0n1p6 /mnt/home
mount -t btrfs -o subvol=@var /dev/nvme0n1p6 /mnt/var
mount -t btrfs -o subvol=@opt /dev/nvme0n1p6 /mnt/opt
mount -t btrfs -o subvol=@snapshot /dev/nvme0n1p6 /mnt/.snapshot
mount -t btrfs -o subvol=subvol=@swap /dev/nvme0n1p6 /mnt/.swap

# 挂载win11的EFI分区
mkdir /mnt/boot/efi
mount -t vfat /dev/nvme0n1p6 /mnt/boot/efi

# 激活swap
swapon /mnt/.swap/swapfile
```

---

## 连接网络

```bash
iwctl                           #进入交互式命令行
device list                     #列出设备名，比如无线网卡看到叫 wlan0
station wlan0 scan              #扫描网络
station wlan0 get-networks      #列出网络 比如想连接CMCC-5AQ7这个无线
station wlan0 connect CMCC-5AQ7 #进行连接 输入密码即可
exit                            #成功后exit退出

# 测试
ping www.baidu.com
```

---

## 更新系统时钟

```bash
# timedatectl set-ntp true    #将系统时间与网络时间进行同步（默认启用）
timedatectl status          #检查服务状态
```

---

## 更换国内镜像源加快下载速度

> 新的镜像会自动检查最快的地址，不需要手动更改

```bash
# 在文件中找到自己用的地址，复制到文件最上面
vim /etc/pacman.d/mirrorlist
```

---

## 安装基础系统

```bash

# intel-ucode intel微码
pacstrap -K /mnt base base-devel linux linux-firmware intel-ucode man-page-zh_cn btrfs-progs dhcpcd iwd neovim xsel zsh

# 或 amd-ucode amd微码
pacstrap -K /mnt base base-devel linux linux-firmware amd-ucode man-page-zh_cn btrfs-progs dhcpcd iwd neovim xsel zsh
```

---

## 生成 fstab 文件

```bash
# 执行命令
genfstab -U /mnt >> /mnt/etc/fstab

# 复查一下 /mnt/etc/fstab 确保没有错误
cat /mnt/etc/fstab
```

---

## 进行基础配置

```bash
# 把环境切换到新系统的/mnt 下
arch-chroot /mnt

# 配置neovim
ln -s /bin/nvim /bin/vi
ln -s /bin/nvim /bin/vim

# 设置时区
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime    
hwclock --systohc

# 本地化设置：将文件中需要的en_US、zh_CN注释取消掉
vi /etc/locale.gen
# 执行命令
locale-gen

# 设置语言，不建议zh_CN,中文可能会出现乱码
echo "LANG=en_US.UTF-8" > /etc/locale.conf

# 设置主机名
echo 主机名 > /etc/hostname

# 配置hosts（用tab,不要用空格）
127.0.0.1       localhost
::1             localhost
127.0.0.1       主机名.localdomain    主机名

# 双系统时间
timedatectl set-ntp true
# 如果不生效需要则执行下面命令
# timedatectl set-local-rtc 1

# 安装引导（此时会无法识别win,等进入桌面后再设置）
pacman -S grub efibootmgr os-prober ntfs-3g
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=ArchLinux
grub-mkconfig -o /boot/grub/grub.cfg

# 安装nvidia显卡
pacman -S nvidia-dkms nvidia-settings nvidia-utils

# 安装声卡
pacman -S pipewire pipewire-pulse pipewire-jack pipewire-alsa pavucontrol

# 配置btrfs
vi /etc/mkinitcpio.conf
# 在文件查找MODULES添加btrfs，nvidia（可能会报错，暂时不懂）模块
MODULES = (btrfs)
# 在文件查找BINARIES添加/usr/bin/btrfs
BINARIES (/usr/bin/btrfs)
# 在文件查找HOOKS更改
HOOKS  (去掉fsck 添加 btrfs ）
# 使其生效，注意看是否有报错
mkinitcpio -P

# 配置root密码
passwd

# 新建管理员用户（其实只需要wheel就行了）
useradd -m -G audio,video,wheel,users -s /bin/zsh lv
# 更改用户密码
passwd lv
# 编辑sudo
EDITOR=nvim visudo
# 找到这样的一行,把前面的注释符号#去掉
#%wheel ALL=(ALL:ALL) ALL

# 启用TRIM 会帮助清理 SSD 中的块，从而延长 SSD 的使用寿命
systemctl enable fstrim.timer

# 打开/etc/pacman.conf
vim /etc/pacman.conf
# 找到这一行并取消注释
ParallelDownloads = 5
# 在/etc/pacman.conf文件中取消 VerbosePkgLists 的注释，软件更新时会更方便新旧版本对比
VerbosePkgLists

# 重启
exit                # 退回安装环境#
umount -R  /mnt     # 卸载新分区
reboot              # 重启 记得拔掉U盘
```

---

## 桌面安装

> 重启后，用root登陆

- 连接网络

```zsh
#立即启动dhcp
systemctl start dhcpcd
# 若为无线链接，则还需要启动 iwd 才可以使用 iwctl 连接网络
systemctl start iwd #立即启动iwd
#和之前的方式一样，连接无线网络
iwctl
#列出设备名，比如无线网卡看到叫 wlan0
device list
station wlan0 scan				#扫描网络
station wlan0 get-networks		#列出网络 比如想连接CMCC-5AQ7这个无线
station wlan0 connect CMCC-5AQ7 #进行连接 输入密码即可
exit                            #成功后exit退出
# 测试
ping www.baidu.com
```

- 安装桌面

```zsh
#安装plasma-meta元软件包、终端、文件管理器、文件编辑器 基础中文字体
pacman -Syu plasma-meta konsole dolphin kate wqy-zenhei

# 启用sddm
systemctl enable sddm

# 启用NetworkManager
#确保iwd开机处于关闭状态，其无线连接会与NetworkManager冲突
sudo systemctl disable iwd
sudo systemctl enable NetworkManager

# 启用蓝牙
sudo systemctl enable bluetooth

# 重启
reboot
```

---

## 桌面配置

> 重启用进入kde桌面

- [配置AUR](https://github.com/archlinuxcn/mirrorlist-repo)

```zsh
# 添加AUR 在/etc/pacman.conf配置文件中添加AUR源
vim /etc/pacman.conf
# 去掉[multilib]一节中两行的注释，来开启 32 位库支持。
# AUR仓库地址
[archlinuxcn]
Server = https://mirrors.ustc.edu.cn/archlinuxcn/$arch

# 执行
sudo pacman -Syyu archlinuxcn-keyring

# 安装yay管理AUR
sudo pacman -S yay

# 如果无法安装：
# 安装程序时有可能报签名问题需要安装archlinux-keyring
sudo pacman -Syu haveged
sudo systemctl start haveged
sudo systemctl enable haveged
sudo rm -fr /etc/pacman.d/gnupg
sudo pacman-key --init
sudo pacman-key --populate archlinux
sudo pacman-key --populate archlinuxcn
# 然后重新安装
```

- 更改中文

```zsh
# 在设置中配置中文
# System Settings > Regional Settings > Language -> 单机语言后面的按钮 -> 选择简体中文加入 -> 重启

# 安装win字体
# 将win上C:/Windows/Fonts/中的字体复制到/usr/share/fonts/中，最好新建个文件夹
sudo mkdir /usr/share/fonts/win-fonts
# 进入C:/Windows/Fonts/进行复制
cp ./* /usr/share/fonts/win-fonts
#执行命令 建立字体索引信息，更新字体缓存
# sudo mkfontscale
# sudo mkfontdir
fc-cache -fv
```

- 修改grub

```zsh
# 开机直接进入系统，而没有grub界面（注释掉这一行）
# GRUB_TIMEOUT_STYLE=hidden

# 修改界面等待时间（默认5）
GRUB_TIMEOUT=10

# 记录上次的启动系统:取消注释(btrfs系统不适用),GRUB_DEFAULT
# GRUB_DEFAULT配置：saved 自动记忆上次的系统；0 代表默认选中第一个
GRUB_DEFAULT=2
# GRUB_DEFAULT=saved		# (btrfs文件系统不适用）
# GRUB_SAVEDEFAULT=true	# (btrfs文件系统不适用）

# 去掉`GRUB_CMDLINE_LINUX_DEFAULT`一行中最后的 quiet 参数，同时把 log level 的数值从 3 改成 5。这样是为了后续如果出现系统错误，方便排错。同时在同一行加入 nowatchdog 参数，这可以显著提高开关机速度
GRUB_CMDLINE_LINUX_DEFAULT='log level=5 nowatchdog'

# 双系统识别；最后一行取消注释，如果没有则添加
GRUB_DISABLE_OS_PROBER=false

# 更新grub
sudo grub-mkconfig -o /boot/grub/grub.cfg

# 或执行
# sudo update-grub

# 如果执行报错‘/usr/share/grub/grub-mkconfig_lib:  “$”：无效格式字符’
# sudo LANG=C grub-mkconfig -o /boot/grub/grub.cfg
```

- 开机挂载硬盘

```zsh
#查看已挂载的磁盘，记住要开机挂在的文件系统名
df -h
#查看文件系统名的uuid，记录uuid
ls -l /dev/disk/by-uuid/ | grep sda1
#编辑/etc/fstab
#如果需要自定义挂载点则需要提前建好挂载点的空文件夹，在文件最后添加
UUID=查询的uuid 要挂在到的目录 ntfs defaults 0 0
#UUID是刚刚查询出来的
#ntfs表示格式，小写
#0 0表示开机不检查磁盘。
#然后保存重启，查看
df -h
```

> <font color='red'>重启，保证界面是中文后再进行下面操作，否则可能会导致有些软件默认是英文</font>

---

- 基础包安装。

```bash
# 安装输入法
yay -Syu fcitx5-im fcitx5-chinese-addons fcitx5-pinyin-moegirl fcitx5-pinyin-zhwiki
# 则需要在/etc/environment中配置环境变量
GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
SDL_IM_MODULE=fcitx

# -------------------------------------------------------------------------------------------------

#安装几个开源中文字体 一般装上文泉驿就能解决大多wine应用中文方块的问题
yay -S adobe-source-han-serif-cn-fonts noto-fonts-cjk noto-fonts-emoji noto-fonts-extra

#ark压缩与dolphin同用右键解压
yay -S ark p7zip unrar unarchiver lzop lrzip

#确保Discover(软件中心）可用 图片查看器
yay -S packagekit-qt5 gwenview

#安装常用的火狐、谷歌浏览器
yay -S firefox chromium

# wps
yay -Syu wps-office ttf-wps-fonts  ttf-ms-fonts wps-office-fonts wps-office-mui-zh-cn

# 安卓和kde桌面连接 远程手机文件系统
yay -S kdeconnect sshfs

# 开启自动登陆可用kwalletmanager将钱包密码置空（可选）
yay -S kwalletmanager

# 博客
yay -S hugo

# -------------------------------------------------------------------------------------------------

# 截图软件
yay -S flameshot
# 配置命令
# 普通截图
flameshot gui
# 延迟2秒截图，适合截取鼠标悬停的提示信息
flameshot gui -d 2000
```

---

- oh-my-zsh

```zsh
# 将oh-my-zsh下载至本地home目录 将文件夹内~/.oh-my-zsh/templates/下的文件复制为~/.zshrc文件自行配置
git clone https://github.com/ohmyzsh/ohmyzsh.git ~/.oh-my-zsh

# Powerlevel10k主题
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
# 将.zshrc文件中的主题改掉
ZSH_THEME="powerlevel10k/powerlevel10k" 

# zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# 在.zshrc中启用插件
plugins=(
    zsh-autosuggestions
    zsh-syntax-highlighting
)
```

- neovim

> 新建配置文件：~/.config/nvim/init.vim

```zsh
" vim配置文件
"--------------------------
" 开启代码高亮
syntax on

" 开启行号显示
set number

" 启用鼠标
set mouse=a

" tab键的宽度
set tabstop=4

" 匹配括号高亮的时间（单位是十分之一秒）
set matchtime=5

" 行号突出显示
" 取消可以在单词前加no
set relativenumber

" 正在编辑的一行显示编辑线
set cursorline

" 编辑时文字不会超出编辑区
set wrap

" vim命令模式下tab键提示
set wildmenu

" 高亮搜索内容
set hlsearch

" 正在搜索输入内容便会高亮显示
set incsearch

" 搜索时忽略大小写
set ignorecase

" 搜索时智能识别大小写
set smartcase

" vim与系统剪切板共享
set clipboard=unnamedplus

" 插件安装
call plug#begin('~/.config/nvim/plugged')

" Plug '插件名或者git路径'获取获取插件
" PlugInstall [name ...] [#threads] 安装插件
" PlugUpdate [name ...] [#threads] 安装或者更新插件
" PlugClean[!] 删除没有列出的插件
" PlugUpgrade 升级 vim-plug
" PlugStatus 检查插件状态
" -------------------------------
" markdown预览（需要nodejs和yarn)
Plug 'iamcco/markdown-preview.nvim', { 'do': 'cd app && yarn install' }

" 状态栏主题
Plug 'vim-airline/vim-airline'
" ---------------------------
" 插件安装结束
call plug#end()
```

- JDK、Maven

```zsh
# 解压安装包 路径根据自己需求调整
sudo tar -zxvf ./jdk1.8 -C /opt
sudo tar -zxvf ./maven -C /opt

# -------------------------------------------------------------------------------------------------

# 添加环境变量/etc/profile
# JDK
export JAVA_HOME=/opt/jdk1.8.0_241/
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH

# -------------------------------------------------------------------------------------------------

# MAVEN
export MAVEN_HOME=/opt/apache-maven-3.6.3/
export PATH=$MAVEN_HOME/bin:$PATH

# -------------------------------------------------------------------------------------------------

# 刷新环境变量（只应用于当前窗口）
source /etc/profile
#查看版本
mvn -v
```

- redis、mariadb

```zsh
# 执行命令安装redis
sudo pacman -Syu redis
# 局域网连接：编辑/etc/redis/redis.conf配置文件
# 1.注释掉 bind 127.0.0.1 可以使所有的ip访问redis
# 2.在redis3.2之后，redis增加了protected-mode，默认开启，需要关闭，protected-mode no

# -------------------------------------------------------------------------------------------------

# 执行命令安装mariadb
sudo pacman -Syu mariadb
# 安装完成后根据提示执行命令（此部分会在终端提示）
sudo mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
# 切换root
su
# 启动服务
systemctl start mariadb
# 进入mariadb
mysql -uroot
# 创建一个密码为空的用户lv
# IDENTIFIED BY后面跟密码，''表示没有密码
MariaDB [(none)]> CREATE USER 'lv'@'localhost' IDENTIFIED BY '';
# 给用户'lv'@'localhost'所有的权限
MariaDB [(none)]> GRANT ALL PRIVILEGES ON *.* TO 'lv'@'localhost';

# 先创建lv@'%'这个远程用户访问权限
MariaDB [(none)]> CREATE USER 'lv'@'%' IDENTIFIED BY '';
# 配置允许访问的用户，采用授权的方式给用户权限
MariaDB [(none)]> GRANT ALL PRIVILEGES ON *.* TO 'lv'@'%' IDENTIFIED BY '' WITH GRANT OPTION;
# 注：'lv'@'%'是登陆数据库的用户，IDENTIFIED BY 后面是登陆数据库的密码，*就是意味着任何来源任何主机

# 取消用户权限
# MariaDB [(none)]> revoke all privileges on *.* from fdgl@%;
# 刷新使之生效
MariaDB [(none)]> FLUSH PRIVILEGES;

# 修改密码
ALTER USER 'root'@'localhost' IDENTIFIED by 'root';
FLUSH PRIVILEGES;

# -------------------------------------------------------------------------------------------------

# 数据库工具Navicat无限重置时间
rm -rf ~/.config/navicat/Premium
rm -rf ~/.config/dconf/user
```

- 快捷方式

```zsh
# 创建文件夹
mkdir /home/lv/.local/share/applications

# 创建.desktop后缀文件

[Desktop Entry]
Encoding=UTF-8
# 版本号
Version=1.0
# 名字
Name=yEd
# 完整名字
GenericName=GUI Port Scanner
# 应用启动路径
Exec=java -jar /opt/yed-3.11.1/yed.jar
# 是否在终端运行
Terminal=false
# 图标路径
Icon=/opt/yed-3.11.1/icons/yicon32.png
# 类型
Type=Application
# 应用所属类别，会根据这个在菜单中分类
Categories=Application;Network;Utility;Development
# 详细描述
Comment=yEd Graph Editor
```

- ssh

```zsh
# ssh 用户名@IP -p 端口号
ssh root@127.0.0.1 -p 22

# sshpass
yay -S sshpass
# sshpass -p 密码 ssh 用户名@IP -p 端口号（需要先在控制台执行一次后才能在.zshrc中创建别名）
sshpass -p 'root' ssh root@127.0.0.1 -p 22
# 连接并执行命令
sshpass -p 'R0ck9' ssh -t secadmin@192.168.1.110 'cd /opt/iot/monitor-xunshi && su && exec $SHELL'
```

- IDEA、DataGrip

[临时打开](https://33tool.com/idea/)、[可参考](https://www.exception.site/)

```txt
版本：IntelliJ IDEA 2021.2.3 (Ultimate Edition)
在插件中添加地址：https://plugins.zhile.io
插件：
	IDE Eval Reset	重置时间插件
	Chinese (Simplified) Language Pack/中文语言包
	MyBatisCodeHelper-Pro
	Rainbow Brackets
	Restful Fast Request
	Translation
	Vue.js
	GitToolBox


版本：DataGrip 2022.3.3
在datagrip64.vmoptions文件中添加：
-javaagent:/opt/development/jetbrains/ja-netfilter/ja-netfilter.jar

--add-opens=java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED
--add-opens=java.base/jdk.internal.org.objectweb.asm.tree=ALL-UNNAMED
```

- pacman

```zsh
# 清除无用包
sudo pacman -Rns $(pacman -Qdtq) # 删除孤立软件包

sudo pacman -S package_name     # 安装软件包
sudo pacman -Syyu               # 升级系统 yy标记强制刷新 u标记升级动作
sudo pacman -R package_name     # 删除软件包
sudo pacman -Rs package_name    # 删除软件包，及其所有没有被其他已安装软件包使用的依赖包
sudo pacman -Rn package_name	# 删除包,依赖和配置文件
sudo pacman -Qdt                # 找出孤立包 Q为查询本地软件包数据库 d标记依赖包 t标记不需要的包 dt合并标记孤立包
sudo pacman -Fy                 # 更新命令查询文件列表数据库
sudo pacman -F xxx              # 当不知道某个命令属于哪个包时，用来查询某个xxx命令属于哪个包
pacman -Ss string1				# 查询服务器上的包
pacman -Si package_name			# 查询服务器上的包的详细内容
pacman -Qs string1 				# 查询本地包
pacman -Qi string1 				# 查询本地包的详细内容
pacman -Ql package_name			# 查询已安装软件包所包含文件的列表
sudo pacman -Sc					# 要删除目前没有安装的所有缓存的包，和没有被使用的同步数据库
sudo pacman -Scc 				# 要删除缓存中的全部文件，使用两次-c开关。这是最为激进的方式，将会清空缓存文件夹
pacman -Sw package_name			# 下载包而不安装它
sudo pacman -U /package_name-version.pkg.tar.zst	# 安装一个本地包(不从源里下载）
IgnorePkg=linux					# 想在升级系统时跳过特定的软件包,多软件包可以用空格隔开,如果只打算忽略一次升级，可以使用 --ignore 选项
#改变shell
chsh -s /bin/zsh
```

---

## 可能遇到的问题

---

- 蓝牙无法启动

如果你在连接设备时看见 `journalctl` 的输出有类似的消息：

`a2dp-source profile connect failed for 9C:64:40:22:E1:3F: Protocol not available`

```zsh
# 安装pulseaudio-bluetooth: 蓝牙 (Bluez) 支持
sudo pacman -Syu pulseaudio-bluetooth
# 重启PulseAudio模块
pulseaudio --kill
pulseaudio --start
# 然后重新连接蓝牙
```

- 解压中文乱码

```zsh
# 使用unar解压
sudo pacman -Sy unarchiver

unar -e cp936 ./xx.zip
```

