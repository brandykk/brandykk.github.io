#!/usr/bin/bash
# 文件备份脚本

#备份路径固定部分
path="/run/media/brandy/store/git_repositories/linux-study/backup/"
# 备份文件最终生成名
file_name_finally=""

if [[ ! -e $1 ]]; then
  echo "文件不存在，无法备份"
  exit 99
fi

# 获取备份后的文件名
get_file() {
  # 获取最后一个/之前的字符，将路径去掉只留下文件名
  local file_name_suffix=${1##*/}
  if [[ ${file_name_suffix} != *"."* ]]; then
    local file_name=${file_name_suffix}
    local suffix=""
  else
    # 去掉文件后缀
    local file_name=${file_name_suffix%.*}
    # 获取文件后缀
    local suffix=.${1##*.}
  fi
  # 生成年-月-日
  #  local time=$(date +%Y-%m-%d)
  #  生成时间戳
  local timestamp=$(($(date '+%s') * 1000 + $(date '+%N') / 1000000))
  # 拼接 文件名字+时间+后缀
  file_name_finally=${file_name}_${timestamp}${suffix}
  echo "生成文件名：${file_name_finally}"
  # 对path进行拼接 固定的路径/文件名——backup/年-月-日
  path=${path}${file_name}_"backup/$(date +%Y-%m-%d)/"
}

# 获取文件备份路径
create_path() {
  read -rp "文件完整路径为：（${path}${file_name_finally}），是否继续操作（y/n）: " flag_one
  if [[ ${flag_one} != "y" ]]; then
    echo "你取消了备份"
    exit 100
  fi

  if [[ ! -d ${path} ]]; then
    read -rp "文件路径（${path}）目录不存在，是否创建（y/n）: " flag_two
    if [[ ${flag_two} != "y" ]]; then
      echo "你取消了备份"
      exit 100
    fi
    mkdir -p "${path}"
  fi
}
# 获取备份文件的路径 存放在全局变量path中
get_file $1
# 创建文件保存目录
create_path
# 复制文件
cp -iv "$1" "${path}${file_name_finally}"
# 在文件夹中创建readme文件，记录备份文件的原始路径
echo -e "# 原始文件路径: \\n$1\\n# 备份的文件名：\\n${path}${file_name_finally}\\n################################" >>"${path}../readme"
