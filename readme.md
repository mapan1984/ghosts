### 更新hosts

下载hosts文件的脚本，来源是[racaljk/hosts](https://github.com/racaljk/hosts)，可以自行判断hosts源是否更新。

### 使用

首在Windows下使用，先为自己增加hosts文件的写权限(或者以管理员方式打开cmd)，打开cmd，输入：

    $ python ghosts.py

就会开始更新hosts，使用参数`-f`或`--force`跳过判断，强制更新。

待更新完成后，输入：

    $ ipconfig /flushdns

### 如何更加方便的使用

在Windows下建立文件夹`c:\bin`，并将文件夹路径加入环境变量`PATH`中，然后就可以在任何路径下用cmd或者powershell执行在`c:\bin`中的脚本或程序。

在`c:\bin`文件夹中，我使用了bat脚本：

``` dosbatch
:: ghosts.bat
@echo off
title "download hosts"
python D:\ghosts\ghosts.py %*
if %errorlevel% == 0 (ipconfig /flushdns) else echo "don't flush dns"
echo on
```

`D:\ghosts\ghosts.py`是我的电脑下`ghosts.py`的绝对路径，你需要更换为自己电脑下`ghosts.py`的绝对路径。

这样只要打开cmd执行：

    $ ghosts

就可以更新hosts文件了。
