---
title: "Java验证码"
date: 2021-06-20T13:58:34+08:00
description: ""
tags: [java]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: 开发
comment : true
---

## Utility.java

<details>
<summary>验证码调用工具类</summary>

```java
import org.apache.commons.lang3.StringUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import java.math.BigDecimal;
import java.text.SimpleDateFormat;
import java.util.*;

public class Utility {
	protected final static Log logger = LogFactory.getLog(Utility.class);

	public static <T> List<T> newArray(int size, Class<T> clazz) {
		List<T> l = new ArrayList<T>();
		for (int i = 0; i < size; i++) {
			T newInstance;
			try {
				newInstance = clazz.newInstance();
			} catch (Exception e) {
				newInstance = null;
			}
			l.add(newInstance);
		}
		return l;
	}

	public static String randomString(int len, int type) {
		StringBuffer str = new StringBuffer();
		// 默认去掉了容易混淆的字符oOLlI，要添加请使用addChars参数
		String codestr = "ABCDEFGHJKMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz";
		String codeNum = "0123456789";
//		switch (type) {
//		case 0:
//			codestr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
//			break;
//		case 1:
//			codestr = "0123456789";
//			break;
//		case 2:
//			codestr = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
//			break;
//		case 3:
//			codestr = "abcdefghijklmnopqrstuvwxyz";
//			break;
//		default:
//			// 默认去掉了容易混淆的字符oOLl和数字01，要添加请使用addChars参数
//			codestr = "ABCDEFGHIJKMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789";
//			break;
//		}
		char[] codes = codestr.toCharArray();
		char[] codeNums = codeNum.toCharArray();
		for (int i = 0; i < len/2; i++) {
			int r = (int) (Math.random() * codestr.length());
			str.append(codes[r]);
			int n = (int) (Math.random()*codeNum.length());
			str.append(n);
		}
		List<String> list=Arrays.asList(str.toString().split(""));
		Collections.shuffle(list);
		StringBuffer str1 = new StringBuffer();
		for(String s:list){
			str1.append(s);
		}
		return str1.toString();
	}

	public static String randomString(int length) {
		return randomString(length, -1);
	}

	public static int random(int number) {
		return (int) (Math.random() * number);
	}

	public static Random random = new Random();

	public static int random(int total, int count) {
		if (count == 1)
			return total;
		if (count == 0) {
			return 0;
		}
		int average = total / count;
		double d = random.nextGaussian();
		if (d < -0.75)
			d = -0.75;
		if (d < -1 + 1.0 / count)
			d = -1 + 1.0 / count;
		if (d > 4)
			d = 4;
		if (d > count - 0.1)
			d = count - 0.1;
		return (int) (d * average + average);
	}

	public static String toString(Object o) {
		if (o == null)
			return null;
		Class c = o.getClass();
		if (c == Integer.class) {
			return Integer.toString((Integer) o);
		} else if (c == Float.class) {
			return Float.toString((Float) o);
		} else if (c == Long.class) {
			return Long.toString((Long) o);
		} else if (c == Double.class) {
			return Double.toString((Double) o);
		} else if (c == BigDecimal.class) {
			return o.toString();
		} else if (c == Boolean.class) {
			return Boolean.toString((Boolean) o);
		} else if (c == Date.class) {
			SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
			String ss = sdf.format(o);
			return ss;
		} else {
			return o.toString();
		}
	}


	@SuppressWarnings("unchecked")
	public static <T> T toObject(String str, Class<T> c) {
		if (str == null)
			return null;
		try {
			str = str.trim();
			if (c == String.class) {
				return (T) str;
			} else if (StringUtils.isBlank(str)) {
				return null;
			} else if (c == Integer.class) {
				return (T) (Integer) Integer.parseInt(str);
			} else if (c == Long.class) {
				return (T) (Long) Long.parseLong(str);
			} else if (c == Byte.class) {
				return (T) new Byte((byte) Integer.parseInt(str, 16));
			} else if (c == Float.class) {
				return (T) (Float) Float.parseFloat(str);
			} else if (c == Double.class) {
				return (T) (Double) Double.parseDouble(str);
			} else if (c == Boolean.class) {
				if("1".equals(str))
					return (T)Boolean.TRUE;
				return (T) (Boolean) Boolean.parseBoolean(str);
			} else if (c == BigDecimal.class) {
				return (T) new BigDecimal(str);
			} else if (c == Date.class) {
				SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
				Date ss = sdf.parse(str);
				return (T) ss;
			} else {
				return (T) str;
			}
		} catch (Exception e) {
			// 打印异常信息，例当一个非常长的数字字符串转Integer时，若没有意识到Integer数字大小限制时，没有异常输出，难于找到原因。非常不利问题的解决
			logger.debug("对象转换异常，调试用", e);
			return null;
		}
	}


	// 列举排序
	public static <T> List<T> sort(Enumeration<T> enumer) {
		List<T> l = new ArrayList<T>();
		while (enumer.hasMoreElements()) {
			T t = (T) enumer.nextElement();
			l.add(t);
		}
		Collections.sort((List) l);
		return l;
	}

	// 列表排序
	public static <T> List<T> sort(List<T> l) {
		Collections.sort((List) l);
		return l;
	}

	public static String substring(String str, int from, int to) {
		if (from >= str.length())
			return null;
		if (from < 0)
			from = 0;
		if (to < 0 || to > str.length())
			return str.substring(from);
		else
			return str.substring(from, to);
	}

//	public static void main(String[] args) {
//		String in = randomString(4);
//		System.out.println(in);
//	}


}

```
</details>

## ImageUtil.java

<details>
<summary>图片生成工具类</summary>

```java
import lombok.extern.slf4j.Slf4j;
import org.jeecg.common.util.IOCloseUtil;
import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.geom.AffineTransform;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.Arrays;
import java.util.Random;

@Slf4j
public class ImageUtil {
    //使用到Algerian字体，系统里没有的话需要安装字体，字体只显示大写，去掉了1,0,i,o几个容易混淆的字符
    public static final String VERIFY_CODES = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ";
    private static Random random = new Random();

    /**
     * 使用系统默认字符源生成验证码
     *
     * @param verifySize 验证码长度
     * @return
     */
    public static String generateVerifyCode(int verifySize) {
        return generateVerifyCode(verifySize, VERIFY_CODES);
    }

    /**
     * 使用指定源生成验证码
     *
     * @param verifySize 验证码长度
     * @param sources    验证码字符源
     * @return
     */
    public static String generateVerifyCode(int verifySize, String sources) {
        if (sources == null || sources.length() == 0) {
            sources = VERIFY_CODES;
        }
        int codesLen = sources.length();
        Random rand = new Random(System.currentTimeMillis());
        StringBuilder verifyCode = new StringBuilder(verifySize);
        for (int i = 0; i < verifySize; i++) {
            verifyCode.append(sources.charAt(rand.nextInt(codesLen - 1)));
        }
        return verifyCode.toString();
    }

    /**
     * 生成随机验证码文件,并返回验证码值
     *
     * @param w
     * @param h
     * @param outputFile
     * @param verifySize
     * @return
     * @throws IOException
     */
//    public static String outputVerifyImage(int w, int h, File outputFile, int verifySize) throws IOException {
//        String verifyCode = generateVerifyCode(verifySize);
//        outputImage(w, h, outputFile, verifyCode);
//        return verifyCode;
//    }

    /**
     * 输出随机验证码图片流,并返回验证码值
     *
     * @param w
     * @param h
     * @param os
     * @param verifySize
     * @return
     * @throws IOException
     */
//    public static String outputVerifyImage(int w, int h, OutputStream os, int verifySize) throws IOException {
//        String verifyCode = generateVerifyCode(verifySize);
//        outputImage(w, h, os, verifyCode);
//        return verifyCode;
//    }

    /**
     * 生成指定验证码图像文件
     *
     * @param w
     * @param h
     * @param outputFile
     * @param code
     * @throws IOException
     */
    public static void outputImage(int w, int h, File outputFile, String code) throws IOException {
        if (outputFile == null) {
            return;
        }
        File dir = outputFile.getParentFile();
        if (!dir.exists()) {
            dir.mkdirs();
        }
        try {
            outputFile.createNewFile();
            FileOutputStream fos = new FileOutputStream(outputFile);
            outputImage(w, h, fos, code);
            IOCloseUtil.close(fos);
        } catch (IOException e) {
            throw e;
        }
    }

    /**
     * 输出指定验证码图片流
     *
     * @param w
     * @param h
     * @param os
     * @param code
     * @throws IOException
     */
    public static void outputImage(int w, int h, OutputStream os, String code) throws IOException {
        int verifySize = code.length();
        BufferedImage image = new BufferedImage(w, h, BufferedImage.TYPE_INT_RGB);
        Random rand = new Random();
        Graphics2D g2 = image.createGraphics();
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        Color[] colors = new Color[5];
        Color[] colorSpaces = new Color[]{Color.WHITE, Color.CYAN,
                Color.GRAY, Color.LIGHT_GRAY, Color.MAGENTA, Color.ORANGE,
                Color.PINK, Color.YELLOW};
        float[] fractions = new float[colors.length];
        for (int i = 0; i < colors.length; i++) {
            colors[i] = colorSpaces[rand.nextInt(colorSpaces.length)];
            fractions[i] = rand.nextFloat();
        }
        Arrays.sort(fractions);

        g2.setColor(Color.GRAY);// 设置边框色
        g2.fillRect(0, 0, w, h);

        Color c = getRandColor(200, 250);
        g2.setColor(c);// 设置背景色
        g2.fillRect(0, 2, w, h - 4);

        //绘制干扰线
        Random random = new Random();
        g2.setColor(getRandColor(160, 200));// 设置线条的颜色
        for (int i = 0; i < 20; i++) {
            int x = random.nextInt(w - 1);
            int y = random.nextInt(h - 1);
            int xl = random.nextInt(6) + 1;
            int yl = random.nextInt(12) + 1;
            g2.drawLine(x, y, x + xl + 40, y + yl + 20);
        }

        // 添加噪点
        float yawpRate = 0.05f;// 噪声率
        int area = (int) (yawpRate * w * h);
        for (int i = 0; i < area; i++) {
            int x = random.nextInt(w);
            int y = random.nextInt(h);
            int rgb = getRandomIntColor();
            image.setRGB(x, y, rgb);
        }

        shear(g2, w, h, c);// 使图片扭曲

        g2.setColor(getRandColor(100, 160));
        int fontSize = h - 4;
        Font font = new Font("Algerian", Font.ITALIC, fontSize);
        g2.setFont(font);
        char[] chars = code.toCharArray();
        for (int i = 0; i < verifySize; i++) {
            AffineTransform affine = new AffineTransform();
            affine.setToRotation(Math.PI / 4 * rand.nextDouble() * (rand.nextBoolean() ? 1 : -1), (w / verifySize) * i + fontSize / 2, h / 2);
            g2.setTransform(affine);
            g2.drawChars(chars, i, 1, ((w - 10) / verifySize) * i + 5, h / 2 + fontSize / 2 - 10);
        }

        g2.dispose();
        ImageIO.write(image, "png", os);
    }

    private static Color getRandColor(int fc, int bc) {
        if (fc > 255) {
            fc = 255;
        }
        if (bc > 255) {
            bc = 255;
        }
        int r = fc + random.nextInt(bc - fc);
        int g = fc + random.nextInt(bc - fc);
        int b = fc + random.nextInt(bc - fc);
        return new Color(r, g, b);
    }

    private static int getRandomIntColor() {
        int[] rgb = getRandomRgb();
        int color = 0;
        for (int c : rgb) {
            color = color << 8;
            color = color | c;
        }
        return color;
    }

    private static int[] getRandomRgb() {
        int[] rgb = new int[3];
        for (int i = 0; i < 3; i++) {
            rgb[i] = random.nextInt(255);
        }
        return rgb;
    }

    private static void shear(Graphics g, int w1, int h1, Color color) {
        shearX(g, w1, h1, color);
        shearY(g, w1, h1, color);
    }

    private static void shearX(Graphics g, int w1, int h1, Color color) {

        int period = random.nextInt(2);

        boolean borderGap = true;
        int frames = 1;
        int phase = random.nextInt(2);

        for (int i = 0; i < h1; i++) {
            double d = (double) (period >> 1)
                    * Math.sin((double) i / (double) period
                    + (6.2831853071795862D * (double) phase)
                    / (double) frames);
            g.copyArea(0, i, w1, 1, (int) d, 0);
            if (borderGap) {
                g.setColor(color);
                g.drawLine((int) d, i, 0, i);
                g.drawLine((int) d + w1, i, w1, i);
            }
        }

    }

    private static void shearY(Graphics g, int w1, int h1, Color color) {

        int period = random.nextInt(40) + 10; // 50;

        boolean borderGap = true;
        int frames = 20;
        int phase = 7;
        for (int i = 0; i < w1; i++) {
            double d = (double) (period >> 1)
                    * Math.sin((double) i / (double) period
                    + (6.2831853071795862D * (double) phase)
                    / (double) frames);
            g.copyArea(i, 0, 1, h1, 0, (int) d);
            if (borderGap) {
                g.setColor(color);
                g.drawLine(i, (int) d, i, 0);
                g.drawLine(i, (int) d + h1, i, h1);
            }

        }
    }

//    public static void main(String[] args) throws IOException {
//
//        for (int i = 0; i < 20; i++) {
//            File dir = new File("E:/img/");
//            int w = 200, h = 80;
//            String verifyCode = generateVerifyCode(4);
//            File file = new File(dir, verifyCode + ".jpg");
//            outputImage(w, h, file, verifyCode);
//        }
//
//    }


}
```
</details>

## 验证码调用方法并返回

<details>
<summary>方法调用</summary>

```java
public Result<String> verify(HttpServletRequest request, HttpServletResponse response) {

		Result<String> result = new Result<>();
		// 获取界面传过来的验证码
		String securityCode = Utility.randomString(4);
		ByteArrayOutputStream bos = new ByteArrayOutputStream();
		try {
			ImageUtil.outputImage(107, 40, bos, securityCode);
			redisUtil.set(getVerifyKey(request), securityCode.toLowerCase(Locale.ENGLISH), 1 * 60);
			String verifys = new String(Base64.encodeBase64(bos.toByteArray()));
			result.setResult(verifys);
		} catch (JeecgBootException e) {
			e.printStackTrace();
			result.error500("生成验证码失败");
		} catch (Exception e) {
			e.printStackTrace();
			result.error500("生成验证码失败");
		} finally {
			if (bos != null) {
				try {
					bos.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
		return result;
	}

	private String getVerifyKey(HttpServletRequest request) {
		// return request.getRequestedSessionId() + "_Verify";
		String ipAddrByRequest = IPUtils.getIpAddr(request);
		if (ipAddrByRequest.contains(".")) {
			ipAddrByRequest = ipAddrByRequest.replace(".", "");
		} else if (ipAddrByRequest.contains(":")) {
			ipAddrByRequest = ipAddrByRequest.replace(":", "");
		}
		return "Verify_" + ipAddrByRequest;
	}
```
<details>
