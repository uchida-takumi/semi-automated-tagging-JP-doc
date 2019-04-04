# -*- coding: utf-8 -*-
"""
MeCabを使った形態素解析でテキストをベクトル化するやつです。
"""
import MeCab
import pandas as pd, numpy as np

class keitaiso:
    def __init__(self, use_PoW=['名詞','動詞','形容詞','副詞',], stop_words=[], use_words=[], user_dic_files=[]):
        self.use_PoW = use_PoW
        self.stop_words = stop_words
        self.use_words = use_words
        if len(user_dic_files)>0:
            arg_user_dic_files = '-u '+','.join(user_dic_files)
        else:
            arg_user_dic_files = ''
        self.tagger = MeCab.Tagger(arg_user_dic_files)

    def tokenize(self, text):
        processing = self.basic_tokenize(text)
        processing = self.filter_PoW(processing)
        processing = self.filter_stop_words(processing)
        processing = self.filter_use_words(processing)
        return processing

    def basic_tokenize(self, text):
        if text is (np.nan or None):
            parsed = [[1,'*','*'],]
        else:
            parsed = self.tagger.parse(text).split('\n')[:-2]
            parsed = [p.split('\t')[1] for p in parsed]
            parsed = [[idx, p.split(',')[0], p.split(',')[6]] for idx, p in enumerate(parsed)]
        return parsed

    def filter_PoW(self, basic_tokenized,):
        return [token for token in basic_tokenized if token[1] in self.use_PoW]

    def filter_stop_words(self, basic_tokenized,):
        return [token for token in basic_tokenized if token[2] not in self.stop_words]

    def filter_use_words(self, basic_tokenized,):
        if self.use_words == []:
            return basic_tokenized
        else:
            return [token for token in basic_tokenized if token[2] in self.use_words]

    def get_X(self, text_array):
        tokenized_array = [self.tokenize(text) for text in text_array]
        dict_array = [self.change_dict(tokenized) for tokenized in tokenized_array]
        return pd.DataFrame(dict_array).fillna(0)

    def change_dict(self, tokenized,):
        words_list = [token[2] for token in tokenized]
        words_set = set(words_list)
        result_dict = dict()
        for word in words_set:
            result_dict[word] = words_list.count(word)
        return result_dict


if __name__ == "__main__":
    text = "今日は何時に帰ってきますか？　と彼女は尋ねてくる"
    use_PoW = ['名詞','動詞','形容詞','副詞','記号',]
    stop_words = ['*','よう','上','の','様','こちら','際','ところ','はず','\u3000',]

    k = keitaiso(use_PoW=use_PoW,stop_words=stop_words)
    print(k.basic_tokenize(text))
    print(k.tokenize(text))
