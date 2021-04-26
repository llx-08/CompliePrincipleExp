//
// Created by llxnb on 2021/4/22.
//

#include <bits/stdc++.h>

using namespace std;

//关键字
vector<pair<string, int>> keyword = {
        // 声明变量
        {"auto"    , 1},
        {"int"     , 2},
        {"double"  , 3},
        {"float"   , 4},
        {"char"    , 5},
        {"string"  , 6},
        {"long"    , 7},
        {"struct"  , 8},
        {"register", 9},
        {"typedef" , 10},
        {"short"   , 11},
        {"union"   , 12},

        // 限定、修饰符号
        {"const"   , 13},
        {"unsigned", 14},
        {"signed"  , 15},
        {"static"  , 16},
        {"extern"  , 17},

        // 循环，分支语句
        {"for"     , 18},
        {"while"   , 19},
        {"switch"  , 20},
        {"case"    , 21},
        {"goto"    , 22},
        {"if"      , 23},
        {"else"    , 24},
        {"continue", 25},
        {"break"   , 26},
        {"do"      , 27},
        {"default" , 28},

        // 输入，输出
        {"scanf"   , 29},
        {"printf"  , 30},

        //函数类别
        {"void"    , 31},
        {"return"  , 32},
        {"volatile", 33},

        // 布尔常量
        {"true"    , 70},
        {"false"   , 70}
};

// 运算符
string operatorChar = "+-*/=><&|~!%";

// 分界符
string delimiters   = "()[]{}#,;'\":";

// 识别是否为合法数字
pair<int, int> checkIfDigit(string str);

// 识别字符串类别（标识符/数字/关键字）
bool judge(string str, int line_count);

// 符号表，用于最后统计单词数量
unordered_map<string, int> chara_mp;

// 临时存储符号表错误表以及常数表的vector
unordered_map<int, string> identifier_mp;
unordered_map<int, string> error_mp;
vector<pair<string, int>> constTable;

// 符号表接口
void output2Symbol_table(unordered_map<int, string> mp,
                         vector<pair<string, int>> constTable,
                         unordered_map<int, string> error_mp);

// 输入输出文件流
ifstream inputFile;    // 待进行词法分析源程序
ofstream outFile;      // 分析结果
ofstream symbol_table; // 符号表,常数表输出流
ofstream error_table;  // 错误表

