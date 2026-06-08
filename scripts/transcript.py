#!/usr/bin/env python3
"""
transcript.py — pull + clean a timestamped transcript from any YouTube / podcast video.

THE GAP THIS CLOSES: research agents reliably *find* the best video/podcast of a
person ("the single best 'you can hear it' asset") but cannot *listen* to it, so
the richest intel — said out loud, never written down — is missed. This turns any
YouTube URL into a clean, timestamped, deduplicated transcript you (or an agent)
can grep and quote. Spoken-word self-description on a podcast is a PRIMARY SOURCE,
not lore.

Requires: yt-dlp (brew install yt-dlp).

Usage:
    python3 scripts/transcript.py <youtube_url_or_id>
    python3 scripts/transcript.py <url> --around 1376          # print ±3 min around t=1376s
    python3 scripts/transcript.py <url> --grep "cello,brother,new lab"
    python3 scripts/transcript.py <url> --out /tmp/foo.txt

Then mine it:
    grep -i -A2 "grew up\\|my brother\\|live\\|founded" /tmp/foo.txt

Tip for podcasts not on YouTube: most AI podcasts (Latent Space, No Priors, the
Hidden Layer) mirror to YouTube — find the YouTube URL and run this. Many also
publish transcripts on their own site; check there first.
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def vid_id(s: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|/shorts/|/embed/)([A-Za-z0-9_-]{11})", s)
    return m.group(1) if m else s.strip()


def fetch_vtt(url: str, workdir: Path) -> Path | None:
    vid = vid_id(url)
    full = f"https://www.youtube.com/watch?v={vid}"
    out = workdir / vid
    cmd = ["yt-dlp", "--skip-download", "--write-auto-sub", "--write-sub",
           "--sub-lang", "en", "--sub-format", "vtt", "-o", str(out) + ".%(ext)s", full]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=180)
    except FileNotFoundError:
        sys.exit("ERROR: yt-dlp not installed. Run: brew install yt-dlp")
    except subprocess.CalledProcessError as e:
        sys.exit(f"ERROR: yt-dlp failed:\n{e.stderr[-500:]}")
    except subprocess.TimeoutExpired:
        sys.exit("ERROR: yt-dlp timed out.")
    vtts = list(workdir.glob(f"{vid}*.vtt"))
    return vtts[0] if vtts else None


def parse(vtt: Path):
    lines = vtt.read_text().splitlines()

    def to_s(ts):
        h, m, s = ts.split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)

    cues, i = [], 0
    while i < len(lines):
        m = re.match(r"(\d{2}:\d{2}:\d{2}\.\d{3}) -->", lines[i])
        if m:
            start = to_s(m.group(1))
            txt, j = [], i + 1
            while j < len(lines) and lines[j].strip() and not re.match(r"\d{2}:\d{2}:\d{2}", lines[j]):
                t = re.sub(r"<[^>]+>", "", lines[j]).strip()
                if t:
                    txt.append(t)
                j += 1
            cues.append((start, " ".join(txt)))
            i = j
        else:
            i += 1
    # dedupe the rolling-window repetition typical of auto-captions
    clean, last = [], ""
    for start, txt in cues:
        if not txt or txt == last or txt in last:
            continue
        clean.append((start, txt))
        last = txt
    return clean


def render(clean, every=20) -> str:
    out, lastts = [], -999
    for start, txt in clean:
        if start - lastts >= every:
            mm, ss = int(start) // 60, int(start) % 60
            out.append(f"\n[{mm:02d}:{ss:02d}] ")
            lastts = start
        out.append(txt + " ")
    return "".join(out).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--around", type=int, help="print ±180s around this second mark")
    ap.add_argument("--grep", help="comma-separated terms to print context around")
    ap.add_argument("--out", help="save full transcript to this path")
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as td:
        vtt = fetch_vtt(args.url, Path(td))
        if not vtt:
            sys.exit("ERROR: no captions available for this video.")
        clean = parse(vtt)

    full = render(clean)
    if args.out:
        Path(args.out).write_text(full)
        print(f"saved {len(full)} chars to {args.out} ({len(clean)} cues, ~{int(clean[-1][0])//60} min)")

    if args.around is not None:
        lo, hi = args.around - 180, args.around + 180
        print(f"\n=== around t={args.around}s ===")
        for start, txt in clean:
            if lo <= start <= hi:
                print(f"[{int(start)//60:02d}:{int(start)%60:02d}] {txt}")
    elif args.grep:
        terms = [t.strip() for t in args.grep.split(",") if t.strip()]
        for term in terms:
            print(f"\n##### '{term}' #####")
            shown = 0
            for idx, (start, txt) in enumerate(clean):
                if term.lower() in txt.lower() and shown < 3:
                    ctx = " ".join(t for _, t in clean[max(0, idx - 1):idx + 2])
                    print(f"[{int(start)//60:02d}:{int(start)%60:02d}] {ctx}")
                    shown += 1
    elif not args.out:
        print(full)


if __name__ == "__main__":
    main()
