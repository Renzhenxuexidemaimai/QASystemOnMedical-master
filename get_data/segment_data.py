# !/usr/bin/env python3
# coding: utf-8
# File: segment_data.py
# Author: houbowen
# Date: 2018-03-28

class Segment:

    def __init__(self):
        dict_path = '../dict/disease.txt'
        self.disease_dict, self.max_len = self.load_diseases(dict_path)

    def load_diseases(self, dict_path):
        diseases = []
        max_len = 0
        for line in open(dict_path, encoding='utf-8'):
            disease = line.strip()
            if not disease:
                continue
            if (len(disease) > max_len):
                max_len = len(disease)
            diseases.append(disease)
        return diseases, max_len

    def maximum_forward_match(self, string):
        segment_list = []
        index = 0
        i = 0
        while index < len(string):
            matched = False
            for i in range(self.max_len, 0, -1):
                temp = string[index:index + i]
                if temp in self.disease_dict:
                    segment_list.append(temp)
                    matched = True
                    break
            if not matched:
                i = 1
                segment_list.append(string[index])
            index += i
        return segment_list

    def maximum_backward_match(self, string):
        segment_list = []
        tmp = 0
        index = len(string)
        while index > 0:
            matched = False
            for i in range(self.max_len, 0, -1):
                tmp = i + 1
                temp = string[index - tmp: index]
                if temp in self.disease_dict:
                    segment_list.append(temp)
                    matched = True
                    break

            if not matched:
                segment_list.append(index - 1)
                tmp = 1

            index -= tmp

        return segment_list[::-1]

    def maximum_biward_match(self, string):
        forward_list = self.maximum_forward_match(string)
        backward_list = self.maximum_backward_match(string)

        count_forward = len(forward_list)
        count_backward = len(backward_list)

        if count_forward == count_backward:
            if (self.count_single_word(forward_list) < self.count_single_word(backward_list)):
                return forward_list
            else:
                return backward_list
        elif count_forward < count_backward:
            return forward_list
        else:
            return backward_list

    def count_single_word(self, word_list):
        count = 0
        for word in word_list:
            if (len(word) == 1):
                count += 1
        return count
