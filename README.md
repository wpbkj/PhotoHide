# 图片隐藏-缩略图与大图不同
## 进入v2时代
当前最新版本：v2.0.1  
> 添加选择图片功能，优化代码  
> 加入小米字体(MiSans)作为图片选择字体，用于显示中文  
> 加入win32timezone模块，供打包使用，为调起kivy的Popup
### 介绍
可实现手Q、微博等平台缩略图与大图不同功能。  
利用手机QQ、微博等平台缩略图背景为白色，查看大图背景为黑色特性制作，基于Python，GUI框架为Kivy。  
中文字体文件已添加至kivy的fonts文件夹中  
为打包为单个可执行程序，kv设计语言文件直接添加到main.py中  
别称：幻影坦克，幻影坦克图片
### 打包环境/依赖
> Python 3.9.9 64-bit  
> Kivy 2.1.0  
> opencv-python 4.5.3.56  
> numpy 1.22.2  
> win32timezone  
> 中文字体：  
> 前景：LeeFont蒙黑体(Leefont.ttf)  
> 图片选择：MiSans(MiSans-Normal.ttf)

### 使用说明
本程序已发布WINDOWS发行版，可直接下载WINDOWS发行版使用或您可以基于Kivy将本程序打包为APP或其他可执行文件
1.  下载发行版
https://github.com/wpbkj/PhotoHide/releases/
2.  运行程序
> 应注意：需要构建的上层图片和下层图片应与程序主体在同一文件夹，运行程序后手动输入文件名

### 参与贡献

1.  Fork 本仓库
2.  新建分支
3.  提交代码
4.  新建 Pull Request

### 开发任务

1.  ~~支持图片选择~~(完成)
2.  支持弹窗提示
3.  多文件批量处理

### 软件截图
![1](https://wpbkj.github.io/PhotoHide/screen1.png)
![2](https://wpbkj.github.io/PhotoHide/screen2.png)
![3](https://wpbkj.github.io/PhotoHide/screen3.png)
