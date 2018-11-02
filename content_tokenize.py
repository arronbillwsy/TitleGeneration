import logging
import sys
import json
import io
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import sent_tokenize
import nltk
import re
nltk.download('punkt')


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


if __name__ == '__main__':
    path = "/home/wsy/桌面/Bytecup2018/data/raw_data/bytecup.corpus.train.{0}.txt"
    output_path = "/home/wsy/桌面/Bytecup2018/data/processed_data/processed_train.{0}.txt"
    # path = "D:/Data/data/raw_data/bytecup.corpus.train.{0}.txt"
    # output_path = "D:/Data/data/processed_data/processed_train.{0}.txt"
    max_sen_len = 48
    for index in range(9):
        with io.open(output_path.format(index), encoding="utf8", mode="w+") as output_file:
            for res_dict in read_file(path.format(index), extract_content):
                content = res_dict["content"]
                title = res_dict["title"]
                dot_no_white_space = re.compile('(?<=[a-z])\.(?=[A-Z0-9”“])')
                content_no_white_space = dot_no_white_space.sub('. ', content)
                dot_standard_punctuation = re.compile('([:;])')
                content_no_white_space = dot_standard_punctuation.sub('.', content_no_white_space)
                sentences = sent_tokenize(content_no_white_space)
                words = []
                for i in range(len(sentences)):
                    word_res = wordpunct_tokenize(sentences[i])
                    if len(word_res) < max_sen_len:
                        words.append(word_res)
                    else:
                        words.append(word_res[:max_sen_len])

                res_dict["content"] = words
                title_words = wordpunct_tokenize(title)
                res_dict["title"] = title_words
                output_file.write(json.dumps(res_dict) + "\n")
