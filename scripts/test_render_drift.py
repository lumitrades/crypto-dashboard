"""Tests for scripts/render_drift.py (site_refresh's rendering-code drift marker), on throwaway git repos."""
import os, subprocess, sys, tempfile, unittest

sys.path.insert(0, os.path.dirname(__file__))
import render_drift  # noqa: E402


class RenderDriftTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = self.tmp.name
        self.git("init", "-q")
        self.git("config", "user.email", "t@example.invalid")
        self.git("config", "user.name", "t")
        self.commit({"index.html": "home", "privacy/index.html": "p1", "scripts/privacy_page.py": "v1",
                     "scripts/site_pages.py": "v1", "assets/site.css": "a"}, "initial full build")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *a):
        subprocess.run(["git", *a], cwd=self.d, check=True, capture_output=True)

    def commit(self, files, msg):
        for p, body in files.items():
            os.makedirs(os.path.join(self.d, os.path.dirname(p) or "."), exist_ok=True)
            with open(os.path.join(self.d, p), "w") as f:
                f.write(body)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", msg)

    def drift(self):
        return render_drift.drift(cwd=self.d)[0]

    def test_clean_after_full_build(self):
        self.assertEqual(self.drift(), [])

    def test_copy_publish_with_its_pages_is_not_drift(self):
        # the Nov 19 case: generator + its own pages in one commit, index.html untouched
        self.commit({"index.html": "home2"}, "daily refresh")
        self.commit({"scripts/privacy_page.py": "v2", "privacy/index.html": "p2"}, "privacy copy publish")
        self.assertEqual(self.drift(), [])

    def test_code_only_commit_is_drift(self):
        self.commit({"scripts/site_pages.py": "v2"}, "unpublished wording change")
        self.assertEqual(self.drift(), ["scripts/site_pages.py"])

    def test_code_then_separate_page_commit_is_still_drift(self):
        # the Nov 11 case: code in one commit, pages in another -> stay conservative
        self.commit({"scripts/site_pages.py": "v2"}, "draft")
        self.commit({"privacy/index.html": "p3"}, "publish some pages")
        self.assertEqual(self.drift(), ["scripts/site_pages.py"])

    def test_later_code_only_edit_after_published_one_is_drift(self):
        self.commit({"scripts/privacy_page.py": "v2", "privacy/index.html": "p2"}, "published")
        self.commit({"scripts/privacy_page.py": "v3"}, "unpublished follow-up")
        self.assertEqual(self.drift(), ["scripts/privacy_page.py"])

    def test_asset_change_without_pages_is_drift(self):
        self.commit({"assets/site.css": "b"}, "css only")
        self.assertEqual(self.drift(), ["assets/site.css"])

    def test_excluded_and_json_files_never_drift(self):
        self.commit({"scripts/publish.sh": "x", "scripts/test_x.py": "x", "scripts/top_sellers_snapshot.json": "{}",
                     "scripts/render_drift.py": "x", "assets/i18n/es.json": "{}"}, "non-rendering")
        self.assertEqual(self.drift(), [])

    def test_full_rebuild_clears_drift(self):
        self.commit({"scripts/site_pages.py": "v2"}, "code")
        self.commit({"index.html": "home3"}, "full rebuild")
        self.assertEqual(self.drift(), [])


if __name__ == "__main__":
    unittest.main()
