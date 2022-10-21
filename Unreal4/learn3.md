
# UE中的JNI实战踩坑

## 一、实战踩坑
1. 函数签名问题,末尾不要加分号。各种函数声明示例
![函数声明](img/截屏2022-10-13%20下午7.25.52.png)
![函数声明](img/截屏2022-10-13%20下午7.30.07.png)
返回值也要注意调用对应的方法
![返回值匹配](img/截屏2022-10-13%20下午7.40.50.png)
该头文件路径：
***Engine/Source/Runtime/Launch/Public/Android/AndroidJNI.h***

2. JNI代码在android studio中没有代码提示，在local.properties文件中配置ndk目录即可查看jni的接口文档。
   
    ```properties
    sdk.dir=/Users/duanhao.ling/Library/Android/sdk
    ndk.dir=/Users/duanhao.ling/Library/Android/sdk/ndk-bundle
    ```

## 二、解析示例JNI函数

```c++
extern "C" JNIEXPORT jstring JNICALL
Java_com_garena_game_myapplication_MainActivity_stringFromJNI(
        JNIEnv *env,
        jobject /* this */) {
    std::string hello = "Hello from C++(Cmake)";
    return env->NewStringUTF(hello.c_str());
}
```
- JNIEXPORT 是宏定义，表示一个函数需要暴露给共享库外部使用时。
- JNICALL 是宏定义，表示一个函数是 JNI 函数。
- jobject 类型是 JNI 层对于 Java 层应用类型对象的表示。每一个从 Java 调用的 native 方法，在 JNI 函数中都会传递一个当前对象的引用。区分 2 种情况：
1、静态 native 方法：第二个参数为 jclass 类型，指向 native 方法所在类的 Class 对象；2、实例 native 方法：第二个参数为 jobject 类型，指向调用 native 方法的对象。
- JavaVM：代表 Java 虚拟机，每个 Java 进程有且仅有一个全局的 JavaVM 对象，JavaVM 可以跨线程共享；对应JNIInvokeInterface*数据结构。
- JNIEnv：代表 Java 运行环境，每个 Java 线程都有各自独立的 JNIEnv 对象，JNIEnv 不可以跨线程共享。对应JNINativeInterface*数据结构。

jni.h
```c
struct _JNIEnv;
struct _JavaVM;

#if defined(__cplusplus)
// 如果定义了 __cplusplus 宏，则按照 C++ 编译
typedef _JNIEnv JNIEnv;
typedef _JavaVM JavaVM;
#else
// 按照 C 编译
typedef const struct JNINativeInterface* JNIEnv;
typedef const struct JNIInvokeInterface* JavaVM;
#endif

/*
 * C++ 版本的 _JavaVM，内部是对 JNIInvokeInterface* 的包装
 */
struct _JavaVM {
    // 相当于 C 版本中的 JNIEnv
    const struct JNIInvokeInterface* functions;

    // 转发给 functions 代理
    jint DestroyJavaVM()
    { return functions->DestroyJavaVM(this); }
    ...
};

/*
 * C++ 版本的 JNIEnv，内部是对 JNINativeInterface* 的包装
 */
struct _JNIEnv {
    // 相当于 C 版本的 JavaVM
    const struct JNINativeInterface* functions;

    // 转发给 functions 代理
    jint GetVersion()
    { return functions->GetVersion(this); }
    ...
};
```
- c++层面的调用比c语言中更加简洁
```c
  // 在 C 语言中，要使用 (*env)->
// 注意看这一句：typedef const struct JNINativeInterface* JNIEnv;
(*env)->FindClass(env, "java/lang/String");

// 在 C++ 中，要使用 env->
// 注意看这一句：jclass FindClass(const char* name)
//{ return functions->FindClass(this, name); }
env->FindClass("java/lang/String");
```