
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

    return {err, point}; // 是否出错&是否为浮点数
}

bool judge(string str, int line_count){// 判断是否为数字/标识符/关键字
    if (str.empty())
        return true;

    for (auto & i : keyword) {
        if (str == i.first){
            outFile <<"( " << i.second << ", - )"<<endl;

            if (chara_mp.find(str)!=chara_mp.end()){// exist
                chara_mp[str] += 1;
            } else {//not exist
                chara_mp[str] = 1;
            }

            return true;
        }
    }

    if ((str[0] >= 'a' and str[0] <= 'z')
        or (str[0] >= 'A' and str[0] <= 'Z')
        or str[0] == '_'){//标识符

        if (chara_mp.find(str)!=chara_mp.end()){// exist
            chara_mp[str] += 1;
        } else {//not exist
            chara_mp[str] = 1;
        }

        identifier_mp[identifier_mp.size()] = str;
        outFile << "( 71, " << identifier_mp.size() << " )" <<endl;

        return true;
    } else if (str[0] >= '0' and str[0] <= '9') { // 数字开头
        pair<int, int> p_temp = checkIfDigit(str);

        if (p_temp.first == 0 and p_temp.second == 0){

            constTable.emplace_back(str, 68);
            outFile << "( 68, "<< constTable.size() << " )" <<endl; //整数

            if (chara_mp.find(str)!=chara_mp.end()){// exist
                chara_mp[str] += 1;
            } else {//not exist
                chara_mp[str] = 1;
            }

        } else if (p_temp.first == 1 and p_temp.second == 0){
            cout << "Error Occurred At Line " << line_count <<", Error Type: Invalid Digit" << endl;
            error_mp[error_mp.size()] = str;
            outFile << "( -1, " << error_mp.size() << " )" <<endl;
        } else if (p_temp.first == 1 and p_temp.second == 1){
            cout << "Error Occurred At Line " << line_count << ", Error Type: Invalid Float Digit" << endl;
            error_mp[error_mp.size()] = str;
            outFile << "( -2, " << error_mp.size() << " )" <<endl;
        } else {
            constTable.emplace_back(str, 69);
            outFile << "( 69, " << constTable.size() <<" )" <<endl; // 浮点数

            if (chara_mp.find(str)!=chara_mp.end()){// exist
                chara_mp[str] += 1;
            } else {//not exist
                chara_mp[str] = 1;
            }
        }

        if (p_temp.first == 1)
            return false;

        return true;
    } else {
        error_mp[error_mp.size()] = str;
        cout << "Error Occurred At Line " << line_count << ", Error Type: Invalid Identifier" << endl;
        outFile << "( -4, " << error_mp.size() <<" )" <<endl;
        return false;
    }

//    cout << flag << endl;
}

void output2Symbol_table(unordered_map<int, string> mp, vector<pair<string, int>> constTable, unordered_map<int, string> error_mp){

    symbol_table << "Const Table:" << endl;

    for (int i = 0; i < constTable.size(); ++i) { // 输入常数表
        symbol_table << i+1 << " " << constTable[i].first << ": Code: " << constTable[i].second << endl;
    }

    symbol_table << endl;

    symbol_table << "Identifier Table:" << endl;

    vector<string> symbol_temp;

    for (auto & i : mp) {
        symbol_temp.push_back(i.second);
    }
    for (int i = symbol_temp.size()-1; i >=0 ; --i) {
        symbol_table << symbol_temp.size()-i << " Name: " << symbol_temp[i] << endl;
    }

    symbol_table << endl;

    symbol_table << "Error Table:" << endl;

    vector<string> err_temp;

    for (auto & i : error_mp) {
        err_temp.push_back(i.second);
    }
    for (int i = err_temp.size()-1; i >=0 ; --i) {
        symbol_table << err_temp.size()-i << " Name: " << err_temp[i] << endl;
    }
    symbol_table << endl;

}

int main() {
    string path;

    cout<<"Input Test File Path, If Using Default Path, Enter default"<<endl;
    cin >> path;
    cout << "====================================Lexical  Analysis  Begin  ====================================" << endl;

    if (path == "default")
        inputFile.open("test_programme.txt");
    else
        inputFile.open(path);

    outFile.open("result.txt");
    symbol_table.open("symbol_table.txt");

    string test_str;

    int line_count = 1;// 统计行数
    int word_count = 0;// 统计单词数
    int char_count = 0;// 统计字符数
    int err_count  = 0;// 统计错误数

    while (getline(inputFile, test_str)){

//        cout<<test_str<<endl;

        int curr = 0;

        for (; curr < test_str.size(); curr++){
//            cout<<"curr: "<<test_str[curr]<<endl;

            int state = 0; // 初始化状态，每次循环读入都需要从开始状态开始

            if (test_str[curr] == ' ' or test_str[curr] == '\t' or test_str[curr] == '\n')
                continue;

            for (char c : delimiters) {
                if (test_str[curr] == c){
                    word_count++;
                    outFile << "( ";

                    switch (c) {
                        case '(' : {
                            outFile <<"56";
                            break;
                        }
                        case ')' : {
                            outFile <<"57";
                            break;
                        }
                        case '[' : {
                            outFile <<"58";
                            break;
                        }
                        case ']' : {
                            outFile <<"59";
                            break;
                        }
                        case '{' : {
                            outFile <<"60";
                            break;
                        }
                        case '}' : {
                            outFile <<"61";
                            break;
                        }
                        case '#' : {
                            outFile <<"62";
                            break;
                        }
                        case ',' : {
                            outFile <<"63";
                            break;
                        }
                        case ';' : {
                            outFile <<"64";
                            break;
                        }
                        case '\'': {
                            outFile <<"65";
                            break;
                        }
                        case '"' : {
                            outFile <<"66";
                            break;
                        }
                        case ':' : {
                            outFile <<"67";
                            break;
                        }
                    }
                    outFile << ", - )" << endl;

                    char tempArray[2];
                    tempArray[0] = test_str[curr];
                    tempArray[1] = '\0';
                    string temp = tempArray;

                    if (chara_mp.find(temp)!=chara_mp.end()){// exist
                        chara_mp[temp] += 1;
                    } else {//not exist
                        chara_mp[temp] = 1;
                    }

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

                            char tempArray[3];
                            tempArray[0] = test_str[curr];
                            tempArray[1] = test_str[curr+1];
                            tempArray[2] = '\0';
                            string temp = tempArray;

                            if (chara_mp.find(temp)!=chara_mp.end()){// exist
                                chara_mp[temp] += 1;
                            } else {//not exist
                                chara_mp[temp] = 1;
                            }

                            if (temp == "++") {// 两个字符的运算符
                                outFile<<"( 45, - )";
                            } else if (temp == "--"){
                                outFile<<"( 46, - )";
                            } else if (temp == "**"){
                                outFile<<"( 47, - )";
                            } else if (temp == "+="){
                                outFile<<"( 48, - )";
                            } else if (temp == "-="){
                                outFile<<"( 49, - )";
                            } else if (temp == "*="){
                                outFile<<"( 50, - )";
                            } else if (temp == "/="){
                                outFile<<"( 51, - )";
                            } else if (temp == "=="){
                                outFile<<"( 52, - )";
                            } else if (temp == ">="){
                                outFile<<"( 53, - )";
                            } else if (temp == "<="){
                                outFile<<"( 54, - )";
                            } else if(temp == "!="){
                                outFile<<"( 55, - )";
                            } else{
                                err_count++;
                                cout<<"Error Occurred At Line "<<line_count<<", Error Type :Invalid Operator"<<endl;
                                error_mp[error_mp.size()] = temp;
                                outFile<<"( -3 , "<< error_mp.size()<<" )"<<endl;
                            }

                        } else {
                            char tempArray[3];

                            tempArray[0] = test_str[curr];
                            tempArray[1] = test_str[curr+1];
                            tempArray[2] = '\0';

                            string temp = tempArray;

                            err_count++;

                            cout<<"Error Occurred At Line "<<line_count<<", Error Type :Invalid Operator"<<endl;
                            error_mp[error_mp.size()] = temp;
                            outFile<<"( -3 , "<< error_mp.size()<<" )"<<endl;
                        }

                        curr++;
                    } else {

                        char tempArray[2];
                        tempArray[0] = test_str[curr];
                        tempArray[1] = '\0';

                        string temp = tempArray;

                        if (chara_mp.find(temp)!=chara_mp.end()){// exist
                            chara_mp[temp] += 1;
                        } else {//not exist
                            chara_mp[temp] = 1;
                        }

                        switch (test_str[curr]) {
                            case '+':{
                                outFile<<"( 34, - )";
                                break;
                            }
                            case '-':{
                                outFile<<"( 35, - )";
                                break;
                            }
                            case '*':{
                                outFile<<"( 36, - )";
                                break;
                            }
                            case '/':{
                                outFile<<"( 37, - )";
                                break;
                            }
                            case '=':{
                                outFile<<"( 38, - )";
                                break;
                            }
                            case '>':{
                                outFile<<"39, - )";
                                break;
                            }
                            case '<':{
                                outFile<<"( 40, - )";
                                break;
                            }
                            case '&':{
                                outFile<<"( 41, - )";
                                break;
                            }
                            case '|':{
                                outFile<<"( 42, - )";
                                break;
                            }
                            case '!':{
                                outFile<<"( 43, - )";
                                break;
                            }
                            case '%':{
                                outFile<<"( 44, - )";
                                break;
                            }

                            default:{
                                err_count++;
                                cout<<"Error Occurred At Line "<<line_count<<", Error Type :Invalid Operator"<<endl;
                                error_mp[error_mp.size()] = temp;
                                outFile<<"( -3 , "<< error_mp.size()<<" )"<<endl;
                            }
                        }
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
                err_count++;
            }
            word_count++;
        }

        line_count++;
        char_count += test_str.size();

    }

    // 统计结果
    outFile << endl << "====================================Statistics Data====================================\n";
    outFile << "Total Lines: " << line_count <<endl;
    outFile << "Total Words: " << word_count << endl;
    outFile << "Total characters: " << char_count << endl;

    outFile << "Total Errors: " << err_count << endl;

    outFile << "====================================Each Word Count====================================" << endl;

    for (auto & iter : chara_mp) {
        outFile << "Word: " << iter.first << " Count: " << iter.second <<endl;
    }

    output2Symbol_table(identifier_mp, constTable, error_mp);

    inputFile.close();
    outFile.close();
    symbol_table.close();

    cout<<"====================================Lexical Analysis Completed===================================="<<endl;
    if (err_count == 0){
        cout << "No Error Happened, Perfect!";
    }
    cout<<endl;

    return 0;
}
