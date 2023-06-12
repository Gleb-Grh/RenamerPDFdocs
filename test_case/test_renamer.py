import unittest
from oop_renamer_v2 import PDFSearcher


class TestListPathes(unittest.TestCase):
    pathes = PDFSearcher(r'C:\Users\glebg\Documents\tests').path_pdf_collect()
    
    def test_list(self):
        self.assertEqual(list, type(self.pathes))
    
    def test_endswith(self):
        for path in self.pathes:
            self.assertTrue(path.lower().endswith('.pdf'))

    def test_not_null(self):
        self.assertTrue(self.pathes)




if __name__ == '__main__':
    unittest.main()
    