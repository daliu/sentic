#!/usr/bin/env python3
"""Download SenticNet 9 multilingual data and install it into sentic/babel/.

For each language the package already ships, we fetch the matching SN9 release
from sentic.net, repair the handful of unparseable emoticon keys (see
sanitize_data.py), and rewrite sentic/babel/data_<legacy>.py canonically so the
existing language codes keep working. Languages with no SN9 release are skipped.

Usage:
    python3 update_multilang.py [legacy_code ...]   # subset, or all if omitted
"""
import ast
import os
import subprocess
import sys
import warnings
import zipfile

BABEL = os.path.join(os.path.dirname(__file__), "sentic", "babel")
CACHE = "/tmp/sn9_ml"
SEP = "] = ["
PREFIX = "senticnet["

# legacy package code -> SN9 ISO 639-1 code (verified by content + HTTP 200)
MAPPING = {
    # identical codes
    "ar": "ar", "bg": "bg", "de": "de", "es": "es", "fi": "fi", "fr": "fr",
    "he": "he", "hi": "hi", "hr": "hr", "ht": "ht", "hu": "hu", "id": "id",
    "it": "it", "lt": "lt", "lv": "lv", "mt": "mt", "nl": "nl", "pt": "pt",
    "ro": "ro", "ru": "ru", "sk": "sk", "th": "th", "tr": "tr", "ur": "ur",
    # remapped legacy/country codes -> ISO language codes
    "cn": "zh", "jp": "ja", "kr": "ko", "gr": "el", "dk": "da", "cz": "cs",
    "se": "sv", "ee": "et", "ua": "uk", "rs": "sr", "ba": "bs", "my": "ms",
    "si": "sl",
}
SKIP = {"ca": "Catalan (no SN9 release)", "hm": "Hmong (no SN9 release)", "en": "handled separately"}


def repair_to_dict(raw):
    """Make raw distribution text parseable, exec it, return (dict, num_fixed)."""
    fixed = 0
    out = []
    for line in raw.splitlines(keepends=True):
        if line.startswith(PREFIX):
            keypart = line.partition(SEP)[0]
            if ("\\" in keypart) or ('"' in keypart) or (keypart.count("'") != 2):
                try:
                    ast.parse(line)
                except SyntaxError:
                    left, sep, right = line.partition(SEP)
                    key = left[len(PREFIX):][1:-1]  # strip outer quotes, literal inner
                    line = PREFIX + repr(key) + SEP + right
                    ast.parse(line)  # raises if our repair didn't fix it
                    fixed += 1
        out.append(line)
    ns = {}
    # The distribution files are executed as Python (they are plain
    # `senticnet[...] = [...]` assignments). We trust them because they come from
    # the official sentic.net over HTTPS; this is maintainer-run tooling, never
    # executed at package install or import time.
    exec(compile("".join(out), "<sn9>", "exec"), ns)
    return ns["senticnet"], fixed


def write_canonical(path, d):
    if not d:
        raise ValueError("refusing to write an empty senticnet dict to %s" % path)
    # Write a sibling temp file and atomically replace, so an interrupted run
    # never leaves a half-written (but still importable) data module in place.
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("senticnet = {}\n")
        for k, v in d.items():
            f.write("senticnet[%r] = %r\n" % (k, v))
    os.replace(tmp, path)


def fetch(iso):
    # sentic.net blocks the urllib user-agent (HTTP 465), so shell out to curl.
    os.makedirs(CACHE, exist_ok=True)
    zp = os.path.join(CACHE, "senticnet_%s.zip" % iso)
    # Refetch if the cache is missing/empty OR a prior interrupted run left a
    # partial (non-empty but truncated) zip that would otherwise be reused.
    if not os.path.exists(zp) or os.path.getsize(zp) == 0 or not zipfile.is_zipfile(zp):
        url = "https://sentic.net/senticnet_%s.zip" % iso
        subprocess.run(["curl", "-sL", "--fail", "-o", zp, url], check=True, timeout=180)
    return zp


def py_member(z):
    names = z.namelist()
    if "senticnet.py" in names:
        return "senticnet.py"
    for n in names:
        if n.endswith(".py"):
            return n
    raise FileNotFoundError("no .py in zip")


def main(codes):
    warnings.simplefilter("ignore")
    results = []
    for legacy in codes:
        iso = MAPPING[legacy]
        try:
            zp = fetch(iso)
            with zipfile.ZipFile(zp) as z:
                raw = z.read(py_member(z)).decode("utf-8")
            d, fixed = repair_to_dict(raw)
            out = os.path.join(BABEL, "data_%s.py" % legacy)
            write_canonical(out, d)
            results.append((legacy, iso, len(d), fixed, "OK"))
            print("  data_%s.py <- senticnet_%s.zip : %d concepts, %d keys repaired"
                  % (legacy, iso, len(d), fixed), flush=True)
        except Exception as e:  # noqa: BLE001 - report and continue
            results.append((legacy, iso, 0, 0, "ERROR: %r" % e))
            print("  data_%s.py <- senticnet_%s.zip : ERROR %r" % (legacy, iso, e), flush=True)
    ok = [r for r in results if r[4] == "OK"]
    print("\nDONE: %d/%d languages updated, %d concepts total"
          % (len(ok), len(results), sum(r[2] for r in ok)))
    bad = [r for r in results if r[4] != "OK"]
    if bad:
        print("FAILURES:")
        for legacy, iso, _, _, status in bad:
            print("  %s<-%s: %s" % (legacy, iso, status))
        return 1
    return 0


if __name__ == "__main__":
    codes = sys.argv[1:] or list(MAPPING.keys())
    sys.exit(main(codes))
