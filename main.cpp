#include <bits/stdc++.h>

using namespace std;

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

string operatorChar = "+-*/=><&|~!";

string delimiters   = "()[]{}#,;'\"";



pair<int, int> checkIfDigit(string str){

    int err = 0;
    int point = 0;

    if (str[0] == '0' and str[1] == 'x'){//16进制
        for (int i = 2; i < str.size(); ++i) {
            if (str[i] == '.' and point == 0){
                point = 1;
                continue;
            } else if (str[i] == '.' and point == 1){
                err = 1;
                break;
            }

            if (isdigit(str[i]) or (str[i] >= 'a' and str[i] < 'f') or (str[i] >= 'A' and str[i] < 'F'))
                continue;
            else{
                err = 1;
                break;
            }
        }
    } else {

        for (int i = 0; i < str.size(); ++i) {

            if (str[i] == '.' and point == 0){
                point = 1;
                continue;
            } else if (str[i] == '.' and point == 1){
                err = 1;
                break;
            }

            if (isdigit(str[i]))
                continue;
            else{
                err = 1;
                break;
            }
        }
    }

    return {err, point};
}
ifstream inputFile;
ofstream outFile;

void judge(string str){// 判断是否为数字/标识符/关键字

    for (auto & i : keyword) {
        if (str == i.first){
            outFile <<"( "<<str<<","<<i.second<<" )"<<endl;
            return;
        }
    }

    if ((str[0] < '0' or str[0] > '9')
        or (str[0] >= 'a' and str[0] <= 'z')
        or (str[0] >= 'A' and str[0] <= 'Z')
        or str[0] == '_'){//标识符

        outFile << "( " << str <<", Identifier )" <<endl;

    } else { // 数字开头
        pair<int, int> p_temp = checkIfDigit(str);
        if        (p_temp.first == 0 and p_temp.second == 0){
            outFile << "( " << str <<", Int Digit )" <<endl;
        } else if (p_temp.first == 1 and p_temp.second == 0){
            outFile << "( " << str <<", Error Digit )" <<endl;
        } else if (p_temp.first == 1 and p_temp.second == 1){
            outFile << "( " << str <<", Error Float Digit )" <<endl;
        } else {
            outFile << "( " << str <<", Float Digit )" <<endl;
        }
    }

//    cout << flag << endl;
}

int main() {
    inputFile.open("test_programme.txt");
    outFile.open("result.txt");

    string test_str;
    while (getline(inputFile, test_str)){
        cout<<test_str<<endl;

        int curr = 0;

        for (; curr < test_str.size(); curr++){

            int state = 0; // 初始化状态，每次循环读入都需要从开始状态开始

            if (test_str[curr] == ' ' or test_str[curr] == '\t' or test_str[curr] == '\n')
                continue;

            for (char c : delimiters) {
                if (test_str[curr] == c){
                    outFile << "(" << test_str[curr] <<", delimiters)" <<endl;
                    state = -1;//本次读取终结状态
                    break;
                }
            }

            if (state == -1) // 是分界符，下一轮读取
                continue;

            for (char c : operatorChar){
                if (test_str[curr] == c){

                    state = -1;

                    char c_next = test_str[curr+1];

                    int doubleOp = 0;

                    for (char c_n : operatorChar){
                        if (c_n == c_next){
                            doubleOp = 1;
                            break;
                        }
                    }

                    if (doubleOp != 0){// +=,-=,*=,/=,%=,==,<=,>=
                        if (
                                (test_str[curr+1] == '='  and test_str[curr] != '&' and test_str[curr] != '|') or
                                (test_str[curr] == '+' and test_str[curr+1] == test_str[curr]) or // ++
                                (test_str[curr] == '-' and test_str[curr+1] == test_str[curr]) or // --
                                (test_str[curr] == '*' and test_str[curr+1] == test_str[curr]) or // **
                                (test_str[curr] == '&' and test_str[curr+1] == test_str[curr]) or // &&
                                (test_str[curr] == '|' and test_str[curr+1] == test_str[curr])    // ||
                                ){
                            outFile<<"( "<<test_str[curr]<<test_str[curr+1]<<", Operator )"<<endl;
                        } else {
                            outFile<<"( "<<test_str[curr]+test_str[curr+1]<<", Error:Invalid Operator )"<<endl;
                        }

                        curr++;
                    } else {
                        outFile<<"( "<<test_str[curr]<<", Operator )"<<endl;
                    }
                    break;
                }
            }

            if (state == -1)
                continue;

            string temp;// 关键字/数字/标识符

            while (('a' <= test_str[curr] and test_str[curr] <= 'z') or
                   ('A' <= test_str[curr] and test_str[curr] <= 'Z') or
                   ('0' <= test_str[curr] and test_str[curr] <= '9') or
                     test_str[curr] == '_' or test_str[curr] == '.'){
                    temp.push_back(test_str[curr]);
                    curr++;
            }
            curr--;

            judge(temp);
        }
    }

    inputFile.close();
    outFile.close();

    cout<<"Lexical Analysis Completed"<<endl;

    return 0;
}
