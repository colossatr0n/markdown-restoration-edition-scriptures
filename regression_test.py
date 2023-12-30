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
    output_args = ['-o', REGRESSION_DIR]
    args_lists = [
        ['--rel-links', '--link-type', 'wikilinks', output_args[0], output_args[1] + "/wikilinks-relative"],
        ['--link-type', 'wikilinks', output_args[0], output_args[1] + "/wikilinks-short"],
        ['--rel-links', '--link-type', 'markdown', output_args[0], output_args[1] + "/markdown-links-relative"],
        ['--link-type', 'markdown', output_args[0], output_args[1] + "/markdown-links-short"],
    ]

    @classmethod
    def setUpClass(cls):
        shutil.rmtree(RegressionTest.REGRESSION_DIR)
        os.mkdir(RegressionTest.REGRESSION_DIR)

        for args in RegressionTest.args_lists:
            main(parse_args(args))

        cls.original_wiki_links_short = sorted(glob.glob(RegressionTest.OUTPUT_DIR + "/wikilinks-short/Scriptures/**", recursive=True))
        cls.original_wiki_links_relative = sorted(glob.glob(RegressionTest.OUTPUT_DIR + "/wikilinks-relative/Scriptures/**", recursive=True))
        cls.original_md_links_short = sorted(glob.glob(RegressionTest.OUTPUT_DIR + "/markdown-links-short/Scriptures/**", recursive=True))
        cls.original_md_links_relative = sorted(glob.glob(RegressionTest.OUTPUT_DIR + "/markdown-links-relative/Scriptures/**", recursive=True))

        cls.new_wiki_links_short = sorted(glob.glob(RegressionTest.REGRESSION_DIR + "/wikilinks-short/Scriptures/**", recursive=True))
        cls.new_wiki_links_relative = sorted(glob.glob(RegressionTest.REGRESSION_DIR + "/wikilinks-relative/Scriptures/**", recursive=True))
        cls.new_md_links_short = sorted(glob.glob(RegressionTest.REGRESSION_DIR + "/markdown-links-short/Scriptures/**", recursive=True))
        cls.new_md_links_relative = sorted(glob.glob(RegressionTest.REGRESSION_DIR + "/markdown-links-relative/Scriptures/**", recursive=True))
        cls.maxDiff = None


    def test_file_tree(self):
        pairs = [
            (self.original_wiki_links_short, self.new_wiki_links_short),
            (self.original_wiki_links_relative, self.new_wiki_links_relative),
            (self.original_md_links_short, self.new_md_links_short),
            (self.original_md_links_relative, self.new_md_links_relative),
        ]
        for pair in pairs:
            with self.subTest():
                original_paths = [re.sub('.*?Scriptures/', '', file) for file in pair[0]]
                new_paths = [re.sub('.*?Scriptures/', '', file) for file in pair[1]]
                self.assertEqual(set(original_paths), set(new_paths))

    def test_file_contents(self):
        pairs = [
            (self.original_wiki_links_short, self.new_wiki_links_short),
            (self.original_wiki_links_relative, self.new_wiki_links_relative),
            (self.original_md_links_short, self.new_md_links_short),
            (self.original_md_links_relative, self.new_md_links_relative),
        ]
        for pair in pairs:
            md_original = [md for md in pair[0] if md.endswith('.md')]
            md_new = [md for md in pair[1] if md.endswith('.md')]
            for i, file in enumerate(md_original):
                orig_text = get_text(file)
                new_text = get_text(md_new[i])
                with self.subTest(f"\n----------------\n{file}\n{md_new[i]}"):
                    self.assertMultiLineEqual(orig_text, new_text, f"\nDIFFERENT:\n{file}\n{md_new[i]}")

    def test_wiki_links_runs_have_same_text(self):
        wiki_short_links_md = [md for md in self.new_wiki_links_short if md.endswith('.md')]
        wiki_relative_links_md = [md for md in self.new_wiki_links_relative if md.endswith('.md')]
        for i, wsl_file in enumerate(wiki_short_links_md):
            wrl_file = wiki_relative_links_md[i]
            wsl_text = re.sub("(\[\[).*[^\]]\|", r"\1", get_text(wsl_file))
            wsl_text = re.sub("\[\[(.*[^\]])\]\]", r"\1", wsl_text)
            wrl_text = re.sub("(\[\[).*[^\]]\|", r"\1", get_text(wrl_file))
            wrl_text = re.sub("\[\[(.*[^\]])\]\]", r"\1", wrl_text)
            with self.subTest(f"\n----------------\n{wsl_file}\n{wiki_relative_links_md[i]}"):
                self.assertMultiLineEqual(wsl_text, wrl_text, f"\nDIFFERENT:\n{wsl_file}\n{wrl_file}\nvimdiff '{wsl_file}' '{wrl_file}'")

    def test_markdown_and_wiki_links_runs_have_same_text(self):
        md_relative_links_md = [md for md in self.new_md_links_relative if md.endswith('.md')]
        wiki_relative_links_md = [md for md in self.new_wiki_links_relative if md.endswith('.md')]
        for i, mrl_file in enumerate(md_relative_links_md):
            mrl_text = re.sub("\[([^\]\[]*?)\]\(.*?\.md\)", r"\1", get_text(mrl_file))
            mrl_text = re.sub("\[([^\]]*?)\]\(.*?\)", r"\1", mrl_text)

            wrl_file = wiki_relative_links_md[i]
            wrl_text = re.sub("(\[\[)[^\]]*?\|", r"\1", get_text(wrl_file))
            wrl_text = re.sub("\[\[([^\]]*?)\]\]", r"\1", wrl_text)
            wrl_text = re.sub("\[([^\]]*?)\]\(.*?\)", r"\1", wrl_text)
            with self.subTest(f"\n----------------\n{mrl_file}\n{wiki_relative_links_md[i]}"):
                self.assertMultiLineEqual(mrl_text, wrl_text, f"\nDIFFERENT:\n{mrl_file}\n{wrl_file}\nvimdiff '{mrl_file}' '{wrl_file}'")


def get_text(file):
    if os.path.isdir(file):
        return ""
    with open(file, 'r') as f:
        return "".join(f.readlines())



if __name__ == '__main__':
    unittest.main()
