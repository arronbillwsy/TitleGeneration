import io
import logging
import sys
import json


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


def read_dict(title_path,content_path):
    word2id = {}
    id2word = {}
    title_vocab_size = 0
    for res_dict in read_file(title_path, extract_content):
        word2id[res_dict["word"]] = res_dict["id"]
        id2word[res_dict["id"]] = res_dict["word"]
    title_vocab_size = len(word2id)
    for res_dict in read_file(content_path, extract_content):
        word2id[res_dict["word"]] = res_dict["id"]
        id2word[res_dict["id"]] = res_dict["word"]
    return word2id, id2word, title_vocab_size

# output_title_path = "/home/wsy/PycharmProjects/TitleGeneration/TitleGeneration/resource/title.txt"
# output_content_path = "/home/wsy/PycharmProjects/TitleGeneration/TitleGeneration/resource/content.txt"
# w2id,id2w,size = read_dict(output_title_path,output_content_path)
# print(w2id.__len__())
# print(id2w.__len__())
# print(size)
# print(1)


def doc2id(word2id, content):
    doc_id = []
    doc_oov_dict = []
    initial = len(word2id)
    for sentence in content:
        sentence_id = []
        sen_oov_dict = {}
        for word in sentence:
            if word in word2id.keys():
                sentence_id.append(word2id[word])
            else:
                oov_index = initial + len(sen_oov_dict)
                sentence_id.append(oov_index)
                sen_oov_dict[word] = oov_index
        doc_id.append(sentence_id)
        doc_oov_dict.append(sen_oov_dict)
    return doc_id, doc_oov_dict


def title2id(word2id, size, title):
    title_id = []
    title_vocab = {key:value for key,value in word2id.items() if value<size}
    for word in title:
        if word in title_vocab.keys():
            title_id.append(title_vocab[word])
        else:
            title_id.append(3)
    return title_id
