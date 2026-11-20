#!/usr/bin/env python3
"""Rendering-code drift check for the daily site_refresh job (/workspace/scheduler/jobs/site_refresh.sh, step 3).

The daily refresh publishes DATA ONLY. Before rebuilding pages it must know that every page-rendering change on
origin/main (scripts/, assets/) has already been published deliberately; otherwise a data rebuild would quietly ship
new wording/layout. Until Nov 20, 2026 the job used "the last commit touching index.html" as its last-page-build
marker, so a copy publish that rebuilt only its own pages (e.g. the Nov 19 privacy update fe1dbc37, which changed
scripts/privacy_page.py together with the six privacy/index.html pages) blocked every later refresh (rc=12).

Better marker, per file: a rendering file changed since the last index.html build counts as published when the
latest commit that changed it also changed generated pages (*.html), i.e. it went out with a page build. A file
changed in a commit with no page output is drift. (site_refresh_guard.py still checks the rebuilt pages afterwards.)

  python3 scripts/render_drift.py            # prints drift files (one per line), exit 1 if any, 0 if none
  python3 scripts/render_drift.py --explain  # also explains each candidate on stderr
"""
import subprocess, sys

# Files under scripts/ and assets/ that never change rendered pages (same list as site_refresh.sh used inline).
EXCLUDE = [
    "*.json", "scripts/test_*", "scripts/top_sellers_refresh.py", "scripts/publish.sh", "scripts/indexnow_ping.py",
    "scripts/derive_attempts_all.py", "scripts/privacy.py", "scripts/track_trades.py", "scripts/locked.sh",
    "scripts/check_well_known_x402.py", "scripts/build_site.py", "scripts/render_drift.py",
]
MARKER = "index.html"


def git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout


def changed_files(commit, cwd=None):
    """Files changed by `commit` relative to its first parent (all files for a root commit)."""
    out = git("show", "--first-parent", "-m", "--format=", "--name-only", commit, cwd=cwd)
    return [l for l in out.splitlines() if l]


def drift(head="HEAD", cwd=None, explain=None):
    last = git("log", "-1", "--format=%H", head, "--", MARKER, cwd=cwd).strip()
    if not last:
        return [], ""
    spec = ["scripts", "assets"] + [f":(exclude){p}" for p in EXCLUDE]
    cands = [l for l in git("diff", "--name-only", last, head, "--", *spec, cwd=cwd).splitlines() if l]
    out = []
    for f in cands:
        c = git("log", "-1", "--format=%H", head, "--", f, cwd=cwd).strip()
        pages = [p for p in changed_files(c, cwd=cwd) if p.endswith(".html")] if c else []
        if explain:
            explain(f"{f}: last changed in {c[:8]} " + (f"with {len(pages)} page(s) rebuilt -> published" if pages
                                                         else "with no page output -> drift"))
        if not pages:
            out.append(f)
    return out, last


if __name__ == "__main__":
    say = (lambda m: print(m, file=sys.stderr)) if "--explain" in sys.argv else None
    files, _ = drift(explain=say)
    for f in files:
        print(f)
    sys.exit(1 if files else 0)
