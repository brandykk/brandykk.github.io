#!/bin/python

import sys
import os
import time

backupPath = "/mnt/store/project-manage/gitee-io/git-source/brandy-blog/content/posts/linux/backup/"

# 接收脚本执行的参数
filePath = ""
try:
    filePath = sys.argv[1]
    print("接收到的内容为：%s" % filePath)
except IndexError:
    print("请添加需要备份的文件名。")
    sys.exit(0)


# 截取文件名
def get_file_name(file_path):
    # 最终的文件复制路径
    back_path = ""
    # 获取最终复制的文件名和后缀
    back_file_name = ""
    try:
        # 获取文件名
        file_name = os.path.basename(file_path)
        print("文件名： %s" % file_name)

        # 将文件路径的符号替换为“-”
        dir_name = file_path.replace("/", "-").replace("_", "-").replace(".", "-")[1:]
        print("文件夹名：%s" % dir_name)

        # 获取时间
        time_time = time.time()
        # 最终的文件复制路径
        back_path = backupPath + dir_name + "-backup/" + time.strftime("%Y-%m-%d", time.localtime(time_time))
        print("最后路径：%s" % back_path)

        # 文件夹不存在则创建
        if not os.path.exists(back_path):
            os.makedirs(back_path)

        # 获取最终复制的文件名和后缀
        back_file_name = str(int(time_time * 1000)) + "-" + file_name
        print("最后文件名：%s" % back_file_name)
        # 执行复制命令
        os.system("cp -iv " + file_path + " " + back_path + "/" + back_file_name)

        # 将内容输出到文件 a+:如果文件不存在就创建，存在就在文件内容后面追加内容
        t = open(back_path + "/readme.txt", "a+")
        print("# 文件名：" + back_file_name, file=t)
        print("# 原始文件路径：" + file_path, file=t)
        print("##############", file=t)
        t.close()
    except Exception as e:
        # 将异常信息保存
        print("备份异常：%s" % e)
        t = open(back_path + "/exception.txt", "a+")
        print("# 文件名：" + back_file_name, file=t)
        print("# 原始文件路径：" + file_path, file=t)
        print("文件备份异常：%s" % e, file=t)
        print("##############", file=t)
        t.close()


pathList = []
if "all" == filePath.lower():
    pathList = [
        # manjaro 主配置文件
        "/etc/profile",
        # manjaro 配置软件源文件
        "/etc/pacman.conf",
        # nevim配置文件
        "/home/lv/.config/nvim/init.vim",
        # host配置
        "/etc/hosts",
        # 数据库配置
        "/etc/my.cnf",
        # zsh配置
        "/home/lv/.zshrc",
        # 个人用户其他配置
        "/home/lv/.xprofile",
    ]
else:
    if '' != filePath:
        pathList.append(filePath)
    else:
        print("请输入文件")

for item in pathList:
    get_file_name(item)
