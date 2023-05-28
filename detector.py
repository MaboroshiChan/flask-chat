# This file is used to detect if a given text contains certain words.
import logging as log
import jieba

class Detector:
    def __init__(self):
        self.keywords = []
        self.load_keywords()
    
    def load_keywords(self):
        with open("./source/敏感词.txt", "r") as f:
            self.keywords = f.readlines()
            self.keywords = [x.strip() for x in self.keywords]
        log.info("Loaded keywords")

    def detect(self, text: str)->bool:
        jieba.cut(text, cut_all=True)
        for word in self.keywords:
            if word in text:
                return True
        return False
    
    def detect_list(self, text: list[str])->bool:
        for t in text:
            if self.detect(t):
                return True
        return False
    