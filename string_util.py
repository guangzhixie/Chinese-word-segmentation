# -*- coding: utf-8 -*-

import string
import json
from zhon.hanzi import punctuation

class StringUtil(object):
    def __init__(self):
        self.EMPTY = ""
        self.SPACE = " "
        self.EQUAL = "="
        self.NEWLINE = "\n"
        self.SENTENCE_START = "<s>"
        self.SENTENCE_END = "</s>"
        self.DATE_CHARS = ["日","月","年"]
        self.NUMBER_CHARS = ["零", "一", "二", "三", "五", "六", "七", "八", "九", "十", "百", "千", "万", "亿", "兆"]
        self.TAG_SET = ['s', 'b', 'm', 'e']
        self.INVALID_TAG_SEQ = ['ms', 'mb', 'sm', 'se', 'bs', 'em', 'bb', 'mm', 'ee']
    
    def is_space(self, c):
        return c == self.SPACE
    
    def is_punctuation(self, c):
        return c in punctuation or c in string.punctuation
    
    def is_separator(self, c):
        return self.is_space(c) or self.is_punctuation(c)
    
    def remove_whitespace(self, s):
        return self.EMPTY.join(s.split())
    
    def get_character_type(self, c):
        c = c.encode('utf-8')
        
        # SENTENCE BOUNDARIES
        if c == self.SENTENCE_START or c == self.SENTENCE_END:
            return "0"
        
        # NUMBER
        elif c in self.NUMBER_CHARS or str.isdigit(c):
            return "1"
        
        # DATES
        elif c in self.DATE_CHARS:
            return "2"
        
        # ENGLISH LETTER
        elif c.isalpha():
            return "3"
        
        # OTHERS
        else:
            return "4"
    
    def is_digit_or_letter(self, s):
        last_char = s[-1].encode('utf-8')
        leading_chars = s[:-1].encode('utf-8')
        
        s = s.encode('utf-8')
        
        if s.isalnum():
            return True
        elif last_char in self.NUMBER_CHARS and leading_chars.isalnum():
            return True
        else:
            return False
    
    
    def to_json(self, d):
        """Save dict to a JSON string.

        Returns:
            (string) serialized dict as JSON string.
        """
        return json.dumps(d)
    
    def from_json(self, s):
        """Read dict from a JSON string.

        Returns:
            Dict read from a JSON string.
        """
        return json.loads(s)