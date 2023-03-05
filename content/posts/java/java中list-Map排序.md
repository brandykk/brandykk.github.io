---
title: "Java中list<Map>排序"
date: 2021-06-19T22:56:16+08:00
description: "List<Map>排序"
tags: [java]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: 开发 
comment : true
---

```java
//通过key排序
    private static void sort1() {
        //List<Map<String,Object>>根据map的key值排序
        List<Map<String,Object>> list = new ArrayList<>();
        Map<String,Object> map = new HashMap<>();
        map.put("a","1");
        Map<String,Object> map1 = new HashMap<>();
        map1.put("a","6");
        Map<String,Object> map2 = new HashMap<>();
        map2.put("a","3");
        Map<String,Object> map3 = new HashMap<>();
        map3.put("a","5");
        Map<String,Object> map4 = new HashMap<>();
        map4.put("a","4");
        Map<String,Object> map5 = new HashMap<>();
        map5.put("a","2");
        list.add(map);
        list.add(map1);
        list.add(map2);
        list.add(map3);
        list.add(map4);
        list.add(map5);
        //重写map的排序方式
        Comparator<Map<String,Object>> co = new Comparator<Map<String, Object>>() {
            @Override
            public int compare(Map<String, Object> o1, Map<String, Object> o2) {
                return String.valueOf(o1.get("a")).compareTo(String.valueOf(o2.get("a")));
            }
        };
        //lambda方式
        Comparator<Map<String,Object>> co1 = (o1,o2)->String.valueOf(o1.get("a")).compareTo(String.valueOf(o2.get("a")));
        //Comparator.comparing()
        Comparator<Map<String,Object>> co2 = Comparator.comparing(o -> String.valueOf(o.get("a")));

        //调用排序
        list.sort(co);
//        list.sort(co.reversed());
//        Collections.sort(list,co);

        System.out.println(list);
    }

    //根据value排序
    private static void sort2(){
        Map<String,Object> map = new HashMap<>();
        map.put("a","1");
        map.put("b","3");
        map.put("c","5");
        map.put("d","2");
        map.put("e","4");
        //用Map.Entry
        Comparator<Map.Entry<String,Object>> co = new Comparator<Map.Entry<String, Object>>() {
            @Override
            public int compare(Map.Entry<String, Object> o1, Map.Entry<String, Object> o2) {
                return String.valueOf(o1.getValue()).compareTo(String.valueOf(o2.getValue()));
            }
        };
        //用lambda
        Comparator<Map.Entry<String,Object>> co1 = (o1, o2) -> String.valueOf(o1.getValue()).compareTo(String.valueOf(o2.getValue()));
        //Comparator.comparing()
        Comparator<Map.Entry<String,Object>> co2 = Comparator.comparing(o -> String.valueOf(o.getValue()));
        //将map转换为map.entrySet()
        List<Map.Entry<String,Object>> listEntry = new ArrayList<>(map.entrySet());
        //调用排序
        listEntry.sort(co);
//        listEntry.sort(co.reversed());
//        Collections.sort(listEntry,co);
        System.out.println(listEntry);
    }
```

