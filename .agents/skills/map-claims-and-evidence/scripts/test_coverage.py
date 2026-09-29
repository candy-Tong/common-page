import copy
import unittest
from check_coverage import check

class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.html = '<div id="one">Case one</div><div id="two">Case two</div><div id="scope">未逐页核验</div>'
        self.data = {
            'user_url': 'https://example.org/post/A', 'primary_source_id': 'A',
            'claims_complete': False,
            'sources': [
                {'id':'A','url':'https://example.org/post/A','role':'primary','read_status':'full_text'},
                {'id':'B','url':'https://example.org/article/B','role':'quoted_article','parent':'A','read_status':'full_text'},
                {'id':'V','url':'https://example.org/video/V','role':'attachment','parent':'A','read_status':'unread','visible_gap_text':'未逐页核验'}],
            'expected_original_ids': ['A1','B1'],
            'coverage': [
                {'id':'A1','source':'A','locator':'step 1','kind':'primary_step','status':'covered','anchor':'one'},
                {'id':'B1','source':'B','locator':'build 1','kind':'original_case','status':'covered','anchor':'two'}]}
    def fails(self, change, html=None):
        data = copy.deepcopy(self.data)
        change(data)
        errors, _ = check(data, self.html if html is None else html)
        self.assertTrue(errors)
    def test_valid_structure_still_reports_unread_media(self):
        errors, gaps = check(self.data, self.html)
        self.assertFalse(errors)
        self.assertTrue(gaps)
    def test_quoted_article_cannot_be_primary(self):
        self.fails(lambda d:d.update(primary_source_id='B'))
    def test_missing_original(self):
        self.fails(lambda d:d['coverage'].pop())
    def test_unread_source_cannot_be_covered(self):
        self.fails(lambda d:d['coverage'][1].update(source='V'))
    def test_missing_anchor(self):
        self.fails(lambda d:d['coverage'][0].update(anchor='absent'))
    def test_false_complete_claim(self):
        self.fails(lambda d:d.update(claims_complete=True))
    def test_unread_notice_must_be_visible(self):
        self.fails(lambda d:None, self.html.replace('未逐页核验',''))
    def test_supplement_cannot_replace_original(self):
        self.fails(lambda d:d['coverage'][1].update(kind='supplementary'))
    def test_original_inventory_required(self):
        self.fails(lambda d:d.update(expected_original_ids=[]))

if __name__ == '__main__':
    unittest.main()
