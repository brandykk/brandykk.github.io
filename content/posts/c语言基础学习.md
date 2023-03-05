---
title: "C语言基础学习"
date: 2021-10-04T17:00:42+08:00
description: "c语言基础学习记录"
tags: ["C"]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: C 
comment : true
---

## 第一个C语言程序

> c语言中在同一个项目中只能有一个主方法入口（main）
>
> 从上往下按照顺序执行代码，所以main方法要在最下面

```c
#include <stdio.h>

//程序入口
int main(){
    //打印内容
    printf("The First C");
    //程序结束
    return 0;
}
```

## 数据类型

- char	字符型
- short   短整型
- int       整型
- long    长整型
- long long    更长的整型
- float   浮点型
- double 双精度浮点型

```c
//数据类型
void dateType(){
    char c = 'a';
    int age = 20;
    long long l = 2000;
    //...
}

int main(){
    printf("The First C\n");
    char c = 'e';
    printf("c:%c\n",c);
    //获取数据类型大小
    printf("%lu\n",sizeof(char));

    printf("%lu\n",sizeof(long ));
    printf("%lu\n",sizeof(long long ));
    //退出
    return 0;
}
```

## 练习

```c
//在控制台输入两个数字
int main(){
    int a = 0;
    int b = 0;
    //控制台输入1,2
    scanf("%d,%d",&a,&b);
    printf("a:%d\n",a);
    printf("b:%d\n",b);
    return 0;
}
```

## 常变量

> 常量用`const`关键字修饰，不可改变

```c
const int num = 10;
```

## 标识符常量

> 用`#define`修饰，值不可改变

```c
#define MAX 100;
void study2(){
    int n = MAX;
    printf("%d",n);
#define MIN 10;
    int a = MIN;
    printf("%d", a);
}
```

## 枚举常量

> 用关键字`enum`修饰

```c
enum Computer{
    DAIER = 1,
    SHENZHOU,
    THINKPAD,
};
int main() {
    enum Computer c = DAIER;
    printf("%d",c);
    return 0;
}

```

## 字符串

> 需要引入头文件`#include <string.h>`

```c
#include <string.h>
//字符串
void string(){
    //在字符串的最后有一个‘\0’表示字符串结束
    char string[] = "string";
    printf("%s\n",string);
    //获取字符串长度
    printf("%lu", strlen(string));
}

int main() {
    string();
    return 0;
}
```

## if判断，选择语句

```c
void ifTest(int a){
    if(a==1){
        printf("%s","1111");
    } else if(a==2){
        printf("%s","222");
    } else{
        printf("%s","aaa");
    }
}

int main() {
    ifTest(1);  
    return 0;
}
```

## 循环

```c
void forTest(int a) {
    for (int i = 0; i < 10; ++i) {
        printf("%d\n", a + i);
        while (a < 10) {
            printf("%d<10\n", a);
            break;
        }
    }

}
```

