#!/usr/bin/env python3
"""Convert Microsoft Teams .vtt transcripts to Markdown for raw/.

Usage:
  vtt2md.py info <file.vtt>                 Print JSON: duration, speakers (with org), cue count
  vtt2md.py convert <file.vtt> <out.md>     Write Markdown; frontmatter is read from stdin
"""
import html
import json
import re
import sys


def parse(path):
    txt = open(path, encoding="utf-8-sig").read()
    cues = []
    for block in re.split(r"\n\s*\n", txt):
        ts = re.search(r"(\d\d:\d\d:\d\d)\.\d+ --> (\d\d:\d\d:\d\d)", block)
        v = re.search(r"<v ([^>]*)>(.*?)</v>", block, re.S)
        if not (ts and v):
            continue
        raw_name = v.group(1).strip()
        org = re.search(r"\((.*)\)", raw_name)
        name = re.sub(r"\s*\(.*\)", "", raw_name)
        if "," in name:
            last, first = [x.strip() for x in name.split(",", 1)]
            name = f"{first} {last}"
        text = html.unescape(" ".join(v.group(2).split()))
        cues.append({"start": ts.group(1), "end": ts.group(2), "name": name,
                     "org": org.group(1) if org else None, "text": text})
    return cues


def info(path):
    cues = parse(path)
    speakers = {}
    for c in cues:
        speakers.setdefault(c["name"], c["org"])
    print(json.dumps({
        "cues": len(cues),
        "duration": cues[-1]["end"] if cues else None,
        "speakers": [{"name": n, "org": o} for n, o in speakers.items()],
    }, ensure_ascii=False, indent=2))


def convert(path, out):
    cues = parse(path)
    frontmatter = sys.stdin.read().strip()
    body = "\n\n".join(f"[{c['start']}] **{c['name']}:** {c['text']}" for c in cues)
    with open(out, "x", encoding="utf-8") as f:  # never overwrite raw/ files
        f.write(frontmatter + "\n\n" + body + "\n")
    print(f"{len(cues)} cues written to {out}")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "info":
        info(sys.argv[2])
    elif len(sys.argv) == 4 and sys.argv[1] == "convert":
        convert(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)
