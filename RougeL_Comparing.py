import logging
import sys
import json
import io
import operator
import os


def read_file(file_path, pre_process=lambda x: x, encoding="utf-8"):
    """
    """
    try:
        with io.open(file_path, encoding=encoding) as file:
            for sentence in file:
                yield (pre_process(sentence))

    except IOError as err:
        logging.error("Failed to open file {0}".format(err))
        sys.exit(1)

def file_name(file_dir):
    L=[]
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.txt':
                L.append(file)
    return L

def extract_content(input_string):
    return json.loads(input_string)

# Dynamic Programming implementation of LCS problem

def lcs(S,T):
    m = len(S)
    n = len(T)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    lcs_set = set()
    for i in range(m):
        for j in range(n):
            if S[i] == T[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(S[i-c+1:i+1])
                elif c == longest:
                    lcs_set.add(S[i-c+1:i+1])

    return lcs_set.__len__()

def word2sentence(content):
    sentence_list = []
    for sentence in content:
        sen = " ".join(str(x) for x in sentence)
        sentence_list.append(sen)
    return sentence_list

def rougeL(content,title):
    key_sentence = {}
    for sentence in content:
        sen = " ".join(str(x) for x in sentence)
        key_sentence[sen] = lcs(sen,title)
    sorted_list = sorted(key_sentence.items(), key=operator.itemgetter(1), reverse=True)[:10]
    res = []
    for t in sorted_list:
        res.append(t[0])
    return res


if __name__ == '__main__':
    path_dir = "/home/wsy/桌面/Bytecup2018/key_sen/processed_key_sen_train.0/train.0.txt"
    path = "/home/wsy/桌面/Bytecup2018/preprocess_data/processed_train.0.txt"
    output_path = "/home/wsy/桌面/Bytecup2018/RougeL/RougeL_compare.0.txt"
    output_path1 = "/home/wsy/桌面/Bytecup2018/RougeL/compare.0.txt"
    compare = {}
    with io.open(output_path1, encoding="utf8", mode="w+") as file1:
        index = 0
        for res_dict in read_file(path_dir, extract_content):
            content = res_dict["sentence_list"]
            title = res_dict["title"]
            res_dict["sentence_list"] = word2sentence(content)
            res_dict["title"] = " ".join(str(x) for x in title)
            file1.write(json.dumps(res_dict) + "\n")

    with io.open(output_path, encoding="utf8", mode="w+") as file1:
        index = 0
        for res_dict in read_file(path, extract_content):
            content = res_dict["content"]
            title = res_dict["title"]
            res_dict["content"] = rougeL(content,title)
            file1.write(json.dumps(res_dict) + "\n")