---
title: "Jdk1.8"
date: 2021-06-20T13:53:54+08:00
description: "java8新特性"
tags: [Java]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: 开发
comment : true
---

## 获取当前日期

```java
LocalDate date = LocalDate.now();
System.out.println("获取当前日期：" + date);
```
```console
获取当前日期：2020-12-23
```

### LocalDate.of(int year, int month, int dayOfMonth)

- 该方法的月份从1开始

```java
LocalDate date = LocalDate.of(2020, 1, 31);
System.out.println("输出时间：" + date);
```
```console
输出时间：2020-01-31
```

## 时间计算

```java
LocalDate date = LocalDate.of(2020, 1, 31);
// 加一天，也可以使用负数-1实现减一天
LocalDate date1 = date.plusDays(1);
// 加月份
LocalDate date2 = date.plusMonths(1);
// 减
LocalDate date3 = date.minusDays(1);
System.out.println("输出时间：" + date);
System.out.println("date加1天：" + date1);
System.out.println("date加1月：" + date2);
System.out.println("date减1天：" + date3);
```
```console
输出时间：2020-01-31
date加1天：2020-02-01
date加1月：2020-02-29
date减1天：2020-01-30
```

## 格式化

### 1. 字符串、时间转换

```java
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

// 日期时间转字符串
LocalDateTime now = LocalDateTime.now();
String nowText = now.format(formatter);
System.out.println("日期转字符串：" + nowText);

// 字符串转日期时间
String datetimeText = "1999-12-31 23:59:59";
LocalDateTime datetime = LocalDateTime.parse(datetimeText, formatter);
System.out.println("字符串转日期：" + datetime);
```
```console
日期转字符串：2020-12-23 14:11:49
字符串转日期：1999-12-31T23:59:59
```

### 2. Date、LocalDateTime转换
- Date --> LocalDateTime
```java
//1.从日期获取ZonedDateTime并使用其方法toLocalDateTime（）获取LocalDateTime
//2.使用LocalDateTime的Instant（）工厂方法
LocalDateTime localDateTime = new Date().toInstant().atZone(ZoneId.systemDefault()).toLocalDateTime();
System.out.println("Date --> LocalDateTime: " + localDateTime);

//我们也可以使用LocalDateTime的FactoryInput（）方法使用系统的默认时区。
LocalDateTime localDateTime1 = LocalDateTime.ofInstant(new Date().toInstant(), ZoneId.systemDefault());
System.out.println("Date --> LocalDateTime: " + localDateTime1);
```
```console
Date --> LocalDateTime: 2020-12-23T14:19:39.227
Date --> LocalDateTime1: 2020-12-23T14:19:39.464
```
- LocalDateTime --> Date

```java
//LocalDateTime --> Date
//1.使用atZone（）方法将LocalDateTime转换为ZonedDateTime
//2.将ZonedDateTime转换为Instant，并从中获取Date
Date date = Date.from(LocalDateTime.now().atZone(ZoneId.systemDefault()).toInstant());
System.out.println("LocalDateTime --> Date: " + date);
```
```console
LocalDateTime --> Date: Wed Dec 23 14:24:34 CST 2020
```
## 将List\<T>转Map\<String,List\<T>>

```java
List<AreaOfOrg> areaOfOrgs = areaOfOrgMapper.countyListAll();
Map<String, List<AreaOfOrg>> map = areaOfOrgs.stream().collect(Collectors.groupingBy(AreaOfOrg::getPOrgNo));
```

## filter

- filter 方法用于通过设置的条件过滤出元素

```java
List<String>strings = Arrays.asList("abc", "", "bc", "efg", "abcd","", "jkl");
// 获取空字符串的数量
long count = strings.stream().filter(string -> string.isEmpty()).count();
```

## 生成随机数集合

```java
//Integer类型
List<Integer> collect = IntStream.range(1, 5).boxed().collect(Collectors.toList());
System.out.println("range()输出结果：" + collect);

List<Integer> collect1 = IntStream.rangeClosed(1, 5).boxed().collect(Collectors.toList());
System.out.println("rangeClosed()输出结果：" + collect1);

int sum = IntStream.range(1, 5).sum();
System.out.println("sum()计算总和：" + sum);

List<Integer> collect2 = IntStream.of(5, 1, 3, 7, 4, 2, 6).sorted().boxed().collect(Collectors.toList());
System.out.println("sorted()排序：" + collect2);
```
```console
range()输出结果：[1, 2, 3, 4]
rangeClosed()输出结果：[1, 2, 3, 4, 5]
sum()计算总和：10
sorted()排序：[1, 2, 3, 4, 5, 6, 7]
```
