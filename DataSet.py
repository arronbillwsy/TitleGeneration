import io
import logging
import sys

def doc2id(word2id,content):
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
    return doc_id,doc_oov_dict

def title2id(word2id,size,title):
    title_id = []
    title_vocab = {key:value for key,value in word2id.items() if value<size}
    for word in title:
        if word in title_vocab.keys():
            title_id.append(title_vocab[word])
        else:
            title_id.append(3)
    return title_id