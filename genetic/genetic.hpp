#include <iostream>
#include <string>
#include <cstdlib>
#include <cstdio>
#include <ctime>
#include <vector>
using namespace std;

string Random_string(int num);                                                 // 随机生成长度为num的字符串
string generate_child(string mother, string father, int mid);                  // 由父母生成子代
string mutate(string child);                                                   // 子代发生变异
double Fitness_score(string src_str, string g_str);                            // 评分函数，为每个解序列评分
void quick_sort(string src_str, vector<string> &solution, int head, int tail); // 根据适应性评分对解池中的解序列进行排序。采用引用&，把排序结果传递回来
void Genetic_something(string some_str);                                       // 遗传算法主体
