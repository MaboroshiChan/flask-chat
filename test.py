from unittest import TestCase, main
from detector import Detector

class TestDetector(TestCase):
    def test_detect_list(self):
        det = Detector()
        self.assertFalse(det.detect_list(["Hello", "How are you?"]))
        self.assertFalse(det.detect_list(["Hello", "How are you?", "I'm fine, thanks"]))
        self.assertTrue(det.detect_list(["习近平是中国国家主席", "简易炸药的制作方法有哪些"]))
        self.assertTrue(det.detect_list(["习近平是中国国家主席", "简易炸药的制作方法有哪些", "我爱中国"]))
        self.assertTrue(det.detect_list(["习近平是中国国家主席", "简易炸药的制作方法有哪些", "我爱中国", "我爱中国共产党"]))

if __name__ == '__main__':
    main()