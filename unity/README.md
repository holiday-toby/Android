# Unity开发Android游戏入门之踩坑篇

## 搭建Unity开发环境
[Unity 官网](https://unity.cn/releases/full) 下载 UnityHub，然后下载需要的unity版本，以及Android平台的支持。
![](README/截屏2022-09-07%20下午4.05.38%201.png)
>使用unity hub 下载的时候，如果进程退出，任务会重新开始，并且会由于缓存的原因失败。这个时候需要到 ***/Applications/Unity/Hub/Editor*** 目录下删除报错的版本重新下载。

### 配置Android环境
1. 使用UnityHub新建Unity Project;
2. 在Preferences > Exrernnal Tools > Android 中配置JDK、Android SDK、NDK以及Gradle的位置;
    > 编译apk默认使用的gradle位置： "/Applications/Unity/Hub/Editor/2020.3.26f1c1/PlaybackEngines/AndroidPlayer/Tools/gradle/lib/gradle-launcher-6.1.1.jar"。
    不同版本unity使用的默认gradle版本不同，可以配置为本地目录。

3. 在File > Build settings中选中 Android 平台;
4. 在Edit > Project Settings > Player 中选择Android平台，进行icon、签名相关配置。
5. 可以在Other Settings > Scripting Backend选择IL2CPP，这样就可以出ARM64的包。

## unity开发
ui是在unity面板中开发的，游戏脚本会在VS中开发
### 简单UI及点击事件
1. 在unity面板中操作，通过菜单创建、拖动调整位置、属性配置
2. 点击事件：写好脚本，将脚本粘贴到对应的GameObject上，然后选择对应的方法
3. 为控件赋值：在脚本中定义控件的引用，然后为画布指定脚本，指定脚本中该引用对应的控件的id。
### C#语法与游戏脚本
   C#的语法和java比较接近，熟悉java可以轻松上手，它们的差异点可以参考这篇文章[C# 与 Java 的一些差异](https://www.cnblogs.com/liuchunlin/p/11750517.html)

    游戏脚本的开发，都要继承MonoBehaviour这个类。
### 转接层代码
   iOS和Android的GMSDK代码在调用时都涉及到高级语言特性，对象拆装包，回调接口实现，在Unity3D中使用C#代码直接调用原生GMSDK代码的话，代码的编写，调试都会很复杂。推荐在Objective-C/Swift和Java/Kotlin中，以及C#中编写转接层，将数据交换限定在基础对象类型级别和字符串，两侧可以使用JSON格式进行序列化和反序列化。对于异步调用过程则在转接层的原生代码部分向Unity3D的C#代码部分发送消息实现。

## 编译为apk

### 1.直接Build And Run有时会报如下错误
```
* What went wrong:
Could not determine the dependencies of task ':launcher:compileReleaseJavaWithJavac'.
> Installed Build Tools revision 32.0.0 is corrupted. Remove and install again using the SDK Manager.
```
这要找到unity默认使用的build Tools所在位置进行修改（可以配置为mac上已安装的Android SDk）。参考[Android Studio error "Installed Build Tools revision 31.0.0 is corrupted"
](https://stackoverflow.com/questions/68387270/android-studio-error-installed-build-tools-revision-31-0-0-is-corrupted)


### 2.选择Export项目在Android Stuido中编译

Unity 会创建一个包含两个模块的 Gradle 项目：
- UnityLibrary module：包含 Unity 运行时和项目数据。该模块是一个库，您可以将其集成到任何其他 Gradle 项目中。您可以使用它将 Unity 嵌入到现有的 Android 应用程序中。
- Launcher module：包含应用程序的名称及其所有图标。这是一个启动 Unity 的简单 Android 应用程序模块。您可以将其替换为您自己的应用程序。

由于笔者电脑上安装的Android Studio版本较新，需要将gradle-wrapper.properties中的gradle-7.3.3-bin.zip降级为6.1.1，可以正常编译。

也可以选择升级gradle：1.修改根项目中build.gradle的gradle配置为最新版(与gradle-wrapper.properties相匹配)；2.改不兼容的http依赖位https；3.删除gradle.properties中的android.enableR8配置。方可正常编译，不过每次重新导出文件后，这些修改会被覆盖。








