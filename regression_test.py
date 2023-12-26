"""
Run in project root directory with:
python -m unittest regression_test.RegressionTest
"""
import re
import glob
import os
import shutil
import unittest

from obsidian_re_scriptures import main, parse_args


class RegressionTest(unittest.TestCase):
    REGRESSION_DIR = 'resources/test/regression'
    OUTPUT_DIR = 'output'
    args = ['-o', REGRESSION_DIR]

    @classmethod
    def setUpClass(cls):
        # shutil.rmtree(RegressionTest.REGRESSION_DIR)
        # os.mkdir(RegressionTest.REGRESSION_DIR)
        # main(parse_args(RegressionTest.args))

        cls.original_wiki_links_short = sorted(glob.glob(RegressionTest.OUTPUT_DIR + "/wiki-links-short/Scriptures/**", recursive=True))
        cls.original_wiki_links_relative = sorted(glob.glob(RegressionTest.OUTPUT_DIR + "/wiki-links-relative/Scriptures/**", recursive=True))
        cls.original = sorted(glob.glob(RegressionTest.OUTPUT_DIR + "wiki-links-short/Scriptures/**", recursive=True))
        cls.new = sorted(glob.glob(RegressionTest.REGRESSION_DIR + "/Scriptures/**", recursive=True))

    def test_file_tree(self):
        original_paths = [re.sub('.*?Scriptures/', '', file) for file in self.original_wiki_links_short]
        new_paths = [re.sub('.*?Scriptures/', '', file) for file in self.new]
        self.assertEqual(set(original_paths), set(new_paths))

    def test_file_contents(self):
        md_original = [md for md in self.original_wiki_links_short if md.endswith('.md')]
        md_new = [md for md in self.new if md.endswith('.md')]
        for i, file in enumerate(md_original):
            orig_text = get_text(file)
            new_text = get_text(md_new[i])
            with self.subTest(f"\n----------------\n{file}\n{md_new[i]}"):
                self.assertMultiLineEqual(orig_text, new_text, f"\nDIFFERENT:\n{file}\n{md_new[i]}")

    def test_wiki_links_runs_have_same_body(self):
        wiki_short_links_md = [md for md in self.original_wiki_links_short if md.endswith('.md')]
        wiki_relative_links_md = [md for md in self.original_wiki_links_relative if md.endswith('.md')]
        for i, file in enumerate(wiki_short_links_md):
            orig_text = re.sub("(\[\[).*[^\]]\|", r"\1", get_text(file))
            new_text = re.sub("(\[\[).*[^\]]\|", r"\1", get_text(wiki_relative_links_md[i]))
            with self.subTest(f"\n----------------\n{file}\n{wiki_relative_links_md[i]}"):
                self.assertMultiLineEqual(orig_text, new_text, f"\nDIFFERENT:\n{file}\n{wiki_relative_links_md[i]}")


def get_text(file):
    if os.path.isdir(file):
        return ""
    with open(file, 'r') as f:
        return "".join(f.readlines())



if __name__ == '__main__':
    unittest.main()
