---
title: "Java中的线程"
date: 2021-07-19T22:04:34+08:00
description: "java中的线程的实现"
tags: ["java","Thread"]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: JAVA
comment : true
---



## 创建线程的方法

- 继承`Thread`类,重写`run()`方法,调用`start()`方法开启
- 实现`Runnable`,重写`run()`方法,调用`start()`方法开启
- 通过`Callable`和`FutureTask`创建线程
- 通过线程池创建线程

### 继承`Thread`类

> 线程开启后不一定立即执行,由CPU调度执行

```java
public class ThreadRun {
    public static void main(String[] args) {
        //开启线程
        ThreadDemoOne threadDemoOne = new ThreadDemoOne();
        threadDemoOne.start();
        for (int i = 0; i < 5000; i++) {
            System.out.printf("普通代码: %d%n", i);
        }
    }
}

/**
*	继承Thread类的方法,并重run()
**/
class ThreadDemoOne extends Thread {
    @Override
    public void run() {
        for (int i = 0; i < 5000; i++) {
            System.out.println("线程在这里!!");
        }
    }
}
```

> 执行结果

```txt
线程在这里!!
普通代码: 694
普通代码: 695
线程在这里!!
普通代码: 696
线程在这里!!
```

- 实现`Runnable`

```java
public class ThreadDemoTwo {
    public static void main(String[] args) {
        //开启线程
        Thread thread = new Thread(new ThreadTest());
        thread.start();
        //普通代码块
        for (int i = 0; i < 5000; i++) {
            System.out.printf("普通代码: %d%n", i);
        }
    }
}

/**
 * 实现Runnable,并重写run()
 */
class ThreadTest implements Runnable {
    @Override
    public void run() {
        for (int i = 0; i < 5000; i++) {
            System.out.println("线程在这里!!");
        }
    }
}

```

> 执行结果

```txt
线程在这里!!
普通代码: 2359
线程在这里!!
线程在这里!!
普通代码: 2360
线程在这里!!
```

- `lambda`表达式方法

```java
public static void main(String[] args) {
        //lambda开启线程
        new Thread(() -> {
            for (int i = 0; i < 5000; i++) {
                System.out.println("线程在这里!!");
            }
        }).start();
        //普通代码块
        for (int i = 0; i < 5000; i++) {
            System.out.printf("普通代码: %d%n", i);
        }
    }
```

### 通过`Callable`和`FutureTask`创建线程

> Callable可以有返回值,调用`get()`时会等待线程执行完毕拿到返回值

```java
/**
     * 有返回值
     */
    private static void CallableDemoOne() {
        //重写Callable的call()
        Callable<String> callable = () -> {
            for (int i = 0; i < 5000; i++) {
                System.out.println("线程在这里!!!");
            }
            return "线程执行完毕";
        };
        //将Callable转为Thread可以调用的Runnable
        FutureTask<String> futureTask = new FutureTask<>(callable);
        Thread thread = new Thread(futureTask);
        //用Thread开启
        thread.start();
        for (int i = 0; i < 5000; i++) {
            System.out.printf("普通代码: %s%n", i);
        }
        //当调用futureTask的get()方法时,会等待线程执行完毕,然后再执行后面的代码,
        //如果没有返回,线程是阻塞状态的,一直等该线程执行完毕
        String s = null;
        try {
            s = futureTask.get();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        System.out.println(s);
        System.out.println("等待线程结束并返回结果,才会执行此语句");
    }
```

> 执行结果

```txt
普通代码: 4694
线程在这里!!!
普通代码: 4694
线程执行完毕
等待线程结束并返回结果,才会执行此语句
```

### 通过线程池创建线程

```java
//阿里不推荐使用Executors创建线程池
private static void test2() {
        //创建一个单线程
        ExecutorService executorService = Executors.newSingleThreadExecutor();
        //启动线程
        executorService.execute(()->{
            for (int i = 0; i < 5000; i++) {
                System.out.println("线程在这里");
            }
        });
        for (int i = 0; i < 5000; i++) {
            System.out.println("普通代码: " + i);
        }
        //关闭线程
        executorService.shutdown();
    }

//推荐使用ThreadPoolExecutor（）自定义创建线程池，因为这比较灵活切可控。
    private static void test1() {
        //创建线程池
        ExecutorService executorService = new ThreadPoolExecutor(5, 8, 8,
                TimeUnit.SECONDS, new ArrayBlockingQueue<>(5));
        //启动线程
        executorService.execute(() -> {
            for (int i = 0; i < 5000; i++) {
                System.out.println("线程在这里");
            }
        });
        for (int i = 0; i < 5000; i++) {
            System.out.println("普通代码: " + i);
        }
        //停止线程
        executorService.shutdown();
    }
```

> ThreadPoolExecutor()参数的意义

- `int corePoolSize`  核心线程数，即确定有多少个核心线程。
- `int maximumPoolSize`  最大线程数，即限定线程池中的最大线程数量。
- `long keepAliveTime`  非核心线程的存活时间，配合下面的`TimeUnit`参数确定时间。
- `TimeUnit unit`  一个时间类型的枚举类。有从纳秒到天的时间量度，配合上面的`keepAliveTime`确定非核心线程的存活时间。
- `BlockingQueue<Runnable> workQueue`   装载`Runnable`的阻塞队列，具体类型可以自己确定。
- `ThreadFactory threadFactory` 线程工厂，这是一个函数式接口，里面只定义了一个`newThread(Runnable task)`方法，需要自己实现工厂的方法，在这里我们可以对线程进行自定义的初始化，例如给线程设定名字，这样方便后期的调试。
- `RejectedExecutionHandler handler`拒绝服务处理，这也是一个函数式接口，我们需要实现`rejectedExecution(Runnable r, ThreadPoolExecutor executor)`这个方法，这里可以根据需求自定义你希望在处理逻辑。当然Java里面也有已经定义好的四种策略静态类。可以通过`ThreadPoolExecutor`调用

