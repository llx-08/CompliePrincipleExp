
#include "main.h"
using namespace std;


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

bool judge(string str, int line_count){// 判断是否为数字/标识符/关键字

    for (auto & i : keyword) {
        if (str == i.first){
            outFile <<"( "<<str<<","<<i.second<<" )"<<endl;

            if (chara_mp.find(str)!=chara_mp.end()){// exist
                chara_mp[str] += 1;
            } else {//not exist
                chara_mp[str] = 1;
            }

            return true;
        }
    }

    if ((str[0] < '0' or str[0] > '9')
        or (str[0] >= 'a' and str[0] <= 'z')
        or (str[0] >= 'A' and str[0] <= 'Z')
        or str[0] == '_'){//标识符

        if (chara_mp.find(str)!=chara_mp.end()){// exist
            chara_mp[str] += 1;
        } else {//not exist
            chara_mp[str] = 1;
        }

        outFile << "( " << str <<", Identifier )" <<endl;
        return true;

    } else { // 数字开头
        pair<int, int> p_temp = checkIfDigit(str);
        if        (p_temp.first == 0 and p_temp.second == 0){

            outFile << "( " << str <<", Int Digit )" <<endl;

            if (chara_mp.find(str)!=chara_mp.end()){// exist
                chara_mp[str] += 1;
            } else {//not exist
                chara_mp[str] = 1;
            }

        } else if (p_temp.first == 1 and p_temp.second == 0){
            cout << "Error Occurred At Line " << line_count << endl;
            outFile << "( " << str <<", Error Digit )" <<endl;
        } else if (p_temp.first == 1 and p_temp.second == 1){
            cout << "Error Occurred At Line " << line_count << endl;
            outFile << "( " << str <<", Error Float Digit )" <<endl;
        } else {
            outFile << "( " << str <<", Float Digit )" <<endl;

            if (chara_mp.find(str)!=chara_mp.end()){// exist
                chara_mp[str] += 1;
            } else {//not exist
                chara_mp[str] = 1;
            }

        }

        if (p_temp.first == 1)
            return false;

        return true;
    }

//    cout << flag << endl;
}

int main() {
    string path;

    cout<<"Input Test File Path, If Using Default Path, Enter default"<<endl;
    cin >> path;
    cout << "====================================Lexical Analysis Begin====================================" << endl;

    if (path == "default")
        inputFile.open("test_programme.txt");
    else
        inputFile.open(path);

    outFile.open("result.txt");

    string test_str;

    int line_count = 0;// 统计行数
    int word_count = 0;// 统计单词数
    int char_count = 0;// 统计字符数
    int err_count  = 0;// 统计错误数

    while (getline(inputFile, test_str)){

        cout<<test_str<<endl;

        int curr = 0;

        for (; curr < test_str.size(); curr++){

            int state = 0; // 初始化状态，每次循环读入都需要从开始状态开始

            if (test_str[curr] == ' ' or test_str[curr] == '\t' or test_str[curr] == '\n')
                continue;

            for (char c : delimiters) {
                if (test_str[curr] == c){
                    word_count++;
                    outFile << "(" << test_str[curr] <<", delimiters)" <<endl;

//                    string temp = reinterpret_cast<const char *>(test_str[curr]);
//                    if (chara_mp.find(temp)!=chara_mp.end()){// exist
//                        chara_mp[temp] += 1;
//                    } else {//not exist
//                        chara_mp[temp] = 1;
//                    }

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

//                            string temp = reinterpret_cast<const char *>(test_str[curr] + test_str[curr + 1]);
//
//                            if (chara_mp.find(temp)!=chara_mp.end()){// exist
//                                chara_mp[temp] += 1;
//                            } else {//not exist
//                                chara_mp[temp] = 1;
//                            }
                        } else {
                            outFile<<"( "<<test_str[curr]+test_str[curr+1]<<", Error:Invalid Operator )"<<endl;
                        }

                        curr++;
                    } else {
                        outFile<<"( "<<test_str[curr]<<", Operator )"<<endl;
//                        string temp = reinterpret_cast<const char *>(test_str[curr]);
//                        if (chara_mp.find(temp)!=chara_mp.end()){// exist
//                            chara_mp[temp] += 1;
//                        } else {//not exist
//                            chara_mp[temp] = 1;
//                        }
                    }
                    word_count++;
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

            bool flag = judge(temp, line_count);

            if (flag == false){
//                cout<<test_str[curr]<<" ???"<<endl;
                err_count++;
            }
            word_count++;
        }

        line_count++;
        char_count += test_str.size();

    }

    // 统计结果
    outFile << endl << "====================================Statistics Data====================================";
    outFile << "Total Lines: " << line_count <<endl;
    outFile << "Total Words: " << word_count << endl;
    outFile << "Total characters: " << char_count << endl;

    outFile << "Total Errors: " << err_count << endl;

    outFile << "====================================Each Word Count====================================" << endl;

    for (auto & iter : chara_mp) {
        outFile << "Word: " << iter.first << " Count: " << iter.second <<endl;
    }

    inputFile.close();
    outFile.close();

    cout<<"====================================Lexical Analysis Completed===================================="<<endl;
    if (err_count == 0){
        cout << "No Error Happened, Perfect!";
    }
    cout<<endl;

    return 0;
}
