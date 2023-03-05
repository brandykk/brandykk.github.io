---
title: "Java模拟鼠标键盘操作"
date: 2021-04-18T12:25:27+08:00
description: ""
tags: ["Java"]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: 开发 
comment : true
---

```java
/**
     * 定时执行模拟鼠标键盘操作
     * Robot中主要的鼠标和键盘控制方法有：
     * •    void keyPress(int keycode) 按下给定的键。
     * •    void keyRelease(int keycode) 释放给定的键。
     * •    void mouseMove(int x, int y) 将鼠标指针移动到给定屏幕坐标。
     * •    void mousePress(int buttons) 按下一个或多个鼠标按钮。
     * •    void mouseRelease(int buttons) 释放一个或多个鼠标按钮。
     * •    void mouseWheel(int wheelAmt) 在配有滚轮的鼠标上旋转滚轮。
     */
    private static void mouse(){
        new Thread(()->{
            while (true){
                try {
                    Thread.sleep(1000*60);

                    Robot robot = new Robot();
                    //设置Robot产生一个动作后的休眠时间,否则执行过快
                    robot.setAutoDelay(1000);

                    //获取屏幕分辨率
                    Dimension d = Toolkit.getDefaultToolkit().getScreenSize();
                    System.out.println(d);
                    Rectangle screenRect = new Rectangle(d);
                    //截图
                    BufferedImage bufferedImage = robot.createScreenCapture(screenRect);
                    //保存截图
                    File file = new File("screenRect.png");
                    ImageIO.write(bufferedImage, "png", file);

                    //移动鼠标
                    robot.mouseMove(500, 500);

                    //点击鼠标
                    //鼠标左键
                    System.out.println("单击");
                    robot.mousePress(InputEvent.BUTTON1_MASK);
                    robot.mouseRelease(InputEvent.BUTTON1_MASK);

                    //鼠标右键
                    System.out.println("右击");
                    robot.mousePress(InputEvent.BUTTON3_MASK);
                    robot.mouseRelease(InputEvent.BUTTON3_MASK);

                    //按下ESC，退出右键状态
                    System.out.println("按下ESC");
                    robot.keyPress(KeyEvent.VK_ESCAPE);
                    robot.keyRelease(KeyEvent.VK_ESCAPE);
                    //滚动鼠标滚轴
                    System.out.println("滚轴");
                    robot.mouseWheel(5);

                    //按下Alt+TAB键
                    robot.keyPress(KeyEvent.VK_ALT);
                    for(int i=1;i<=2;i++)
                    {
                        robot.keyPress(KeyEvent.VK_TAB);
                        robot.keyRelease(KeyEvent.VK_TAB);
                    }
                    robot.keyRelease(KeyEvent.VK_ALT);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (AWTException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });
    }
```
