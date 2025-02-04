#include <iostream>
#include <cstring>

using namespace std;

// 声明一个结构体类型 Books
struct Books
{
   char title[50];
   char author[50];
   char subject[100];
   int book_id;
};

int main(void)
{
   Books Book1; // 定义结构体类型 Books 的变量 Book1
   Books Book2; // 定义结构体类型 Books 的变量 Book2

   // Book1 详述
   strcpy(Book1.title, "C++ 教程");
   strcpy(Book1.author, "Runoob");
   strcpy(Book1.subject, "编程语言");
   Book1.book_id = 12345;

   // Book2 详述
   strcpy(Book2.title, "CSS 教程");
   strcpy(Book2.author, "Runoob");
   strcpy(Book2.subject, "前端技术");
   Book2.book_id = 12346;

   Books &book_my = Book1;

   strcpy(book_my.author, "Toby");

   // 输出 Book1 信息
   cout << "第一本书标题 : " << Book1.title << endl;
   cout << "第一本书作者 : " << Book1.author << endl;
   cout << "第一本书类目 : " << Book1.subject << endl;
   cout << "第一本书 ID : " << Book1.book_id << endl;

   // 输出 Book2 信息
   cout << "第二本书标题 : " << Book2.title << endl;
   cout << "第二本书作者 : " << Book2.author << endl;
   cout << "第二本书类目 : " << Book2.subject << endl;
   cout << "第二本书 ID : " << Book2.book_id << endl;

   // 输出 Book1 信息
   cout << "第一本书标题 : " << book_my.title << endl;
   cout << "第一本书作者 : " << book_my.author << endl;
   cout << "第一本书类目 : " << book_my.subject << endl;
   cout << "第一本书 ID : " << book_my.book_id << endl;

   return 0;
}