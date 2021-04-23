//
// Created by llxnb on 2021/4/22.
//

#include <bits/stdc++.h>

using namespace std;

//关键字
vector<pair<string, int>> keyword = {
        // 声明变量
        {"auto"    , 1},
        {"int"     , 1},
        {"double"  , 1},
        {"float"   , 1},
        {"char"    , 1},
        {"string"  , 1},
        {"long"    , 1},
        {"struct"  , 1},
        {"register", 1},
        {"typedef" , 1},
        {"short"   , 1},
        {"union"   , 1},

        // 限定、修饰符号
        {"const"   , 2},
        {"unsigned", 2},
        {"signed"  , 2},
        {"static"  , 2},
        {"extern"  , 2},

        // 循环，分支语句
        {"for"     , 3},
        {"while"   , 3},
        {"switch"  , 3},
        {"case"    , 3},
        {"goto"    , 3},
        {"if"      , 3},
        {"else"    , 3},
        {"continue", 3},
        {"break"   , 3},
        {"do"      , 3},
        {"default" , 3},

        // 输入，输出
        {"scanf"   , 4},
        {"printf"  , 4},

        //函数类别
        {"void"    , 5},
        {"return"  , 5},
        {"volatile", 5}
};

// 运算符
string operatorChar = "+-*/=><&|~!%";

// 分界符
string delimiters   = "()[]{}#,;'\"";

// 识别是否为合法数字
pair<int, int> checkIfDigit(string str);

// 识别字符串类别（标识符/数字/关键字）
bool judge(string str, int line_count);

// 符号表，用于最后统计单词数量
unordered_map<string, int> chara_mp;

// 输入输出文件流
ifstream inputFile;
ofstream outFile;