"""IndexNow helper checks. Run: python3 scripts/test_indexnow.py"""
import os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indexnow_ping as ip


class IndexNow(unittest.TestCase):
    def test_key_file_at_root(self):
        key = ip.find_key()
        self.assertRegex(key or "", r"^[0-9a-f]{32}$")
        with open(os.path.join(ip.ROOT, key + ".txt"), encoding="utf-8") as f:
            self.assertEqual(f.read().strip(), key)

    def test_pages_served_without_jekyll(self):
        self.assertTrue(os.path.exists(os.path.join(ip.ROOT, ".nojekyll")))

    def test_bing_site_auth(self):
        with open(os.path.join(ip.ROOT, "BingSiteAuth.xml"), encoding="utf-8") as f:
            self.assertIn("<user>", f.read())

    def test_path_to_url(self):
        self.assertEqual(ip.path_to_url("index.html"), "https://lumitrades.io/")
        self.assertEqual(ip.path_to_url("es/agents/index.html"), "https://lumitrades.io/es/agents/")
        self.assertEqual(ip.path_to_url("feed.xml"), "https://lumitrades.io/feed.xml")

    def test_sitemap_urls(self):
        urls = ip.sitemap_urls(os.path.join(ip.ROOT, "sitemap.xml"))
        self.assertIn("https://lumitrades.io/", urls)
        self.assertEqual(len(urls), len(set(urls)))
        self.assertTrue(all(u.startswith("https://lumitrades.io/") for u in urls))

    def test_unstamped_matches_build_pages(self):
        import build_pages
        self.assertEqual(ip._STAMP.pattern, build_pages._STAMP.pattern)
        a = '<p>Page generated 2026-11-01 · x</p>"dateModified": "2026-11-01"'
        b = '<p>Page generated 2026-11-02 · x</p>"dateModified": "2026-11-02"'
        self.assertEqual(ip.unstamped(a), ip.unstamped(b))
        # timestamps, US-style dates and data changes still count as changes
        self.assertNotEqual(ip.unstamped('"observed_at":"2026-11-01T10:00:11Z"'), ip.unstamped('"observed_at":"2026-11-02T10:00:11Z"'))
        self.assertNotEqual(ip.unstamped("11-01-2026"), ip.unstamped("11-02-2026"))
        self.assertNotEqual(ip.unstamped("12 paid test-buys 2026-11-01"), ip.unstamped("13 paid test-buys 2026-11-02"))

    def test_changed_urls_skips_stamp_only_pages(self):
        """The Nov 1, 2026 daily refresh (ef396c20) changed 84 files, but /terms/ only moved its footer date."""
        import subprocess
        if subprocess.run(["git", "-C", ip.ROOT, "cat-file", "-e", "ef396c20^{commit}"], capture_output=True).returncode:
            self.skipTest("commit ef396c20 not in this clone")
        allowed = ip.sitemap_urls(os.path.join(ip.ROOT, "sitemap.xml"))
        urls = ip.changed_urls("ef396c20", allowed)
        self.assertNotIn("https://lumitrades.io/terms/", urls)
        self.assertNotIn("https://lumitrades.io/how-it-works/", urls)
        self.assertIn("https://lumitrades.io/trust/", urls)


class SitemapLastmod(unittest.TestCase):
    """build_pages: <lastmod> only moves when a page changed beyond its build-date stamps."""
    def test_old_lastmods_reads_sitemap(self):
        import build_pages
        lm = build_pages.old_lastmods(os.path.join(ip.ROOT, "sitemap.xml"))
        self.assertIn("https://lumitrades.io/trust/", lm)
        self.assertTrue(all(len(v) == 10 for v in lm.values()))
        self.assertEqual(build_pages.old_lastmods("/nonexistent/sitemap.xml"), {})

    def test_blog_post_lastmod_not_build_date(self):
        """A hand-built blog post keeps the date of its last commit, not the date of every rebuild."""
        import build_pages, re as _re
        with open(os.path.join(ip.ROOT, "sitemap.xml"), encoding="utf-8") as f:
            sm = f.read()
        for d in os.listdir(os.path.join(ip.ROOT, "blog")):
            rel = f"blog/{d}/index.html"
            if not os.path.exists(os.path.join(ip.ROOT, rel)):
                continue
            day = build_pages.git_day(rel)
            m = _re.search(rf"<loc>https://lumitrades.io/blog/{_re.escape(d)}/</loc><lastmod>([0-9-]+)</lastmod>", sm)
            if day and m:
                self.assertEqual(m.group(1), day)


class JsonLdDateModified(unittest.TestCase):
    """build_pages: JSON-LD dateModified only moves when a page changed beyond its build-date stamps (P1, 2026-11-04)."""
    OLD = ('<script type="application/ld+json">[{"@type": "Article", "dateModified": "2026-11-01"}]</script>'
           '<p>12 checks</p><p class="meta">Page generated 2026-11-03</p>')

    def test_stamp_only_change_keeps_sitemap_date(self):
        import build_pages as bp
        new = self.OLD.replace("2026-11-01", "2026-11-04").replace("2026-11-03", "2026-11-04")
        out = bp.stable_ld_dates("how-it-works/index.html", self.OLD, new, {"https://lumitrades.io/how-it-works/": "2026-10-30"})
        self.assertIn('"dateModified": "2026-10-30"', out)       # agrees with the sitemap lastmod
        self.assertIn("Page generated 2026-11-04", out)          # the visible footer is untouched
        self.assertEqual(bp.unstamped(out), bp.unstamped(new))

    def test_stamp_only_change_without_sitemap_keeps_old(self):
        import build_pages as bp
        new = self.OLD.replace("2026-11-01", "2026-11-04").replace("2026-11-03", "2026-11-04")
        out = bp.stable_ld_dates("sellers/x/index.html", self.OLD, new, {})
        self.assertIn('"dateModified": "2026-11-01"', out)

    def test_real_change_and_new_page_take_build_date(self):
        import build_pages as bp
        new = self.OLD.replace("2026-11-01", "2026-11-04").replace("12 checks", "13 checks")
        lm = {"https://lumitrades.io/how-it-works/": "2026-10-30"}
        self.assertEqual(bp.stable_ld_dates("how-it-works/index.html", self.OLD, new, lm), new)
        self.assertEqual(bp.stable_ld_dates("how-it-works/index.html", None, new, lm), new)
        self.assertEqual(bp.stable_ld_dates("sitemap.xml", self.OLD, new.replace("13", "12"), lm), new.replace("13", "12"))

    def test_fixed_dates_and_timestamps_untouched(self):
        import build_pages as bp
        old = '{"dateModified": "2026-10-25"} {"dateModified": "2026-11-03T11:01:10.002Z"} 2026-11-03'
        new = '{"dateModified": "2026-10-25"} {"dateModified": "2026-11-03T11:01:10.002Z"} 2026-11-04'
        self.assertEqual(bp.keep_date_modified(old, new, "2026-10-01"), new)

    def test_page_url(self):
        import build_pages as bp
        self.assertEqual(bp.page_url("index.html"), "https://lumitrades.io/")
        self.assertEqual(bp.page_url("es/how-it-works/index.html"), "https://lumitrades.io/es/how-it-works/")
        self.assertEqual(bp.page_url("sellers/xrplhub-io/index.html"), "https://lumitrades.io/sellers/xrplhub-io/")

    def test_committed_how_page_rebuild(self):
        """Tomorrow's rebuild of the committed /how-it-works/ (stamps moved only) keeps its sitemap date in JSON-LD."""
        import build_pages as bp, re as _re
        with open(os.path.join(ip.ROOT, "how-it-works", "index.html"), encoding="utf-8") as f:
            old = f.read()
        new = bp._STAMP.sub("2099-01-01", old)
        lm = bp.old_lastmods(os.path.join(ip.ROOT, "sitemap.xml"))
        out = bp.stable_ld_dates("how-it-works/index.html", old, new, lm)
        self.assertEqual(_re.findall(r'"dateModified": "([0-9-]{10})"', out), [lm["https://lumitrades.io/how-it-works/"]])


if __name__ == "__main__":
    unittest.main()
