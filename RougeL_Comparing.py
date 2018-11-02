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


def extract_content(input_string):
    return json.loads(input_string)


def lcs(s, t):
    m = len(s)
    n = len(t)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    for i in range(m):
        for j in range(n):
            if s[i] == t[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c > longest:
                    longest = c
    return longest


if __name__ == '__main__':
    path_dir = "D:/Data/bytecup2018/part-00000-48d20e09-30e0-463d-b0dd-42425ed6abc3-c000.txt"
    path = "D:/Data/bytecup2018/processed_train.0.txt"
    output_path = "D:/Data/bytecup2018/RougeL/RougeL_compare.0.txt"
    output_path1 = "D:/Data/bytecup2018/RougeL/compare.0.txt"
    compare = {}
    with io.open(output_path1, encoding="utf8", mode="w+") as file1:
        index = 0
        res = {}
        count = 0
        for res_dict in read_file(path_dir, extract_content):
            if count > 1000:
                break
            count += 1
            content = res_dict["sentence_list"]
            title = res_dict["title"]
            num = []
            for sen in content:
                num.append(lcs(sen, title))
            res["rouge l"] = num
            file1.write(json.dumps(res) + "\n")
    with io.open(output_path, encoding="utf8", mode="w+") as file2:
        index = 0
        res = {}
        count = 0
        for res_dict in read_file(path, extract_content):
            if count > 1000:
                break
            count += 1
            content = res_dict["content"]
            title = res_dict["title"]
            num = []
            for sen in content:
                num.append(lcs(sen, title))
            num.sort(reverse=True)
            num = num[:10]
            res["rouge l"] = num
            file2.write(json.dumps(res) + "\n")