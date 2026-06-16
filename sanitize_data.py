#!/usr/bin/env python3
"""Sanitize a raw SenticNet distribution .py into an importable babel data module.

The official sentic.net/downloads distribution files ship with a handful of
emoticon keys that are not valid Python -- some contain unescaped single quotes
(e.g. senticnet[':'-)']), others contain a stray backslash (e.g.
senticnet[': \\']). This rewrites ONLY the unparseable key lines, re-quoting the
key with repr() so it faithfully represents the literal text the author typed.
Every already-valid line is passed through byte-for-byte.

Detection is authoritative: a line is "broken" iff ast.parse() rejects it. To
stay fast on ~293k lines we only parse lines whose key portion looks suspicious
(contains a backslash, a double quote, or != 2 single quotes); a key of the form
'<chars-with-none-of-those>' is always valid Python and is skipped.

Usage: python3 sanitize_data.py <src.py> <dst.py>
"""
import ast
import sys

SEP = "] = ["
PREFIX = "senticnet["


def suspicious(keypart):
    return ("\\" in keypart) or ('"' in keypart) or (keypart.count("'") != 2)


def parseable(line):
    try:
        ast.parse(line)
        return True
    except SyntaxError:
        return False


def fix_line(line):
    left, sep, right = line.partition(SEP)
    if not sep:
        return None
    keysrc = left[len(PREFIX):]
    key = keysrc[1:-1]  # strip the outer quote chars; inner text taken literally
    return PREFIX + repr(key) + SEP + right


def sanitize(src_path, dst_path):
    out = []
    total = 0
    fixed = []
    still_broken = []
    with open(src_path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if line.startswith(PREFIX):
                total += 1
                keypart = line.partition(SEP)[0]
                if suspicious(keypart) and not parseable(line):
                    nl = fix_line(line)
                    if nl is not None and parseable(nl):
                        fixed.append((i, keypart, nl.partition(SEP)[0]))
                        line = nl
                    else:
                        still_broken.append((i, line.rstrip("\n")))
            out.append(line)
    with open(dst_path, "w", encoding="utf-8") as f:
        f.writelines(out)
    return total, fixed, still_broken


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    total, fixed, still_broken = sanitize(src, dst)
    print("data lines: {}  keys re-quoted: {}".format(total, len(fixed)))
    for i, old, new in fixed:
        print("  line {}: {}]  ->  {}]".format(i, old, new))
    if still_broken:
        print("STILL BROKEN ({}):".format(len(still_broken)))
        for i, ln in still_broken:
            print("  line {}: {}".format(i, ln[:160]))
        sys.exit(2)
