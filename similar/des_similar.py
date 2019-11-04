# -*- coding:utf-8 -*-
"""
   File Name:     tf_idf
   Description:   
   Author:        lsa
   date:          2019/10/11
"""
import jieba
import numpy as np
from config import *


class DesSimilar(object):
    def __init__(self):
        self.stopwords = set()

    # 加载停用词表
    def load_stopwords_list(self):
        with open(stopwords_filepath, 'r', encoding='utf-8') as f:
            for word_lst in f.readlines():
                word = word_lst[0]
                self.stopwords.update(word)

    # 加载自定义词库
    def load_jieba_userdict(self):
        # 加载自定义词库
        jieba.load_userdict(userdict_filepath)

    # 对句子进行分词
    def seg_sentence(self, description):
        seg = ' '.join([x for x in jieba.cut(description) if
                        x not in self.stopwords and x != ' ' and x != '\r\n' and x != '\r' and x != '\n' and x != '\t'])
        return seg

    # 获取总词集
    def general_word_set(self, sentence):
        wordset = set()
        for seg in sentence:
            wordset = wordset | set(seg)
        return list(wordset)

    # 将一个句子转换成向量
    def setOfWord(self, seg, wordset):
        num = len(wordset)
        vect = [0] * num
        for i in range(num):
            if wordset[i] in seg:
                vect[i] = 1
        return vect

    # 余弦求相似度
    def cosine_similar(self, vec1, vec2):
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        numerator = sum(vec1 * vec2)
        denominator = np.sqrt(sum(map(lambda x: x*x, vec1))) * np.sqrt(sum(map(lambda x: x*x, vec2)))
        cosin = numerator/denominator
        return cosin

    # 给user匹配相似度最大的百度百科结果
    def match_only_spider(self, des_seg, spider_sums):
        vocabList = self.general_word_set(spider_sums + [des_seg])
        des_vec = self.setOfWord(des_seg, vocabList)
        max_cosin, max_index = 0.0, -1
        for i in range(len(spider_sums)):
            spider_vec = self.setOfWord(spider_sums[i], vocabList)
            cosin = self.cosine_similar(des_vec, spider_vec)
            if cosin > max_cosin:
                max_cosin = cosin
                max_index = i
        return max_index

    # 同体名人百度百科描述匹配
    def match_user_spider(self, users, spiders):
        spider_sums = []
        print(f'spiders: {len(spiders)}')
        for i in range(len(spiders)):
            sums = spiders[i].get('summary', '')
            if len(sums) > 0:
                sums = self.seg_sentence(sums)
            spider_sums.append(sums)
        print(f'spider_sums: {len(spider_sums)}')
        for i in range(len(users)):
            des = users[i].get('description', '')
            if len(des) > 0:
                des_seg = self.seg_sentence(des)
                index = self.match_only_spider(des_seg, spider_sums)
                if index != -1:
                    users[i]['spider'] = spiders[index]
        return users


