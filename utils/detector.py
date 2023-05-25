# This file is used to detect if a given text contains certain words.

import re
import os
import logging as log
import jieba

class Detector:
    def __init__(self):
        self.keywords = []
        self.load_keywords()
    
    def load_keywords(self):
        with open("keywords.txt", "r") as f:
            self.keywords = f.readlines()
            self.keywords = [x.strip() for x in self.keywords]
        log.info("Loaded keywords")

    def detect(self, text: str)->bool:
        pass