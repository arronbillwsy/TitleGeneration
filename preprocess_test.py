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







if __name__ == '__main__':
    path = "C:/Users/31476/Desktop/543/bytecup2018/bytecup.corpus.train.{0}.txt"
    i = 0
    output_path = "C:/Users/31476/Desktop/543/bytecup2018/processed_train.{0}.txt"
    with corenlp.CoreNLPClient(annotators="tokenize ssplit".split()) as client:
        for index in range(9):
            with io.open(output_path.format(index), encoding="utf8", mode="w+") as file:
                for res_dict in read_file(path.format(index), extract_content):
                    content = res_dict["content"]
                    title = res_dict["title"]
                    ann = client.annotate(content)
                    words = content_to_sentences(client, content)
                    title_words = content_to_sentences(client,title)
                    res_dict["content"] = words
                    res_dict["title"] = title_words
                    file.write(json.dumps(res_dict) + "\n")
