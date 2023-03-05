---
title: "Java枚举使用"
date: 2021-07-08T21:25:54+08:00
description: "枚举简单使用"
tags: [java]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: java
comment : true
---

## 实现接口,相当于简单的抽象工厂

### 接口方法

```java
//接口方法
interface EnumInterface{
    void show();
}
```

### 枚举

```java
//实现接口并重写方法
enum Enumenum implements EnumInterface{
    AAA(1){
        @Override
        public void show() {
            System.out.println("AAA");
        }
    },
    BBB(2){
        @Override
        public void show() {
            System.out.println("BBB");
        }
    }
    ;
    private int i;

    //通过i调用show()
    static void getEnumbyI(int a){
        Arrays.stream(Enumenum.values()).filter(item->item.getI() == a).findFirst().get().show();
    }

    //构造方法
    Enumenum(int i) {
        this.i = i;
    }

    public int getI() {
        return i;
    }
}
```

### 测试

```java
/**
 * 枚举的使用
 */
public class EnumApplication {
    public static void main(String[] args) {
        getEnumByI();
    }

    //通过值获取枚举的方法
    private static void getEnumByI(){
        try {
            Enumenum.getEnumbyI(1);
        } catch (NoSuchElementException e) {
            System.out.println("枚举中没有此值");
        }
    }
}
```

