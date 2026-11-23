"""prices_snapshot.py --refresh (Nov 23, 2026): rewrite prices/index.json only when a quote changed; publish.sh runs it."""
import copy, json, os, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import prices_snapshot as ps

ROOT = os.path.dirname(HERE)


class PricesRefresh(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(ROOT, "prices", "index.json"), encoding="utf-8") as f:
            self.snap = json.load(f)
        self.tmp = tempfile.mkdtemp()
        self.out = os.path.join(self.tmp, "prices", "index.json")
        ps.write(self.snap, self.out)

    def _read(self):
        with open(self.out, encoding="utf-8") as f:
            return json.load(f)

    def test_same_quotes_new_time_keeps_file(self):
        new = copy.deepcopy(self.snap)
        new["as_of"], new["as_of_ct"] = "2030-01-01T00:00:00Z", "Jan 1, 2030 12:00 AM CST"
        self.assertFalse(ps.refresh(new, self.out))
        self.assertEqual(self._read()["as_of"], self.snap["as_of"])

    def test_xrp_amount_change_rewrites(self):
        new = copy.deepcopy(self.snap)
        new["as_of"] = "2030-01-01T00:00:00Z"
        xrp = next(o for o in new["paid"][0]["accepts"] if o["asset"] == "XRP")
        xrp["amount"] = "9.99"
        self.assertTrue(ps.refresh(new, self.out))
        self.assertEqual(self._read()["as_of"], "2030-01-01T00:00:00Z")

    def test_missing_file_writes(self):
        os.remove(self.out)
        self.assertTrue(ps.refresh(self.snap, self.out))

    def test_publish_sh_refreshes_before_build_and_keeps_on_failure(self):
        with open(os.path.join(HERE, "publish.sh"), encoding="utf-8") as f:
            sh = f.read()
        i, j = sh.find("prices_snapshot.py --refresh)"), sh.find("BUILD_REQUIRE_LIVE=1 python3 scripts/build_pages.py --paths")
        self.assertTrue(0 < i < j, "the prices refresh must run before the page build")
        self.assertIn("WARNING prices_snapshot.py --refresh failed; keeping prices/index.json", sh)

    def test_not_rendering_drift(self):
        import render_drift
        self.assertIn("scripts/prices_snapshot.py", render_drift.EXCLUDE)


if __name__ == "__main__":
    unittest.main()
