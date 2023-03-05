---
title: "Spring定时器依赖注入"
date: 2021-04-18T16:09:32+08:00
description: "spring配置定时器时service注入问题"
tags: ["Spring"]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: JAVA 
comment : true
---

- 工具类
```java
/**
* 创建工具类
**/
public class ApplicationContextUtil implements ApplicationContextAware {
    private static ApplicationContext applicationContext;

    public static ApplicationContext getApplicationContext() {
        return applicationContext;
    }

    public void setApplicationContext(ApplicationContext applicationContext) {
        ApplicationContextUtil.applicationContext = applicationContext;
    }

    public static Object getBean(String beanName) {
        return applicationContext.getBean(beanName);
    }
}
```

- 配置bean

```xml
<bean  id ="applicationContextUtil"  class ="org.sihai.soil.util.ApplicationContextUtil" ></bean >
```

- 获取service

```java
realmEbi = (RealmEbi) ApplicationContextUtil.getBean("realmEbi");

realmEbi.insertHour(RealmApplianceModel.sendData3);
```
