#!/usr/bin/env python3
"""Compare curriculum records with downloaded official guide text for agent review.

Requires Python 3.10+ only. Text files must be UTF-8, named YEAR/NN.txt,
where NN comes from each department's guidePdf URL. This detects discrepancies;
it does not decide whether a printed code is a course row or an equivalence note.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

CODE = re.compile(r"\b[A-Z]{3}\.[A-Z]\d{3}(?:\.[A-Z])?\b")


def repair_latin(text):
    """Repair the observed -29 Latin font mapping, preserving layout whitespace."""
    return "".join(
        chr(ord(char) + 29)
        if 3 <= ord(char) <= 93 and char not in "\t\n\r\f "
        else char
        for char in text
    )


def title_findings(records):
    findings = []
    for record in records:
        title = record.get("title", {}).get("ja", "")
        normalized = title.replace("（", "(").replace("）", ")")
        reasons = []
        if not title.strip():
            reasons.append("empty Japanese title")
        if normalized.count("(") != normalized.count(")"):
            reasons.append("unbalanced parentheses: review continuation lines")
        if re.search(r"\s{3,}", title) or re.match(r"\(?[23]00\b|番台[)）]", title):
            reasons.append("possible adjacent table column in title")
        if reasons:
            findings.append({"code": record["code"], "title": title, "reasons": reasons})
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", required=True, type=Path)
    parser.add_argument("--guides-dir", required=True, type=Path)
    parser.add_argument("--year", action="append", required=True, help="Repeat for each admission year")
    parser.add_argument("--department", action="append", help="Optional department ID filter; repeatable")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument(
        "--shift29", action="append", default=[], metavar="YEAR:DEPARTMENT",
        help="Explicitly repair Latin font mapping for this source only; repeatable. Japanese still needs OCR.",
    )
    args = parser.parse_args()
    for year in args.year:
        if not re.fullmatch(r"\d{4}", year):
            parser.error("--year must contain four digits")
    for selector in args.shift29:
        if not re.fullmatch(r"\d{4}:[a-z][a-z0-9-]*", selector):
            parser.error("--shift29 must be YEAR:DEPARTMENT")
    results, errors = [], []
    selected_ids = set(args.department or [])
    seen_ids = set()
    for year in dict.fromkeys(args.year):
        dataset = args.data_root / "departments" / f"{year}.json"
        try:
            departments = json.loads(dataset.read_text(encoding="utf-8"))["departments"]
        except (OSError, ValueError, KeyError, TypeError) as error:
            errors.append({"path": str(dataset), "error": str(error)})
            continue
        for department in departments:
            department_id = department.get("id", "")
            if selected_ids and department_id not in selected_ids:
                continue
            seen_ids.add(department_id)
            try:
                pdf_name = Path(urlparse(department["guidePdf"]).path).name
                match = re.fullmatch(r"\d{2}-(\d{2})\.pdf", pdf_name)
                if not match:
                    raise ValueError(f"unsupported guidePdf filename: {pdf_name}")
                source = args.guides_dir / year / f"{match.group(1)}.txt"
                text = source.read_text(encoding="utf-8")
                repaired = f"{year}:{department_id}" in args.shift29
                if repaired:
                    text = repair_latin(text)
                published = {code[:8] for code in CODE.findall(text)}
                if not published:
                    raise ValueError("no readable course codes; review font mapping/OCR before claiming coverage")
                records = department["recommended"]
                present = {record["code"] for record in records}
                titles = title_findings(records)
                results.append({
                    "year": year, "department": department_id, "source": str(source),
                    "strategy": "latin-shift29" if repaired else "plain-text",
                    "published": len(published), "stored": len(present),
                    "missing": sorted(published - present), "extra": sorted(present - published),
                    "titleFindings": titles,
                })
            except (OSError, ValueError, KeyError, TypeError) as error:
                errors.append({"year": year, "department": department_id, "error": str(error)})
    for unknown in sorted(selected_ids - seen_ids):
        errors.append({"department": unknown, "error": "selected department not found"})
    findings = any(item["missing"] or item["extra"] or item["titleFindings"] for item in results)
    status = "input-error" if errors else "review" if findings else "ok"
    report = {"status": status, "results": results, "errors": errors}
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(f"{item['year']} {item['department']}: published={item['published']} "
                  f"stored={item['stored']} missing={len(item['missing'])} extra={len(item['extra'])} "
                  f"titleFindings={len(item['titleFindings'])} strategy={item['strategy']}")
            for key in ("missing", "extra"):
                if item[key]:
                    print(f"  {key}: {', '.join(item[key])}")
            for finding in item["titleFindings"]:
                print(f"  title: {finding['code']} {finding['title']} ({'; '.join(finding['reasons'])})")
        for error in errors:
            print(f"ERROR: {json.dumps(error, ensure_ascii=False)}", file=sys.stderr)
    return 2 if errors else 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
