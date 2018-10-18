import logging
import sys
import json
import io
import corenlp


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
    for word in content:
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

    path = "/home/wsy/桌面/Bytecup2018/bytecup.corpus.train.{0}.txt"
    i = 0
    output_path = "/home/wsy/桌面/Bytecup2018/processed_train.{0}.txt"
    output_id2word_path = "./resource/id2word.txt"
    output_word2id_path = "./resource/word2id.txt"

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

    with corenlp.CoreNLPClient(annotators="tokenize ssplit".split()) as client:
        for index in range(9):
            with io.open(output_path.format(index), encoding="utf8", mode="w+") as file:
                for res_dict in read_file(path.format(index), extract_content):
                    content = res_dict["content"]
                    title = res_dict["title"]
                    ann = client.annotate(content)
                    content_words = content_to_sentences(client, content)
                    title_words = content_to_sentences(client,title)[0]
                    add_title_word(word2id,id2word,title_words)
                    res_dict["content"] = content_words
                    res_dict["title"] = title_words
                    file.write(json.dumps(res_dict) + "\n")
    title_vocab_size = len(word2id)

    for index in range(9):
        with io.open(output_path.format(index), encoding="utf8", mode="w+") as file:
            for res_dict in read_file(path.format(index), extract_content):
                content = res_dict["content"]
                add_content_word(word2id,id2word,content)

    with io.open(output_id2word_path,encoding="utf8", mode="a+") as file1:
        for id,word in id2word.items():
            file1.write(id+","+word+"\n")

    with io.open(output_word2id_path,encoding="utf8", mode="a+") as file2:
        for word,id in word2id.items():
            file2.write(word+","+id+"\n")
