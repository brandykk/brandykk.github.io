+++
title='Win10使用记录'
tags=["windows"]
categories=["windows"]
date="2021-04-17T18:47:06+08:00"
toc=true
+++

## 安装JDK

1. 新建系统变量

   - 变量名： `JAVA_HOME`
   - 变量值：安装目录

2. 新建CLASSPATH变量

   - 变量名： `CLASSPATH`
   - 变量值： `.;%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\lib\tools.jar`

3. 添加Path：

   在系统变量区域，选择Path,点击下面的编辑按钮，在弹出的框中选择新建添加2行，一行输入 %JAVA_HOME%\bin ，一行输入 %JAVA_HOME%\jre\bin

4. 在命令提示符中输入javac命令测试

---

## MAVEN配置

1. 新建系统变量

   - 变量名： `MAVEN_HOME`
   - 变量值：安装目录

2. 添加Path：

   在系统变量区域，选择Path,点击下面的编辑按钮，在弹出的框中选择新建添加 %MAVEN_HOME%\bin

3. 在命令提示符中输入 mvn -v 命令

---

## 安装mariadb代替mysql

1. [下载](https://mariadb.org/download/?t=mariadb&p=mariadb&r=10.6.5&os=Linux&cpu=x86_64&pkg=tar_gz&i=systemd&m=blendbyte)`mariadb`压缩包

2. 配置`mariadb`环境变量

   在`path`中添加mariadb安装文件夹中的bin目录下

3. 在bin目录下执行命令

   > 注意安装实际情况更改路径和密码

   ```cmd
   mysql_install_db.exe --datadir=F:\projectManager\mariadbData --service=mariadb --password=  --port=13306
   # --datadir=后面是数据存放路径，可自定义；--service=后面是服务名称；--password=后面是密码，空就是没有密码；--port=后面是端口号，为了防止和mysql用了13306
   ```

---

## mysql安装 [推荐mariadb](安装mariadb代替mysql)

>安装目录下新建 my.ini 文件（注意修改下面的路径）

```ini
[Client]
#设置3306端口
port = 3306
[mysqld]
#设置3306端口
port = 3306
# 设置mysql的安装目录
basedir=D:\MySQL5.7\mysql-5.7.27-winx64
# 设置mysql数据库的数据的存放目录
datadir=D:\MySQL5.7\mysql-5.7.27-winx64\data
# 允许最大连接数
max_connections=200
# 服务端使用的字符集默认为8比特编码的latin1字符集
character-set-server=utf8
# 创建新表时将使用的默认存储引擎
default-storage-engine=INNODB
sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES
[mysql]
# 设置mysql客户端默认字符集
default-character-set=utf8
#开启查询缓存
explicit_defaults_for_timestamp=true
```

1. 新建系统变量  
变量名称： MYSQL_HOME
变量值： MySQL安装目录

2. 编辑系统变量 Path  
将 %MYSQL_HOME%\bin 添加到 Path即可

3. 管理员身份运行命令提示符cmd  
进入mysql安装bin目录,执行mysqld -install命令进行安装

4. 执行命mysqld --initialize --console令初始化成功后，会生成data目录,并将初始密码打印在控制台

5. 输入启动命令: net start mysql
>输入：mysql -u root -p控制台密码，直接回车  
接着输入以下命令：  
alter user user() identified by "root";	//修改密码为root  
再次输入mysql -u root -proot即可  

6. 卸载服务

```
# 管理员在安装目录的bin目录下执行
.\mysqld.exe --remove mariadb
```



## redis后台启动

在reids安装目录执行命令，将其注册为服务  
`redis-server --service-install redis.windows.conf`

---

## win10双系统删除多余EFI分区

`win10下进行以下操作：`
参考：[CSDN博客](<https://blog.csdn.net/g1027785756/article/details/82999451>)

> - 1. 管理员权限打开cmd控制台，输入：【diskpart】进入命令行分区管理工具
> - 2. 输入【list disk】查看磁盘信息
> - 3. 输入【select disk n】选择所安装的系统EFI分区的磁盘。n：表示磁盘号。 例如：select disk 1；标识选择了磁盘号为1的磁盘
> - 4. 输入【list partition】查看所选磁盘下的分区信息
> - 5. 输入【select partition n】选择EFI分区所在的系统分区上。n：表示分区号。例如：select partition 1；表示选择了当前磁盘下分区号为1的磁盘分区
> - 6. 输入【assign letter=p】p是盘符，只要和自己本地已有的盘符不重复即可，这一步可以将EFI分区转为和普通盘一样的可见磁盘
> - 7. 在我的电脑处查看win10的磁盘会发现多了一个盘，不能直接打开，会提示权限不够
> - 8. 管理员权限打开记事本，从文件打开p盘，会发现有已安装系统的引导，直接删除即可
> - 9. 回到【diskpart】工具处输入【remove letter=p】即可删除p盘—

---

## 定时关机

```cmd
shutdown -s -t 秒数
# 取消关机
shutdown -a
```

## 修改win11计算机名称

> 管理员打开终端执行命令后重启

```po
Rename-Computer -NewName "name"
```

