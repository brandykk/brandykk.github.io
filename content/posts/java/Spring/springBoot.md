---
title: "SpringBoot"
date: 2021-08-07T23:03:10+08:00
description: "srpingboot基础"
tags: ["springboot"]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: java
comment : true
---

- 小彩蛋：修改springboot启动banner,也就是控制台打印的图像

> 在`resources`在创建`banner.txt`,然后把网上复制的`banner`粘贴进去

```txt

                                .::::.
                              .::::::::.
                              :::::::::::
                              ':::::::::::..
                               :::::::::::::::'
                                ':::::::::::.
                                  .::::::::::::::'
                                .:::::::::::...
                               ::::::::::::::''
                   .:::.       '::::::::''::::
                 .::::::::.      ':::::'  '::::
                .::::':::::::.    :::::    '::::.
              .:::::' ':::::::::. :::::      ':::.
            .:::::'     ':::::::::.:::::       '::.
          .::::''         '::::::::::::::       '::.
         .::''              '::::::::::::         :::...
      ..::::                  ':::::::::'        .:' ''''
   ..''''':'                    ':::::.'
```

## 1. springboot依赖

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.5.3</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.bin</groupId>
    <artifactId>springboot</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>springboot</name>
    <description>Demo project for Spring Boot</description>
    <properties>
        <java.version>1.8</java.version>
    </properties>
    <dependencies>
        <!--启动器-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <!--集成web ： tomcat-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <!--单元测试-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>
```

## 2. 原理

自动配置：	

`pom.xml`

- spring-boot-dependencies：核心依赖在父工程中
- 我们在引入springboot依赖时也可以不指定版本，因为已经有这些仓库了



**1. 启动器**

```xml
<dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
</dependency>
```

- 启动器：就是`Srpingboot的启动场景`；

  比如：

  ```xml
  <dependency>
              <groupId>org.springframework.boot</groupId>
              <artifactId>spring-boot-starter-web</artifactId>
  </dependency>
  ```

  就会自动导入`web`环境所有依赖

- springboot会将所有的功能场景变成一个个启动器，需要什么功能找对应的启动器就可以

### 2. 主程序

```java
@SpringBootApplication
public class SpringbootApplication {

    public static void main(String[] args) {
        //springboot应用启动
        SpringApplication.run(SpringbootApplication.class, args);
    }

}
```

- @SpringBootApplication	
  - @SpringBootConfiguration：springboot的配置
    - @Configuration：spring配置类
    - @Component ：说明这也是spring组件
  - @EnableAutoConfiguration ：自动配置
    - @AutoConfigurationPackage：自动配置包
      - @Import({Registrar.class})：自动配置“包注册”
    - @Import({AutoConfigurationImportSelector.class})：自动配置导入选择

> 结论： `springboot`所有自动配置都是在启动的时候扫描并加载：`spring.factories`所有的自动配置类都在这里，但不一定生效，要判断条件是否成立，只要导入对应的start就有对应的启动器，然后自动装配就会生效。

1. `springboot`在启动时，从类路径下`/META-INF/spring.factories`获取指定值
2. 将这些自动配置的类导入容器，自动配置就会生效
3. 整合`javaEE`，解决方案和自动配置的东西都在`spring-boot-autoconfigure-2.2.0.RELEASE.jar`下
4. 它会把所有需要的组件以类型方式返回，然后添加进容器
5. 容器中存在非常多`xxxAutoConfiguration`的文件（`@bean`），就是这些类给容器中导入了这个场景需要的所有组件，并自动配置，`@Configuration`, `javaConfig`

## SpringApplication

> springboot启动类主要做了四件事：

1. 推断应用的类型是普通项目还是WEB项目
2. 查找并加载所有可用初始化器，设置到`initializers`属性中
3. 找出所有的应用程序监听器，设置到`listeners`属性中
4. 推断并设置main方法的定义类，找到运行的主类

## [Springboot配置文件](https://docs.spring.io/spring-boot/docs/current/reference/html/)

`Springboot`使用一个全局配置文件，文件名称是固定的

- `application.properties`
  - ket=value
- `application.yml`
  - key: 空格 value

**yaml配置**

```yaml
server:
	prot: 8080
```

**xml配置**

```xml
<server>
	<port>8080</port>
</server>
```

**yaml实例**

```yaml
# key= value

# 普通写法
name: lv

# 对象{}
student:
  name: lv
  age: 32
## 对象的行内写法s
students: { name: lv,age: 32 }

# 数组
array:
  - cat
  - dog
## 数组行内写法
arrays: [ cat,dog ]
```

### 1. 使用`yaml`给属性赋值

> 使用`@ConfigurationProperties(prefix = "user")`注解找到配置文件中的`user`属性，要注意**空格很重要**

1. 基础对象类

   ```java
   package com.bin.pojo;
   
   public class Dog {
       private String dogName;
       private String dogEat;
   
       @Override
       public String toString() {
           return "Dog{" +
                   "dogName='" + dogName + '\'' +
                   ", dogEat='" + dogEat + '\'' +
                   '}';
       }
   
       public String getDogName() {
           return dogName;
       }
   
       public void setDogName(String dogName) {
           this.dogName = dogName;
       }
   
       public String getDogEat() {
           return dogEat;
       }
   
       public void setDogEat(String dogEat) {
           this.dogEat = dogEat;
       }
   }
   ```

2. 封装对象类

   ```java
   package com.bin.pojo;
   
   import com.fasterxml.jackson.annotation.JsonFormat;
   import org.springframework.boot.context.properties.ConfigurationProperties;
   import org.springframework.format.annotation.DateTimeFormat;
   import org.springframework.stereotype.Component;
   
   import java.time.LocalDateTime;
   import java.util.List;
   import java.util.Map;
   
   @Component
   @ConfigurationProperties(prefix = "user")
   public class User {
   
       private String name;
       private Integer age;
       private Boolean flag;
       @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
       @DateTimeFormat(pattern = "yyyy-MM-dd HH:mm:ss")
       private LocalDateTime time;
       private Map<String,String> map;
       private List<String> list;
       private Dog dog;
   
       public LocalDateTime getTime() {
           return time;
       }
   
       public void setTime(LocalDateTime time) {
           this.time = time;
       }
   
       @Override
       public String toString() {
           return "User{" +
                   "name='" + name + '\'' +
                   ", age=" + age +
                   ", flag=" + flag +
                   ", time=" + time +
                   ", map=" + map +
                   ", list=" + list +
                   ", dog=" + dog +
                   '}';
       }
   
       public Dog getDog() {
           return dog;
       }
   
       public void setDog(Dog dog) {
           this.dog = dog;
       }
   
       public String getName() {
           return name;
       }
   
       public void setName(String name) {
           this.name = name;
       }
   
       public Integer getAge() {
           return age;
       }
   
       public void setAge(Integer age) {
           this.age = age;
       }
   
       public Boolean getFlag() {
           return flag;
       }
   
       public void setFlag(Boolean flag) {
           this.flag = flag;
       }
   
   
       public Map<String, String> getMap() {
           return map;
       }
   
       public void setMap(Map<String, String> map) {
           this.map = map;
       }
   
       public List<String> getList() {
           return list;
       }
   
       public void setList(List<String> list) {
           this.list = list;
       }
   }
   ```

3. application.yml

   ```yaml
   user:
     name: lv
     age: 36
     flag: true
     time: 2021-10-10 12:32:20
     map: { key: 1,value: 2 }
     list: [ a,b,c ]
     dog:
       dogName: dog
       dogEat: 吃
   ```

4. 测试

   ```java
   package com.bin;
   
   import com.bin.pojo.User;
   import org.junit.jupiter.api.Test;
   import org.springframework.beans.factory.annotation.Autowired;
   import org.springframework.boot.test.context.SpringBootTest;
   
   @SpringBootTest
   class SpringbootApplicationTests {
   
       @Autowired
       private User user;
   
       @Test
       void contextLoads() {
           System.out.println(user);
           //User{name='lv', age=36, flag=true, time=2021-10-10T12:32:20, map={key=1, value=2}, list=[a, b, c], dog=Dog{dogName='dog', dogEat='吃'}}
       }
   
   }
   ```

   使用`@ConfigurationProperties(prefix = "user")`时会有idea报红提示，可以添加下面的依赖，也可以不添加，这个不影响

   ```xml
   <dependency>
               <groupId>org.springframework.boot</groupId>
               <artifactId>spring-boot-configuration-processor</artifactId>
           </dependency>
   ```

### 2.使用`properties`赋值

- 更改注解：`@PropertySource(value = "classpath:config.properties")`
- 在实体参数上加上注解`@Value("${name}")`

```java
@PropertySource(value = "classpath:config.properties")
public class Persion{
    @Value("${name}")
    private String name;
}
```

### 3.yaml支持松散绑定

- 实体中的驼峰命名`userName`
- `yaml`中可以用`-`分割：`user-name`

### 4.yaml支持`jsr-303`

> 即[数据校验](https://blog.csdn.net/xueguchen/article/details/111406671)

- 在实体类上添加`@Validated`开启校验

- 在实体属性上添加校验注解

  > Bean Validation 中内置的 constraint

  | Constraint                  | 详细信息                                                 |
  | --------------------------- | -------------------------------------------------------- |
  | @Null                       | 被注释的元素必须为 null                                  |
  | **@NotNull**                | 被注释的元素必须不为 null                                |
  | @AssertTrue                 | 被注释的元素必须为 true                                  |
  | @AssertFalse                | 被注释的元素必须为 false                                 |
  | @Min(value)                 | 被注释的元素必须是一个数字，其值必须大于等于指定的最小值 |
  | @Max(value)                 | 被注释的元素必须是一个数字，其值必须小于等于指定的最大值 |
  | @DecimalMin(value)          | 被注释的元素必须是一个数字，其值必须大于等于指定的最小值 |
  | @DecimalMax(value)          | 被注释的元素必须是一个数字，其值必须小于等于指定的最大值 |
  | @Size(max, min)             | 被注释的元素的大小必须在指定的范围内                     |
  | @Digits (integer, fraction) | 被注释的元素必须是一个数字，其值必须在可接受的范围内     |
  | @Past                       | 被注释的元素必须是一个过去的日期                         |
  | @Futuret                    | 被注释的元素必须是一个将来的日期                         |
  | **@Pattern(value)**         | 被注释的元素必须符合指定的正则表达式                     |

  > 分类：Hibernate Validator 附加的 constraint

  | Constraint | 详细信息                               |
  | ---------- | -------------------------------------- |
  | @Email     | 被注释的元素必须是电子邮箱地址         |
  | @Length    | 被注释的字符串的大小必须在指定的范围内 |
  | @NotEmpty  | 被注释的字符串的必须非空               |
  | @Range     | 被注释的元素必须在合适的范围内         |

- pom

```xml

<dependency>
            <groupId>javax.validation</groupId>
            <artifactId>validation-api</artifactId>
            <version>2.0.1.Final</version>
</dependency>
<dependency>
            <groupId>org.hibernate</groupId>
            <artifactId>hibernate-validator</artifactId>
            <version>5.2.0.Final</version>
</dependency>
```

## Springboot Web开发

web项目总结：

1. 在springboot可以使用一下方法	处理静态资源
   - webjars：`localhost:8080/webjars/`
   - public, static, /**, resources: `localhost:8080/`
2. 优先级：resources>static>public

### Springboot配置无法注入问题

```java
    private static String xsjzServerName;

    @Value("${capricorn.xsjzServerName}")
    public void setXsjzServerName(String xsjzServerName) {
        this.xsjzServerName = xsjzServerName;
    }
```

