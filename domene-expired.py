#!/usr/bin/env -S uv run -q
# /// script
# requires-python = ">=3.10"
# ///
"""
domene-expired: Fetch expired and soon-to-expire domains from domene.shop/expired

Usage:
  domene-expired [options]

License:
  MIT License (c) 2025 bjornmorten
"""
import argparse
import csv
import json
import re
import signal
import sys
from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://domene.shop/expired"
PROJECT_URL = "https://github.com/bjornmorten/domene-expired"
USER_AGENT = f"domene-expired/1.0 (+{PROJECT_URL})"

signal.signal(signal.SIGPIPE, signal.SIG_DFL)


def fetch_domains():
    req = Request(URL, headers={"User-Agent": USER_AGENT})
    with urlopen(req) as resp:
        html = resp.read().decode("utf-8")

    results = []
    date = None

    for line in html.splitlines():
        line = line.strip()

        date_match = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", line)
        if date_match:
            day, month, year = date_match.groups()
            date = f"{year}-{month}-{day}"
            continue

        link_match = re.search(r'<a href="/\?domain=([^"]+)">([^<]+)</a>', line)
        if link_match and date:
            _, text_domain = link_match.groups()
            results.append((date, text_domain))

    return results


def compile_filters(patterns):
    regexes = []
    for p in patterns:
        try:
            regexes.append(re.compile(p, re.IGNORECASE))
        except re.error as e:
            sys.exit(f"Invalid regex '{p}': {e}")
    return regexes


def write_output(data_str, output_file, force=False):
    if output_file:
        path = Path(output_file)

        if path.exists() and not force:
            sys.exit(f"Error: '{path}' already exists (use --force to overwrite).")

        path.write_text(data_str, encoding="utf-8")
    else:
        if data_str:
            print(data_str)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch expired and expiring domains from domene.shop"
    )

    parser.add_argument(
        "-x", "--only-expired", action="store_true", help="Show only expired domains"
    )
    parser.add_argument(
        "-u",
        "--expiring-soon",
        action="store_true",
        help="Show only domains which expires soon",
    )
    parser.add_argument(
        "-s",
        "--include-se",
        action="store_true",
        help="Include .se domains (default: .no only)",
    )
    parser.add_argument(
        "-f",
        "--filter",
        action="append",
        metavar="RX",
        help="Regex filter for domain (repeatable)",
    )
    parser.add_argument(
        "-l", "--max-len", type=int, metavar="N", help="Filter by max domain length"
    )
    parser.add_argument(
        "-d",
        "--only-domains",
        action="store_true",
        help="Print only domain names (no dates)",
    )

    parser.add_argument(
        "-o", "--output", metavar="FILE", help="Write output to file (default: stdout)"
    )
    parser.add_argument("-j", "--json", action="store_true", help="Output JSON format")
    parser.add_argument("-c", "--csv", action="store_true", help="Output CSV format")
    parser.add_argument(
        "-y", "--force", action="store_true", help="Overwrite output file if it exists"
    )

    args = parser.parse_args()

    fmt_flags = sum([args.json, args.csv])
    if fmt_flags > 1:
        parser.error("Choose only one of --json or --csv")

    domains = fetch_domains()

    if not args.include_se:
        domains = [(d, n) for d, n in domains if n.endswith(".no")]

    unique_dates = sorted(set(d for d, _ in domains), reverse=True)
    expired_date = unique_dates[-1] if unique_dates else None
    soon_dates = [d for d in unique_dates if d != expired_date]

    if args.only_expired:
        domains = [(d, n) for d, n in domains if d == expired_date]
    elif args.expiring_soon:
        domains = [(d, n) for d, n in domains if d in soon_dates]

    if args.filter:
        regexes = compile_filters(args.filter)
        domains = [(d, n) for d, n in domains if any(r.search(n) for r in regexes)]

    if args.max_len:
        domains = [
            (d, n) for d, n in domains if len(n.rsplit(".", 1)[0]) <= args.max_len
        ]

    if args.json:
        data_str = json.dumps([{"date": d, "domain": n} for d, n in domains], indent=2)
    elif args.csv:
        import io

        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["date", "domain"])
        writer.writerows(domains)
        data_str = buf.getvalue().strip()
    else:
        if args.only_domains:
            data_str = "\n".join(n for _, n in domains)
        else:
            data_str = "\n".join(f"{d}\t{n}" for d, n in domains)

    write_output(data_str, args.output, args.force)


if __name__ == "__main__":
    main()
