---
title: "Java中常用工具类"
date: 2021-07-20T21:53:26+08:00
description: "java中常用的方便使用的工具合集"
tags: ["java","utils"]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: java
comment : true
---

## java自带的方法

1. List集合拼接成以逗号分隔的字符串

```java
        //将list转为字符串
        List<String> strings = Arrays.asList("a,b,c,d");
		//List<String> strings = Collections.singletonList("a,b,c,d");
        System.out.println(strings);//[a,b,c,d]

        //第一种方法: stream流
        String collect = strings.stream().collect(Collectors.joining(","));
        System.out.println(collect);//a,b,c,d

        //第二种方法: String自己的join方法
        String join = String.join(",", strings);
        System.out.println(join);//a,b,c,d
```

2. 比较字符串是否相等,忽略大小写

```java
if (strA.equalsIgnoreCase(strB)) {  
  System.out.println("相等");  
}  
```

3. 比较两个对象

> 当我们用equals比较两个对象是否相等的时候，还需要对左边的对象进行判空，不然可能会报空指针异常，我们可以用java.util包下Objects封装好的比较是否相等的方法

```java
Objects.equals(strA, strB);  
```

> 源码是这样的

```java
public static boolean equals(Object a, Object b) {  
    return (a == b) || (a != null && a.equals(b));  
}  
```

4. 两个List集合取交集

> 必须是ArrayList

```java
List<String> list1 = new ArrayList<>();  
list1.add("a");  
list1.add("b");  
list1.add("c");  
List<String> list2 = new ArrayList<>();  
list2.add("a");  
list2.add("b");  
list2.add("d");  
list1.retainAll(list2);  
System.out.println(list1); // 输出[a, b]  
```

## apache commons工具类库

> apache commons是最强大的，也是使用最广泛的工具类库，里面的子库非常多，下面介绍几个最常用的

###  commons-lang，java.lang的增强版

> 建议使用commons-lang3，优化了一些api，原来的commons-lang已停止更新

```xml
<dependency>  
    <groupId>org.apache.commons</groupId>  
    <artifactId>commons-lang3</artifactId>  
    <version>3.12.0</version>  
</dependency>  
```

1. 首字母转成大写

```java
String str = "yideng";  
String capitalize = StringUtils.capitalize(str);  
System.out.println(capitalize); // 输出Yideng  
```

2. 重复拼接字符串

```java
// Date类型转String类型  
String date = DateFormatUtils.format(new Date(), "yyyy-MM-dd HH:mm:ss");  
System.out.println(date); // 输出 2021-05-01 01:01:01  
  
// String类型转Date类型  
Date date = DateUtils.parseDate("2021-05-01 01:01:01", "yyyy-MM-dd HH:mm:ss");  
  
// 计算一个小时后的日期  
Date date = DateUtils.addHours(new Date(), 1);  
```

3. 包装临时对象

> 当一个方法需要返回两个及以上字段时，我们一般会封装成一个临时对象返回，现在有了Pair和Triple就不需要了

```java
// 返回两个字段  
ImmutablePair<Integer, String> pair = ImmutablePair.of(1, "yideng");  
System.out.println(pair.getLeft() + "," + pair.getRight()); // 输出 1,yideng  
// 返回三个字段  
ImmutableTriple<Integer, String, Date> triple = ImmutableTriple.of(1, "yideng", new Date());  
System.out.println(triple.getLeft() + "," + triple.getMiddle() + "," + triple.getRight()); // 输出 1,yideng,Wed Apr 07 23:30:00 CST 2021  
```

### commons-collections 集合工具类

```xml
<dependency>  
    <groupId>org.apache.commons</groupId>  
    <artifactId>commons-collections4</artifactId>  
    <version>4.4</version>  
</dependency> 
```

1. 集合取交集

```java
// 两个集合取交集  
Collection<String> collection = CollectionUtils.retainAll(listA, listB);  
// 两个集合取并集  
Collection<String> collection = CollectionUtils.union(listA, listB);  
// 两个集合取差集  
Collection<String> collection = CollectionUtils.subtract(listA, listB);  
```

### common-beanutils 操作对象

```xml
<dependency>  
    <groupId>commons-beanutils</groupId>  
    <artifactId>commons-beanutils</artifactId>  
    <version>1.9.4</version>  
</dependency>  
```

1. 对象和map互转

```java
// 对象转map  
Map<String, String> map = BeanUtils.describe(user);  
System.out.println(map); // 输出 {"id":"1","name":"yideng"}  
// map转对象  
User newUser = new User();  
BeanUtils.populate(newUser, map);  
System.out.println(newUser); // 输出 {"id":1,"name":"yideng"}  
```

### commons-io 文件流处理

```xml
<dependency>  
    <groupId>commons-io</groupId>  
    <artifactId>commons-io</artifactId>  
    <version>2.8.0</version>  
</dependency>  
```

1. 文件处理

```java
File file = new File("demo1.txt");  
// 读取文件  
List<String> lines = FileUtils.readLines(file, Charset.defaultCharset());  
// 写入文件  
FileUtils.writeLines(new File("demo2.txt"), lines);  
// 复制文件  
FileUtils.copyFile(srcFile, destFile);  
```

