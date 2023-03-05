---
title: "Jdbc"
date: 2021-08-05T22:01:35+08:00
description: "jdbc连接"
tags: ["mybatis"]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: java
comment : true
---

## JDBC程序

```java
 private static void jdbcUtil() throws ClassNotFoundException, SQLException {
        //1. 加载驱动
        Class.forName("com.mysql.jdbc.Driver");

        //2.用户信息和url
        /**
         * useUnicode=true  使用unicode编码,支持中文
         * characterEncoding=utf8   设置字符集为UTF-8
         * useSSL=true  使用SSL安全连接
         */
        String url = "jdbc:mysql://localhost:3306/lvxiaobin?useUnicode=true&characterEncoding=utf8&useSSL=true";
        String username = "lv";
        String password = "xiao";
        //3.接连成功,获取数据库对象
        Connection connection = DriverManager.getConnection(url, username, password);
        //4.执行sql的对象
        Statement statement = connection.createStatement();
        //5.执行sql
        String sql = "select * from user";
        //返回的结果集
        ResultSet resultSet = statement.executeQuery(sql);
        while (resultSet.next()) {
            System.out.println(resultSet.getString("id"));
        }
        //6.释放连接
        resultSet.close();
        statement.close();
        connection.close();

    }
```

