import logging
import sys
import json
import io
import corenlp
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

def content_to_sentences(client, input_string):
    ann = client.annotate(input_string)
    content = []
    for sentence in ann.sentence:
        sentence2words = []
        for index,token in enumerate(sentence.token):
            sentence2words.append(token.word)
        content.append(sentence2words)
    return content

def add_title_word(word2id, id2word, title):
    for word in title:
        if word not in word2id.keys():
            id = len(word2id)
            word2id[word] = id
            id2word[id] = word

def add_content_word(word2id, id2word, content):
    for sentence in content:
        for word in sentence:
            if word not in word2id.keys():
                id = len(word2id)
                word2id[word] = id
                id2word[id] = word

if __name__ == '__main__':

    # preprocess dataset as :
    # content : List<List<String>>
    # title : List<String>
    # id: Int
    # create word2id : String,Int
    # create id2word : Int, String

    path_dir = "/home/wsy/桌面/Bytecup2018/key_sen/processed_key_sen_train.{0}/"
    output_path = "train.{0}.txt"
    output_title_path = "/home/wsy/PycharmProjects/TitleGeneration/resource/title.txt"
    output_content_path = "/home/wsy/PycharmProjects/TitleGeneration/resource/content.txt"

    word2id = {}
    id2word = {}
    id2word[0] = 'PAD'
    id2word[1] = 'SOS'
    id2word[2] = 'EOS'
    id2word[3] = 'OOV'
    word2id['PAD'] = 0
    word2id['SOS'] = 1
    word2id['EOS'] = 2
    word2id['OOV'] = 3
    content_word2id = {}
    content_id2word = {}

    with corenlp.CoreNLPClient(annotators="tokenize ssplit".split()) as client:
        for index in range(9):
            path_list = file_name(path_dir.format(index))
            with io.open(path_dir.format(index)+output_path.format(index), encoding="utf8", mode="w+") as file:
                for res_dict in read_file(path_dir.format(index)+path_list[0], extract_content):
                    content = res_dict["sentence_list"]
                    title = res_dict["title"]
                    content = res_dict["sentence_list"]
                    add_content_word(content_word2id, content_id2word, content)
                    title_words = content_to_sentences(client,title)[0]
                    add_title_word(word2id,id2word,title_words)
                    res_dict["title"] = title_words
                    file.write(json.dumps(res_dict) + "\n")
    title_vocab_size = len(word2id)

    # for index in range(9):
    #     for res_dict in read_file(path_dir.format(index)+output_path.format(index), extract_content):
    #         title = res_dict["title"]
    #         add_title_word(word2id,id2word,title)
    #
    # for index in range(9):
    #     for res_dict in read_file(path_dir.format(index)+output_path.format(index), extract_content):
    #         content = res_dict["sentence_list"]
    #         add_content_word(word2id,id2word,content)

    with io.open(output_title_path,encoding="utf8", mode="a+") as file1:
        id_word = {}
        for id,word in id2word.items():
            id_word["id"] = id
            id_word["word"] = word
            file1.write(json.dumps(id_word)+"\n")
    with io.open(output_content_path, encoding="utf8", mode="a+") as file2:
        id_word2 = {}
        for id,word in content_id2word.items():
            id_word2["id"] = id+title_vocab_size
            id_word2["word"] = word
            file2.write(json.dumps(id_word2)+"\n")
