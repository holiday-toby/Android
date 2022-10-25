#include <stdio.h>
#include <stdlib.h>

/**
 * @brief 
 * ANSI C 定义了许多宏。在编程中您可以使用这些宏，但是不能直接修改这些预定义的宏。
 */
void test1()
{
    printf("File :%s\n", __FILE__); //这会包含当前文件名，一个字符串常量。
    printf("Date :%s\n", __DATE__); //当前日期，一个以 "MMM DD YYYY" 格式表示的字符常量。
    printf("Time :%s\n", __TIME__); //当前时间，一个以 "HH:MM:SS" 格式表示的字符常量。
    printf("Line :%d\n", __LINE__); //这会包含当前行号，一个十进制常量。
    printf("ANSI :%d\n", __STDC__); //当编译器以 ANSI 标准编译时，则定义为 1。
    
}

/**
 * @brief 
 *  宏延续运算符（\）
一个宏通常写在一个单行上。但是如果宏太长，一个单行容纳不下，则使用宏延续运算符（\）。例如：
 */
#define  message_for(a, b)  \
    printf(#a " and " #b ": We love you!\n")

void test2()
{
     message_for(Lucy,Toby);
}

int main()
{
    test1();
    test2();
    return 0;
}