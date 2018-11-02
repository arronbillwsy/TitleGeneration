import logging
import sys
import json
import io
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
    file_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.txt':
                file_list.append(file)
    return file_list


def extract_content(input_string):
    return json.loads(input_string)


def add_title_word(title_word2id, title):
    for word_title in title:
        word_title = str.lower(word_title)
        if word_title not in title_word2id.keys():
            id_t = len(title_word2id)
            title_word2id[word_title] = id_t


def add_content_word(content_word2id, title_word2id, content, size):
    for sentence in content:
        for word_content in sentence:
            word_content = str.lower(word_content)
            if word_content not in title_word2id.keys() and word_content not in content_vocab.keys():
                id_c = len(content_word2id) + size
                content_word2id[word_content] = id_c


if __name__ == '__main__':

    # preprocess dataset as :
    # content : List<List<String>>
    # title : List<String>
    # id: Long
    # create word2id : String,Long

    path_dir = "/home/wsy/桌面/Bytecup2018/data/key_sen/processed_key_sen_train.{0}/"
    output_title_path = "/home/wsy/桌面/Bytecup2018/data/vovab/title.txt"
    output_content_path = "/home/wsy/桌面/Bytecup2018/data/vovab/content.txt"
    title_vocab = {}
    title_vocab['PAD'] = 0
    title_vocab['SOS'] = 1
    title_vocab['EOS'] = 2
    title_vocab['OOV'] = 3
    content_vocab = {}
    for index in range(9):
        path_list = file_name(path_dir.format(index))
        for res_dict in read_file(path_dir.format(index)+path_list[0], extract_content):
            title = res_dict["title"]
            add_title_word(title_vocab, title)
    title_vocab_size = len(title_vocab)
    for index in range(9):
        path_list = file_name(path_dir.format(index))
        for res_dict in read_file(path_dir.format(index)+path_list[0], extract_content):
            content = res_dict["sentence_list"]
            add_content_word(content_vocab, title_vocab, content, title_vocab_size)
    with io.open(output_title_path,encoding="utf8", mode="a+") as file1:
        id_word = {}
        for word, id_title in title_vocab.items():
            id_word["id"] = id_title
            id_word["word"] = word
            file1.write(json.dumps(id_word)+"\n")
    with io.open(output_content_path, encoding="utf8", mode="a+") as file2:
        id_word2 = {}
        for word, id_content in content_vocab.items():
            id_word2["id"] = id_content
            id_word2["word"] = word
            file2.write(json.dumps(id_word2)+"\n")
