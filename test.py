import unittest

import markdownify
from bs4 import BeautifulSoup

from main import get_chapter_paths, get_info_paths, get_material_paths, get_chapter_title, html_to_md


class OutputTest(unittest.TestCase):

    def setup(self):
        self.maxDiff = None

    def test_tc_jsh(self):
        expected = self.get_text("resources/expected/tc_jsh.md")
        soup = self.get_soup("resources/tc_jsh.html")
        actual = html_to_md(soup)
        self.assertEqual(expected, actual)

    def test_tc_foreword(self):
        expected = self.get_text("resources/expected/tc_foreword.md")
        soup = self.get_soup("resources/tc_foreword.html")
        actual = html_to_md(soup)
        self.assertEqual(expected, actual)

    def test_tc_section(self):
        expected = self.get_text("resources/expected/tc_section.md")
        soup = self.get_soup("resources/tc_section.html")
        actual = html_to_md(soup)
        self.assertEqual(expected, actual)

    def test_tc_section_endnotes(self):
        soup = self.get_soup("resources/tc_section_endnotes.html")
        actual = html_to_md(soup)
        # for some reason newlines are added after
        # <sup>
        # <i>blah</i>
        # Not sure why.
        pass

    def test_tc_correlation_tables(self):
        soup = self.get_soup("resources/tc_toc.html")
        actual = html_to_md(soup)
        # actual = markdownify.MarkdownConverter().convert_soup(soup)
        print(actual)

    def test_get_chapter_paths(self):
        soup = BeautifulSoup(self.get_text("resources/tc_toc.html"), 'html.parser')
        expected = ['/scriptures/tc/jshistory', '/scriptures/tc/section/2', '/scriptures/tc/section/3', '/scriptures/tc/section/4',
         '/scriptures/tc/section/5', '/scriptures/tc/section/6', '/scriptures/tc/section/7', '/scriptures/tc/section/8',
         '/scriptures/tc/section/9', '/scriptures/tc/section/10', '/scriptures/tc/section/11',
         '/scriptures/tc/section/12', '/scriptures/tc/section/13', '/scriptures/tc/section/14',
         '/scriptures/tc/section/15', '/scriptures/tc/section/16', '/scriptures/tc/section/17',
         '/scriptures/tc/section/18', '/scriptures/tc/section/19', '/scriptures/tc/section/20',
         '/scriptures/tc/section/21', '/scriptures/tc/section/22', '/scriptures/tc/section/23',
         '/scriptures/tc/section/24', '/scriptures/tc/section/25', '/scriptures/tc/section/26',
         '/scriptures/tc/section/27', '/scriptures/tc/section/28', '/scriptures/tc/section/29',
         '/scriptures/tc/section/30', '/scriptures/tc/section/31', '/scriptures/tc/section/32',
         '/scriptures/tc/section/33', '/scriptures/tc/section/34', '/scriptures/tc/section/35',
         '/scriptures/tc/section/36', '/scriptures/tc/section/37', '/scriptures/tc/section/38',
         '/scriptures/tc/section/39', '/scriptures/tc/section/40', '/scriptures/tc/section/41',
         '/scriptures/tc/section/42', '/scriptures/tc/section/43', '/scriptures/tc/section/44',
         '/scriptures/tc/section/45', '/scriptures/tc/section/46', '/scriptures/tc/section/47',
         '/scriptures/tc/section/48', '/scriptures/tc/section/49', '/scriptures/tc/section/50',
         '/scriptures/tc/section/51', '/scriptures/tc/section/52', '/scriptures/tc/section/53',
         '/scriptures/tc/section/54', '/scriptures/tc/section/55', '/scriptures/tc/section/56',
         '/scriptures/tc/section/57', '/scriptures/tc/section/58', '/scriptures/tc/section/59',
         '/scriptures/tc/section/60', '/scriptures/tc/section/61', '/scriptures/tc/section/62',
         '/scriptures/tc/section/63', '/scriptures/tc/section/64', '/scriptures/tc/section/65',
         '/scriptures/tc/section/66', '/scriptures/tc/section/67', '/scriptures/tc/section/68',
         '/scriptures/tc/section/69', '/scriptures/tc/section/70', '/scriptures/tc/section/71',
         '/scriptures/tc/section/72', '/scriptures/tc/section/73', '/scriptures/tc/section/74',
         '/scriptures/tc/section/75', '/scriptures/tc/section/76', '/scriptures/tc/section/77',
         '/scriptures/tc/section/78', '/scriptures/tc/section/79', '/scriptures/tc/section/80',
         '/scriptures/tc/section/81', '/scriptures/tc/section/82', '/scriptures/tc/section/83',
         '/scriptures/tc/section/84', '/scriptures/tc/section/85', '/scriptures/tc/section/86',
         '/scriptures/tc/section/87', '/scriptures/tc/section/88', '/scriptures/tc/section/89',
         '/scriptures/tc/section/90', '/scriptures/tc/section/91', '/scriptures/tc/section/92',
         '/scriptures/tc/section/93', '/scriptures/tc/section/94', '/scriptures/tc/section/95',
         '/scriptures/tc/section/96', '/scriptures/tc/section/97', '/scriptures/tc/section/98',
         '/scriptures/tc/section/99', '/scriptures/tc/section/100', '/scriptures/tc/section/101',
         '/scriptures/tc/section/102', '/scriptures/tc/section/103', '/scriptures/tc/section/104',
         '/scriptures/tc/section/105', '/scriptures/tc/section/106', '/scriptures/tc/section/107',
         '/scriptures/tc/section/108', '/scriptures/tc/section/109', '/scriptures/tc/lecture',
         '/scriptures/tc/section/111', '/scriptures/tc/section/112', '/scriptures/tc/section/113',
         '/scriptures/tc/section/114', '/scriptures/tc/section/115', '/scriptures/tc/section/116',
         '/scriptures/tc/section/117', '/scriptures/tc/section/118', '/scriptures/tc/section/119',
         '/scriptures/tc/section/120', '/scriptures/tc/section/121', '/scriptures/tc/section/122',
         '/scriptures/tc/section/123', '/scriptures/tc/section/124', '/scriptures/tc/section/125',
         '/scriptures/tc/section/126', '/scriptures/tc/section/127', '/scriptures/tc/section/128',
         '/scriptures/tc/section/129', '/scriptures/tc/section/130', '/scriptures/tc/section/131',
         '/scriptures/tc/section/132', '/scriptures/tc/section/133', '/scriptures/tc/section/134',
         '/scriptures/tc/section/135', '/scriptures/tc/section/136', '/scriptures/tc/section/137',
         '/scriptures/tc/section/138', '/scriptures/tc/section/139', '/scriptures/tc/section/140',
         '/scriptures/tc/section/141', '/scriptures/tc/section/142', '/scriptures/tc/section/143',
         '/scriptures/tc/section/144', '/scriptures/tc/abraham', '/scriptures/tc/section/146',
         '/scriptures/tc/section/147', '/scriptures/tc/section/148', '/scriptures/tc/section/149',
         '/scriptures/tc/section/150', '/scriptures/tc/section/151', '/scriptures/tc/section/152',
         '/scriptures/tc/section/153', '/scriptures/tc/section/154', '/scriptures/tc/section/155',
         '/scriptures/tc/section/156', '/scriptures/tc/section/157', '/scriptures/tc/section/158',
         '/scriptures/tc/section/159', '/scriptures/tc/section/160', '/scriptures/tc/section/161',
         '/scriptures/tc/section/162', '/scriptures/tc/section/163', '/scriptures/tc/section/164',
         '/scriptures/tc/section/165', '/scriptures/tc/section/166', '/scriptures/tc/section/167',
         '/scriptures/tc/section/168', '/scriptures/tc/section/169', '/scriptures/tc/section/170', '/scriptures/tc/toj',
         '/scriptures/tc/section/172', '/scriptures/tc/section/173', '/scriptures/tc/section/174',
         '/scriptures/tc/section/175', '/scriptures/tc/section/176', '/scriptures/tc/section/177']
        self.assertEqual(expected, get_chapter_paths(soup))

    def test_get_info_paths(self):
        soup = BeautifulSoup(self.get_text("resources/tc_toc.html"), 'html.parser')
        expected = ['/scriptures/tc/tcforeword', '/scriptures/tc/tccanonization', '/scriptures/tc/tcpreface', '/scriptures/tc/tcintro', '/scriptures/tc/epigraph']
        actual = get_info_paths(soup)
        self.assertEqual(expected, actual)

    def test_get_material_paths_tc_toc(self):
        soup = BeautifulSoup(self.get_text("resources/tc_toc.html"), 'html.parser')
        expected = ['/scriptures/tc/tcforeword', '/scriptures/tc/tccanonization', '/scriptures/tc/tcpreface',
         '/scriptures/tc/tcintro', '/scriptures/tc/epigraph', '/scriptures/tc/jshistory', '/scriptures/tc/section/2',
         '/scriptures/tc/section/3', '/scriptures/tc/section/4', '/scriptures/tc/section/5', '/scriptures/tc/section/6',
         '/scriptures/tc/section/7', '/scriptures/tc/section/8', '/scriptures/tc/section/9',
         '/scriptures/tc/section/10', '/scriptures/tc/section/11', '/scriptures/tc/section/12',
         '/scriptures/tc/section/13', '/scriptures/tc/section/14', '/scriptures/tc/section/15',
         '/scriptures/tc/section/16', '/scriptures/tc/section/17', '/scriptures/tc/section/18',
         '/scriptures/tc/section/19', '/scriptures/tc/section/20', '/scriptures/tc/section/21',
         '/scriptures/tc/section/22', '/scriptures/tc/section/23', '/scriptures/tc/section/24',
         '/scriptures/tc/section/25', '/scriptures/tc/section/26', '/scriptures/tc/section/27',
         '/scriptures/tc/section/28', '/scriptures/tc/section/29', '/scriptures/tc/section/30',
         '/scriptures/tc/section/31', '/scriptures/tc/section/32', '/scriptures/tc/section/33',
         '/scriptures/tc/section/34', '/scriptures/tc/section/35', '/scriptures/tc/section/36',
         '/scriptures/tc/section/37', '/scriptures/tc/section/38', '/scriptures/tc/section/39',
         '/scriptures/tc/section/40', '/scriptures/tc/section/41', '/scriptures/tc/section/42',
         '/scriptures/tc/section/43', '/scriptures/tc/section/44', '/scriptures/tc/section/45',
         '/scriptures/tc/section/46', '/scriptures/tc/section/47', '/scriptures/tc/section/48',
         '/scriptures/tc/section/49', '/scriptures/tc/section/50', '/scriptures/tc/section/51',
         '/scriptures/tc/section/52', '/scriptures/tc/section/53', '/scriptures/tc/section/54',
         '/scriptures/tc/section/55', '/scriptures/tc/section/56', '/scriptures/tc/section/57',
         '/scriptures/tc/section/58', '/scriptures/tc/section/59', '/scriptures/tc/section/60',
         '/scriptures/tc/section/61', '/scriptures/tc/section/62', '/scriptures/tc/section/63',
         '/scriptures/tc/section/64', '/scriptures/tc/section/65', '/scriptures/tc/section/66',
         '/scriptures/tc/section/67', '/scriptures/tc/section/68', '/scriptures/tc/section/69',
         '/scriptures/tc/section/70', '/scriptures/tc/section/71', '/scriptures/tc/section/72',
         '/scriptures/tc/section/73', '/scriptures/tc/section/74', '/scriptures/tc/section/75',
         '/scriptures/tc/section/76', '/scriptures/tc/section/77', '/scriptures/tc/section/78',
         '/scriptures/tc/section/79', '/scriptures/tc/section/80', '/scriptures/tc/section/81',
         '/scriptures/tc/section/82', '/scriptures/tc/section/83', '/scriptures/tc/section/84',
         '/scriptures/tc/section/85', '/scriptures/tc/section/86', '/scriptures/tc/section/87',
         '/scriptures/tc/section/88', '/scriptures/tc/section/89', '/scriptures/tc/section/90',
         '/scriptures/tc/section/91', '/scriptures/tc/section/92', '/scriptures/tc/section/93',
         '/scriptures/tc/section/94', '/scriptures/tc/section/95', '/scriptures/tc/section/96',
         '/scriptures/tc/section/97', '/scriptures/tc/section/98', '/scriptures/tc/section/99',
         '/scriptures/tc/section/100', '/scriptures/tc/section/101', '/scriptures/tc/section/102',
         '/scriptures/tc/section/103', '/scriptures/tc/section/104', '/scriptures/tc/section/105',
         '/scriptures/tc/section/106', '/scriptures/tc/section/107', '/scriptures/tc/section/108',
         '/scriptures/tc/section/109', '/scriptures/tc/lecture', '/scriptures/tc/section/111',
         '/scriptures/tc/section/112', '/scriptures/tc/section/113', '/scriptures/tc/section/114',
         '/scriptures/tc/section/115', '/scriptures/tc/section/116', '/scriptures/tc/section/117',
         '/scriptures/tc/section/118', '/scriptures/tc/section/119', '/scriptures/tc/section/120',
         '/scriptures/tc/section/121', '/scriptures/tc/section/122', '/scriptures/tc/section/123',
         '/scriptures/tc/section/124', '/scriptures/tc/section/125', '/scriptures/tc/section/126',
         '/scriptures/tc/section/127', '/scriptures/tc/section/128', '/scriptures/tc/section/129',
         '/scriptures/tc/section/130', '/scriptures/tc/section/131', '/scriptures/tc/section/132',
         '/scriptures/tc/section/133', '/scriptures/tc/section/134', '/scriptures/tc/section/135',
         '/scriptures/tc/section/136', '/scriptures/tc/section/137', '/scriptures/tc/section/138',
         '/scriptures/tc/section/139', '/scriptures/tc/section/140', '/scriptures/tc/section/141',
         '/scriptures/tc/section/142', '/scriptures/tc/section/143', '/scriptures/tc/section/144',
         '/scriptures/tc/abraham', '/scriptures/tc/section/146', '/scriptures/tc/section/147',
         '/scriptures/tc/section/148', '/scriptures/tc/section/149', '/scriptures/tc/section/150',
         '/scriptures/tc/section/151', '/scriptures/tc/section/152', '/scriptures/tc/section/153',
         '/scriptures/tc/section/154', '/scriptures/tc/section/155', '/scriptures/tc/section/156',
         '/scriptures/tc/section/157', '/scriptures/tc/section/158', '/scriptures/tc/section/159',
         '/scriptures/tc/section/160', '/scriptures/tc/section/161', '/scriptures/tc/section/162',
         '/scriptures/tc/section/163', '/scriptures/tc/section/164', '/scriptures/tc/section/165',
         '/scriptures/tc/section/166', '/scriptures/tc/section/167', '/scriptures/tc/section/168',
         '/scriptures/tc/section/169', '/scriptures/tc/section/170', '/scriptures/tc/toj', '/scriptures/tc/section/172',
         '/scriptures/tc/section/173', '/scriptures/tc/section/174', '/scriptures/tc/section/175',
         '/scriptures/tc/section/176', '/scriptures/tc/section/177', '/scriptures/tc/appendix/sectionendnotes',
         '/scriptures/tc/appendix/excludedrevelations', '/scriptures/tc/appendix/prerogative',
         '/scriptures/tc/glossary', '/scriptures/tc/appendix/correlationtable', '/scriptures/tc/appendix/timeline',
         '/scriptures/tc/appendix/maps']
        actual = get_material_paths(soup)
        self.assertEqual(expected, actual)

    def test_get_material_paths_oc_toc(self):
        soup = BeautifulSoup(self.get_text("resources/oc_toc.html"), 'html.parser')
        expected = ['/scriptures/oc/ocforeword', '/scriptures/oc/occanonization', '/scriptures/oc/ocpreface', '/scriptures/oc/genesis', '/scriptures/oc/exodus', '/scriptures/oc/leviticus', '/scriptures/oc/numbers', '/scriptures/oc/deuteronomy', '/scriptures/oc/joshua', '/scriptures/oc/judges', '/scriptures/oc/ruth', '/scriptures/oc/1samuel', '/scriptures/oc/2samuel', '/scriptures/oc/1kings', '/scriptures/oc/2kings', '/scriptures/oc/1chronicles', '/scriptures/oc/2chronicles', '/scriptures/oc/ezra', '/scriptures/oc/nehemiah', '/scriptures/oc/esther', '/scriptures/oc/job', '/scriptures/oc/psalm', '/scriptures/oc/proverbs', '/scriptures/oc/ecclesiastes', '/scriptures/oc/isaiah', '/scriptures/oc/jeremiah', '/scriptures/oc/lamentations', '/scriptures/oc/ezekiel', '/scriptures/oc/daniel', '/scriptures/oc/hosea', '/scriptures/oc/joel', '/scriptures/oc/amos', '/scriptures/oc/obadiah', '/scriptures/oc/jonah', '/scriptures/oc/micah', '/scriptures/oc/nahum', '/scriptures/oc/habakkuk', '/scriptures/oc/zephaniah', '/scriptures/oc/haggai', '/scriptures/oc/zechariah', '/scriptures/oc/malachi', '/scriptures/oc/ocappendix']
        actual = get_material_paths(soup)
        self.assertEqual(expected, actual)

    def test_get_material_paths_nc_toc(self):
        soup = BeautifulSoup(self.get_text("resources/nc_toc.html"), 'html.parser')
        actual = get_material_paths(soup)
        expected = ['/scriptures/nc/ncforeword', '/scriptures/nc/nccanonization', '/scriptures/nt/ntpreface', '/scriptures/nt/matthew', '/scriptures/nt/mark', '/scriptures/nt/luke', '/scriptures/nt/john', '/scriptures/nt/acts', '/scriptures/nt/romans', '/scriptures/nt/1corinthians', '/scriptures/nt/2corinthians', '/scriptures/nt/galatians', '/scriptures/nt/ephesians', '/scriptures/nt/philippians', '/scriptures/nt/colossians', '/scriptures/nt/1thessalonians', '/scriptures/nt/2thessalonians', '/scriptures/nt/1timothy', '/scriptures/nt/2timothy', '/scriptures/nt/titus', '/scriptures/nt/philemon', '/scriptures/nt/hebrews', '/scriptures/nt/ejacob', '/scriptures/nt/1peter', '/scriptures/nt/2peter', '/scriptures/nt/1john', '/scriptures/nt/2john', '/scriptures/nt/3john', '/scriptures/nt/judas', '/scriptures/nt/revelation', '/scriptures/nt/ntappendix', '/scriptures/bofm/bompreface', '/scriptures/bofm/bomintro', '/scriptures/bofm/title', '/scriptures/bofm/tow', '/scriptures/bofm/1nephi', '/scriptures/bofm/2nephi', '/scriptures/bofm/jacob', '/scriptures/bofm/enos', '/scriptures/bofm/jarom', '/scriptures/bofm/omni', '/scriptures/bofm/words', '/scriptures/bofm/mosiah', '/scriptures/bofm/alma', '/scriptures/bofm/helaman', '/scriptures/bofm/3nephi', '/scriptures/bofm/4nephi', '/scriptures/bofm/mormon', '/scriptures/bofm/ether', '/scriptures/bofm/moroni', '/scriptures/bofm/bomappendix']
        self.assertEqual(expected, actual)

    def test_get_chapter_title_tc(self):
        soup = BeautifulSoup(self.get_text("resources/tc_section.html"), 'html.parser')
        expected = get_chapter_title(soup)
        actual = "Section 2"
        self.assertEqual(expected, actual)

        soup = BeautifulSoup(self.get_text("resources/tc_jsh.html"), 'html.parser')
        expected = get_chapter_title(soup)
        print(expected)
        actual = 'Part 1 (1805–1820)'
        self.assertEqual(expected, actual)

    def test_table_links(self):
        soup = self.get_soup("resources/tc_correlation_tables.html")
        md = html_to_md(soup, {'/scriptures/tc/jshistory/3': "Joseph Smith History 3"})
        text_position = md.find("[[Joseph Smith History 3\|JSH 3:4]]")
        self.assertTrue(text_position > -1)


    @staticmethod
    def get_text(filepath):
        with open(filepath, 'r') as f:
            return "".join(f.readlines())

    @staticmethod
    def get_soup(filepath):
        return BeautifulSoup(OutputTest.get_text(filepath), 'html.parser')


if __name__ == '__main__':
    unittest.main()