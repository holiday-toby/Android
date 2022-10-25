# README

## 参考文档：
csapp目录为《深入理解计算机系统》一书的源码
[csapp.h头文件的使用 ---- 3种方法运行《深入理解计算机系统》中的代码](https://blog.csdn.net/ustc_sse_shenzhang/article/details/105744435)

## 编译代码步骤
1. csapp.c文件和 csapp.h文件 都复制到一个默认目录下，例如 /usr/local/include。
2. 生成动态库.so文件移入 /usr/local/lib目录下
3. 执行编译命令
   ```
   gcc -o prog cpstdin.c -lcsapp
   ```